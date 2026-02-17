# Project: toggle_chrome_google_translate

This project is managed using `uv`.

## 1. Development & Testing
Run the root script directly:
```bash
uv run main.py
```

## 2. Execute Module (CLI)
Run the packaged module entry point (toggle_chrome_google_translate.cli:main)
```
uv run toggle_chrome_google_translate
```

## 3. Local Installation
Install the module globally via `uv` tool storage to run it from anywhere:
```
uv tool install .
toggle_chrome_google_translate
```

## 4. Standalone Binary Build
Generate a single `.exe` for environments without Python or `uv`:
```
uv run --with pyinstaller pyinstaller --onefile src/toggle_chrome_google_translate/cli.py --name toggle_chrome_google_translate_standalone
dist\toggle_chrome_google_translate_standalone.exe
```
