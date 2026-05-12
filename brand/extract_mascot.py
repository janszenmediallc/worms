"""
Conservative mascot extraction.
Tight crop to remove jersey hem + side wrinkles, then a simple flood fill from
the four corners. No interior color-keying so the cream worm body stays intact.
"""
from PIL import Image, ImageDraw

src = "/Users/taylorjanszen/Desktop/Claude.ai/teamteamworms/brand/worms-mascot.png"
out = "/Users/taylorjanszen/Desktop/Claude.ai/teamteamworms/brand/worms-mascot-clean.png"

img = Image.open(src).convert('RGBA')
w, h = img.size

# Tight crop — remove jersey hem (bottom) and right-side wrinkle (right)
img = img.crop((
    int(w * 0.03),  # left
    int(h * 0.06),  # top — cut more (jersey texture)
    int(w * 0.88),  # right — cut more (wrinkle)
    int(h * 0.82),  # bottom (cut hem)
))
w, h = img.size
print(f"cropped: {w}x{h}")

# Single flood fill from corners, conservative threshold
for corner in [(0,0), (w-1,0), (0,h-1), (w-1,h-1)]:
    ImageDraw.floodfill(img, corner, (0,0,0,0), thresh=65)

# Plus a few mid-edge seeds in case orange isn't fully connected
for x in range(0, w, 30):
    if img.getpixel((x, 0))[3] != 0:
        ImageDraw.floodfill(img, (x, 0), (0,0,0,0), thresh=55)
    if img.getpixel((x, h-1))[3] != 0:
        ImageDraw.floodfill(img, (x, h-1), (0,0,0,0), thresh=55)
for y in range(0, h, 30):
    if img.getpixel((0, y))[3] != 0:
        ImageDraw.floodfill(img, (0, y), (0,0,0,0), thresh=55)
    if img.getpixel((w-1, y))[3] != 0:
        ImageDraw.floodfill(img, (w-1, y), (0,0,0,0), thresh=55)

img.save(out)
print(f"wrote {out}")
