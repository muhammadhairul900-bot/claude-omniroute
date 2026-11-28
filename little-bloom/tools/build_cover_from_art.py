"""Cover from the user's own artwork (assets/cover_reference_art.jpg), fitted to A4
with a branded bottom band.  Usage: python3 build_cover_from_art.py -> ../cover.png + ../cover.pdf"""
import io, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

T = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(T)
W, H = 2480, 3508


def F(n, s):
    return ImageFont.truetype(os.path.join(T, "fonts", n), s)


art = Image.open(os.path.join(T, "assets", "cover_reference_art.jpg")).convert("RGB")
s = W / art.width
art = art.resize((W, round(art.height * s)), Image.LANCZOS)
art = art.filter(ImageFilter.UnsharpMask(radius=2.2, percent=90, threshold=2))
img = Image.new("RGB", (W, H), (30, 100, 50))
img.paste(art, (0, 0))
# extend artwork into the band area with a blurred, darkened copy of its bottom edge
strip = art.crop((0, art.height - 260, W, art.height)).resize((W, H - art.height + 260))
strip = strip.filter(ImageFilter.GaussianBlur(14))
img.paste(strip, (0, art.height - 260))
img.paste(art.crop((0, 0, W, art.height - 140)), (0, 0))
# soft fade between art and extension
fade = art.crop((0, art.height - 140, W, art.height))
mask = Image.linear_gradient("L").rotate(180).resize(fade.size)
img.paste(fade, (0, art.height - 140), mask)

d = ImageDraw.Draw(img, "RGBA")
# band
BY0, BY1 = H - 330, H - 50
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((90, BY0 + 20, W - 70, BY1 + 26), radius=110, fill=(0, 0, 0, 120))
img.paste(sh.filter(ImageFilter.GaussianBlur(20)), (0, 0), sh.filter(ImageFilter.GaussianBlur(20)))
d = ImageDraw.Draw(img)
d.rounded_rectangle((80, BY0, W - 80, BY1), radius=110, fill=(214, 160, 50))
d.rounded_rectangle((98, BY0 + 18, W - 98, BY1 - 18), radius=95, fill=(255, 246, 222))
cy = (BY0 + BY1) / 2
# left badge: ages
d.ellipse((150, cy - 120, 390, cy + 120), fill=(255, 205, 50), outline=(214, 160, 50), width=8)
d.text((270, cy - 40), "AGES", font=F("Nunito-Black.ttf", 52), fill=(120, 60, 0), anchor="mm")
d.text((270, cy + 30), "3–10", font=F("Fredoka-SemiBold.ttf", 84), fill=(120, 60, 0), anchor="mm")
# right badge: activities
d.ellipse((W - 390, cy - 120, W - 150, cy + 120), fill=(25, 45, 140), outline=(214, 160, 50), width=8)
d.text((W - 270, cy - 45), "FUN", font=F("Nunito-Black.ttf", 50), fill=(255, 255, 255), anchor="mm")
d.text((W - 270, cy + 5), "FACTS +", font=F("Nunito-Black.ttf", 42), fill=(255, 255, 255), anchor="mm")
d.text((W - 270, cy + 50), "GAMES", font=F("Nunito-Black.ttf", 42), fill=(255, 225, 110), anchor="mm")
# centre text
d.text((W / 2, cy - 48), "Colour  •  Learn  •  Explore", font=F("Fredoka-SemiBold.ttf", 96), fill=(25, 45, 140), anchor="mm")
d.text((W / 2, cy + 62), "LITTLE BLOOM STUDIO", font=F("Nunito-Black.ttf", 70), fill=(200, 30, 40), anchor="mm")

img.save(os.path.join(L, "cover.png"), optimize=True)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
buf = io.BytesIO()
img.save(buf, "JPEG", quality=92)
buf.seek(0)
c = canvas.Canvas(os.path.join(L, "cover.pdf"), pagesize=A4)
c.setTitle("Flowers Coloring Book – Cover")
c.drawImage(ImageReader(buf), 0, 0, A4[0], A4[1])
c.showPage()
c.save()
print("cover saved", img.size)
