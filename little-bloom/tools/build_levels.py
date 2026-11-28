"""Easy (p. 35-64) and Challenge (p. 65-94) level pages.

Drop illustrations into ../illustrations named like
    easy_01_hibiscus.png ... easy_30_periwinkle.png
    challenge_01_hibiscus.png ... challenge_30_periwinkle.png
(.png / .jpg / .jpeg / .webp). Missing ones become a dashed placeholder.

Usage: python3 build_levels.py <output_dir>
"""
import glob, os, sys, io
import numpy as np
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
OUTDIR = sys.argv[1]
ILL = os.path.join(S, "..", "illustrations")
src = open(f"{S}/build_en.py").read().split("# ---------------------------------------------------------------- word search")[0]
sys.argv = [sys.argv[0], os.path.join(OUTDIR, "_unused.pdf")]
exec(src)
from reportlab import rl_config
rl_config.useA85 = 0

NAMES = ["Hibiscus", "Jasmine", "Orchid", "Rose", "Sunflower", "Bougainvillea", "Frangipani", "Water Lily",
         "Queen of the Night", "Champaca", "Ylang-Ylang", "Spanish Cherry", "Torch Ginger", "Butterfly Pea",
         "Lavender", "Chrysanthemum", "Tulip", "Daffodil", "Lily", "Daisy", "Moss Rose", "Ten O'Clock Flower",
         "Golden Trumpet", "Canna Lily", "Coleus", "Ixora", "Crown of Thorns", "Rafflesia", "Sacred Lotus",
         "Periwinkle"]


def find_art(level, i):
    for ext in ("png", "jpg", "jpeg", "webp", "PNG", "JPG"):
        hits = sorted(glob.glob(os.path.join(ILL, f"{level}_{i:02d}_*.{ext}")))
        if hits:
            return hits[0]
    return None


def clean(path):
    """Greyscale, pure-white background, trimmed. Returns an ImageReader-ready buffer."""
    im = Image.open(path).convert("L")
    a = np.array(im)
    a[a > 200] = 255
    ys, xs = np.where(a < 200)
    if len(ys):
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = Image.fromarray(a)
    if im.height > 2400:
        s = 2400 / im.height
        im = im.resize((round(im.width * s), 2400), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    buf.seek(0)
    return buf


def badge(c, x, y, text, icon):
    w = pdfmetrics.stringWidth(text, "Black", 10) + 40
    c.saveState()
    c.setLineWidth(1.4)
    c.roundRect(x - w / 2, y - 9, w, 22, 11)
    if icon == "easy":
        # little seedling
        sx, sy = x - w / 2 + 16, y - 4
        c.setLineWidth(1.2)
        c.line(sx, sy, sx, sy + 9)
        c.ellipse(sx - 7, sy + 6, sx, sy + 11)
        c.ellipse(sx, sy + 8, sx + 7, sy + 13)
    else:
        doodle_flower(c, x - w / 2 + 16, y + 2, 4.2)
    c.setFont("Black", 10)
    c.drawString(x - w / 2 + 28, y - 2, text)
    c.restoreState()


def placeholder(c, x, y, w, h, code, fname, name):
    c.saveState()
    c.setLineWidth(1.5)
    c.setDash(6, 4)
    c.roundRect(x + 30, y + 10, w - 60, h - 20, 16)
    c.setDash()
    c.setFillColor(LIGHT)
    c.setFont("Title", 18)
    c.drawCentredString(x + w / 2, y + h / 2 + 10, f"{code} – {name.upper()}")
    c.setFont("Bold", 11)
    c.drawCentredString(x + w / 2, y + h / 2 - 12, f"Add illustration: {fname}")
    c.restoreState()


def build(level):
    easy = level == "easy"
    first = 35 if easy else 65
    out = os.path.join(OUTDIR, f"Level-{'Easy-p35-64' if easy else 'Challenge-p65-94'}-EN.pdf")
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle(f"Flowers Coloring Book Vol. 1 – {'Easy' if easy else 'Challenge'} Level")
    c.setAuthor("Little Bloom Studio")
    found = 0
    for i, name in enumerate(NAMES, 1):
        page = first + i - 1
        code = f"{'E' if easy else 'C'}{i:02d}"
        ts = 46 if easy else 30
        while pdfmetrics.stringWidth(name.upper() if easy else name, "Title", ts) > W - 2 * M - 70:
            ts -= 1
        title = name.upper() if easy else name
        ty = H - 72 if easy else H - 60
        c.setFont("Title", ts)
        c.drawCentredString(W / 2, ty, title)
        tw = pdfmetrics.stringWidth(title, "Title", ts)
        doodle_flower(c, W / 2 - tw / 2 - 24, ty + ts * 0.3, 8)
        doodle_flower(c, W / 2 + tw / 2 + 24, ty + ts * 0.3, 8)
        if easy:
            badge(c, W / 2, H - 100, "EASY  •  AGES 3–5", "easy")
            ax, ay, aw, ah = M, 82, W - 2 * M, H - 118 - 82
        else:
            badge(c, W / 2, H - 84, "CHALLENGE  •  AGES 9+", "chal")
            ax, ay, aw, ah = M - 8, 80, W - 2 * M + 16, H - 102 - 80
        art = find_art(level, i)
        if art:
            draw_img(c, clean(art), ax, ay, aw, ah)
            found += 1
        else:
            placeholder(c, ax, ay, aw, ah, code, f"{level}_{i:02d}_{name.lower().replace(' ', '_').replace(chr(39), '')}.png", name)
        # finish line
        star(c, M + 6, 62, 6)
        c.setFont("Bold", 9.5)
        c.drawString(M + 18, 58, "Finished? Stamp your Flower Passport on page 103!" if not easy else "All done? Give yourself a star!")
        footer(c, page)
        c.showPage()
    c.save()
    print(level, "illustrations found:", found, "/ 30 ->", out)


build("easy")
build("challenge")
