"""Isolated, read-only Canon RAW rendering with a generated PF3 applied.

Uses only the user's installed PSE/DPP4Lib and input profile. No Canon assets
are distributed. Native calls run in a child process so failures cannot crash Tk.
"""
from pathlib import Path
import ctypes as C
import json
import os
import subprocess
import sys
import tempfile
import numpy as np
from PIL import Image


def find_runtime(dll):
    folder=Path(dll).resolve().parent
    for candidate in (folder,folder/'DPP4Lib',folder.parent/'DPP4Lib'):
        if (candidate/'DppCore.dll').is_file() and (candidate/'icc'/'NS.ICC').is_file():
            return candidate
    raise FileNotFoundError('Canon PSE의 DPP4Lib와 icc/NS.ICC를 찾지 못했습니다.')


class CanonRawRenderer:
    def __init__(self, directory):
        if sys.platform!='win32':
            raise OSError('캐논 PF3 실제 현상은 Windows와 설치된 PSE가 필요합니다.')
        self.directory=Path(directory).resolve()
        self.cookie=os.add_dll_directory(str(self.directory))
        # Only this isolated child process changes directory.
        os.chdir(self.directory)
        self.dll=C.WinDLL(str(self.directory/'DppCore.dll'))
        u=C.c_uint32; p=C.c_void_p; pp=C.POINTER(p)
        signatures={
            'DppInitializeSDK':([],u),'DppTerminateSDK':([],u),
            'DppCreateFileStream':([C.c_wchar_p,u,u,pp],u),
            'DppCreateImageServer':([p,pp],u),'DppRevertRecipeToCaptured':([p],u),
            'DppSetPropertyData':([p,u,u,u,p],u),
            'DppCreateMemoryStreamFromPointer':([p,u,pp],u),
            'DppSetPictureStyleUserProfile':([p,p],u),
            'DppSetPictureStyleFile':([p,C.c_wchar_p],u),
            'DppProcessImageEx':([p,u,u,u,p,C.c_uint64,p,pp],u),
            'DppProcessImageWithImageEx':([p,p,u,u,p,C.c_uint64,p,pp],u),
            'DppOutputImageToStream':([p,u,u,p],u),'DppRelease':([p],u),
        }
        for name,(args,result) in signatures.items():
            fn=getattr(self.dll,name);fn.argtypes=args;fn.restype=result
        self.check(self.dll.DppInitializeSDK(),'initialize')
        self.stream=p();self.recipe=p()
        self.profile=(self.directory/'icc'/'NS.ICC').read_bytes()
        if len(self.profile)<132 or self.profile[36:40]!=b'acsp' or self.profile[12:16]!=b'scnr':
            raise ValueError('Canon input profile is invalid')

    @staticmethod
    def check(code,label):
        if code:raise RuntimeError(f'Canon {label}: 0x{code:08X}')

    def release(self,reference):
        if reference.value:self.dll.DppRelease(reference)

    def set_value(self,prop,value,typ):
        data=typ(value)
        self.check(self.dll.DppSetPropertyData(self.recipe,prop,0,C.sizeof(data),C.byref(data)),f'property {prop:08X}')

    def open(self,raw):
        self.check(self.dll.DppCreateFileStream(str(Path(raw).resolve()),2,0,C.byref(self.stream)),'open RAW')
        self.check(self.dll.DppCreateImageServer(self.stream,C.byref(self.recipe)),'RAW image server')

    def render(self,pf3,portrait):
        # These are the frame dimensions validated in this standalone runtime.
        # Requesting a smaller portrait frame crops; larger portrait buffers can
        # be silently corrupted by Canon's standalone path. Resize only after.
        width,height=(1080,1620) if portrait else (1620,1080)
        refs=[]
        try:
            self.check(self.dll.DppRevertRecipeToCaptured(self.recipe),'reset captured recipe')
            self.set_value(0x20001,0,C.c_double)  # exposure
            self.set_value(0x20101,255,C.c_uint32) # as-shot WB
            self.set_value(0x20106,0,C.c_double)
            self.set_value(0x20105,0,C.c_double)
            self.set_value(0x10200,1,C.c_uint32) # sRGB
            profile_buffer=C.create_string_buffer(self.profile)
            profile_stream=C.c_void_p();refs.append(profile_stream)
            self.check(self.dll.DppCreateMemoryStreamFromPointer(profile_buffer,len(self.profile),C.byref(profile_stream)),'input profile stream')
            self.check(self.dll.DppSetPictureStyleUserProfile(self.recipe,profile_stream),'input profile')
            self.check(self.dll.DppSetPictureStyleFile(self.recipe,str(Path(pf3).resolve())),'load PF3')
            self.set_value(0x20301,255,C.c_uint32) # select loaded file, not base enum
            rect_type=C.c_int32*4
            native_w,native_h=(height,width) if portrait else (width,height)
            rect=rect_type(0,0,native_w,native_h)
            auxiliary=(C.c_ubyte*256)()
            developed=C.c_void_p();refs.append(developed)
            self.check(self.dll.DppProcessImageEx(self.recipe,1,1,1,C.byref(rect),
                       (native_h<<32)|native_w,auxiliary,C.byref(developed)),'develop')
            rect=rect_type(0,0,width,height)
            output=C.c_void_p();refs.append(output)
            self.check(self.dll.DppProcessImageWithImageEx(self.recipe,developed,0,0,C.byref(rect),
                       (height<<32)|width,auxiliary,C.byref(output)),'output image')
            stride=width*3
            buffer=C.create_string_buffer(stride*height)
            stream=C.c_void_p();refs.append(stream)
            self.check(self.dll.DppCreateMemoryStreamFromPointer(buffer,len(buffer),C.byref(stream)),'RGB stream')
            self.check(self.dll.DppOutputImageToStream(output,0x0D,stride,stream),'RGB pixels')
            rgb=np.frombuffer(buffer,dtype=np.uint8).reshape(height,width,3)[...,::-1].copy()
            return Image.fromarray(rgb)
        finally:
            for ref in reversed(refs):self.release(ref)

    def close(self):
        self.release(self.recipe);self.release(self.stream)
        self.dll.DppTerminateSDK();self.cookie.close()


