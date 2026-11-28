"""Little Bloom Studio – Flowers Coloring Book Vol. 1, Edition 2.0
English activity pages (95-107) + answer key (108). A4."""
import math, random, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import ImageReader

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
F = f"{S}/fonts"
pdfmetrics.registerFont(TTFont("Title", f"{F}/Fredoka-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Body", f"{F}/Nunito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Bold", f"{F}/Nunito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Black", f"{F}/Nunito-Black.ttf"))

W, H = A4
M = 40
GREY = HexColor("#666666")
LIGHT = HexColor("#BBBBBB")
HL = HexColor("#FFE08A")


def img(n):
    return f"{S}/crops/f{n:02d}.png"


def draw_img(c, path, x, y, w, h):
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    c.drawImage(ir, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")
    return x + (w - dw) / 2, y + (h - dh) / 2, dw, dh


def wrap(text, font, size, width):
    out, line = [], ""
    for wd in text.split():
        t = (line + " " + wd).strip()
        if pdfmetrics.stringWidth(t, font, size) > width and line:
            out.append(line)
            line = wd
        else:
            line = t
    out.append(line)
    return out


# ---------------------------------------------------------------- doodles
def doodle_flower(c, x, y, r=9, petals=5):
    c.saveState()
    c.setLineWidth(1.3)
    c.setFillColor(white)
    for k in range(petals):
        a = 2 * math.pi * k / petals + math.pi / 2
        c.circle(x + r * math.cos(a), y + r * math.sin(a), r * 0.62, stroke=1, fill=1)
    c.circle(x, y, r * 0.5, stroke=1, fill=1)
    c.restoreState()


def star(c, x, y, r, fill=0, lw=1.3):
    c.saveState()
    c.setLineWidth(lw)
    c.setLineJoin(1)
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        (p.moveTo if k == 0 else p.lineTo)(x + rr * math.cos(a), y + rr * math.sin(a))
    p.close()
    c.drawPath(p, stroke=1, fill=fill)
    c.restoreState()


def bee(c, x, y, s=1.0):
    """Bibi the Bee – outline only so kids can colour her too."""
    c.saveState()
    c.setLineWidth(1.5)
    c.setFillColor(white)
    # wings
    c.ellipse(x - 14 * s, y + 6 * s, x + 4 * s, y + 30 * s, stroke=1, fill=1)
    c.ellipse(x - 2 * s, y + 4 * s, x + 18 * s, y + 26 * s, stroke=1, fill=1)
    # stinger
    p = c.beginPath()
    p.moveTo(x + 24 * s, y + 3 * s); p.lineTo(x + 33 * s, y); p.lineTo(x + 24 * s, y - 3 * s)
    c.drawPath(p, stroke=1, fill=1)
    # body
    c.ellipse(x - 22 * s, y - 14 * s, x + 26 * s, y + 14 * s, stroke=1, fill=1)
    c.saveState()
    p = c.beginPath()
    p.ellipse(x - 22 * s, y - 14 * s, 48 * s, 28 * s)
    c.clipPath(p, stroke=0)
    c.setFillColor(black)
    for sx in (-2, 10):
        c.rect(x + sx * s, y - 15 * s, 6 * s, 30 * s, stroke=0, fill=1)
    c.restoreState()
    # head
    c.setFillColor(white)
    c.circle(x - 26 * s, y + 2 * s, 12 * s, stroke=1, fill=1)
    c.setFillColor(black)
    c.circle(x - 30 * s, y + 5 * s, 1.8 * s, stroke=0, fill=1)
    c.circle(x - 23 * s, y + 5 * s, 1.8 * s, stroke=0, fill=1)
    c.arc(x - 32 * s, y - 6 * s, x - 21 * s, y + 3 * s, 200, 140)
    # antennae
    c.line(x - 30 * s, y + 13 * s, x - 35 * s, y + 24 * s)
    c.line(x - 22 * s, y + 13 * s, x - 18 * s, y + 24 * s)
    c.circle(x - 35 * s, y + 25 * s, 2.2 * s, stroke=0, fill=1)
    c.circle(x - 18 * s, y + 25 * s, 2.2 * s, stroke=0, fill=1)
    c.restoreState()


def bee_tip(c, x, y, text, width=200, s=0.8):
    """Bee at (x,y) with a speech bubble to its right."""
    bee(c, x, y, s)
    lines = wrap(text, "Bold", 9.5, width - 20)
    bh = 14 + 12 * len(lines)
    bx, by = x + 40 * s, y - bh / 2 + 6
    c.saveState()
    c.setLineWidth(1.3)
    c.setFillColor(white)
    c.roundRect(bx, by, width, bh, 9, stroke=1, fill=1)
    p = c.beginPath()
    p.moveTo(bx + 1, by + bh / 2 + 5); p.lineTo(bx - 9, by + bh / 2 - 2); p.lineTo(bx + 1, by + bh / 2 - 5)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(white)
    c.setStrokeColor(white)
    c.rect(bx - 0.5, by + bh / 2 - 4.3, 2.2, 8.6, stroke=0, fill=1)
    c.setFillColor(black)
    c.setFont("Bold", 9.5)
    for i, ln in enumerate(lines):
        c.drawString(bx + 10, by + bh - 15 - 12 * i, ln)
    c.restoreState()


def header(c, title, sub, ins, ins2=None):
    c.setFillColor(black)
    c.setFont("Title", 34)
    c.drawCentredString(W / 2, H - 70, title)
    tw = pdfmetrics.stringWidth(title, "Title", 34)
    doodle_flower(c, W / 2 - tw / 2 - 26, H - 60, 8)
    doodle_flower(c, W / 2 + tw / 2 + 26, H - 60, 8)
    c.setFont("Bold", 15)
    c.setFillColor(GREY)
    c.drawCentredString(W / 2, H - 92, sub)
    c.setFillColor(black)
    c.setFont("Bold", 11.5)
    c.drawCentredString(W / 2, H - 118, ins)
    if ins2:
        c.setFont("Body", 10.5)
        c.setFillColor(GREY)
        c.drawCentredString(W / 2, H - 132, ins2)
        c.setFillColor(black)


def footer(c, page):
    c.setFont("Body", 9)
    c.setFillColor(GREY)
    c.drawCentredString(W / 2, 38, "Little Bloom Studio  •  Flowers Coloring Book Vol. 1  •  Edition 2.0")
    c.setFillColor(black)
    c.setFont("Bold", 11)
    c.drawCentredString(W / 2, 20, str(page))


# ---------------------------------------------------------------- word search
def make_wordsearch(words, n, dirs, seed):
    rnd = random.Random(seed)
    all_dirs = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
    for _ in range(3000):
        g = [[None] * n for _ in range(n)]
        place, ok = {}, True
        for w in sorted(words, key=len, reverse=True):
            opts = []
            for dx, dy in dirs:
                for r in range(n):
                    for col in range(n):
                        er, ec = r + dy * (len(w) - 1), col + dx * (len(w) - 1)
                        if not (0 <= er < n and 0 <= ec < n):
                            continue
                        good, ov = True, 0
                        for i, ch in enumerate(w):
                            cell = g[r + dy * i][col + dx * i]
                            if cell is not None and cell != ch:
                                good = False
                                break
                            ov += cell == ch
                        if good:
                            opts.append((ov, rnd.random(), r, col, dx, dy))
            if not opts:
                ok = False
                break
            opts.sort(reverse=True)
            _, _, r, col, dx, dy = rnd.choice(opts[: max(1, len(opts) // 6)])
            for i, ch in enumerate(w):
                g[r + dy * i][col + dx * i] = ch
            place[w] = (r, col, dx, dy)
        if not ok:
            continue
        for r in range(n):
            for col in range(n):
                if g[r][col] is None:
                    g[r][col] = rnd.choice("ABCDEFGHIKLMNOPRSTUVWY")

        def count(w):
            k = 0
            for dx, dy in all_dirs:
                for r in range(n):
                    for col in range(n):
                        if all(0 <= r + dy * i < n and 0 <= col + dx * i < n and g[r + dy * i][col + dx * i] == ch
                               for i, ch in enumerate(w)):
                            k += 1
            return k

        if all(count(w) == 1 for w in words):
            return g, place
    raise RuntimeError("wordsearch failed")


def draw_grid_ws(c, g, x0, ytop, cell, fs, place=None):
    n = len(g)
    if place:
        for w, (r, col, dx, dy) in place.items():
            L = len(w) - 1
            c.saveState()
            c.setLineCap(1)
            c.setLineWidth(cell * 0.78)
            c.setStrokeColor(HL)
            c.line(x0 + (col + .5) * cell, ytop - (r + .5) * cell,
                   x0 + (col + dx * L + .5) * cell, ytop - (r + dy * L + .5) * cell)
            c.restoreState()
    c.setLineWidth(1.6)
    c.roundRect(x0 - 4, ytop - n * cell - 4, n * cell + 8, n * cell + 8, 10)
    c.setLineWidth(0.5)
    c.setStrokeColor(LIGHT)
    for i in range(1, n):
        c.line(x0 + i * cell, ytop, x0 + i * cell, ytop - n * cell)
        c.line(x0, ytop - i * cell, x0 + n * cell, ytop - i * cell)
    c.setStrokeColor(black)
    c.setFont("Bold", fs)
    for r in range(n):
        for col in range(n):
            c.drawCentredString(x0 + (col + .5) * cell, ytop - (r + .5) * cell - fs * .36, g[r][col])


def wordlist(c, words, y, cols=3):
    colw = (W - 2 * M) / cols
    rows = (len(words) + cols - 1) // cols
    for i, word in enumerate(words):
        col, row = divmod(i, rows)
        x = M + 30 + col * colw
        yy = y - row * 26
        c.setLineWidth(1.2)
        c.rect(x, yy - 3, 12, 12)
        c.setFont("Bold", 12.5)
        c.drawString(x + 20, yy, word)


WS1 = ["BEE", "BUTTERFLY", "PETAL", "STEM", "LEAF", "ROOT", "SEED", "POLLEN", "NECTAR", "SUNSHINE", "RAIN", "BLOOM"]
WS2 = ["HIBISCUS", "JASMINE", "ORCHID", "ROSE", "SUNFLOWER", "LOTUS", "LILY", "DAISY", "TULIP", "LAVENDER", "IXORA", "RAFFLESIA"]
g1, p1 = make_wordsearch(WS1, 12, [(1, 0), (0, 1)], 3)
g2, p2 = make_wordsearch(WS2, 12, [(1, 0), (0, 1), (1, 1)], 11)

# ---------------------------------------------------------------- crossword
CW = [
    ("RAFFLESIA", "The biggest single flower in the world – almost 1 metre wide!", 32),
    ("SUNFLOWER", "Its big head is made of hundreds of tiny flowers. Its seeds are a yummy snack.", 9),
    ("HIBISCUS", "The national flower of Malaysia. It has 5 petals.", 5),
    ("JASMINE", "A sweet-smelling white flower used to make a famous tea.", 6),
    ("ORCHID", "Vanilla flavour comes from the fruit of this flower!", 7),
    ("LOTUS", "Its leaves are waterproof – water drops roll right off!", 33),
    ("DAFFODIL", "The national flower of Wales. Never eat it – it is poisonous!", 22),
    ("TULIP", "This flower is famous in the Netherlands.", 21),
    ("DAISY", "Its name comes from “day's eye” – it opens in the day.", 24),
    ("LILY", "A flower with 6 petals. Keep its pollen away from cats!", 23),
]


def make_crossword(entries, seeds=5000):
    best = None
    words = [e[0] for e in entries]
    for seed in range(seeds):
        rnd = random.Random(seed)
        order = words[:]
        rnd.shuffle(order)
        order.sort(key=lambda w: -len(w) + rnd.random() * 3)
        grid, placed = {}, {}

        def can(w, r, col, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            if (r - dr, col - dc) in grid or (r + dr * len(w), col + dc * len(w)) in grid:
                return -1
            inter = 0
            for i, ch in enumerate(w):
                rr, cc = r + dr * i, col + dc * i
                if (rr, cc) in grid:
                    if grid[(rr, cc)] != ch:
                        return -1
                    inter += 1
                else:
                    for sr, sc in ((dc, dr), (-dc, -dr)):
                        if (rr + sr, cc + sc) in grid:
                            return -1
            return inter

        def put(w, r, col, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            for i, ch in enumerate(w):
                grid[(r + dr * i, col + dc * i)] = ch
            placed[w] = (r, col, d)

        put(order[0], 0, 0, "A")
        for w in order[1:]:
            cands = []
            for (gr, gc), gch in list(grid.items()):
                for i, ch in enumerate(w):
                    if ch != gch:
                        continue
                    for d in "AD":
                        r, col = (gr, gc - i) if d == "A" else (gr - i, gc)
                        k = can(w, r, col, d)
                        if k > 0:
                            cands.append((k, rnd.random(), r, col, d))
            if cands:
                cands.sort(reverse=True)
                _, _, r, col, d = cands[0] if rnd.random() < .5 else rnd.choice(cands)
                put(w, r, col, d)
        rs = [k[0] for k in grid]
        cs = [k[1] for k in grid]
        hgt, wid = max(rs) - min(rs) + 1, max(cs) - min(cs) + 1
        if wid > 15 or hgt > 13:
            continue
        score = (len(placed), -max(hgt, wid * 0.9))
        if best is None or score > best[0]:
            best = (score, dict(grid), dict(placed), min(rs), min(cs), hgt, wid)
    _, grid, placed, r0, c0, hgt, wid = best
    grid = {(r - r0, cc - c0): ch for (r, cc), ch in grid.items()}
    placed = {w: (r - r0, cc - c0, d) for w, (r, cc, d) in placed.items()}
    starts = sorted({(r, cc) for (r, cc, d) in placed.values()})
    num = {pos: i + 1 for i, pos in enumerate(starts)}
    return grid, placed, num, hgt, wid


cwg, cwp, cwn, cwh, cww = make_crossword(CW)


def draw_crossword(c, x0, ytop, cell, fill=False, numfont=7.5):
    c.setLineWidth(1.3)
    for (r, cc), ch in cwg.items():
        x, y = x0 + cc * cell, ytop - (r + 1) * cell
        c.setFillColor(white)
        c.rect(x, y, cell, cell, fill=1, stroke=1)
        c.setFillColor(black)
        if (r, cc) in cwn:
            c.setFont("Bold", numfont)
            c.drawString(x + 1.8, y + cell - numfont - 0.3, str(cwn[(r, cc)]))
        if fill:
            c.setFont("Bold", cell * .5)
            c.drawCentredString(x + cell * .56, y + cell * .22, ch)


# ---------------------------------------------------------------- book list (Edition 2.0 order)
FLOWERS = ["Hibiscus", "Jasmine", "Orchid", "Rose", "Sunflower", "Bougainvillea", "Frangipani", "Water Lily",
           "Queen of the Night", "Champaca", "Ylang-Ylang", "Spanish Cherry", "Torch Ginger", "Butterfly Pea",
           "Lavender", "Chrysanthemum", "Tulip", "Daffodil", "Lily", "Daisy", "Moss Rose", "Ten O'Clock Flower",
           "Golden Trumpet", "Canna Lily", "Coleus", "Ixora", "Crown of Thorns", "Rafflesia", "Sacred Lotus",
           "Periwinkle"]

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Flowers Coloring Book Vol. 1 – Activity Pages")
c.setAuthor("Little Bloom Studio")

# ===== 95 Parts of a flower
header(c, "Petal Detective", "Parts of a Flower",
       "Can you name every part of this hibiscus? Write the words in the boxes.",
       "Use the Word Box at the bottom to help you.")
bx, by, bw, bh = draw_img(c, img(1), 170, 215, 255, 395)
pts = {"PETAL": (0.10, 0.30), "STAMEN": (0.80, 0.08), "LEAF VEIN": (0.20, 0.71), "STEM": (0.30, 0.86), "LEAF": (0.62, 0.79)}
boxes = {"PETAL": (M, 470), "STAMEN": (W - M - 130, 560), "LEAF VEIN": (M, 330), "STEM": (M, 235), "LEAF": (W - M - 130, 300)}
ANS95 = {}
for i, (k, (fx, fy)) in enumerate(pts.items()):
    px, py = bx + fx * bw, by + bh - fy * bh
    x, y = boxes[k]
    c.setLineWidth(1.4)
    c.roundRect(x, y, 130, 34, 8)
    c.setFont("Bold", 10)
    c.drawString(x + 6, y + 22, f"{i + 1}.")
    ex = x + 130 if x < W / 2 else x
    c.setDash(3, 2)
    c.line(ex, y + 17, px, py)
    c.setDash()
    c.circle(px, py, 3.2, fill=1)
    ANS95[i + 1] = k
bee_tip(c, W / 2 - 120, 655, "The stamen holds the pollen that bees like me carry from flower to flower!", 230, 0.75)
c.setLineWidth(1.5)
c.roundRect(M, 128, W - 2 * M, 62, 12)
c.setFont("Title", 13)
c.drawString(M + 14, 170, "Word Box")
x = M + 14
for wd in ["PETAL", "STAMEN", "STEM", "LEAF", "LEAF VEIN"]:
    c.setFont("Bold", 13)
    c.drawString(x, 145, wd)
    x += pdfmetrics.stringWidth(wd, "Bold", 13) + 38
star(c, M + 8, 98, 8)
c.setFont("Bold", 11.5)
c.drawString(M + 22, 94, "Bonus question: How many petals does a hibiscus have?  ______")
c.setFont("Body", 9.5)
c.setFillColor(GREY)
c.drawString(M + 22, 80, "Hint: read the “Did You Know?” fact on page 5.")
c.setFillColor(black)
footer(c, 95)
c.showPage()

# ===== 96 Garden word search (easy)
header(c, "Garden Word Search", "Level: Easy",
       "Find 12 garden words hidden in the grid.",
       "Words go across (left to right) and down (top to bottom).")
cell = 34
x0 = (W - 12 * cell) / 2
draw_grid_ws(c, g1, x0, H - 160, cell, 17)
wordlist(c, WS1, H - 160 - 12 * cell - 36)
bee_tip(c, M + 60, 112, "Bzzz! I found BEE already... just kidding, your turn!", 190, 0.7)
footer(c, 96)
c.showPage()

# ===== 97 Flower word search (challenge)
header(c, "Flower Word Search", "Level: Challenge",
       "Find 12 flower names from this book.",
       "Words go across, down and diagonally.")
draw_grid_ws(c, g2, x0, H - 160, cell, 17)
wordlist(c, WS2, H - 160 - 12 * cell - 36)
footer(c, 97)
c.showPage()

# ===== 98 Crossword
header(c, "Flower Crossword", "Read the clues and fill in the flower names.",
       "Stuck? Check the “Did You Know?” fact on the page shown in each clue.")
cell = min((W - 2 * M) / cww, 290 / cwh, 28)
gx = (W - cww * cell) / 2
gtop = H - 140
draw_crossword(c, gx, gtop, cell)
clue = {e[0]: (e[1], e[2]) for e in CW}
across = sorted([(cwn[(r, cc)], w) for w, (r, cc, d) in cwp.items() if d == "A"])
down = sorted([(cwn[(r, cc)], w) for w, (r, cc, d) in cwp.items() if d == "D"])
y = gtop - cwh * cell - 28
colw = (W - 2 * M) / 2
for ci, (ttl, lst) in enumerate([("ACROSS", across), ("DOWN", down)]):
    xx, yy = M + ci * colw, y
    c.setFont("Title", 15)
    c.drawString(xx, yy, ttl)
    yy -= 19
    for n_, w in lst:
        t, pg = clue[w]
        c.setFont("Bold", 10.5)
        c.drawString(xx, yy, f"{n_}.")
        for ln in wrap(t, "Body", 10.5, colw - 34):
            c.setFont("Body", 10.5)
            c.drawString(xx + 18, yy, ln)
            yy -= 13
        c.setFont("Body", 9)
        c.setFillColor(GREY)
        c.drawString(xx + 18, yy, f"({len(w)} letters  •  page {pg})")
        c.setFillColor(black)
        yy -= 18
missing = [e[0] for e in CW if e[0] not in cwp]
footer(c, 98)
c.showPage()

# ===== 99 Match picture to name
header(c, "Who's Who in the Garden?", "Match the Flower to Its Name",
       "Draw a line from each flower to its name.")
PAIRS = [(2, "JASMINE"), (7, "FRANGIPANI"), (13, "TORCH GINGER"), (14, "BUTTERFLY PEA"),
         (16, "CHRYSANTHEMUM"), (29, "SACRED LOTUS"), (3, "ORCHID"), (5, "SUNFLOWER")]
right = [p[1] for p in PAIRS]
rnd = random.Random(5)
while True:
    rnd.shuffle(right)
    if all(right[i] != PAIRS[i][1] for i in range(len(PAIRS))):
        break
top, rowh = H - 150, 70
for i, (n_, nm) in enumerate(PAIRS):
    yc = top - i * rowh - rowh / 2
    draw_img(c, img(n_), M + 30, yc - 31, 90, 62)
    c.setFont("Bold", 11)
    c.drawString(M + 5, yc - 4, chr(65 + i))
    c.circle(200, yc, 5.5, fill=1)
    c.circle(330, yc, 5.5, fill=1)
    c.setFont("Bold", 14)
    c.drawString(347, yc - 5, right[i])
ANS99 = [(chr(65 + i), nm) for i, (_, nm) in enumerate(PAIRS)]
bee_tip(c, M + 60, 95, "Tip: count the petals and look at the leaves to find the right match!", 220, 0.7)
footer(c, 99)
c.showPage()

# ===== 100 Match to colour
header(c, "Rainbow Garden", "Match the Flower to Its Real Colour",
       "Draw a line from each flower to its colour. Then colour the flower in!")
CF = [(1, "HIBISCUS", "RED", "#E53935"), (14, "BUTTERFLY PEA", "BLUE", "#1E5BD8"),
      (5, "SUNFLOWER", "YELLOW", "#FFD21F"), (2, "JASMINE", "WHITE", "#FFFFFF"),
      (15, "LAVENDER", "PURPLE", "#8E44C9"), (6, "BOUGAINVILLEA", "PINK", "#EC4FA4")]
order = [3, 0, 4, 1, 5, 2]
top, rowh = H - 145, 100
for i, (n_, nm, *_r) in enumerate(CF):
    yc = top - i * rowh - rowh / 2
    draw_img(c, img(n_), M, yc - 44, 100, 88)
    c.setFont("Bold", 11.5)
    c.drawString(M + 110, yc - 4, nm)
    c.circle(290, yc, 5.5, fill=1)
    _, _, cn, hexc = CF[order[i]]
    c.circle(365, yc, 5.5, fill=1)
    c.setFillColor(HexColor(hexc))
    c.setLineWidth(1.5)
    c.circle(410, yc, 24, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Bold", 13)
    c.drawString(444, yc - 4, cn)
ANS100 = [(nm, cn) for _, nm, cn, _ in CF]
footer(c, 100)
c.showPage()

# ===== 101 Favourite flower
header(c, "My Favourite Flower", "Draw it, colour it, love it!",
       "Draw and colour your favourite flower, then answer the questions below.")
c.setLineWidth(2)
c.roundRect(M, 290, W - 2 * M, H - 150 - 290, 18)
for (sx, sy) in [(M + 22, H - 172), (W - M - 22, H - 172), (M + 22, 312), (W - M - 22, 312)]:
    star(c, sx, sy, 7)
c.setFont("Body", 10)
c.setFillColor(LIGHT)
c.drawCentredString(W / 2, 302, "Draw here")
c.setFillColor(black)
y = 250
for q in ["My flower is called:", "Its colours are:", "I like this flower because:"]:
    c.setFont("Bold", 12.5)
    c.drawString(M, y, q)
    c.setStrokeColor(LIGHT)
    c.setLineWidth(1)
    lx = M + pdfmetrics.stringWidth(q, "Bold", 12.5) + 10
    c.line(lx, y - 3, W - M, y - 3)
    if q.startswith("I like"):
        c.line(M, y - 32, W - M, y - 32)
    c.setStrokeColor(black)
    y -= 48
footer(c, 101)
c.showPage()

# ===== 102 Dream garden
header(c, "My Dream Garden", "You are the gardener!",
       "Design your very own garden using flowers from this book.")
fx, fy, fw, fh = M, 230, W - 2 * M, H - 150 - 230
c.setLineWidth(2)
c.roundRect(fx, fy, fw, fh, 18)
c.setLineWidth(1.6)
sx, sy = fx + 55, fy + fh - 55
c.circle(sx, sy, 22)
for k in range(10):
    a = k * math.pi / 5
    c.line(sx + 28 * math.cos(a), sy + 28 * math.sin(a), sx + 38 * math.cos(a), sy + 38 * math.sin(a))
cx, cy = fx + fw - 120, fy + fh - 60
CL = [(0, 0, 16), (20, 8, 20), (44, 2, 16), (60, -4, 12)]
c.setLineWidth(3.2)
for (ox, oy, r) in CL:
    c.circle(cx + ox, cy + oy, r, stroke=1, fill=0)
c.setFillColor(white)
for (ox, oy, r) in CL:
    c.circle(cx + ox, cy + oy, r, stroke=0, fill=1)
c.setFillColor(black)
c.setLineWidth(1.6)
bee(c, fx + fw - 80, fy + 150, 0.7)
p = c.beginPath()
p.moveTo(fx, fy + 70)
for k in range(12):
    x1, x2 = fx + fw * (k + .5) / 12, fx + fw * (k + 1) / 12
    p.curveTo(x1 - 10, fy + 82, x1 + 10, fy + 82, x2, fy + 70)
c.drawPath(p, stroke=1, fill=0)
y = 195
for q in ["Draw at least 5 flowers from this book", "Add butterflies, bees or birds",
          "Give your garden a name:  ______________________________"]:
    c.setLineWidth(1.2)
    c.rect(M, y - 2, 12, 12)
    c.setFont("Bold", 12.5)
    c.drawString(M + 22, y, q)
    y -= 30
footer(c, 102)
c.showPage()

# ===== 103 Flower Passport
c.setFont("Title", 34)
c.drawCentredString(W / 2, H - 70, "My Flower Passport")
tw = pdfmetrics.stringWidth("My Flower Passport", "Title", 34)
doodle_flower(c, W / 2 - tw / 2 - 26, H - 60, 8)
doodle_flower(c, W / 2 + tw / 2 + 26, H - 60, 8)
c.setFont("Bold", 11.5)
c.drawCentredString(W / 2, H - 94, "Every time you finish colouring a flower, give it a stamp: draw a star or add a sticker!")
# ID card
idx, idy, idw, idh = M, H - 215, W - 2 * M, 105
c.setLineWidth(1.8)
c.roundRect(idx, idy, idw, idh, 12)
c.setDash(4, 3)
c.setLineWidth(1)
c.roundRect(idx + 6, idy + 6, idw - 12, idh - 12, 9)
c.setDash()
c.setLineWidth(1.4)
c.roundRect(idx + 18, idy + 16, 70, 74, 6)
c.setFont("Body", 7.5)
c.setFillColor(GREY)
c.drawCentredString(idx + 53, idy + 50, "Draw")
c.drawCentredString(idx + 53, idy + 41, "yourself")
c.setFillColor(black)
c.setFont("Title", 11)
c.drawString(idx + 104, idy + 78, "FLOWER EXPLORER ID")
fields = [("Name:", idy + 56), ("Age:", idy + 34), ("Explorer since:", idy + 12 + 2)]
for lab, yy in fields:
    c.setFont("Bold", 10.5)
    c.drawString(idx + 104, yy, lab)
    c.setStrokeColor(LIGHT)
    lx = idx + 106 + pdfmetrics.stringWidth(lab, "Bold", 10.5)
    c.line(lx, yy - 2, idx + 360, yy - 2)
    c.setStrokeColor(black)
# official-looking round stamp
sx, sy = idx + idw - 70, idy + idh / 2
c.setLineWidth(1.5)
c.circle(sx, sy, 38)
c.circle(sx, sy, 31)
doodle_flower(c, sx, sy + 6, 7)
c.setFont("Black", 6.5)
c.drawCentredString(sx, sy - 13, "LITTLE BLOOM")
c.drawCentredString(sx, sy - 20, "STUDIO")
# stamp grid 6 x 5
cols, rows = 5, 6
gx0, gy_top = M, idy - 18
cw_ = (W - 2 * M) / cols
rh = 74
for k, nm in enumerate(FLOWERS):
    r, col = divmod(k, cols)
    cx_ = gx0 + col * cw_ + cw_ / 2
    cy_ = gy_top - r * rh - 30
    c.setLineWidth(1.3)
    c.setDash(3, 2.5)
    c.circle(cx_, cy_, 23)
    c.setDash()
    c.setFont("Bold", 9)
    c.setFillColor(LIGHT)
    c.drawCentredString(cx_, cy_ - 3, str(k + 1))
    c.setFillColor(black)
    fs = 8.5 if pdfmetrics.stringWidth(nm, "Bold", 8.5) < cw_ - 6 else 7.5
    c.setFont("Bold", fs)
    c.drawCentredString(cx_, cy_ - 36, nm)
# levels
ly = gy_top - rows * rh - 8
c.setLineWidth(1.4)
c.roundRect(M, ly - 40, W - 2 * M, 44, 10)
c.setFont("Title", 11.5)
c.drawString(M + 12, ly - 13, "Explorer Levels:")
lv = [("10 stamps", "Seedling"), ("20 stamps", "Blossom"), ("30 stamps", "Flower Expert!")]
x = M + 112
for i, (a, b) in enumerate(lv):
    star(c, x, ly - 9, 6, fill=0)
    c.setFont("Bold", 9.5)
    c.drawString(x + 10, ly - 13, f"{a} = {b}")
    x += 118
c.setFont("Body", 9)
c.setFillColor(GREY)
c.drawString(M + 12, ly - 31, "Reach 30 stamps and you earn your Flower Expert Certificate on page 105!")
c.setFillColor(black)
footer(c, 103)
c.showPage()

# ===== 104 Flower Hunt Mission
header(c, "Flower Hunt Mission", "Become a real-life flower explorer!",
       "Look for these flowers in gardens, parks, flower shops or botanical gardens.",
       "Tick the box when you spot one and write where you found it.")
hunt = [("Rose", "gardens, parks, flower shops"), ("Sunflower", "fields & gardens in summer"),
        ("Tulip", "gardens in spring"), ("Daffodil", "parks in early spring"),
        ("Lavender", "gardens & herb pots"), ("Daisy", "lawns & meadows"),
        ("Orchid", "supermarkets & house plants"), ("Lily", "flower shops & bouquets"),
        ("Chrysanthemum", "garden centres in autumn"), ("Hibiscus", "garden centres & sunny windows"),
        ("Lotus or Water Lily", "ponds & botanical gardens"), ("Jasmine", "climbing on walls & fences")]
tx, ty = M, H - 160
colx = [M, M + 44, M + 178, M + 355]
c.setFont("Bold", 10)
for xx, t in zip(colx, ["Found", "Flower", "Where to look", "Where I found it"]):
    c.drawString(xx, ty, t)
c.setLineWidth(1.2)
c.line(M, ty - 6, W - M, ty - 6)
rowh = 27
for i, (nm, hint) in enumerate(hunt):
    yy = ty - 26 - i * rowh
    c.setLineWidth(1.2)
    c.rect(colx[0] + 6, yy - 3, 13, 13)
    c.setFont("Bold", 11.5)
    c.drawString(colx[1], yy, nm)
    c.setFont("Body", 9.5)
    c.setFillColor(GREY)
    c.drawString(colx[2], yy, hint)
    c.setFillColor(black)
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.8)
    c.line(colx[3], yy - 3, W - M, yy - 3)
    c.setStrokeColor(black)
by0 = ty - 26 - len(hunt) * rowh - 6
c.setLineWidth(1.5)
c.roundRect(M, by0 - 125, W - 2 * M, 125, 12)
c.setFont("Title", 14)
c.drawString(M + 14, by0 - 22, "Bonus Spotting Challenges")
chal = ["A flower with exactly 5 petals", "A bee or butterfly visiting a flower", "A flower taller than you",
        "A flower that smells sweet", "Three flowers of different colours", "A flower bud that hasn't opened yet"]
for i, t in enumerate(chal):
    col, row = divmod(i, 3)
    xx = M + 16 + col * ((W - 2 * M) / 2)
    yy = by0 - 48 - row * 30
    star(c, xx + 6, yy + 4, 7)
    c.setFont("Bold", 10.5)
    c.drawString(xx + 20, yy, t)
bee_tip(c, M + 55, 112, "Explorer rule: always ask a grown-up first, and take a photo instead of picking the flowers!", 300, 0.7)
footer(c, 104)
c.showPage()

# ===== 105 Certificate (landscape)
LW, LH = H, W
c.setPageSize((LW, LH))
c.setLineWidth(3)
c.roundRect(24, 24, LW - 48, LH - 48, 18)
c.setLineWidth(1)
c.setDash(4, 3)
c.roundRect(34, 34, LW - 68, LH - 68, 14)
c.setDash()
for (x, y) in [(52, 52), (LW - 52, 52), (52, LH - 52), (LW - 52, LH - 52)]:
    doodle_flower(c, x, y, 10)
# corner flowers to colour
draw_img(c, img(1), 48, 66, 120, 170)
draw_img(c, img(3), LW - 168, 66, 120, 170)
c.setFont("Title", 20)
c.setFillColor(GREY)
c.drawCentredString(LW / 2, LH - 88, "CERTIFICATE OF ACHIEVEMENT")
c.setFillColor(black)
c.setFont("Title", 52)
c.drawCentredString(LW / 2, LH - 145, "Flower Expert")
tw = pdfmetrics.stringWidth("Flower Expert", "Title", 52) / 2
for k, dx in enumerate((-tw - 34, -tw - 16, tw + 16, tw + 34)):
    star(c, LW / 2 + dx, LH - 128 + (8 if k in (0, 3) else -6), 7 if k in (0, 3) else 5)
c.setFont("Bold", 14)
c.drawCentredString(LW / 2, LH - 185, "This certificate is proudly presented to")
c.setLineWidth(1.2)
c.line(LW / 2 - 190, LH - 235, LW / 2 + 190, LH - 235)
c.setFont("Body", 12.5)
for i, ln in enumerate(["for colouring all 30 flowers, completing the Flower Passport",
                        "and exploring the wonderful world of flowers!"]):
    c.drawCentredString(LW / 2, LH - 262 - i * 17, ln)
# seal
sx, sy = LW / 2, 140
c.setLineWidth(1.8)
c.circle(sx, sy, 46)
c.setDash(2, 2)
c.setLineWidth(1)
c.circle(sx, sy, 39)
c.setDash()
star(c, sx, sy + 6, 20, lw=1.6)
c.setFont("Black", 7)
c.drawCentredString(sx, sy - 24, "OFFICIAL")
c.drawCentredString(sx, sy - 32, "FLOWER EXPERT")
# signature lines
for (x0, lab) in [(LW / 2 - 232, "Date"), (LW / 2 + 72, "Signed by (grown-up)")]:
    c.setLineWidth(1)
    c.line(x0, 130, x0 + 160, 130)
    c.setFont("Bold", 10.5)
    c.drawCentredString(x0 + 80, 116, lab)
bee(c, LW / 2 + 250, LH - 300, 0.65)
c.setFont("Body", 8.5)
c.setFillColor(GREY)
c.drawCentredString(LW / 2, 44, "Little Bloom Studio  •  Flowers Coloring Book Vol. 1  •  105")
c.setFillColor(black)
c.showPage()
c.setPageSize(A4)

# ===== 106 Bookmarks
header(c, "Colour-Your-Own Bookmarks", "Colour, cut out and keep your place in every story!",
       "Cut along the dashed lines. Ask a grown-up to help with the scissors.")
BM = [(1, "Bloom where", "you are planted"), (3, "Read, dream", "& bloom"),
      (5, "Keep calm and", "colour on"), (29, "Every page is", "a new adventure")]
n_ = 4
gap = 14
bw_ = (W - 2 * M - gap * (n_ - 1)) / n_
btop, bbot = H - 152, 70
for i, (fi, l1, l2) in enumerate(BM):
    x = M + i * (bw_ + gap)
    c.setLineWidth(1.1)
    c.setDash(5, 3)
    c.roundRect(x, bbot, bw_, btop - bbot, 10)
    c.setDash()
    # ribbon hole
    c.setLineWidth(1.2)
    c.circle(x + bw_ / 2, btop - 18, 5)
    # stars
    star(c, x + 18, btop - 45, 6)
    star(c, x + bw_ - 18, btop - 60, 5)
    # quote
    c.setFont("Title", 13.5)
    c.drawCentredString(x + bw_ / 2, btop - 85, l1)
    c.drawCentredString(x + bw_ / 2, btop - 103, l2)
    # flower art
    draw_img(c, img(fi), x + 8, bbot + 120, bw_ - 16, btop - 125 - (bbot + 120))
    # doodles + name
    for k in range(3):
        doodle_flower(c, x + bw_ / 2 + (k - 1) * 30, bbot + 95, 7)
    c.setFont("Bold", 8.5)
    c.drawCentredString(x + bw_ / 2, bbot + 58, "This bookmark")
    c.drawCentredString(x + bw_ / 2, bbot + 47, "belongs to:")
    c.setStrokeColor(LIGHT)
    c.line(x + 12, bbot + 26, x + bw_ - 12, bbot + 26)
    c.setStrokeColor(black)
c.setFont("Body", 9)
c.setFillColor(GREY)
c.drawCentredString(W / 2, 56, "Tip: print on card stock (160–250 gsm) so your bookmarks last longer.")
c.setFillColor(black)
footer(c, 106)
c.showPage()

# ===== 107 Postcards
header(c, "Flower Postcards", "Colour it, write it, send it!",
       "Colour the picture, write a message, then cut out your postcard and give it to someone special.")
PC = [(1, "Thank You,", "Teacher!"), (5, "Love You,", "Mum & Dad!")]
ph = 300
for i, (fi, t1, t2) in enumerate(PC):
    y0 = H - 165 - (i + 1) * ph - i * 18
    x0, pw = M, W - 2 * M
    c.setLineWidth(1.1)
    c.setDash(5, 3)
    c.rect(x0, y0, pw, ph)
    c.setDash()
    half = pw * 0.52
    # left: picture side
    c.setFont("Title", 22)
    c.drawCentredString(x0 + half / 2, y0 + ph - 40, t1)
    c.drawCentredString(x0 + half / 2, y0 + ph - 66, t2)
    draw_img(c, img(fi), x0 + 20, y0 + 18, half - 40, ph - 98)
    star(c, x0 + 22, y0 + ph - 30, 7)
    star(c, x0 + half - 22, y0 + ph - 50, 6)
    # divider
    c.setLineWidth(1)
    c.line(x0 + half, y0 + 22, x0 + half, y0 + ph - 22)
    # right: message + address
    rx = x0 + half + 16
    rw = pw - half - 32
    c.setLineWidth(1.2)
    c.rect(x0 + pw - 70, y0 + ph - 82, 54, 62)
    c.setFont("Body", 7.5)
    c.setFillColor(GREY)
    c.drawCentredString(x0 + pw - 43, y0 + ph - 48, "Draw a")
    c.drawCentredString(x0 + pw - 43, y0 + ph - 57, "stamp")
    c.setFillColor(black)
    doodle_flower(c, x0 + pw - 43, y0 + ph - 32, 5)
    c.setFont("Bold", 11)
    c.drawString(rx, y0 + ph - 40, "Dear")
    c.setStrokeColor(LIGHT)
    c.line(rx + 32, y0 + ph - 42, x0 + pw - 82, y0 + ph - 42)
    for k in range(5):
        yy = y0 + ph - 78 - k * 24
        c.line(rx, yy, x0 + pw - (82 if yy > y0 + ph - 90 else 16), yy)
    c.setStrokeColor(black)
    c.setFont("Bold", 11)
    c.drawString(rx, y0 + 70, "From:")
    c.setStrokeColor(LIGHT)
    c.line(rx + 40, y0 + 68, x0 + pw - 16, y0 + 68)
    c.setStrokeColor(black)
    bee(c, rx + rw - 40, y0 + 34, 0.5)
footer(c, 107)
c.showPage()

# ===== 108 Answer key
c.setFont("Title", 30)
c.drawCentredString(W / 2, H - 62, "Answer Key")
c.setFont("Bold", 13)
c.setFillColor(GREY)
c.drawCentredString(W / 2, H - 82, "For parents & teachers – no peeking, explorers!")
c.setFillColor(black)
cell = 15
yt = H - 120
c.setFont("Bold", 11)
c.drawString(M, yt + 6, "Garden Word Search (p. 96)")
draw_grid_ws(c, g1, M + 4, yt - 4, cell, 8, p1)
x2 = W - M - 12 * cell - 4
c.setFont("Bold", 11)
c.drawString(x2 - 4, yt + 6, "Flower Word Search (p. 97)")
draw_grid_ws(c, g2, x2, yt - 4, cell, 8, p2)
yt2 = yt - 12 * cell - 30
c.setFont("Bold", 11)
c.drawString(M, yt2, "Flower Crossword (p. 98)")
ccell = min(16, (W / 2 - M - 10) / cww)
draw_crossword(c, M + 4, yt2 - 8, ccell, fill=True, numfont=5)
yl = yt2 - 8 - cwh * ccell - 20
c.setFont("Body", 9.5)
for ttl, lst in (("Across", across), ("Down", down)):
    txt = f"{ttl}: " + ", ".join(f"{n_}. {w}" for n_, w in lst)
    for ln in wrap(txt, "Body", 9.5, W / 2 - M - 10):
        c.drawString(M, yl, ln)
        yl -= 12
    yl -= 4
xr, yy = W / 2 + 20, yt2
sections = [("Petal Detective (p. 95)", [f"{k}. {v}" for k, v in ANS95.items()] + ["Bonus: 5 petals"]),
            ("Who's Who in the Garden? (p. 99)", [f"{a} – {b.title()}" for a, b in ANS99]),
            ("Rainbow Garden (p. 100)", [f"{a.title()} – {b.title()}" for a, b in ANS100])]
for ttl, lines in sections:
    c.setFont("Bold", 11)
    c.drawString(xr, yy, ttl)
    yy -= 15
    c.setFont("Body", 10)
    for ln in lines:
        c.drawString(xr, yy, ln)
        yy -= 13
    yy -= 9
footer(c, 108)
c.showPage()
c.save()
print("crossword placed", len(cwp), "missing", missing, "size", cww, "x", cwh)
