"""Draw Rafflesia (f28) and Periwinkle (f30) as kids' line art + coloured examples.
Writes crops/f28.png, crops/f30.png (line art) and insets/s_i28.png, s_i30.png (colour)."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw

T = os.path.dirname(os.path.abspath(__file__))
SS = 2  # supersampling


def ellipse_pts(cx, cy, rx, ry, ang, n=120):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
            for t in (2 * math.pi * k / n for k in range(n))]


def lens_pts(x0, y0, x1, y1, width, n=60, bulge=0.0):
    """Pointed leaf from (x0,y0) to (x1,y1)."""
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.atan2(y1 - y0, x1 - x0)
    ca, sa = math.cos(ang), math.sin(ang)
    top, bot = [], []
    for k in range(n + 1):
        t = k / n
        w = math.sin(math.pi * t) ** 0.85 * width / 2
        x = t * L
        top.append((x, w * (1 + bulge)))
        bot.append((x, -w * (1 - bulge)))
    pts = top + bot[::-1]
    return [(x0 + x * ca - y * sa, y0 + x * sa + y * ca) for x, y in pts]


class Art:
    def __init__(self, w, h, lw):
        self.w, self.h, self.lw = w, h, lw
        self.ops = []

    def poly(self, pts, fill):
        self.ops.append(("poly", pts, fill))

    def line(self, pts, width=None):
        self.ops.append(("line", pts, width))

    def circle(self, cx, cy, r, fill, width=None):
        self.ops.append(("circle", (cx, cy, r), fill, width))

    def render(self, colour):
        im = Image.new("RGB", (self.w * SS, self.h * SS), "white")
        d = ImageDraw.Draw(im)
        S = lambda p: [(x * SS, y * SS) for x, y in p]
        for op in self.ops:
            if op[0] == "poly":
                _, pts, fill = op
                d.polygon(S(pts), fill=fill if colour else "white")
                d.line(S(pts + [pts[0]]), fill="black", width=self.lw * SS, joint="curve")
            elif op[0] == "line":
                _, pts, width = op
                d.line(S(pts), fill="black", width=(width or self.lw // 2) * SS, joint="curve")
            else:
                _, (cx, cy, r), fill, width = op
                w = (width or self.lw) * SS
                d.ellipse(((cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS),
                          fill=fill if colour else "white", outline="black", width=w)
        im = im.resize((self.w, self.h), Image.LANCZOS)
        return im


def trim(im):
    a = np.array(im.convert("L"))
    ys, xs = np.where(a < 240)
    return im.crop((xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5))


# ------------------------------------------------------------ Rafflesia
def rafflesia():
    rnd = random.Random(3)
    A = Art(2000, 1960, 16)
    cx, cy = 1000, 1000
    RED, SPOT, DISC, HOLE, PROC = (178, 58, 43), (243, 217, 200), (150, 45, 35), (95, 28, 22), (205, 130, 105)
    petals = []
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        px, py = cx + 520 * math.cos(ang), cy + 520 * math.sin(ang)
        pts = ellipse_pts(px, py, 400, 360, ang)
        petals.append((pts, px, py, ang))
    # each petal is drawn with its own spots, so later petals cover earlier spots
    for pts, px, py, ang in petals:
        A.poly(pts, RED)
        placed = []
        tries = 0
        while len(placed) < 16 and tries < 500:
            tries += 1
            u, v = rnd.uniform(-0.6, 0.8), rnd.uniform(-0.75, 0.75)
            if u * u + v * v > 0.55:
                continue
            ca, sa = math.cos(ang), math.sin(ang)
            x = px + 400 * u * ca - 360 * v * sa
            y = py + 400 * u * sa + 360 * v * ca
            if math.hypot(x - cx, y - cy) < 420:
                continue
            r = rnd.uniform(26, 46)
            if any(math.hypot(x - a, y - b) < r + rr + 18 for a, b, rr in placed):
                continue
            placed.append((x, y, r))
            A.circle(x, y, r, SPOT, width=9)
    # central disc
    A.circle(cx, cy, 360, DISC)
    A.circle(cx, cy, 300, (170, 60, 45), width=10)
    A.circle(cx, cy, 190, HOLE)
    for k in range(18):
        a = k * 2 * math.pi / 18
        A.line([(cx + 205 * math.cos(a), cy + 205 * math.sin(a)), (cx + 285 * math.cos(a), cy + 285 * math.sin(a))], 7)
    # processes (spiky disc) inside the opening
    for k in range(7):
        a = k * 2 * math.pi / 7
        A.circle(cx + 105 * math.cos(a), cy + 105 * math.sin(a), 28, PROC, width=8)
    A.circle(cx, cy, 34, PROC, width=8)
    return A


# ------------------------------------------------------------ Periwinkle
def periwinkle():
    A = Art(1500, 1900, 15)
    PINK, EYE, CEN, LEAF, STEM = (240, 110, 170), (200, 30, 90), (255, 210, 60), (70, 160, 80), (60, 130, 60)
    # stems
    def stem(path, w):
        left, right = [], []
        for i in range(len(path) - 1):
            (x0, y0), (x1, y1) = path[i], path[i + 1]
            ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
            left.append((x0 + w * math.cos(ang), y0 + w * math.sin(ang)))
            right.append((x0 - w * math.cos(ang), y0 - w * math.sin(ang)))
        x0, y0 = path[-1]
        left.append((x0 + w * math.cos(ang), y0 + w * math.sin(ang)))
        right.append((x0 - w * math.cos(ang), y0 - w * math.sin(ang)))
        A.poly(left + right[::-1], STEM)

    def curve(p0, p1, p2, n=30):
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                 (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (k / n for k in range(n + 1))]

    main = curve((760, 1850), (720, 1300), (760, 820))
    br_l = curve((745, 1300), (520, 1100), (430, 760))
    br_r = curve((752, 1180), (1000, 1000), (1080, 700))
    for p in (br_l, br_r, main):
        stem(p, 26)

    def leaf(x0, y0, x1, y1, width):
        pts = lens_pts(x0, y0, x1, y1, width)
        A.poly(pts, LEAF)
        A.line([(x0, y0), (x0 + (x1 - x0) * 0.92, y0 + (y1 - y0) * 0.92)], 8)
        L = math.hypot(x1 - x0, y1 - y0)
        ang = math.atan2(y1 - y0, x1 - x0)
        for t in (0.3, 0.5, 0.7):
            bx, by = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for s in (1, -1):
                a2 = ang + s * 0.7
                A.line([(bx, by), (bx + 0.18 * L * math.cos(a2), by + 0.18 * L * math.sin(a2))], 6)

    for (x0, y0, x1, y1, w) in [(745, 1680, 300, 1560, 260), (765, 1650, 1210, 1530, 260),
                                (740, 1440, 340, 1300, 240), (755, 1410, 1150, 1270, 240),
                                (580, 1160, 230, 1080, 200), (920, 1060, 1260, 1020, 200),
                                (470, 920, 200, 880, 160), (1050, 830, 1320, 820, 160)]:
        leaf(x0, y0, x1, y1, w)

    def flower(cx, cy, R, rot):
        for k in range(5):
            a = rot + k * 2 * math.pi / 5
            # obovate petal, slightly offset for a pinwheel look
            pts = ellipse_pts(cx + R * 0.55 * math.cos(a + 0.12), cy + R * 0.55 * math.sin(a + 0.12), R * 0.55, R * 0.42, a + 0.12)
            A.poly(pts, PINK)
            A.line([(cx + R * 0.32 * math.cos(a + 0.1), cy + R * 0.32 * math.sin(a + 0.1)),
                    (cx + R * 0.78 * math.cos(a + 0.12), cy + R * 0.78 * math.sin(a + 0.12))], 6)
        A.circle(cx, cy, R * 0.26, EYE, width=12)
        A.circle(cx, cy, R * 0.09, CEN, width=8)

    flower(760, 640, 260, 0.2)
    flower(420, 600, 210, -0.3)
    flower(1090, 560, 220, 0.6)
    return A


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
