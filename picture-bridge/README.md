# Picture Bridge v1.0

**제작자 : LimeT** · 오픈소스 (MIT 라이선스)

**Interface languages:** 한국어 (Korean, default) · English · 日本語 (Japanese) · 简体中文 (Simplified Chinese). The language selector is in the upper-right corner of the application. Changes take effect without restarting, and the selection is stored locally. See `WINDOWS_GUIDE_KO.txt`, `WINDOWS_GUIDE_EN.txt`, `WINDOWS_GUIDE_JA.txt`, and `WINDOWS_GUIDE_ZH_CN.txt` for a quick start in each language.

Windows GUI and CLI for opening **3D CUBE LUTs and Adobe XMP looks**, inspecting
full-resolution photos/RAW, exporting an **approximate Canon Picture Style (.pf3)**,
and creating a **Lightroom/Camera Raw creative XMP profile from a CUBE** (MIT).

## v1.0 — Picture Bridge by LimeT

### Four-language GUI edition (2026-10-28)

The interface now ships with an offline translation catalog (`i18n.py`) for Korean,
English, Japanese, and Simplified Chinese. The language selector changes menus,
actions, preview labels, import/export dialogs, status text and known XMP warnings
immediately without affecting image data or triggering Canon re-renders. Preferences
are stored under `%APPDATA%\PictureBridge\settings.json` on Windows, or
`~/.config/picture-bridge/settings.json` elsewhere. Optional environment variable
`PICTURE_BRIDGE_CONFIG_DIR` overrides the settings folder (useful for testing).
No translation service, API key, internet access or additional Python packages
are required. The Canon base-style identifiers and file extensions remain in
English because they are native technical values. Internal conversion diagnostics
from third-party libraries may still appear in their original language.

This is an update of **v1.0**, retaining the requested program version and the
same Windows executable identity; the localization does not change file formats.


Version 1.0 updates the application name and credits, the Windows EXE name and
version metadata, and the default Adobe profile group. Converters, preview and
Canon-native export are otherwise retained from v0.6. Run `build_windows.bat` on
Windows to build `dist\PictureBridge.exe` with version and creator metadata.
The source ZIP does not contain a prebuilt EXE.

## XMP support (introduced in v0.6)

| Input | Output | Operation | Requirements |
| --- | --- | --- | --- |
| `.cube` | `.pf3` | Existing Canon editable-color fit | Windows + installed Canon PSE |
| `.xmp` creative profile | `.pf3` | Decode embedded Adobe RGBTable, then Canon fit | Windows + installed Canon PSE |
| `.xmp` develop preset | `.pf3` | Sample supported slider adjustments into an approximate 33³ LUT, then Canon fit | Windows + installed Canon PSE |
| `.cube` | `.xmp` | Generate Adobe **creative profile** with a real 32³ RGB color table | Any supported Python platform; no Canon DLL |

An Adobe XMP *creative profile* is not the same as an XMP *develop preset* or
an XMP *photo sidecar*. Creative profiles can contain a real 3D LUT (`crs:RGBTable`
/ `crs:Table_<hash>`); this table is decoded without fitting it to sliders.
Profiles with alternate declared primary colors and transfer functions are
converted into a display-sRGB table for the Canon approximation, with gamut
clipping where necessary. A develop preset instead stores Adobe processing
parameters; we cannot run Adobe's proprietary development engine, so slider
conversions are **heuristic and not colorimetrically identical**.

Approximate preset adjustments currently include Exposure, Contrast, Highlights,
Shadows, Whites, Blacks, Saturation, Vibrance, global/per-channel PV2012 point
curves (linear interpolation), eight-band Hue/Saturation/Luminance, parametric
Shadows/Darks/Lights/Highlights, and Shadow/Midtone/Highlight/Global Color Grading
and legacy split-toning hue/saturation. These are sampled in display sRGB, not
RAW working-space Adobe rendering. **Unsupported** include temperature/tint
(raw-dependent white balance), adaptive masks, Auto Tone, clarity, texture, dehaze,
noise reduction, sharpening, camera calibration, lens corrections, grain,
vignetting, external creative-look references, and other photo-specific features.
The importer warns about omitted settings. If an XMP has no supported non-neutral
adjustments or embedded RGB LUT it refuses conversion rather than writing an
unexpectedly neutral file. Extra settings in an RGB-table profile are not applied.

