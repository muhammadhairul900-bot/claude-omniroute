"""Flower pages 5-34 (Medium level + Flower Fact Card), English."""
import os, sys
S = os.path.dirname(os.path.abspath(__file__))
src = open(f"{S}/build_en.py").read().split("# ---------------------------------------------------------------- word search")[0]
OUT = sys.argv[1]
sys.argv = [sys.argv[0], OUT]
exec(src)
pdfmetrics.registerFont(TTFont("Italic", f"{F}/Nunito-Italic.ttf"))
from reportlab import rl_config
rl_config.useA85 = 0

RED, YEL, GRN, WHT = "#E53935", "#FFD21F", "#4CAF50", "#FFFFFF"
PNK, PUR, ORG, BLU = "#F48FB1", "#8E44C9", "#FB8C00", "#1E5BD8"
DATA = [
 ("Hibiscus", "Bunga Raya", "Hibiscus rosa-sinensis", "The hibiscus is Malaysia's national flower! Its five petals stand for the five principles of the Rukun Negara, Malaysia's national promise.", [RED, YEL, GRN]),
 ("Jasmine", "Bunga Melur", "Jasminum sambac", "This jasmine is the national flower of Indonesia and the Philippines. Its sweet scent is used to make jasmine tea.", [WHT, "#FFF3C4", GRN]),
 ("Orchid", "Bunga Orkid", "Orchidaceae", "There are more than 25,000 kinds of orchids in the world! Vanilla flavour actually comes from the fruit of an orchid.", [PUR, "#EC4FA4", YEL, GRN]),
 ("Rose", "Bunga Ros", "Rosa", "Roses love cool weather, so in tropical Malaysia they grow best high up in the cool mountains of Cameron Highlands.", [RED, PNK, "#2E7D32"]),
 ("Sunflower", "Bunga Matahari", "Helianthus annuus", "A sunflower head is really hundreds of tiny flowers packed together. Its seeds are a crunchy snack!", [YEL, ORG, "#6D4C41", GRN]),
 ("Bougainvillea", "Bunga Kertas", "Bougainvillea", "The bright “petals” are actually special leaves! The real flowers are the tiny white ones in the middle.", ["#D81B60", WHT, GRN]),
 ("Frangipani", "Bunga Kemboja", "Plumeria", "Frangipani comes from Central America and is the national flower of Laos. It smells sweetest at night.", [WHT, YEL, GRN]),
 ("Water Lily", "Bunga Teratai", "Nymphaea", "Water lily leaves float flat on the water and have a little notch. It is the national flower of Bangladesh.", [PNK, WHT, YEL, GRN, "#4FC3F7"]),
 ("Queen of the Night", "Bunga Bakawali", "Epiphyllum oxypetalum", "This flower is a cactus! It opens only at night and wilts before the sun comes up.", [WHT, "#FFF3C4", GRN]),
 ("Champaca", "Bunga Cempaka", "Magnolia champaca", "Champaca flowers grow on very tall trees, not small bushes. Their lovely scent is used in perfumes.", [YEL, "#FFB74D", GRN]),
 ("Ylang-Ylang", "Bunga Kenanga", "Cananga odorata", "Ylang-ylang flowers start green and turn yellow when they are ready. Their oil is used in famous perfumes around the world.", [YEL, "#AED581", GRN]),
 ("Spanish Cherry", "Bunga Tanjung", "Mimusops elengi", "These tiny star-shaped flowers stay fragrant even after they fall and dry!", ["#FFF3C4", "#FFF59D", GRN]),
 ("Torch Ginger", "Bunga Kantan", "Etlingera elatior", "You can eat this flower! In Malaysia it goes into asam laksa, a famous sour fish noodle soup. It belongs to the ginger family.", [RED, PNK, GRN]),
 ("Butterfly Pea", "Bunga Telang", "Clitoria ternatea", "In Malaysia this flower colours rice bright blue! Add lemon juice to butterfly pea tea and watch it turn purple like magic.", [BLU, WHT, YEL, GRN]),
 ("Lavender", "Bunga Lavender", "Lavandula", "Lavender loves cool, sunny places like Provence in France. In hot Malaysia it only grows in the cool highlands.", [PUR, "#CE93D8", "#8FA98F"]),
 ("Chrysanthemum", "Bunga Kekwa", "Chrysanthemum", "Dried chrysanthemum flowers make chrysanthemum tea, a favourite cold drink in Malaysia!", [YEL, ORG, GRN]),
 ("Tulip", "Bunga Tulip", "Tulipa", "Tulips first came from Central Asia and became famous in the Netherlands. They can't grow naturally in Malaysia's hot weather.", [RED, YEL, PNK, GRN]),
 ("Daffodil", "Bunga Daffodil", "Narcissus", "The daffodil is the national flower of Wales. Careful: every part of it is poisonous if eaten!", [YEL, ORG, GRN]),
 ("Lily", "Bunga Lili", "Lilium", "Lilies have 6 petals. Lily pollen is very dangerous for cats, so keep lilies away from your kitty!", [PNK, WHT, YEL, GRN]),
 ("Daisy", "Bunga Daisy", "Bellis perennis", "“Daisy” comes from “day's eye” because the flower opens in the day and closes at night.", [WHT, YEL, GRN]),
 ("Moss Rose", "Bunga Mawar Jepun", "Portulaca grandiflora", "Its thick little leaves store water, so it survives hot sun and needs very little watering.", ["#D81B60", ORG, YEL, GRN]),
 ("Ten O'Clock Flower", "Bunga Pukul Sepuluh", "Portulaca", "It got its name because it opens at around 10 o'clock in the morning when the sun is bright, then closes in the afternoon.", [PNK, YEL, GRN]),
 ("Golden Trumpet", "Bunga Alamanda", "Allamanda cathartica", "Its flowers are shaped like a trumpet. Its sap is poisonous, so look but never taste!", [YEL, "#FFB74D", GRN]),
 ("Canna Lily", "Bunga Tasbih", "Canna indica", "Its round, hard, black seeds were once used to make prayer beads. That's how it got its Malay name, which means “prayer bead flower”!", [RED, ORG, YEL, GRN]),
 ("Coleus", "Pokok Ati-ati", "Coleus scutellarioides", "Coleus is famous for its colourful leaves, not its flowers. Its real flowers are tiny and bluish-purple.", ["#D81B60", "#C0CA33", PUR]),
 ("Ixora", "Bunga Jejarum", "Ixora", "Each tiny flower has a long, thin tube like a needle, and one cluster can hold dozens of little flowers!", [RED, ORG, GRN]),
 ("Crown of Thorns", "Bunga Janda Kaya", "Euphorbia milii", "The red parts are special leaves, not petals. The stem is covered in thorns and its white sap can sting your skin.", [RED, GRN, "#6D4C41"]),
 ("Rafflesia", "Bunga Pakma", "Rafflesia", "Rafflesia is the biggest single flower in the world, almost 1 metre (3 feet) wide! It has no leaves, stem or roots, and it smells like rotting meat to attract flies.", ["#B23A2B", WHT, "#6D4C41"]),
 ("Sacred Lotus", "Bunga Seroja", "Nelumbo nucifera", "Lotus leaves are waterproof: water drops roll off and carry the dirt away! Its seeds are made into the sweet filling of mooncakes.", [PNK, YEL, GRN]),
 ("Periwinkle", "Bunga Tapak Dara", "Catharanthus roseus", "Scientists use substances from this little flower to make cancer medicine. But never eat it, because it's poisonous!", [PNK, WHT, GRN]),
]
NO_ART = {28, 30}          # new drawings needed
NO_INSET = {9, 28, 30}      # example colour wrong / missing


