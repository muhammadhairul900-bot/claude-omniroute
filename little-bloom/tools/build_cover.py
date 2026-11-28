"""New cover for Flowers Coloring Book Vol. 1 – Edition 2.0.
Usage: python3 build_cover.py   -> ../cover.png (2480x3508) and ../cover.pdf (A4)
Needs: crops/f01.png (hibiscus line art) and assets/colour_*.png (coloured flowers)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as nd

T = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(T)
W, H = 2480, 3508


def F(name, size):
    return ImageFont.truetype(os.path.join(T, "fonts", name), size)


# ------------------------------------------------------------ half-coloured hibiscus
def coloured_hibiscus():
    a = np.array(Image.open(os.path.join(T, "crops", "f01.png")).convert("L"))
    a = np.pad(a, 20, constant_values=255)
    h, w = a.shape
    line = a < 150
    white = ~nd.binary_dilation(line, iterations=1)
    lab, n = nd.label(white)
    sizes = nd.sum(white, lab, range(1, n + 1))
    cents = nd.center_of_mass(white, lab, range(1, n + 1))
    rgb = np.full((h, w, 3), 255, np.uint8)
    yy, xx = np.mgrid[0:h, 0:w]
    fcx, fcy = 0.47 * w, 0.40 * h
    dist = np.sqrt((xx - fcx) ** 2 + (yy - fcy) ** 2) / (0.45 * w)
    dist = np.clip(dist, 0, 1)[..., None]
    for i in range(n):
        sz = sizes[i]
        if sz < 30:
            continue
        cy, cx = cents[i][0] / h, cents[i][1] / w
        m = lab == i + 1
        if m[0, 0]:
            continue  # background
        if sz > 90000:                       # petals: radial red
            inner, outer = np.array([170, 20, 40]), np.array([240, 60, 60])
            col = (inner + (outer - inner) * dist).astype(np.uint8)
            rgb[m] = col[m]
        elif sz > 40000 or (cy > 0.65 and sz > 15000):   # leaves & stem
            base = np.array([70, 160, 80]) if sz > 40000 else np.array([55, 135, 65])
            shade = (base * (0.85 + 0.25 * (1 - dist))).clip(0, 255).astype(np.uint8)
            rgb[m] = shade[m]
        elif sz > 10000:                     # stamen column
            rgb[m] = (250, 200, 40)
        else:                                # pollen knobs
            rgb[m] = (255, 165, 30)
    col = rgb.copy()
    col[line] = 0
    # soften: anti-aliased lines from original greyscale
    g = a[..., None].astype(float) / 255
    col = (col.astype(float) * g).astype(np.uint8)
    lineart = np.repeat(a[..., None], 3, axis=2)
    out = lineart.copy()
    split = int(0.5 * w)
    out[:, split:] = col[:, split:]
    alpha = np.where(a < 250, 255, 0).astype(np.uint8)
    alpha[(lab > 0) & ~np.isin(lab, [lab[0, 0]])] = 255
    im = Image.fromarray(out).convert("RGBA")
    im.putalpha(Image.fromarray(alpha))
    return im, split


# ------------------------------------------------------------ helpers
def leaf(d, cx, cy, length, width, angle, fill, vein):
    pts = []
    for k in range(41):
        t = k / 40
        x = (t - 0.5) * length
        y = math.sin(math.pi * t) * width / 2
        pts.append((x, y))
    pts += [(x, -y) for (x, y) in reversed(pts)]
    ca, sa = math.cos(angle), math.sin(angle)
    P = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for (x, y) in pts]
    d.polygon(P, fill=fill)
    d.line([(cx - length / 2 * ca, cy - length / 2 * sa), (cx + length / 2 * ca, cy + length / 2 * sa)], fill=vein, width=10)
    for k in range(1, 6):
        t = -0.4 + k * 0.15
        bx, by = cx + t * length * ca, cy + t * length * sa
        for s in (1, -1):
            ex = bx + (0.12 * length) * ca - s * (0.32 * width) * sa
            ey = by + (0.12 * length) * sa + s * (0.32 * width) * ca
            d.line([(bx, by), (ex, ey)], fill=vein, width=6)


def shadowed(base, im, xy, blur=25, off=(18, 24), alpha=90):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.split()[3].point(lambda v: alpha if v > 10 else 0))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1]))
    base.alpha_composite(im, xy)


def colour_flower(name, height):
    im = Image.open(os.path.join(T, "assets", f"colour_{name}.png")).convert("RGB")
    a = np.array(im)
    alpha = np.where(a.min(2) > 245, 0, 255).astype(np.uint8)
    alpha = nd.binary_fill_holes(alpha > 0).astype(np.uint8) * 255
    im = im.convert("RGBA")
    im.putalpha(Image.fromarray(alpha))
    s = height / im.height
    return im.resize((int(im.width * s), int(height)), Image.LANCZOS)


def bee(d, x, y, s):
    d.ellipse((x - 30 * s, y - 70 * s, x + 25 * s, y - 5 * s), fill=(235, 248, 255), outline=(40, 40, 40), width=int(6 * s))
    d.ellipse((x + 5 * s, y - 60 * s, x + 60 * s, y - 2 * s), fill=(235, 248, 255), outline=(40, 40, 40), width=int(6 * s))
    d.polygon([(x + 95 * s, y + 5 * s), (x + 125 * s, y + 15 * s), (x + 95 * s, y + 28 * s)], fill=(40, 40, 40))
    d.ellipse((x - 70 * s, y - 25 * s, x + 105 * s, y + 60 * s), fill=(255, 205, 40), outline=(40, 40, 40), width=int(7 * s))
    for sx in (-5, 35):
        d.rounded_rectangle((x + sx * s, y - 22 * s, x + (sx + 20) * s, y + 57 * s), radius=8 * s, fill=(40, 40, 40))
    d.ellipse((x - 120 * s, y - 30 * s, x - 40 * s, y + 50 * s), fill=(255, 205, 40), outline=(40, 40, 40), width=int(7 * s))
    for ex in (-98, -70):
        d.ellipse((x + ex * s, y - 2 * s, x + (ex + 12) * s, y + 12 * s), fill=(40, 40, 40))
    d.arc((x - 100 * s, y + 5 * s, x - 62 * s, y + 35 * s), 20, 160, fill=(40, 40, 40), width=int(5 * s))
    d.ellipse((x - 112 * s, y + 14 * s, x - 100 * s, y + 26 * s), fill=(255, 140, 150))
    for (ax, bx) in ((-95, -110), (-65, -50)):
        d.line((x + ax * s, y - 25 * s, x + bx * s, y - 70 * s), fill=(40, 40, 40), width=int(6 * s))
        d.ellipse((x + bx * s - 10 * s, y - 80 * s, x + bx * s + 10 * s, y - 60 * s), fill=(40, 40, 40))


def outlined_text(base, xy, text, font, fill, stroke=(255, 255, 255), sw=20, shadow=True, anchor="mm"):
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 14, xy[1] + 18), text, font=font, fill=(0, 0, 0, 110),
                                stroke_width=sw, stroke_fill=(0, 0, 0, 110), anchor=anchor)
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(base).text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)


# ------------------------------------------------------------ compose (lush style)
import random
rnd = random.Random(7)
img = Image.new("RGBA", (W, H))
# sky
top, mid = np.array([70, 160, 235]), np.array([170, 220, 250])
g = np.linspace(0, 1, H)[:, None]
grad = (top + (mid - top) * np.clip(g * 3, 0, 1)).astype(np.uint8)
img.paste(Image.fromarray(np.repeat(grad[:, None, :], W, axis=1)).convert("RGBA"))
# sun rays + clouds
ray = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ray)
sx0, sy0 = W / 2, 520
for k in range(24):
    a0 = k * 2 * math.pi / 24
    rd.polygon([(sx0, sy0), (sx0 + 3000 * math.cos(a0), sy0 + 3000 * math.sin(a0)),
                (sx0 + 3000 * math.cos(a0 + 0.12), sy0 + 3000 * math.sin(a0 + 0.12))], fill=(255, 255, 230, 40))
rd.ellipse((sx0 - 380, sy0 - 380, sx0 + 380, sy0 + 380), fill=(255, 250, 210, 150))
img.alpha_composite(ray.filter(ImageFilter.GaussianBlur(20)))
cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cdd = ImageDraw.Draw(cl)
for (x, y, s) in [(700, 230, 1.0), (1650, 160, 1.2), (2250, 420, 0.8), (200, 520, 0.9)]:
    for (ox, oy, r) in [(0, 0, 90), (90, -40, 110), (200, 0, 90), (100, 30, 100)]:
        cdd.ellipse((x + ox * s - r * s, y + oy * s - r * s, x + ox * s + r * s, y + oy * s + r * s), fill=(255, 255, 255, 230))
img.alpha_composite(cl.filter(ImageFilter.GaussianBlur(6)))

# dense leafy jungle (back to front, darker at back)
lv = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(lv)
ld.rectangle((0, 1250, W, H), fill=(30, 100, 50))
for layer, (n, gmin, gmax, ytop) in enumerate([(70, 70, 110, 700), (90, 110, 160, 900), (80, 140, 200, 1100)]):
    for _ in range(n):
        cx = rnd.uniform(-150, W + 150)
        cy = rnd.uniform(ytop, H + 100)
        if 330 < cx < 2150 and 560 < cy < 1700:
            continue   # keep the plaque area cleaner
        Lg = rnd.uniform(380, 720)
        Wd = Lg * rnd.uniform(0.32, 0.45)
        gcol = int(rnd.uniform(gmin, gmax))
        col = (int(gcol * 0.35), gcol, int(gcol * 0.45))
        leaf(ld, cx, cy, Lg, Wd, rnd.uniform(0, math.pi * 2), col, (min(255, col[0] + 70), min(255, col[1] + 60), min(255, col[2] + 50)))
lv = lv.filter(ImageFilter.GaussianBlur(1.2))
img.alpha_composite(lv)
# water droplets on leaves
dd = ImageDraw.Draw(img)
for _ in range(90):
    x, y = rnd.uniform(0, W), rnd.uniform(1300, H)
    r = rnd.uniform(8, 18)
    dd.ellipse((x - r, y - r, x + r, y + r), fill=(220, 245, 230, 170))
    dd.ellipse((x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2), fill=(255, 255, 255, 230))


def put(name, h, x, y, angle=0, shadow=True):
    f = colour_flower(name, h)
    if angle:
        f = f.rotate(angle, expand=True, resample=Image.BICUBIC)
    if shadow:
        shadowed(img, f, (int(x), int(y)), blur=20, off=(14, 20), alpha=110)
    else:
        img.alpha_composite(f, (int(x), int(y)))


# corner + side flowers (behind plaque)
put("hibiscus", 1250, -170, -40, angle=12)
put("orchid", 1250, 1500, -60, angle=-8)
put("bougainvillea", 700, -120, 1150, angle=15)
put("frangipani", 640, 1990, 1080, angle=-12)

# plaque
P0, P1, Q0, Q1 = 250, 2230, 640, 1610
pl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(pl)
pd.rounded_rectangle((P0 + 25, Q0 + 35, P1 + 25, Q1 + 35), radius=120, fill=(0, 0, 0, 120))
img.alpha_composite(pl.filter(ImageFilter.GaussianBlur(28)))
d = ImageDraw.Draw(img)
d.rounded_rectangle((P0, Q0, P1, Q1), radius=120, fill=(214, 160, 50))
d.rounded_rectangle((P0 + 22, Q0 + 22, P1 - 22, Q1 - 22), radius=100, fill=(255, 230, 140))
d.rounded_rectangle((P0 + 40, Q0 + 40, P1 - 40, Q1 - 40), radius=86, fill=(255, 248, 228))
d.rounded_rectangle((P0 + 62, Q0 + 62, P1 - 62, Q1 - 62), radius=70, outline=(225, 185, 90), width=6)
# top flower ornament
put("golden_trumpet", 420, W / 2 - 150, Q0 - 250)

FT = F("PlayfairDisplay-Black.ttf", 300)
outlined_text(img, (W / 2, 930), "Tropical", FT, (200, 30, 40), stroke=(255, 255, 255), sw=12, shadow=True)
outlined_text(img, (W / 2, 1220), "Flowers", FT, (200, 30, 40), stroke=(255, 255, 255), sw=12, shadow=True)
d = ImageDraw.Draw(img)
d.text((W / 2, 1460), "Coloring & Activity Book", font=F("Fredoka-SemiBold.ttf", 150), fill=(25, 45, 140), anchor="mm")

# ribbon
R0, R1, RY0, RY1 = 330, 2150, 1590, 1780
for side in (-1, 1):
    ex = R0 if side < 0 else R1
    d.polygon([(ex, RY0 + 50), (ex + side * 230, RY0 + 50), (ex + side * 150, (RY0 + RY1) / 2 + 25),
               (ex + side * 230, RY1 + 50), (ex, RY1 + 50)], fill=(196, 140, 30))
    d.polygon([(ex, RY1), (ex, RY1 + 50), (ex - side * 40, RY1)], fill=(150, 100, 20))
d.rectangle((R0, RY0, R1, RY1), fill=(250, 205, 70))
d.rectangle((R0, RY0 + 14, R1, RY0 + 22), fill=(255, 235, 150))
d.text((W / 2, (RY0 + RY1) / 2), "– 30 Fun Flowers from Malaysia –", font=F("PlayfairDisplay-Black.ttf", 96), fill=(25, 75, 35), anchor="mm")

# lower garden
put("ixora", 640, 1850, 1820, angle=-8)
put("sunflower", 640, 60, 1820, angle=8)
# centre half-coloured hibiscus on a soft glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((W / 2 - 760, 1880, W / 2 + 760, 3340), fill=(255, 255, 255, 235))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
hib, split = coloured_hibiscus()
s = 1400 / hib.height
hib = hib.resize((int(hib.width * s), 1400), Image.LANCZOS)
hx, hy = W // 2 - hib.width // 2 + 30, 1930
img.alpha_composite(hib, (hx, hy))
d = ImageDraw.Draw(img)
sxl = hx + int(split * s)
for yy in range(hy + 60, hy + hib.height - 60, 46):
    d.line((sxl, yy, sxl, yy + 22), fill=(226, 74, 92), width=9)
put("lotus", 1050, -120, 2520, angle=6)
put("torch_ginger", 1100, 1820, 2480, angle=-5)
put("butterfly_pea", 620, 1350, 2930, angle=-10)
put("chrysanthemum", 520, 760, 3050, angle=10)

d = ImageDraw.Draw(img)
# bee with dotted trail
for k in range(11):
    t = k / 10
    px = 560 + 380 * t
    py = 1980 - 140 * math.sin(math.pi * t) + 60 * t
    d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=(60, 60, 60))
bee(d, 1080, 2010, 1.5)

# VOL badge
d.ellipse((2060, 1880 - 1830, 2410, 1880 - 1480), fill=(200, 30, 40), outline=(255, 255, 255), width=16)
d.text((2235, 165), "VOL.", font=F("Nunito-Black.ttf", 76), fill=(255, 255, 255), anchor="mm")
d.text((2235, 275), "1", font=F("Fredoka-SemiBold.ttf", 140), fill=(255, 255, 255), anchor="mm")
# age badge
bx, by = 270, 2400
d.ellipse((bx - 200, by - 200, bx + 200, by + 200), fill=(255, 210, 50), outline=(255, 255, 255), width=18)
d.text((bx, by - 70), "AGES", font=F("Nunito-Black.ttf", 78), fill=(120, 60, 0), anchor="mm")
d.text((bx, by + 40), "3–10", font=F("Fredoka-SemiBold.ttf", 128), fill=(120, 60, 0), anchor="mm")
# fun facts pill (right)
f = F("Nunito-Black.ttf", 70)
for i, t_ in enumerate(["FUN FACTS", "+ ACTIVITIES"]):
    pass
d.ellipse((1990, 2200, 2400, 2610), fill=(25, 45, 140), outline=(255, 255, 255), width=18)
d.text((2195, 2335), "FUN", font=F("Nunito-Black.ttf", 82), fill=(255, 255, 255), anchor="mm")
d.text((2195, 2415), "FACTS +", font=F("Nunito-Black.ttf", 66), fill=(255, 255, 255), anchor="mm")
d.text((2195, 2487), "GAMES", font=F("Nunito-Black.ttf", 66), fill=(255, 230, 120), anchor="mm")
# brand
f = F("Nunito-Black.ttf", 76)
txt = "LITTLE BLOOM STUDIO"
tw = d.textlength(txt, font=f)
d.rounded_rectangle((W / 2 - tw / 2 - 70, 3330, W / 2 + tw / 2 + 70, 3465), radius=68, fill=(255, 248, 228), outline=(214, 160, 50), width=10)
d.text((W / 2, 3398), txt, font=f, fill=(200, 30, 40), anchor="mm")

out = img.convert("RGB")
out.save(os.path.join(L, "cover.png"), optimize=True)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io
buf = io.BytesIO()
out.save(buf, "JPEG", quality=92)
buf.seek(0)
c = canvas.Canvas(os.path.join(L, "cover.pdf"), pagesize=A4)
c.setTitle("Tropical Flowers – Coloring & Activity Book – Cover")
c.drawImage(ImageReader(buf), 0, 0, A4[0], A4[1])
c.showPage()
c.save()
print("cover saved")
