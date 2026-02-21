# SwitchPic-Py
A small Tkinter GUI utility to convert images between common formats using Pillow (PIL).

## Project structure
- `main.py` — the GUI application.
- `images/` — image assets used by the GUI (icons).
- `Results/` — created at runtime to hold converted images.

## Features
- Upload an image from disk.
- Convert and save to: PNG, JPEG, ICO, BMP, TIFF, WEBP.
- Saves converted images into a `Results` folder with a timestamped filename.

## Requirements
- Python 3.7+ (tested on Windows).
- Pillow library.

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install Pillow
```

## Run
From the project folder (PowerShell example):

```powershell
python .\main.py
```

## Usage
- Click `Upload Image` and choose an image file.
- Select the target format from the dropdown (e.g. `PNG (.png)`).
- Click `Change and save` — the app creates `Results` (if missing) and saves the converted file there with a timestamped name.
- Use `Unload Image` to clear the current image and upload a different one.

## Supported input file types
- JPEG/JPG, PNG, WEBP, TIFF, ICO, BMP (as provided to the file dialog in `main.py`).

## Notes & Troubleshooting
- If the app raises an error on startup, ensure the `images/` folder contains the GUI icons referenced in `main.py` (`downloadimg.png`, `uploadimg.png`). If you don't have those images, either add them or remove/change the `PhotoImage` lines in `main.py`.
- For JPEG output, the script converts images to RGB before saving (to avoid mode issues with formats like `RGBA`).
- Converted images are saved with a filename like `05Jan2026011234.png` in `Results/` — the timestamp format is `%d%b%Y%H%M%S`.

## Contributing
Feel free to open issues or submit improvements — e.g., drag-and-drop support, batch conversion, or file name options.
