"""Etsy listing images (2000x2000 PNG) for Flowers Coloring Book Vol. 1 – Edition 2.0.
Usage: python3 build_listing_images.py <out_dir>"""
import os, sys
import pymupdf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

T = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(T)
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SZ = 2000
BG = (255, 246, 233)
INK = (40, 40, 40)
ACC = (226, 74, 92)      # coral
GRN = (60, 150, 90)
GREY = (110, 110, 110)


def font(name, size):
    return ImageFont.truetype(os.path.join(T, "fonts", name), size)


FT = lambda s: font("Fredoka-SemiBold.ttf", s)
FB = lambda s: font("Nunito-Bold.ttf", s)
FK = lambda s: font("Nunito-Black.ttf", s)
FR = lambda s: font("Nunito-Regular.ttf", s)

FLOW = os.path.join(L, "Flower-Pages-p5-34-EN.pdf")
ACT = os.path.join(L, "Activity-Pages-p95-107-Answer-Key-EN.pdf")
FRONT = os.path.join(L, "Front-Pages-p2-4-EN.pdf")
ORIG = os.path.join(T, "assets", "original_cover_and_back.pdf")


def page(path, idx, width):
    d = pymupdf.open(path)
    p = d[idx]
    z = width / p.rect.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def canvas_(title, sub=None):
    im = Image.new("RGB", (SZ, SZ), BG)
    d = ImageDraw.Draw(im)
    # soft corner dots
    for (x, y, r, c) in [(120, 1880, 70, (255, 214, 220)), (1880, 140, 90, (214, 240, 222)), (1900, 1850, 50, (255, 236, 179))]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    d.text((SZ / 2, 120), title, font=FT(108), fill=INK, anchor="mm")
    if sub:
        d.text((SZ / 2, 225), sub, font=FB(54), fill=ACC, anchor="mm")
    d.text((SZ / 2, SZ - 60), "Little Bloom Studio  •  Instant PDF download", font=FB(38), fill=GREY, anchor="mm")
    return im, d


def paste_card(im, card, xy, angle=0, shadow=True, border=0):
    if border:
        b = Image.new("RGB", (card.width + 2 * border, card.height + 2 * border), (255, 255, 255))
        b.paste(card, (border, border))
        card = b
    card = card.convert("RGBA")
    if angle:
        card = card.rotate(angle, expand=True, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
        alpha = card.split()[3].point(lambda a: 70 if a else 0)
        sh.putalpha(alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(18))
        im.paste(sh, (xy[0] + 18, xy[1] + 22), sh)
    im.paste(card, xy, card)
    return card.size


def pill(d, cx, cy, text, fill=ACC, fg=(255, 255, 255), size=46):
    f = FK(size)
    w = d.textlength(text, font=f) + 70
    h = size + 40
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h / 2, fill=fill)
    d.text((cx, cy), text, font=f, fill=fg, anchor="mm")


def save(im, name):
    im.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


# 01 Cover (uses ../cover.png when present)
im, d = canvas_("Tropical Flower Coloring Book", "30 real flowers from Malaysia  •  Ages 3–10")
_cp = os.path.join(L, "cover.png")
if os.path.exists(_cp):
    cov = Image.open(_cp).convert("RGB")
    cov = cov.resize((1000, int(cov.height * 1000 / cov.width)), Image.LANCZOS)
else:
    cov = page(ORIG, 0, 1000)
paste_card(im, page(FLOW, 0, 620), (1180, 520), angle=-8)
paste_card(im, cov, (280, 330), angle=3)
pill(d, 1500, 1500, "Fun Facts + Activities")
pill(d, 1500, 1640, "Printable PDF", fill=GRN)
save(im, "01-cover.png")

