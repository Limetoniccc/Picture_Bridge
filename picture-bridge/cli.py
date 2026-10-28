"""CLI for CUBE/XMP -> PF3, and CUBE -> Adobe creative XMP profile (MIT)."""
import argparse
import json
from pathlib import Path
import sys

from lut import load_cube
from xmp_bridge import load_xmp, export_xmp
from app_info import APP_NAME, APP_AUTHOR, display_name, XMP_GROUP
from pf3_native import STYLE_IDS, export_pf3, find_canon_library


def main(argv=None):
    parser = argparse.ArgumentParser(description=f'{display_name()} by {APP_AUTHOR}: CUBE/XMP to approximate Canon PF3; CUBE to Lightroom creative XMP profile.')
    parser.add_argument('--version', action='version', version=f'{display_name()} | 제작자 : {APP_AUTHOR}')
    parser.add_argument('input', nargs='?', help='Input 3D .cube or Adobe .xmp file')
    parser.add_argument('-o', '--output', help='Output .pf3 or .xmp (CUBE input only)')
    parser.add_argument('--name', help='Profile name')
    parser.add_argument('--base', default='Neutral', choices=STYLE_IDS.keys())
    parser.add_argument('--strength', type=float, default=1., help='Blend factor for PF3, 0..1')
    parser.add_argument('--dll', help='Path to installed Canon EdsCFParse.dll')
    parser.add_argument('--xmp-group', default=XMP_GROUP, help='Adobe XMP creative profile group')
    parser.add_argument('--probe', action='store_true', help='Locate Canon engine')
    args = parser.parse_args(argv)
    try:
        if args.probe:
            print(str(find_canon_library(args.dll)))
            return 0
        if not args.input:parser.error('an input .cube or .xmp is required')
        source=Path(args.input)
        if source.suffix.lower()=='.cube':
            cube=load_cube(source)
            xmp_info=None
        elif source.suffix.lower()=='.xmp':
            xmp_info=load_xmp(source)
            cube=xmp_info.cube
        else:
            raise ValueError('Input must end in .cube or .xmp')
        dest=Path(args.output) if args.output else source.with_suffix('.pf3')
        if dest.suffix.lower()=='.xmp':
            if source.suffix.lower()!='.cube':raise ValueError('.xmp output requires a .cube input')
            info=export_xmp(cube,dest,name=args.name or source.stem,group=args.xmp_group)
        elif dest.suffix.lower()=='.pf3':
            info=export_pf3(cube,dest,name=args.name or source.stem,dll=args.dll,
                            base=args.base,strength=args.strength)
            if xmp_info:
                info['xmp_source']={'kind':xmp_info.kind,'included':xmp_info.included,
                                    'ignored':xmp_info.ignored,'warnings':xmp_info.warnings,
                                    'table_color_space':xmp_info.color_space}
        else:raise ValueError('Output must end in .pf3 or .xmp')
        print(json.dumps(info,indent=2,ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1


if __name__=='__main__':sys.exit(main())
