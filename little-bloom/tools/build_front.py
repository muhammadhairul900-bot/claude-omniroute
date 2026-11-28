"""Front pages 2-4 (English) – reuses helpers from build_en.py."""
import os, sys
S = os.path.dirname(os.path.abspath(__file__))
src = open(f"{S}/build_en.py").read().split("# ---------------------------------------------------------------- word search")[0]
OUT = sys.argv[1]
sys.argv = [sys.argv[0], OUT]
exec(src)


def seedling(c, x, y, s=1):
    c.saveState()
    c.setLineWidth(1.5)
    c.line(x, y, x, y + 16 * s)
    p = c.beginPath()
    p.moveTo(x, y + 12 * s); p.curveTo(x - 4 * s, y + 20 * s, x - 12 * s, y + 20 * s, x - 14 * s, y + 16 * s)
    p.curveTo(x - 10 * s, y + 10 * s, x - 4 * s, y + 10 * s, x, y + 12 * s)
    c.drawPath(p)
    p = c.beginPath()
    p.moveTo(x, y + 15 * s); p.curveTo(x + 4 * s, y + 23 * s, x + 12 * s, y + 23 * s, x + 14 * s, y + 19 * s)
    p.curveTo(x + 10 * s, y + 13 * s, x + 4 * s, y + 13 * s, x, y + 15 * s)
    c.drawPath(p)
    c.line(x - 10 * s, y, x + 10 * s, y)
    c.restoreState()


def para(c, text, x, y, width, font="Body", size=11.5, lead=16):
    for ln in wrap(text, font, size, width):
        c.setFont(font, size)
        c.drawString(x, y, ln)
        y -= lead
    return y


c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Flowers Coloring Book Vol. 1 – Front Pages")
c.setAuthor("Little Bloom Studio")

# ===== P2 This book belongs to
c.setFont("Title", 38)
c.drawCentredString(W / 2, H - 78, "This Book Belongs To")
tw = pdfmetrics.stringWidth("This Book Belongs To", "Title", 38)
doodle_flower(c, W / 2 - tw / 2 - 28, H - 66, 9)
doodle_flower(c, W / 2 + tw / 2 + 28, H - 66, 9)
y = H - 135
for lab, end in [("Name:", W - M), ("Age:", M + 220), ("I started colouring on:", W - M)]:
    c.setFont("Bold", 15)
    c.drawString(M + 10, y, lab)
    c.setStrokeColor(LIGHT)
    c.setLineWidth(1.2)
    c.line(M + 18 + pdfmetrics.stringWidth(lab, "Bold", 15), y - 3, end - 10, y - 3)
    c.setStrokeColor(black)
    y -= 38
# big frame with scalloped flower border
fx, fy, fw, fh = M + 30, 150, W - 2 * M - 60, y - 160
c.setLineWidth(2.2)
c.roundRect(fx, fy, fw, fh, 22)
c.setLineWidth(1)
c.setDash(4, 3)
c.roundRect(fx + 9, fy + 9, fw - 18, fh - 18, 16)
c.setDash()
for k in range(7):
    doodle_flower(c, fx + 20 + k * (fw - 40) / 6, fy + fh, 9)
    doodle_flower(c, fx + 20 + k * (fw - 40) / 6, fy, 9)
c.setFont("Title", 16)
c.setFillColor(LIGHT)
c.drawCentredString(W / 2, fy + fh / 2 + 6, "Draw yourself here!")
c.setFont("Body", 11)
c.drawCentredString(W / 2, fy + fh / 2 - 12, "Who is the new flower explorer?")
c.setFillColor(black)
bee_tip(c, M + 60, 98, "Hi, I'm Bibi the Bee! I'll buzz along with you on every page. Let's go!", 260, 0.75)
c.setFont("Bold", 11)
c.drawCentredString(W / 2, 52, "Every flower you colour makes your garden brighter!")
c.setFont("Bold", 11)
c.drawCentredString(W / 2, 20, "2")
c.showPage()

# ===== P3 How to use
header(c, "How To Use This Book", "A quick guide for little explorers (and their grown-ups)",
       "")
y0 = H - 128
c.setFont("Title", 16)
c.drawString(M, y0, "1. Pick your level")
levels = [("seed", "EASY", "Ages 3–5", "Thick lines and simple shapes", "pages 35–64"),
          ("flower", "MEDIUM", "Ages 6–8", "With Flower Fact Cards", "pages 5–34"),
          ("big", "CHALLENGE", "Ages 9+ & grown-ups", "More detail to colour", "pages 65–94")]
cw3 = (W - 2 * M - 20) / 3
for i, (ic, lv, age, desc, pg) in enumerate(levels):
    x = M + i * (cw3 + 10)
    yt = y0 - 14
    c.setLineWidth(1.6)
    c.roundRect(x, yt - 112, cw3, 112, 12)
    cx_ = x + cw3 / 2
    if ic == "seed":
        seedling(c, cx_, yt - 38, 1.1)
    elif ic == "flower":
        doodle_flower(c, cx_, yt - 24, 10)
    else:
        doodle_flower(c, cx_ - 16, yt - 24, 9)
        doodle_flower(c, cx_ + 16, yt - 24, 9, petals=6)
    c.setFont("Title", 15)
    c.drawCentredString(cx_, yt - 58, lv)
    c.setFont("Bold", 10.5)
    c.drawCentredString(cx_, yt - 74, age)
    c.setFont("Body", 9.5)
    c.drawCentredString(cx_, yt - 88, desc)
    c.setFillColor(GREY)
    c.drawCentredString(cx_, yt - 102, pg)
    c.setFillColor(black)