# 02 Grid of 30 flowers
im, d = canvas_("30 Tropical Flowers to Colour", "Hibiscus, orchid, lotus, Rafflesia & more")
cols, rows = 6, 5
cw, ch = 290, 300
x0, y0 = (SZ - cols * cw) / 2, 300
names = ["Hibiscus", "Jasmine", "Orchid", "Rose", "Sunflower", "Bougainvillea", "Frangipani", "Water Lily",
         "Queen of the Night", "Champaca", "Ylang-Ylang", "Spanish Cherry", "Torch Ginger", "Butterfly Pea",
         "Lavender", "Chrysanthemum", "Tulip", "Daffodil", "Lily", "Daisy", "Moss Rose", "Ten O'Clock",
         "Golden Trumpet", "Canna Lily", "Coleus", "Ixora", "Crown of Thorns", "Rafflesia", "Sacred Lotus", "Periwinkle"]
for k in range(30):
    r, c = divmod(k, cols)
    x, y = int(x0 + c * cw), int(y0 + r * ch)
    d.rounded_rectangle((x + 8, y + 8, x + cw - 8, y + ch - 8), radius=24, fill=(255, 255, 255), outline=(230, 220, 205), width=3)
    f = os.path.join(T, "crops", f"f{k + 1:02d}.png")
    if os.path.exists(f) and (k + 1) not in (28, 30):
        a = Image.open(f).convert("RGB")
        a.thumbnail((cw - 60, ch - 90))
        im.paste(a, (int(x + (cw - a.width) / 2), int(y + 22 + (ch - 90 - a.height) / 2)))
    else:
        cx_, cy_ = x + cw / 2, y + ch / 2 - 30
        d.ellipse((cx_ - 70, cy_ - 70, cx_ + 70, cy_ + 70), outline=(215, 205, 190), width=6)
        d.text((cx_, cy_), "new art", font=FB(30), fill=(190, 180, 165), anchor="mm")
    d.text((x + cw / 2, y + ch - 40), names[k], font=FB(30), fill=INK, anchor="mm")
save(im, "02-30-flowers.png")

# 03 Page close-up with callouts
im, d = canvas_("Every Page Teaches Something New", None)
pw = 1060
pg = page(FLOW, 0, pw)
px, py = 470, 250
paste_card(im, pg, (px, py))
s = pw / 595
calls = [((330, 66), "Malay & scientific name", 380),
         ((100, 842 - 203), "“Did You Know?” fun fact", 900),
         ((450, 842 - 182), "Real-colour palette + example", 1180),
         ((200, 842 - 72), "Trace-the-name handwriting", 1600)]
for (ptx, pty), label, ly in calls:
    tx, ty = px + ptx * s, py + pty * s
    d.line((440, ly, tx, ty), fill=ACC, width=8)
    d.ellipse((tx - 16, ty - 16, tx + 16, ty + 16), fill=ACC)
    f = FB(40)
    ws = label.split()
    l1, l2 = label, ""
    if d.textlength(label, font=f) > 380:
        mid = len(ws) // 2
        l1, l2 = " ".join(ws[:mid]), " ".join(ws[mid:])
    bh = 80 if not l2 else 140
    d.rounded_rectangle((40, ly - bh / 2, 440, ly + bh / 2), radius=28, fill=(255, 255, 255), outline=ACC, width=5)
    d.text((240, ly - (28 if l2 else 0)), l1, font=FB(40), fill=INK, anchor="mm")
    if l2:
        d.text((240, ly + 30), l2, font=FB(40), fill=INK, anchor="mm")
save(im, "03-page-features.png")