For `.cube → .xmp` the output is a **creative profile carrying a 3D LUT**, not a
set of editable Lightroom Develop sliders. Adobe's profile RGB-table grids have
a 32-node-per-axis limit: 33³ and 65³ CUBEs are resampled. The converter assumes
the source CUBE maps display **sRGB → sRGB**, unless the author has explicitly
built a suitably color-managed LUT. CUBE names do not specify Log or gamut.
The generated XMP has an Amount slider when imported as a profile (subject to
Adobe version behavior). Import via Lightroom Classic's **File → Import Develop
Profiles and Presets** or Camera Raw's **Import Profiles and Presets**. Look for
the profile group **Picture Bridge**. Profile XML/binary round-trip is tested,
but actual Lightroom import has not been verified in this environment.

### v1.0 steps

1. Extract the ZIP and launch `launch_windows.bat` (Python dependencies required).
2. Click **1. .cube / .xmp 불러오기**, choose the source and read any conversion warnings.
3. Optionally load a photo or RAW and compare the full-resolution target look.
4. For a Canon `.pf3`, set base style, strength and PSE DLL, then click **3. 실제 .pf3 파일 생성**.
5. For an Adobe `.xmp` from a `.cube`, click **4. .cube → Lightroom .xmp 생성**. This
   option is disabled when the input is an XMP.
6. Verify final color in Canon DPP (PF3) or Adobe Lightroom/Camera Raw (XMP).

### v1.0 CLI examples

`python cli.py --version` prints the app name, version and author.

```powershell
python cli.py look.cube -o look.pf3 --base Neutral --strength 1.0
python cli.py LightroomPreset.xmp -o CanonLook.pf3 --base Portrait
python cli.py look.cube -o LightroomLook.xmp --name "My Look" --xmp-group "My Profiles"
```

The `.cube → .xmp` path runs on macOS/Linux too, without Canon software.
PF3 output still requires the installed **Windows** Canon DLL. JSON output
reports held-out Canon fit metrics for PF3 and a round-trip/resampling metric
for XMP; neither substitutes for a test in the target Adobe/Canon application.

## What changed in v0.5 (retained)


## What changed in v0.5

The old exporter wrote the requested look into the two 33³ camera tables while
leaving editable colour matrices/curves neutral. In the reported DPP workflow,
those tables did not produce the displayed LUT look. A constant-magenta table
probe was also ignored by DPP. A byte-perfect serializer round trip was therefore
insufficient evidence of correct colour rendering.

v0.5 fits the look into the editable cubic RGB coefficients and post curves that
Canon's developer consumes. Both camera tables are identity so the look is not
also applied there. **This is an approximation, not lossless CUBE-to-PF3.**
The fit uses a 17³ training grid plus extra neutral samples; an offset 18³ grid
measures model error independently. Arbitrary LUTs may fit poorly, especially
non-monotonic transforms, discontinuities, lifted black, and strong local hue
changes. The GUI/CLI report numerical RGB fit error; it is not perceptual Delta E.

## Start on Windows

1. Install 64-bit Python 3.10+ and Canon Picture Style Editor (PSE).
2. Extract this entire folder and run `launch_windows.bat`.
3. Load a CUBE and a photo/RAW. Set the base style and LUT strength.
4. For Canon CR2/CR3/CRW choose **캐논 PF3 실제 현상** (default).
5. Inspect the actual generated PF3 result. Export with **실제 .pf3 파일 생성**.
6. Open the new file in DPP and assess it under matching exposure/WB settings.

`EdsCFParse.dll` can be located automatically or selected manually. Canon binaries,
ICC profiles, input photos and LUTs are not bundled. The local PSE installation
supplies its own DPP4Lib and `icc/NS.ICC`; there is no download at conversion time.
RAW input additionally uses rawpy/LibRaw from `requirements.txt`.

## Two clearly labelled comparison modes

- **캐논 PF3 실제 현상**: generates the same fitted editable properties used by
  export, loads the generated PF3 into the installed Canon DPP4Lib, and renders
  the Canon RAW. The left pane is Canon base development; the right pane is the
  generated PF3 actually applied by Canon. WB is As Shot, exposure is 0, output
  is sRGB. No LUT is applied on top of the rendered right pane. The toolbar
  reports image error against the target LUT applied to the Canon baseline.
- **고해상도 LUT 목표 참고**: preserves the v0.4 full-resolution raster/LibRaw
  source and shows the target CUBE look. It is a target reference, not a claim
  about what a PF3 will reproduce. JPEG/PNG/TIFF and non-Canon RAW use this view.

