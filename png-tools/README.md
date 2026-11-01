# PNG Tools

Updated PNG Codex + tools for analysis and basic repair.

## Contents

- `PNG_CODEX.md` – Full structure reference (signature, chunks, IHDR, CRC, etc.)
- `header_search.py` – Parse and search PNG chunks / headers
- `fix_corrupt_png.py` – Attempt to fix common corruption (bad signature, missing IEND, rebuild via Pillow)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

**Search chunks:**
```bash
python header_search.py image.png
python header_search.py image.png --search IHDR --dump
```

**Fix corrupt PNG:**
```bash
python fix_corrupt_png.py broken.png
python fix_corrupt_png.py broken.png fixed.png
```

Note: The fixer handles simple structural issues. Severe corruption (heavily damaged IDAT, etc.) may still fail.