y = y0 - 152
c.setFont("Title", 16)
c.drawString(M, y, "2. Every flower page has")
items = [("Did You Know?", "a fun fact about the flower"),
         ("Colour palette", "the flower's real colours as a guide"),
         ("Trace the name", "practise writing the flower's name"),
         ("Example picture", "see what the real flower looks like")]
y -= 24
for i, (a, b) in enumerate(items):
    x = M + 6
    yy = y - i * 21
    doodle_flower(c, x + 6, yy + 4, 4.5)
    c.setFont("Bold", 11)
    c.drawString(x + 18, yy, a)
    c.setFont("Body", 10)
    c.drawString(x + 22 + pdfmetrics.stringWidth(a, "Bold", 11), yy, "– " + b)
y -= 4 * 21 + 14
c.setFont("Title", 16)
c.drawString(M, y, "3. Don't forget!")
y -= 24
for t in ["Stamp your Flower Passport (page 103) every time you finish a flower.",
          "Go on a Flower Hunt Mission (page 104) and find real flowers near you.",
          "Collect all 30 stamps to earn your Flower Expert Certificate (page 105)!"]:
    star(c, M + 12, y + 4, 6)
    c.setFont("Bold", 11)
    c.drawString(M + 26, y, t)
    y -= 21
# parents box
bh_ = 118
by_ = y - 14 - bh_
c.setLineWidth(1.5)
c.setDash(5, 3)
c.roundRect(M, by_, W - 2 * M, bh_, 12)
c.setDash()
c.setFont("Title", 13.5)
c.drawString(M + 14, by_ + bh_ - 22, "A note for parents & teachers")
notes = ["Print only the pages or level you need – separate files for each level are included.",
         "Paper: A4 or US Letter, 80–120 gsm. Use card stock for markers or watercolours.",
         "Printer: choose “Actual size / 100%”. Pure white pages save ink.",
         "Works with coloured pencils, crayons, markers and watercolours.",
         "For personal and family use only. A Classroom Licence is available for schools."]
yy = by_ + bh_ - 42
for t in notes:
    c.circle(M + 18, yy + 3.5, 1.8, fill=1)
    c.setFont("Body", 10)
    c.drawString(M + 26, yy, t)
    yy -= 15
bee_tip(c, M + 60, by_ - 48, "Psst! There are answers at the back of the book, but try it yourself first!", 250, 0.7)
footer(c, 3)
c.showPage()

# ===== P4 About
header(c, "Hello from Little Bloom Studio!", "Greetings from sunny Malaysia", "")
y = H - 132
txt = ("Our country is home to some of the most amazing flowers on Earth: the bright red hibiscus, "
       "the sweet-smelling jasmine, and even the giant Rafflesia, the biggest single flower in the world! "
       "We made this book so children everywhere can colour, learn about and fall in love with tropical "
       "flowers – and maybe find a few of them close to home, too.")
draw_img(c, img(1), W - M - 110, y - 105, 110, 120)
y = para(c, txt, M, y, W - 2 * M - 125, size=11.5, lead=17)
y -= 22
c.setFont("Title", 16)
c.drawString(M, y, "Our promise to you")
y -= 12
prom = [("Fact-checked", "Every fact is checked against botanical sources (listed on page 109)."),
        ("Printer-friendly", "Pure white backgrounds and clean lines that save ink."),
        ("Made with care", "Every page is checked by hand so it is accurate and easy to colour."),
        ("Always improving", "Edition 2.0 was made using feedback from families like yours.")]
cw2 = (W - 2 * M - 14) / 2
for i, (a, b) in enumerate(prom):
    col, row = i % 2, i // 2
    x = M + col * (cw2 + 14)
    yt = y - row * 74
    c.setLineWidth(1.4)
    c.roundRect(x, yt - 64, cw2, 60, 10)
    star(c, x + 18, yt - 22, 7)
    c.setFont("Bold", 12)
    c.drawString(x + 32, yt - 26, a)
    para(c, b, x + 14, yt - 44, cw2 - 24, size=9.5, lead=12)
y -= 160
c.setFont("Title", 14)
c.drawString(M, y, "How this book was made")
y = para(c, "The illustrations were created with the help of digital tools, then checked and refined "
            "one by one so they are accurate and easy to colour.", M, y - 18, W - 2 * M, size=10.5, lead=14)
y -= 20
c.setFont("Title", 16)
c.drawString(M, y, "Say hello!")
y = para(c, "Questions, a file problem, or a flower you'd love to see in Volume 2? We'd love to hear from you!",
         M, y - 20, W - 2 * M, size=11, lead=15)
y -= 6
for lab, ph in [("Email:", "[your email]"), ("Instagram / Pinterest:", "[your handle]"), ("Shop:", "[your Etsy shop link]")]:
    c.setFont("Bold", 11)
    c.drawString(M + 10, y, lab)
    c.setFont("Body", 11)
    c.setFillColor(GREY)
    c.drawString(M + 150, y, ph)
    c.setFillColor(black)
    y -= 18
y -= 8
c.setLineWidth(1.4)
c.roundRect(M, y - 34, W - 2 * M, 40, 10)
doodle_flower(c, M + 20, y - 14, 6)
c.setFont("Bold", 11)
c.drawString(M + 36, y - 18, "Share your little artist's work with #LittleBloomStudio – we might feature it!")
y -= 70
c.setFont("Body", 12)
c.drawString(M, y, "With love from Malaysia,")
c.setFont("Title", 17)
c.drawString(M, y - 22, "[Your name]")
c.setFont("Bold", 11)
c.drawString(M, y - 40, "Little Bloom Studio")
bee(c, W - M - 60, y - 15, 0.9)
footer(c, 4)
c.showPage()
c.save()
