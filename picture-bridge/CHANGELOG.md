## v1.0 — Four-language interface update (2026-10-28)

- Added runtime UI language selection: 한국어, English, 日本語, 简体中文.
- Localized main controls, preview toolbar and modes, status messages, file-dialog
  filters, success/error dialogs, common XMP conversion warnings, and About panel.
- Remember language across launches via local settings.json; operate fully offline.
- Added quick-start instructions in Korean, English, Japanese, and Simplified Chinese.
- Preserved Picture Bridge v1.0 branding (Created by LimeT) and all file converters.
- Added localization catalog validation and GUI integration regression tests.

# Changelog

## v1.0 (2026-10-28)

- Rename the application to **Picture Bridge** and set version **1.0**.
- Credit **LimeT** as the creator in the GUI, About window, CLI and documentation.
- Package the Windows executable as `PictureBridge.exe` and embed Windows file
  metadata (product name, version 1.0 and LimeT).
- Default Adobe creative profiles to the `Picture Bridge` group.
- Retain v0.6 CUBE/XMP/PF3 conversion, high-resolution preview and native export.


## v0.6 (2026-10-28)

- Add `.xmp` to existing CUBE/PF3 GUI source picker.
- Decode XMP creative profile RGBTable with bounded Adobe-base85/zlib parser,
  color-space metadata and sRGB conversion.
- Convert supported XMP develop-preset sliders/curves/HSL/color grading into
  explicitly approximate sampled RGB cube; flag ignored features.
- Export real Adobe creative profile XMP with an embedded 32³ RGBTable from CUBE,
  including round-trip verification and source resampling error.
- Route CLI based on source/output file extensions, preserve Windows Canon
  PSE/DLL PF3 pipeline, maintain full-resolution photo preview.
- 40 unit/integration tests passed under Linux/Xvfb; two external Canon/RAW
  fixture tests skipped. Adobe application import and newly converted XMP→PF3
  native rendering must be checked on a Windows PC with licensed software.

## v0.5 (2026-10-28)

- Fix DPP ignoring LUT-only exports: fit into editable RGB polynomial/curves.
- Keep camera grids identity to avoid applying the look twice.
- Add actual generated-PF3 Canon RAW preview in an isolated native worker.
- Distinguish native PF3 results from high-resolution target LUT references.
- Report held-out model error and actual native-image target error.
- Verify every generated property on readback; serialize DLL sessions safely.
- Pass 28 tests including real Canon RAW/PF3 rendering and GUI mode changes.
- Reported fixture: native-image RGB MAE 3.78/255; camera hardware untested.


## v0.4 (2026-10-28)

- Add rawpy/LibRaw full-resolution RAW input and grouped photo/RAW file filters.
- Develop RAW with camera WB, 8-bit sRGB and automatic brightness disabled.
- Decode photos on a background worker; preserve the previous photo on errors.
- Include rawpy native libraries in EXE build commands.
- Cancel GUI timers during shutdown to prevent stale Tk callback errors.
- Pass 20 tests, including an actual Canon 40D sRAW CR2 decode.


## v0.3 (2026-10-28)

- Retain original photo resolution and apply EXIF orientation.
- Add synchronized resizable dual canvases, Fit/100%, zoom and pan.
- Add resolution/zoom display, Lanczos rendering and live strength updates.
- Add background visible-region rendering, debounce, latest-result checks and 64 MiB LRU.
- Add Windows DPI awareness and five preview tests including Tk integration.
- Preserve PF3 export implementation; Canon DLL/camera validation remains outstanding.

## v0.2 (2026-10-28)

- Added direct Canon PF3 generation using locally installed PSE `EdsCFParse.dll`.
- Added Windows native DLL discovery and manual override.
- Converted .cube into dual 33³/12-bit LUT tables, with strength blending.
- Added neutral post-LUT curves/matrices to avoid zero-map black output.
- Added PF3 PSP header and native table readback verification.
- Added base style selection and command-line batch conversion.
- Added Windows packaging workflow and unit tests.
- Real Windows, PSE-import and EOS-camera validation **not yet performed**.

## v0.1

- LUT inspect/preview and CUBE resampling.
- No direct PF3 generation (superseded by v0.2).
