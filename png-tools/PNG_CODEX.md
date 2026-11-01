# PNG Codex – Updated File Structure Reference

**Signature (first 8 bytes)**  
`89 50 4E 47 0D 0A 1A 0A`  
(ASCII: `\x89PNG\r\n\x1A\n`)

## Chunk Layout
Every chunk after the signature:

| Field     | Size     | Description                                      |
|-----------|----------|--------------------------------------------------|
| Length    | 4 bytes  | Big-endian unsigned integer (data length only)   |
| Type      | 4 bytes  | ASCII chunk type (e.g. `IHDR`)                   |
| Data      | N bytes  | Chunk payload                                    |
| CRC-32    | 4 bytes  | CRC over Type + Data (not Length)                |

**CRC** is the standard CRC-32 (ISO 3309 / ITU-T V.42).

## Critical Chunks (required)
| Chunk | Must be | Notes |
|-------|---------|-------|
| **IHDR** | First   | 13-byte data: width, height, bit depth, color type, compression, filter, interlace |
| **PLTE** | Before IDAT (if present) | Palette (required for color type 3) |
| **IDAT** | After PLTE (if any) | Compressed image data (zlib/DEFLATE). Multiple allowed, must be consecutive |
| **IEND** | Last    | Empty data. Marks end of file |

### IHDR Fields (13 bytes)
| Offset | Size | Field              | Values |
|--------|------|--------------------|--------|
| 0      | 4    | Width              | > 0    |
| 4      | 4    | Height             | > 0    |
| 8      | 1    | Bit depth          | 1,2,4,8,16 |
| 9      | 1    | Color type         | 0=Gray, 2=RGB, 3=Indexed, 4=Gray+Alpha, 6=RGBA |
| 10     | 1    | Compression method | Always 0 |
| 11     | 1    | Filter method      | Always 0 |
| 12     | 1    | Interlace method   | 0=None, 1=Adam7 |

## Common Ancillary Chunks
| Chunk | Purpose |
|-------|---------|
| **sRGB** | Standard RGB color space |
| **gAMA** | Gamma |
| **cHRM** | Chromaticities |
| **iCCP** | ICC profile |
| **sBIT** | Significant bits |
| **tRNS** | Transparency |
| **bKGD** | Background color |
| **pHYs** | Physical pixel dimensions |
| **tEXt** / **zTXt** / **iTXt** | Text metadata |
| **tIME** | Modification time |
| **eXIf** | EXIF data |

## Chunk Naming Rules
- Uppercase first letter = critical
- Lowercase first letter = ancillary
- Second letter uppercase = public, lowercase = private
- etc. (see PNG spec for full rules)

## Minimal Valid PNG
Signature + IHDR + (one or more) IDAT + IEND

---

*Reference: PNG Specification (W3C / ISO/IEC 15948). Useful for analysis, steganography, corruption diagnosis, and custom tooling.*
