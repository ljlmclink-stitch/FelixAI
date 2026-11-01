#!/usr/bin/env python3
"""
PNG Header / Chunk Search Tool

Parse a PNG and list all chunks, search for specific types, or dump details.

Usage:
    python header_search.py image.png
    python header_search.py image.png --search IHDR
    python header_search.py image.png --search tEXt --dump
"""

import sys
import struct
import zlib
from pathlib import Path

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

def crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xffffffff

def parse_chunks(data: bytes):
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Not a valid PNG signature")
    pos = 8
    chunks = []
    while pos + 12 <= len(data):
        length = struct.unpack('>I', data[pos:pos+4])[0]
        ctype = data[pos+4:pos+8]
        if pos + 12 + length > len(data):
            break
        cdata = data[pos+8:pos+8+length]
        stored_crc = struct.unpack('>I', data[pos+8+length:pos+12+length])[0]
        computed_crc = crc32(ctype + cdata)
        chunks.append({
            'offset': pos,
            'length': length,
            'type': ctype.decode('ascii', errors='replace'),
            'data': cdata,
            'crc': stored_crc,
            'crc_ok': stored_crc == computed_crc,
        })
        pos += 12 + length
        if ctype == b'IEND':
            break
    return chunks

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = Path(sys.argv[1])
    search = None
    dump = False
    if '--search' in sys.argv:
        idx = sys.argv.index('--search')
        if idx + 1 < len(sys.argv):
            search = sys.argv[idx + 1].upper()
    if '--dump' in sys.argv:
        dump = True

    data = path.read_bytes()
    try:
        chunks = parse_chunks(data)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"File: {path.name}")
    print(f"Size: {len(data)} bytes")
    print(f"Chunks found: {len(chunks)}\n")

    for i, c in enumerate(chunks):
        if search and c['type'].upper() != search:
            continue
        status = "OK" if c['crc_ok'] else "BAD CRC"
        print(f"[{i}] {c['type']:4}  len={c['length']:8}  offset={c['offset']:8}  CRC={status}")
        if dump and c['type'] in ('tEXt', 'iTXt', 'zTXt', 'IHDR'):
            if c['type'] == 'IHDR' and len(c['data']) >= 13:
                w, h = struct.unpack('>II', c['data'][:8])
                print(f"     Width={w} Height={h} BitDepth={c['data'][8]} ColorType={c['data'][9]}")
            else:
                preview = c['data'][:80]
                try:
                    print(f"     Data: {preview.decode('utf-8', errors='replace')}")
                except:
                    print(f"     Data (hex): {preview.hex()}")

if __name__ == '__main__':
    main()
