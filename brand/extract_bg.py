"""
Extract clean transparent logos by flood-filling the background from each corner.
Tolerance is set high enough to clear the jersey/sticker bg but preserve the art.
"""
from PIL import Image, ImageDraw

def color_dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def remove_bg_floodfill(in_path, out_path, tolerance=70, edge_tol=110):
    img = Image.open(in_path).convert('RGBA')
    w, h = img.size
    px = img.load()

    # Sample background color from the four corners
    corners = [px[0,0], px[w-1,0], px[0,h-1], px[w-1,h-1]]
    # Average them as the assumed bg
    bg = (
        sum(c[0] for c in corners)//4,
        sum(c[1] for c in corners)//4,
        sum(c[2] for c in corners)//4,
    )
    print(f"{in_path}: bg sampled as {bg}")

    # Flood fill from corners with mid tolerance, then a global pass to catch anti-alias halos.
    seeds = [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
    for sx, sy in seeds:
        ImageDraw.floodfill(img, (sx,sy), (0,0,0,0), thresh=tolerance)

    # Clean up: any pixel within edge_tol of bg AND adjacent to alpha=0 -> alpha=0 too
    # (single pass for speed)
    for y in range(h):
        for x in range(w):
            r,g,b,a = px[x,y]
            if a == 0: continue
            if color_dist((r,g,b), bg) < edge_tol:
                # check if any neighbor is transparent
                neighbor_alpha_zero = False
                for dx in (-1,0,1):
                    for dy in (-1,0,1):
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < w and 0 <= ny < h and px[nx,ny][3] == 0:
                            neighbor_alpha_zero = True
                            break
                    if neighbor_alpha_zero: break
                if neighbor_alpha_zero:
                    px[x,y] = (r,g,b,0)

    img.save(out_path)
    print(f"  -> wrote {out_path}")

if __name__ == "__main__":
    base = "/Users/taylorjanszen/Desktop/Claude.ai/teamteamworms/brand"
    remove_bg_floodfill(f"{base}/team-team-logo.png", f"{base}/team-team-logo-clean.png", tolerance=80, edge_tol=130)
    remove_bg_floodfill(f"{base}/worms-mascot.png", f"{base}/worms-mascot-clean.png", tolerance=55, edge_tol=90)