def fit(text, font, maxsize, width):
    s = maxsize
    while pdfmetrics.stringWidth(text, font, s) > width and s > 10:
        s -= 1
    return s


c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Flowers Coloring Book Vol. 1 – Flower Pages")
c.setAuthor("Little Bloom Studio")
for n, (en, ms, sci, fact, pal) in enumerate(DATA, 1):
    page = n + 4
    # title
    ts = fit(en.upper(), "Title", 40, W - 2 * M - 70)
    c.setFont("Title", ts)
    c.drawCentredString(W / 2, H - 66, en.upper())
    tw = pdfmetrics.stringWidth(en.upper(), "Title", ts)
    doodle_flower(c, W / 2 - tw / 2 - 24, H - 54, 8)
    doodle_flower(c, W / 2 + tw / 2 + 24, H - 54, 8)
    a = "In Malaysia: " + ms + "   •   "
    wa = pdfmetrics.stringWidth(a, "Bold", 12)
    wb = pdfmetrics.stringWidth(sci, "Italic", 12)
    x = W / 2 - (wa + wb) / 2
    c.setFillColor(GREY)
    c.setFont("Bold", 12)
    c.drawString(x, H - 88, a)
    c.setFont("Italic", 12)
    c.drawString(x + wa, H - 88, sci)
    c.setFillColor(black)
    # drawing area
    ax, ay, aw, ah = M, 242, W - 2 * M, H - 104 - 242
    if n in NO_ART:
        c.setLineWidth(1.5)
        c.setDash(6, 4)
        c.roundRect(ax + 40, ay + 10, aw - 80, ah - 20, 16)
        c.setDash()
        c.setFont("Title", 18)
        c.setFillColor(LIGHT)
        c.drawCentredString(W / 2, ay + ah / 2 + 8, "PLACE NEW ILLUSTRATION HERE")
        c.setFont("Bold", 11)
        c.drawCentredString(W / 2, ay + ah / 2 - 14, f"{en} – black line art, white background, closed lines")
        c.setFillColor(black)
    else:
        draw_img(c, img(n), ax, ay, aw, ah)
    # fact card
    cy, ch = 108, 122
    c.setLineWidth(1.6)
    c.roundRect(M, cy, W - 2 * M, ch, 14)
    split = M + 300
    c.setLineWidth(1)
    c.setDash(3, 3)
    c.line(split, cy + 12, split, cy + ch - 12)
    c.setDash()
    star(c, M + 20, cy + ch - 22, 8)
    c.setFont("Title", 15)
    c.drawString(M + 34, cy + ch - 27, "Did You Know?")
    yy = cy + ch - 48
    fl = wrap(fact, "Body", 10.5, split - M - 28)
    assert len(fl) <= 5, (en, len(fl))
    for ln in fl:
        c.setFont("Body", 10.5)
        c.drawString(M + 16, yy, ln)
        yy -= 14
    # right side: example + palette
    rx0, rw = split + 12, W - M - split - 24
    c.setFont("Bold", 10)
    c.drawString(rx0, cy + ch - 22, "Real colours")
    if n not in NO_INSET:
        draw_img(c, f"{S}/insets/s_i{n:02d}.png", rx0 + rw - 74, cy + 12, 74, ch - 22)
        pw_ = rw - 82
    else:
        pw_ = rw
    k = len(pal)
    r = 8.5
    per_row = max(1, int((pw_ + 6) // (2 * r + 7)))
    for j, col in enumerate(pal):
        row, cc = divmod(j, per_row)
        c.setFillColor(HexColor(col))
        c.setLineWidth(1.2)
        c.circle(rx0 + r + cc * (2 * r + 7), cy + ch - 48 - row * (2 * r + 8), r, fill=1, stroke=1)
    c.setFillColor(black)
    c.setFont("Body", 8.5)
    c.setFillColor(GREY)
    yh = cy + ch - 48 - ((k - 1) // per_row) * (2 * r + 8) - r - 16
    for ln in wrap("Use these colours, or invent your own!", "Body", 8.5, pw_):
        c.drawString(rx0, yh, ln)
        yh -= 11
    c.setFillColor(black)
    # trace the name
    c.setFont("Bold", 11)
    c.drawString(M, 76, "Trace the name:")
    tx = M + 100
    tsz = fit(en, "Title", 36, W - M - tx)
    c.saveState()
    c.setStrokeColor(HexColor("#7A7A7A"))
    c.setLineWidth(1.1)
    c.setDash(2.2, 1.8)
    t = c.beginText(tx, 66)
    t.setFont("Title", tsz)
    t.setTextRenderMode(1)
    t.textLine(en)
    c.drawText(t)
    c.restoreState()
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.6)
    c.line(tx, 64, W - M, 64)
    c.setStrokeColor(black)
    footer(c, page)
    c.showPage()
c.save()
