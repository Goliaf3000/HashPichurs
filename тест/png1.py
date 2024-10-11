import sys
import struct

fn1 = "1.png"
fn2 = "2.png"
with open(fn1, "rb") as f:
  d1 = f.read()
with open(fn2, "rb") as f:
  d2 = f.read()

# Картинки должны начинаться с данных префиксов
PNGSIG = b"\x89PNG\r\n\x1a\n"

# Assert проверяет подленность условия, что картинки PNG
assert d1.startswith(PNGSIG)
assert d2.startswith(PNGSIG)

# short coll
with open("png1.bin", "rb") as f:
  blockS = f.read()
# long coll
with open("png2.bin", "rb") as f:
  blockL = f.read()

ascii_art = b'209 141 209 130 208 190 32 208 178 208 183 208 187 208 190 208 188 32 109 100 53 209 141 209 130 208 190 32 208 178 208 183 208 187 208 190 208 188 32 109 100 53 209 141 209 130 208 190 32 208 178 208 183 208 187 208 190 208 188 32 109 100 53 1'
# 2 CRCs, 0x100 of UniColl difference, and d2 chunks
skipLen = 0x100 - 4*2 + len(d2[8:])


from binascii import crc32
_crc32 = lambda d:(crc32(d) % 0x100000000)

suffix = struct.pack(">I", _crc32(blockS[0x4b:0xc0]))

suffix += b"".join([
  # sKIP chunk
    struct.pack(">I", skipLen),
    b"sKIP",
      # it will cover all data chunks of d2,
      # and the 0x100 buffer
  ascii_art,
  b"\xDE\xAD\xBE\xEF", # fake CRC for cOLL chunk

      d2[8:],
      # long cOLL CRC
    b"\x5E\xAF\x00\x0D", # fake CRC for sKIP chunk

    # first image chunk
    d1[8:],
    ])

with open("collision1.png", "wb") as f:
  f.write(b"".join([
    blockS,
    suffix
    ]))

with open("collision2.png", "wb") as f:
  f.write(b"".join([
    blockL,
    suffix
    ]))