The standalone Canon path has been validated at **1080×1620 portrait /
1620×1080 landscape**, for 3:2 Canon RAW images. It deliberately does not request
larger unvalidated portrait buffers. Smaller frame requests were observed to
crop, while larger portrait requests can silently corrupt Canon's output.
The source dimensions and comparison render dimensions are shown separately.
Use the high-resolution reference mode for source-pixel inspection.

Fit/100%, wheel/button zoom, synchronized drag-to-pan, Lanczos display resampling,
and the 64 MiB rendered-pair cache are retained. Native work runs in an isolated
child process; debounced UI requests coalesce and obsolete results are discarded.
Closing a window does not forcibly interrupt an already running native call;
it may finish before the process exits. A failed native render is labelled as
failed, without substituting a target LUT frame as a verified result.

## RAW / colour conditions

The file chooser includes CR2/CR3/CRW, DNG, NEF/NRW, ARW, RAF, ORF, RW2 and other
rawpy/LibRaw extensions. Actual support depends on camera and compression mode.
LibRaw target mode develops full-resolution sensor data with camera WB,
no auto brightness, and 8-bit sRGB. Native mode uses Canon development instead.
No automatic Log/gamut input conversion is inferred from a LUT filename.
An N-Log/Rec.2020 LUT applied directly to sRGB is interpreted as that explicit
RGB mapping, not as a complete colour-managed N-Log workflow.

## Validation (2026-10-28)

The original 28 v0.5 tests passed on Windows, including real Canon DLL rendering, full editable
property readback, RAW decode, native comparison pixels, UI latest-request
handling/mode switching, fit error, identity/zero-strength, and high-resolution
preview interactions. Native tests used the user's `832A1631.CR3` and
`RED_FilmBiasOffset_Rec2020_N-Log_to_Rec709_BT1886.cube` without redistributing them.

For that test (Neutral / 100%):

- Held-out model RGB MAE: **4.73 / 255**.
- Actual Canon PF3 image versus target-on-Canon-baseline RGB MAE: **3.78 / 255**.
- Actual image 95th percentile channel difference: **11 / 255**.

These are results for one photograph/LUT/settings combination, not a guarantee
for other LUTs or files. They compare the target with the fitted result; the
right-hand native preview itself consists of the actual generated PF3 pixels.
Physical camera output and standalone EXE packaging were not tested.

Run `python -m unittest discover -s tests -v`. Optional native test variables:
`CLB_NATIVE_RAW`, `CLB_NATIVE_LUT`, `CLB_NATIVE_DLL`. `CANON_RAW_TEST_FILE` enables
a real rawpy decode test. Those tests skip when fixtures are absent; Tk tests
skip when no desktop display is available. The native colour-error threshold
in the integration test is a regression target for the reported fixture.

## CLI / build

`python cli.py input.cube -o output.pf3 --base Neutral --strength 1.0` (also accepts `.xmp` inputs; see above)

The JSON output includes approximation metrics and a parser round-trip flag.
It does not claim native image validation unless a separate render is performed.
`build_windows.bat` or the included GitHub workflow builds the EXE and collects
rawpy's native dependencies. Both source and EXE use the same isolated Canon worker.

## Implementation notes

`canon_fit.py` implements a 19-term cubic colour model with three 12-knot post
curves. Fixed-point coefficients and curve points are quantized before validation.
`pf3_native.py` serializes through the locally installed Canon DLL and reads back
**all generated properties**, not just the 3D tables. Native serializer sessions
are locked because Canon initialization is process-global.
`canon_render.py` performs read-only development in a separate process and uses
the loaded-file Picture Style selector (255), not the built-in base selector.
The first development frame is discarded to avoid initial colour instability.

API research reference: https://github.com/LvClFER/Lut-to-Canon-Picture-Style
Canon resources remain in the user's installation and are not redistributed.

## XMP technical and compatibility references

- Adobe official Photoshop Camera Raw XMP sidecar documentation:
  https://helpx.adobe.com/camera-raw/desktop/get-started/overview-and-setup/camera-raw-settings.html
- Adobe DNG SDK (RGB table serialization):
  https://www.adobe.com/support/downloads/dng/dng_sdk.html
- Open documentation of Adobe RGBTable encoding and color-space fields:
  https://github.com/mvimercati/xmp2cube
  https://github.com/MariuzM/learning-archive/tree/main/lut-to-lightroom-camera-profile

These links are interoperability references; the project ships its own Python
implementation. It does not redistribute Canon DLLs or Adobe assets.
