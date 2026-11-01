#!/usr/bin/env python3
"""
Simple Corrupt PNG Fixer

Attempts common repairs:
- Fix bad PNG signature
- Add missing IEND chunk
- Re-save via Pillow (rebuilds valid structure)
- Optional: skip bad CRCs with Pillow's LOAD_TRUNCATED_IMAGES

Usage:
    python fix_corrupt_png.py input.png [output.png]
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageFile
except ImportError:
    print("Pillow is required: pip install Pillow")
    sys.exit(1)

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
IEND_CHUNK = b'\x00\x00\x00\x00IEND\xae\x42\x60\x82'

def fix_signature(data: bytearray) -> bool:
    if data[:8] != PNG_SIGNATURE:
        print("Fixing PNG signature...")
        data[:8] = PNG_SIGNATURE
        return True
    return False

def ensure_iend(data: bytearray) -> bool:
    if b'IEND' not in data[-16:]:
        print("Adding missing IEND chunk...")
        data.extend(IEND_CHUNK)
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_fixed.png")

    data = bytearray(src.read_bytes())
    changed = False
    changed |= fix_signature(data)
    changed |= ensure_iend(data)

    if changed:
        tmp = src.with_suffix('.tmp.png')
        tmp.write_bytes(data)
        src_to_open = tmp
    else:
        src_to_open = src

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    try:
        with Image.open(src_to_open) as img:
            print(f"Opened: {img.size} {img.mode}")
            img.save(dst, format='PNG', optimize=False)
            print(f"Saved fixed PNG: {dst}")
    except Exception as e:
        print(f"Failed to repair: {e}")
        sys.exit(1)
    finally:
        if changed and 'tmp' in locals():
            tmp.unlink(missing_ok=True)

if __name__ == '__main__':
    main()
