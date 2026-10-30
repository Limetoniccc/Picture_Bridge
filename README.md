# Picture Bridge

Picture Bridge is an image profile conversion tool developed by LimeT.

It enables conversion between various image profile formats used in photography and image editing, including Adobe XMP, 3D LUT (CUBE), and Canon Picture Style (PF3).

## Information

- **Name:** Picture Bridge
- **Version:** 1.1
- **Developer:** LimeT
- **License:** MIT

## Features

### Image Profile Conversion

- **CUBE → PF3:** Convert 3D LUT files into Canon Picture Style files.
- **XMP → PF3:** Convert Adobe Lightroom presets into Canon Picture Style files.
- **CUBE → XMP:** Convert 3D LUT files into Adobe Lightroom-compatible presets.
- **XMP → CUBE:** Convert Adobe Lightroom presets into 3D LUT files for applications such as Adobe Photoshop.
- **CUBE / XMP → LUMIX CUBE:** Generate LUT files compatible with supported Panasonic LUMIX workflows.

### Additional Features

- High-resolution image previews
- RAW image preview support
- Automatic conversion strength recommendations using 1–5 RAW reference images
- LUT structure analysis
- Adjustable conversion parameters
- Multilingual user interface

## Supported Formats

| Format | Description |
|---|---|
| `.cube` | 3D Lookup Table (LUT) |
| `.xmp` | Adobe Lightroom / Camera Raw Preset |
| `.pf3` | Canon Picture Style File |

Conversion results may vary depending on the characteristics of the source profile and the limitations of the target format.

## Supported Languages

- Korean
- English
- Japanese
- Simplified Chinese

## Installation

Download the latest version from the **Releases** section.

### Windows

1. Download and extract the release ZIP file.
2. Install Python 3.10 or later (64-bit).
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run `launch_windows.bat` to launch Picture Bridge.

The source distribution does not include a precompiled Windows executable.

## Usage

1. Launch Picture Bridge.
2. Select a supported input file.
3. Choose the desired output format.
4. Adjust the conversion settings if necessary.
5. Preview the conversion result.
6. Convert and save the output file.

## Compatibility

Picture Bridge supports profile conversion workflows involving:

- Canon Picture Style
- Adobe Lightroom
- Adobe Photoshop
- Panasonic LUMIX LUT workflows

Compatibility and conversion accuracy may vary depending on the source file, target application, and supported camera model.

## Developer

**LimeT**

## Disclaimer

Picture Bridge is an independent, open-source project.

It is not affiliated with, endorsed by, or officially supported by Canon Inc., Adobe Inc., or Panasonic Corporation.

All trademarks and product names are the property of their respective owners.
