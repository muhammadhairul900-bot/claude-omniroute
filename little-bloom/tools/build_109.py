"""Page 109 – Thank You, review request, Vol. 2 teaser, sources."""
import os, sys
S = os.path.dirname(os.path.abspath(__file__))
src = open(f"{S}/build_en.py").read().split("# ---------------------------------------------------------------- word search")[0]
OUT = sys.argv[1]
sys.argv = [sys.argv[0], OUT]
exec(src)


def para(c, text, x, y, width, font="Body", size=11.5, lead=16, center=False):
    for ln in wrap(text, font, size, width):
        c.setFont(font, size)
        (c.drawCentredString(x + width / 2, y, ln) if center else c.drawString(x, y, ln))
        y -= lead
    return y


c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Flowers Coloring Book Vol. 1 – Page 109")
c.setAuthor("Little Bloom Studio")
header(c, "Thank You, Flower Explorer!", "You coloured, learned and explored. We're so proud of you!", "")
y = H - 128
y = para(c, "Every flower you coloured made your garden a little brighter. Keep looking for flowers wherever you go: "
            "in parks, in gardens, on your way to school. Now you know their secrets!",
         M + 20, y, W - 2 * M - 40, size=11.5, lead=16, center=True)
draw_img(c, img(5), M + 10, y - 150, 120, 140)
draw_img(c, img(3), W - M - 130, y - 150, 120, 140)
bee(c, W / 2, y - 60, 1.1)
c.setFont("Title", 13)
c.drawCentredString(W / 2, y - 120, "See you in the next book!")
y -= 190

# review box
bh = 92
c.setLineWidth(1.7)
c.roundRect(M, y - bh, W - 2 * M, bh, 14)
c.setFont("Title", 16)
c.drawString(M + 18, y - 28, "Grown-ups: did you enjoy this book?")
for k in range(5):
    star(c, W - M - 120 + k * 22, y - 22, 8.5)
para(c, "A quick review on Etsy helps our small studio more than you know, and it helps other parents and teachers "
        "find us. A photo of your child's coloured page makes our day!",
     M + 18, y - 50, W - 2 * M - 36, size=10.5, lead=14)
y -= bh + 26

# coming next
bh = 116
c.setDash(5, 3)
c.roundRect(M, y - bh, W - 2 * M, bh, 14)
c.setDash()
c.setFont("Title", 16)
c.drawString(M + 18, y - 28, "Coming next from Little Bloom Studio")
nxt = [("Vol. 2", "Tropical Fruits of Malaysia"), ("Vol. 3", "Rainforest Animals of Malaysia")]
for i, (a, b) in enumerate(nxt):
    xx = M + 18 + i * ((W - 2 * M) / 2)
    doodle_flower(c, xx + 8, y - 54, 7)
    c.setFont("Bold", 12)
    c.drawString(xx + 22, y - 58, a)
    c.setFont("Body", 11.5)
    c.drawString(xx + 22, y - 74, b)
c.setFont("Body", 9.5)
c.setFillColor(GREY)
c.drawString(M + 18, y - bh + 14, "Follow our shop on Etsy so you don't miss them:  [your Etsy shop link]")
c.setFillColor(black)
y -= bh + 34

# sources
c.setFont("Title", 13)
c.drawString(M, y, "Sources")
y -= 15
y = para(c, "The “Did You Know?” facts in this book were checked against these trusted sources:",
         M, y, W - 2 * M, size=10, lead=13)
srcs = ["Plants of the World Online – Royal Botanic Gardens, Kew (powo.science.kew.org)",
        "Flora & Fauna Web – National Parks Board, Singapore (nparks.gov.sg/florafaunaweb)",
        "Forest Research Institute Malaysia – FRIM (frim.gov.my)",
        "Encyclopaedia Britannica (britannica.com)",
        "ASPCA Animal Poison Control – Toxic and Non-Toxic Plants (aspca.org)"]
for s_ in srcs:
    c.circle(M + 5, y + 3, 1.6, fill=1)
    c.setFont("Body", 10)
    c.drawString(M + 12, y, s_)
    y -= 14
y -= 6
c.setFont("Body", 8.5)
c.setFillColor(GREY)
c.drawString(M, y, "© Little Bloom Studio. For personal and family use only. Please do not share or resell this file. Thank you!")
c.setFillColor(black)
footer(c, 109)
c.showPage()
c.save()