# 04 Before / after
im, d = canvas_("Colour It In!", "Line art + a colour example on every page")
la = Image.open(os.path.join(T, "crops", "f01.png")).convert("RGB")
la.thumbnail((780, 1250))
ins = os.path.join(T, "assets", "hibiscus_colour.png")
cimg = Image.open(ins).convert("RGB")
cimg = cimg.resize((int(cimg.width * 1150 / cimg.height), 1150), Image.LANCZOS)
for (img_, x, lab) in [(la, 120, "BEFORE"), (cimg, 1060, "AFTER")]:
    card = Image.new("RGB", (840, 1340), (255, 255, 255))
    card.paste(img_, ((840 - img_.width) // 2, (1340 - img_.height) // 2 + 20))
    paste_card(im, card, (x, 360))
    pill(d, x + 420, 1760, lab, fill=GRN if lab == "AFTER" else INK, size=50)
d.polygon([(940, 990), (1020, 990), (1020, 950), (1090, 1030), (1020, 1110), (1020, 1070), (940, 1070)], fill=ACC)
save(im, "04-before-after.png")

# 05 Activities collage
im, d = canvas_("Puzzles & Games Included", "Word searches • Crossword • Matching • Parts of a flower")
for idx, (x, y, a) in zip([1, 3, 4, 0], [(110, 330, 6), (1010, 320, -5), (160, 1060, -4), (1000, 1050, 5)]):
    paste_card(im, page(ACT, idx, 760), (x, y), angle=a)
save(im, "05-activities.png")

# 06 Passport + certificate
im, d = canvas_("Collect Stamps, Earn a Certificate!", "Flower Passport + Flower Expert Certificate")
paste_card(im, page(ACT, 8, 900), (110, 330), angle=-4)
paste_card(im, page(ACT, 10, 1050), (850, 900), angle=4)
save(im, "06-passport-certificate.png")

# 07 Bookmarks + postcards
im, d = canvas_("Bonus: Bookmarks & Postcards", "Colour, cut out, keep or send to someone special")
paste_card(im, page(ACT, 11, 880), (130, 330), angle=-3)
paste_card(im, page(ACT, 12, 880), (1000, 380), angle=3)
save(im, "07-bookmarks-postcards.png")

# 08 Flower Hunt Mission
im, d = canvas_("Go on a Real Flower Hunt!", "Find flowers in your park, garden or flower shop")
paste_card(im, page(ACT, 9, 1050), (190, 300), angle=-3)
pill(d, 1600, 900, "Outdoor fun", fill=GRN)
pill(d, 1600, 1040, "Screen-free")
pill(d, 1600, 1180, "Safety tips", fill=INK)
save(im, "08-flower-hunt.png")

# 09 What's inside
im, d = canvas_("What's Inside", "50 printable pages")
items = ["30 flower colouring pages", "A fun fact on every page", "Real-colour palettes + examples",
         "Trace-the-name handwriting", "2 word searches + crossword", "Matching games & drawing pages",
         "Flower Passport + Hunt Mission", "Flower Expert Certificate", "4 bookmarks + 2 postcards", "Answer key for grown-ups"]
d.rounded_rectangle((180, 310, 1820, 1860), radius=60, fill=(255, 255, 255), outline=(230, 220, 205), width=4)
for i, t in enumerate(items):
    y = 400 + i * 142
    d.ellipse((260, y - 38, 336, y + 38), fill=GRN)
    d.line((278, y, 294, y + 18), fill=(255, 255, 255), width=10)
    d.line((292, y + 18, 320, y - 16), fill=(255, 255, 255), width=10)
    d.text((380, y), t, font=FB(62), fill=INK, anchor="lm")
save(im, "09-whats-inside.png")

# 10 Printing info
im, d = canvas_("Easy to Print at Home", "Instant download • No shipping")
info = [("A4 & US Letter", "Prints on both paper sizes"), ("Ink-friendly", "Pure white backgrounds"),
        ("Print unlimited", "One for every sibling"), ("Personal use", "Classroom licence available")]
for i, (a, b) in enumerate(info):
    r, c = divmod(i, 2)
    x, y = 170 + c * 860, 360 + r * 760
    d.rounded_rectangle((x, y, x + 800, y + 680), radius=60, fill=(255, 255, 255), outline=(230, 220, 205), width=4)
    d.ellipse((x + 300, y + 80, x + 500, y + 280), fill=[ACC, GRN, (240, 180, 40), INK][i])
    d.text((x + 400, y + 180), str(i + 1), font=FT(110), fill=(255, 255, 255), anchor="mm")
    d.text((x + 400, y + 400), a, font=FT(78), fill=INK, anchor="mm")
    d.text((x + 400, y + 500), b, font=FB(50), fill=GREY, anchor="mm")
save(im, "10-printing-info.png")