def render_worker(request_path):
    request=json.loads(Path(request_path).read_text(encoding='utf-8'))
    renderer=CanonRawRenderer(request['runtime'])
    try:
        renderer.open(request['raw'])
        renderer.render(request['base_pf3'],request['portrait']) # discard first unstable frame
        original=renderer.render(request['base_pf3'],request['portrait'])
        altered=renderer.render(request['look_pf3'],request['portrait'])
        original.save(request['original'])
        altered.save(request['altered'])
    finally:
        renderer.close()


def render_pair(raw_path,cube,strength,base,dll,source_size):
    from canon_fit import fit_cube,target_rgb
    from lut import Cube
    from pf3_native import make_properties,NativeSerializer,validate_envelope
    ratio=max(source_size)/min(source_size)
    if not 1.45<ratio<1.55:
        raise ValueError('현재 캐논 실제 미리보기는 3:2 사진에서 검증되었습니다. 고해상도 LUT 참고 보기를 선택하세요.')
    fitted=fit_cube(cube,strength)
    identity_axis=np.array([0,1],dtype=np.float32)
    identity=Cube(np.stack(np.meshgrid(identity_axis,identity_axis,identity_axis,indexing='ij'),-1),np.zeros(3),np.ones(3))
    neutral_fit=fit_cube(identity)
    with tempfile.TemporaryDirectory(prefix='CLBPreview_') as folder:
        folder=Path(folder)
        base_pf3=folder/'base.pf3';look_pf3=folder/'look.pf3'
        serializer=NativeSerializer(dll)
        for path,properties in ((base_pf3,make_properties(identity,'CLB_BASE',base,fitted=neutral_fit)),
                                (look_pf3,make_properties(cube,'CLB_PREVIEW',base,strength,fitted=fitted))):
            serializer.write(path,properties);validate_envelope(path);serializer.verify(path,properties)
        request={'runtime':str(find_runtime(dll)),'raw':str(Path(raw_path).resolve()),
                 'base_pf3':str(base_pf3),'look_pf3':str(look_pf3),
                 'portrait':source_size[1]>source_size[0],
                 'original':str(folder/'original.png'),'altered':str(folder/'altered.png')}
        request_path=folder/'request.json';request_path.write_text(json.dumps(request),encoding='utf-8')
        if getattr(sys,'frozen',False):
            command=[sys.executable,'--canon-render-worker',str(request_path)]
        else:
            command=[sys.executable,str(Path(__file__).with_name('app.py')),'--canon-render-worker',str(request_path)]
        result=subprocess.run(command,capture_output=True,timeout=90,
                              creationflags=0x08000000 if sys.platform=='win32' else 0)
        if result.returncode:
            detail=result.stderr.decode('utf-8',errors='replace')[-1600:]
            raise RuntimeError(f'캐논 현상 작업 실패 ({result.returncode}): {detail}')
        with Image.open(request['original']) as im:original=im.convert('RGB')
        with Image.open(request['altered']) as im:altered=im.convert('RGB')
    rgb=np.asarray(original,dtype=np.float32)/255
    # Chunked image comparison avoids full-image interpolation temporaries.
    absolute=[]
    for y in range(0,original.height,128):
        target=np.rint(target_rgb(cube,rgb[y:y+128],strength)*255)
        absolute.append(abs(np.asarray(altered)[y:y+128].astype(float)-target).reshape(-1))
    errors=np.concatenate(absolute)
    report=dict(fitted.report,native_render_verified=True,native_rgb_mae_255=float(errors.mean()),
                native_rgb_p95_255=float(np.percentile(errors,95)),render_size=list(original.size))
    return original,altered,report
