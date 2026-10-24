# Capture tools

These are the current implementations used for the Appearance-preview and expanded-showcase workflows. There are no archived calibration scripts, numbered versions, or compiled executables here. The builders emit small x86 Windows executables directly; they do not require a C compiler or install Python inside Windows 98.

## Host requirements

Use Python 3.10 or newer on the modern host:

```sh
python -m pip install -r scripts/requirements.txt
```

Run the commands below from the repository root. Paths inside the scripts are resolved relative to the checkout, so an absolute script path also works from another directory. No personal host paths are embedded.

`build/` contains generated executables and full raw captures and is ignored by Git. Keep only reviewed previews and final showcase composites in the published collection.

## Windows 98 Appearance previews

```sh
python scripts/build_preview.py
python scripts/receive.py --mode preview
```

In the 800×600 Windows 98 guest, open **Display Properties → Appearance**. Place the dialog as in the original captures: the calibrated preview rectangle is `(91,126)` through `(446,319)` in guest-screen coordinates. If the dialog is elsewhere, pass `--crop LEFT TOP RIGHT BOTTOM` to the receiver. Inspect a first result before trusting the batch.

Download and run this in the guest:

```text
http://10.0.2.2:8001/capture-preview.exe
```

The helper finds schemes by exact name, selects each preview without pressing Apply, captures the 800×600 display, and uploads it. It restores the initial preview selection. All 34 schemes must be available in Appearance, including the separately imported Windows Standard (default) reconstruction.

The receiver saves full images and its log under `build/raw-preview/` and writes the cropped images to `previews/`. It does not commit or push changes.

## Native showcase captures

Build the two-scheme test first:

```sh
python scripts/build_showcase.py --test
python scripts/receive.py --mode showcase
```

Download and run in the guest:

```text
http://10.0.2.2:8003/showcase-test.exe
```

The test temporarily applies Brick and Maple and captures five views of each: controls, menu, tooltip, message box, and desktop-color sample. Leave the guest undisturbed until the completion dialog. Message boxes are ended on their owning UI thread after capture. The test saves its live starting metrics, icon font, and colors in `C:\THEMECAP\SHOWTEST.BIN` and attempts to restore them before reporting completion.

Once the test passes, build and run the full batch:

```sh
python scripts/build_showcase.py
```

```text
http://10.0.2.2:8003/showcase.exe
```

The full run captures 34 × 5 = 170 source images, snapshots its starting state in `C:\THEMECAP\SHOWFULL.BIN`, and attempts restoration. It uses live system settings without requesting persistent profile writes. This does temporarily change the appearance of other guest applications.

If a run is forcibly terminated, automatic cleanup cannot run. Recovery executables are generated alongside the capture helper:

- `restore-test-appearance.exe`: restore `SHOWTEST.BIN` after an interrupted test.
- `restore-appearance.exe`: restore `SHOWFULL.BIN` after an interrupted full batch.

Download the appropriate executable from the same receiver URL. Keep the recovery files in the guest until restoration is verified. Ordinary detected failures attempt restoration and show the failing stage and Windows error code. Closing the sample window requests an orderly stop; allow an in-progress capture or upload to finish.

Full images are stored locally in the guest under `C:\THEMECAP` as a fallback. The host receives PNGs and a hash/background-check log under `build/raw-showcase/`. The background check tolerates eight intensity levels per RGB channel for display quantization. It does not prove coverage of every system-color consumer.

## Make the final unified images

```sh
python scripts/compose_showcases.py
```

This reads `build/raw-showcase/` and writes 34 unified scenes plus a crop manifest to `showcases/`. Each scene is 960 pixels wide, with height fitted to the font sizes. Native elements are copied at 1:1 pixel scale, cropped tightly without the extra one-pixel margin, and rearranged over the captured desktop color. No AI redraw or font substitution is used.

To reuse an existing raw-capture archive, or render to a review directory:

```sh
python scripts/compose_showcases.py --input /path/to/raw-captures --output /path/to/review-images
```

The layout expects the current helper's fixed window positions and 800×600 output. Large-font samples retain clipping already present in the source windows. Multiple active-looking states coexist in a composite; it is an illustration, not a screenshot of simultaneous interactive controls. The icon is a stock application icon, and label contrast is chosen by the helper. The desktop field is not Explorer or a wallpaper capture.

## Network and source layout

The guest downloads from and uploads to the host through the 86Box SLiRP alias `10.0.2.2`. The receivers listen on host loopback by default. `capture_common.py` contains the host alias, the two ports, and the collection's scheme order. If those constants change, rebuild the guest executables; `receive.py --port` alone does not change a compiled helper's destination.

- `build_preview.py`: native Appearance capture builder, also supplying the shared PE/assembler emission blocks reused by the showcase builder.
- `build_showcase.py`: current five-view native sample program, modal handling, recovery entry point, and capture/upload implementation.
- `receive.py`: one host receiver with explicit `preview` and `showcase` modes.
- `compose_showcases.py`: the final unified-scene crop and layout implementation.
- `capture_common.py`: portable paths, constants, payload validation, and source ordering.

The showcase builder reuses marked source blocks from `build_preview.py`; keep the two files together when modifying or distributing them. The bundled build is an archival capture utility tested with this Windows 98 VM, not a general-purpose theme installer. The scripts never publish to GitHub automatically.
