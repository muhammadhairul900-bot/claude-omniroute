"""Draw Rafflesia (f28) and Periwinkle (f30) as kids' line art + coloured examples (v2, more detailed).
Writes crops/f28.png, crops/f30.png (line art), insets/s_i28.png, s_i30.png and assets/colour_new_NN.png."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw

T = os.path.dirname(os.path.abspath(__file__))
SS = 2
LW = 15


def rot(pts, cx, cy, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def ell(cx, cy, rx, ry, ang=0, n=140, wave=0, freq=0, arc=None):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = 1.0
        if wave and (arc is None or math.cos(t) > arc):
            r += wave * math.sin(freq * t)
        pts.append((rx * r * math.cos(t), ry * r * math.sin(t)))
    return rot(pts, cx, cy, ang)


def lens(x0, y0, x1, y1, width, n=60, tip=0.9):
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.atan2(y1 - y0, x1 - x0)
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        w = (math.sin(math.pi * t ** tip)) * width / 2
        top.append((t * L, w))
        bot.append((t * L, -w))
    return rot(top + bot[::-1], x0, y0, ang)


def bez(p0, p1, p2, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (k / n for k in range(n + 1))]


class Art:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []

    def poly(self, pts, fill, lw=LW):
        self.ops.append(("poly", pts, fill, lw))

    def line(self, pts, lw=7):
        self.ops.append(("line", pts, lw))

    def circle(self, cx, cy, r, fill, lw=LW):
        self.poly(ell(cx, cy, r, r, n=max(24, int(r))), fill, lw)

    def render(self, colour):
        im = Image.new("RGB", (self.w * SS, self.h * SS), "white")
        d = ImageDraw.Draw(im)
        S = lambda p: [(x * SS, y * SS) for x, y in p]
        for op in self.ops:
            if op[0] == "poly":
                _, pts, fill, lw = op
                d.polygon(S(pts), fill=(fill if colour else "white") if fill else None)
                d.line(S(pts + [pts[0], pts[1]]), fill="black", width=lw * SS, joint="curve")
            else:
                _, pts, lw = op
                d.line(S(pts), fill="black", width=lw * SS, joint="curve")
                for (x, y) in (pts[0], pts[-1]):
                    r = lw * SS / 2
                    d.ellipse((x * SS - r, y * SS - r, x * SS + r, y * SS + r), fill="black")
        return im.resize((self.w, self.h), Image.LANCZOS)


def stem(A, path, w, fill):
    left, right = [], []
    for i in range(len(path)):
        x0, y0 = path[max(i - 1, 0)]
        x1, y1 = path[min(i + 1, len(path) - 1)]
        ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        ww = w * (1 - 0.35 * i / len(path))
        x, y = path[i]
        left.append((x + ww * math.cos(ang), y + ww * math.sin(ang)))
        right.append((x - ww * math.cos(ang), y - ww * math.sin(ang)))
    A.poly(left + right[::-1], fill)


def leaf(A, x0, y0, x1, y1, width, fill, veins=4, shine=True):
    A.poly(lens(x0, y0, x1, y1, width), fill)
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.atan2(y1 - y0, x1 - x0)
    A.line(rot([(0.04 * L, 0), (0.9 * L, 0)], x0, y0, ang), 7)
    for k in range(veins):
        t = 0.22 + k * 0.6 / max(1, veins - 1)
        for s in (1, -1):
            t2 = min(t + 0.13, 0.9)
            hw = math.sin(math.pi * t2 ** 0.9) * width / 2
            A.line(rot([(t * L, 0), (t2 * L, s * hw * 0.7)], x0, y0, ang), 5)
    if shine:
        A.line(rot([(0.25 * L, -width * 0.2), (0.45 * L, -width * 0.3)], x0, y0, ang), 5)


def fern(A, x0, y0, ang, length, n, fill):
    rach = [(t * length, 0.12 * length * math.sin(t * math.pi)) for t in (k / 30 for k in range(31))]
    rach = rot(rach, x0, y0, ang)
    for k in range(1, n):
        t = k / n
        i = int(t * 30)
        bx, by = rach[i]
        size = length * 0.26 * (1 - 0.7 * t)
        for s in (1, -1):
            a2 = ang + s * 1.05
            A.poly(lens(bx, by, bx + size * math.cos(a2), by + size * math.sin(a2), size * 0.38), fill, 10)
    A.line(rach, 10)


def fly(A, x, y, s, ang=0):
    WING, BODY = (220, 240, 255), (60, 70, 90)
    A.poly(ell(x - 18 * s, y - 34 * s, 22 * s, 38 * s, -0.5 + ang), WING, 9)
    A.poly(ell(x + 18 * s, y - 34 * s, 22 * s, 38 * s, 0.5 + ang), WING, 9)
    A.poly(ell(x, y, 26 * s, 36 * s, ang), BODY, 10)
    for k in (-1, 1):
        A.circle(x + k * 14 * s, y - 26 * s, 14 * s, (255, 255, 255), 8)
        A.circle(x + k * 14 * s, y - 24 * s, 5 * s, (0, 0, 0), 4)
    A.line(bez((x - 10 * s, y - 2 * s), (x, y + 8 * s), (x + 10 * s, y - 2 * s), 12), 6)


# ------------------------------------------------------------ Rafflesia v2
def rafflesia():
    rnd = random.Random(11)
    A = Art(2300, 2200)
    cx, cy = 1150, 1120
    RED, RED2, SPOT, DISC, WIN, HOLE, PROC = (178, 52, 40), (150, 40, 32), (246, 222, 205), (140, 40, 30), (240, 200, 185), (80, 24, 18), (200, 120, 95)
    FERN = (70, 150, 80)
    # rainforest ferns behind
    fern(A, 330, 2080, -1.15, 1100, 11, FERN)
    fern(A, 1980, 2100, -2.0, 1050, 11, FERN)
    fern(A, 280, 720, -0.35, 760, 9, (95, 170, 95))
    fern(A, 2040, 660, 3.55, 740, 9, (95, 170, 95))
    # petals (each with rim + warts; later petals cover earlier ones)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        pcx, pcy = cx + 560 * math.cos(a), cy + 560 * math.sin(a)
        outline = ell(pcx, pcy, 430, 395, a, n=200, wave=0.035, freq=11, arc=-0.2)
        A.poly(outline, RED)
        rim = ell(pcx, pcy, 380, 345, a, n=200, wave=0.03, freq=11, arc=-0.2)
        outer = [p for p, kk in zip(rim, range(200)) if math.cos(2 * math.pi * kk / 200) > 0.05]
        # keep the rim as one continuous arc (indices wrap around 0)
        idx = [kk for kk in range(200) if math.cos(2 * math.pi * kk / 200) > 0.05]
        start = next((i for i in range(1, len(idx)) if idx[i] - idx[i - 1] != 1), 0)
        outer = [rim[i] for i in idx[start:] + idx[:start]]
        A.line(outer, 7)
        placed = []
        tries = 0
        while len(placed) < 22 and tries < 1500:
            tries += 1
            u, v = rnd.uniform(-0.5, 0.8), rnd.uniform(-0.7, 0.7)
            if (u / 0.85) ** 2 + (v / 0.75) ** 2 > 0.8:
                continue
            x, y = rot([(430 * u, 395 * v)], pcx, pcy, a)[0]
            dcen = math.hypot(x - cx, y - cy)
            if dcen < 450:
                continue
            r = 18 + 34 * min(1, (dcen - 450) / 500) + rnd.uniform(-5, 5)
            if any(math.hypot(x - px, y - py) < r + pr + 14 for px, py, pr in placed):
                continue
            placed.append((x, y, r))
            A.poly(ell(x, y, r * 1.12, r * 0.92, rnd.uniform(0, 3)), SPOT, 9)
            if r > 30:
                A.line(bez((x - r * 0.45, y - r * 0.15), (x - r * 0.25, y - r * 0.5), (x + r * 0.1, y - r * 0.5), 10), 5)
    # central disc
    A.circle(cx, cy, 400, DISC)
    A.circle(cx, cy, 340, RED2, 10)
    for k in range(16):
        a = k * 2 * math.pi / 16
        A.poly(ell(cx + 290 * math.cos(a), cy + 290 * math.sin(a), 30, 18, a), WIN, 7)
    A.circle(cx, cy, 235, HOLE)
    A.circle(cx, cy, 165, PROC, 10)
    for ring, n_, r in ((115, 12, 20), (60, 6, 18)):
        for k in range(n_):
            a = k * 2 * math.pi / n_ + ring
            px, py = cx + ring * math.cos(a), cy + ring * math.sin(a)
            A.poly(rot([(-r, r * 0.8), (0, -r * 1.3), (r, r * 0.8)], px, py, a + math.pi / 2), (235, 170, 140), 6)
    A.circle(cx, cy, 22, (235, 170, 140), 6)
    # buzzing flies
    fly(A, 1870, 270, 1.5, 0.2)
    fly(A, 2080, 470, 1.15, -0.3)
    for (x0, y0, x1, y1, x2, y2) in [(1700, 380, 1620, 300, 1700, 220), (1960, 590, 1880, 640, 1830, 560)]:
        A.line(bez((x0, y0), (x1, y1), (x2, y2), 16), 5)
    return A


# ------------------------------------------------------------ Periwinkle v2
def periwinkle():
    A = Art(1800, 2300)
    PINK, PINK2, EYE, STAR, LEAF, STEMC = (243, 120, 178), (230, 90, 155), (200, 25, 90), (255, 225, 90), (60, 155, 80), (75, 135, 65)
    POT, RIM, SOIL = (205, 110, 70), (225, 135, 90), (110, 70, 45)
    A.poly(ell(900, 1665, 380, 60), SOIL)
    s_main = bez((900, 1680), (870, 1250), (900, 720))
    s_left = bez((890, 1350), (640, 1150), (520, 760))
    s_right = bez((895, 1250), (1150, 1050), (1260, 700))
    s_budl = bez((600, 1060), (420, 960), (360, 820))
    s_budr = bez((1170, 990), (1420, 930), (1470, 820))
    for p in (s_budl, s_budr, s_left, s_right, s_main):
        stem(A, p, 18, STEMC)
    for (x0, y0, x1, y1, w) in [(890, 1560, 520, 1440, 230), (905, 1540, 1280, 1420, 230),
                                (880, 1400, 560, 1270, 205), (900, 1380, 1230, 1250, 205),
                                (720, 1210, 460, 1180, 170), (1040, 1140, 1320, 1110, 170),
                                (560, 960, 330, 990, 140), (1210, 900, 1440, 980, 140),
                                (890, 1030, 700, 930, 150), (905, 1000, 1090, 900, 150)]:
        leaf(A, x0, y0, x1, y1, w, LEAF)

    def bud(x, y, ang):
        A.poly(lens(x, y, x + 150 * math.cos(ang), y + 150 * math.sin(ang), 70, tip=1.3), PINK2, 12)
        for t in (0.35, 0.65):
            bx, by = x + 150 * t * math.cos(ang), y + 150 * t * math.sin(ang)
            A.line(bez((bx - 28 * math.sin(ang), by + 28 * math.cos(ang)),
                       (bx + 25 * math.cos(ang), by + 25 * math.sin(ang)),
                       (bx + 28 * math.sin(ang), by - 28 * math.cos(ang)), 10), 6)

    bud(360, 830, -1.9)
    bud(1470, 830, -1.25)

    def flower(cx, cy, R, rot0):
        for k in range(5):
            a = rot0 + k * 2 * math.pi / 5
            # broad, rounded petal with a tiny point, slightly skewed (pinwheel)
            P = []
            for i in range(90):
                th = 2 * math.pi * i / 90
                rr = 1 + 0.06 * max(0, math.cos(th)) ** 12          # tiny tip
                x = R * 0.58 + R * 0.44 * rr * math.cos(th)
                y = R * 0.40 * math.sin(th) + 0.10 * R * (x / R) ** 2
                if x < R * 0.25:
                    y *= 0.55 + 0.45 * x / (R * 0.25)              # narrow base
                P.append((x, y))
            A.poly(rot(P, cx, cy, a), PINK)
            for off in (-0.12, 0, 0.12):
                A.line(rot([(R * 0.3, 0), (R * 0.75, off * R)], cx, cy, a + off * 0.5), 5)
        A.circle(cx, cy, R * 0.24, EYE, 12)
        st = []
        for k in range(10):
            r = R * (0.1 if k % 2 == 0 else 0.045)
            a = -math.pi / 2 + k * math.pi / 5
            st.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        A.poly(st, STAR, 6)

    flower(520, 720, 230, 0.4)
    flower(1260, 660, 240, -0.2)
    flower(900, 600, 280, 0.1)
    # butterfly
    bx, by = 1450, 300
    for s_, (ox, oy, rx, ry, a) in enumerate([(-60, -40, 85, 60, -0.6), (60, -40, 85, 60, 0.6), (-50, 40, 60, 45, 0.5), (50, 40, 60, 45, -0.5)]):
        A.poly(ell(bx + ox, by + oy, rx, ry, a), (90, 160, 240) if s_ < 2 else (255, 170, 60))
        A.circle(bx + ox * 1.15, by + oy * 1.1, 16 if s_ < 2 else 12, (255, 255, 255), 7)
    A.poly(ell(bx, by, 16, 75), (60, 60, 80), 9)
    A.line(bez((bx - 5, by - 70), (bx - 30, by - 120), (bx - 50, by - 130), 12), 6)
    A.line(bez((bx + 5, by - 70), (bx + 30, by - 120), (bx + 50, by - 130), 12), 6)
    for k in range(9):
        t = k / 8
        A.circle(1100 + 260 * t, 470 - 120 * t - 50 * math.sin(math.pi * t), 6, None, 6)
    # pot front
    A.poly([(560, 1720), (1240, 1720), (1160, 2240), (640, 2240)], POT)
    A.poly([(510, 1630), (1290, 1630), (1290, 1750), (510, 1750)], RIM)
    for k in range(4):
        x = 690 + k * 140
        A.circle(x, 1960, 38, (250, 210, 120), 8)
        A.circle(x, 1960, 12, POT, 6)
    A.line([(600, 2100), (1200, 2100)], 7)
    return A


def trim(im):
    a = np.array(im.convert("L"))
    ys, xs = np.where(a < 240)
    return im.crop((xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5))


for num, maker in ((28, rafflesia), (30, periwinkle)):
    art = maker()
    line = trim(art.render(False)).convert("L")
    a = np.array(line)
    a[a > 200] = 255
    Image.fromarray(a).save(os.path.join(T, "crops", f"f{num:02d}.png"))
    col = trim(art.render(True))
    s = 260 / col.height
    col.resize((round(col.width * s), 260), Image.LANCZOS).save(os.path.join(T, "insets", f"s_i{num:02d}.png"))
    col.save(os.path.join(T, "assets", f"colour_new_{num:02d}.png"))
    print("drew", num, line.size)
