"""
Convert photo PNGs to JPGs (smaller for non-transparent images).
Brand logos stay PNG — they need transparency.
"""
from PIL import Image
import os, glob

def to_jpg(path, quality=85, max_w=1600):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    if w > max_w:
        new_h = int(h * max_w / w)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    out = path.rsplit('.',1)[0] + '.jpg'
    img.save(out, 'JPEG', quality=quality, optimize=True, progressive=True)
    os.remove(path)
    return out, os.path.getsize(out)

base = "/Users/taylorjanszen/Desktop/Claude.ai/teamteamworms"
total_before = 0
total_after = 0

# Gallery photos
for p in sorted(glob.glob(f"{base}/photos/photo-*.png")):
    sz_before = os.path.getsize(p)
    out, sz_after = to_jpg(p, quality=82, max_w=1400)
    total_before += sz_before
    total_after += sz_after
    print(f"{os.path.basename(p)}: {sz_before//1024}KB -> {sz_after//1024}KB")

# Cup trophy photos (slightly higher quality, larger max)
for p in sorted(glob.glob(f"{base}/photos/cups/cup-*.png")):
    sz_before = os.path.getsize(p)
    out, sz_after = to_jpg(p, quality=88, max_w=1600)
    total_before += sz_before
    total_after += sz_after
    print(f"{os.path.basename(p)}: {sz_before//1024}KB -> {sz_after//1024}KB")

print(f"\nTotal: {total_before//1024//1024}MB -> {total_after//1024//1024}MB")
