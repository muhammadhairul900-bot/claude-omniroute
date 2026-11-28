"""Merge all parts into one book PDF.

Usage: python3 combine.py [--with-levels]
  default        -> cover, p.2-34, p.95-109, back cover (sellable now)
  --with-levels  -> also inserts Easy (p.35-64) and Challenge (p.65-94)
"""
import os, sys
import pymupdf

T = os.path.dirname(os.path.abspath(__file__))
L = os.path.dirname(T)
with_levels = "--with-levels" in sys.argv
cover_pdf = os.path.join(L, "cover.pdf")          # put the NEW cover here (1 page, A4) when ready
orig = pymupdf.open(os.path.join(T, "assets", "original_cover_and_back.pdf"))

parts = ["Front-Pages-p2-4-EN.pdf", "Flower-Pages-p5-34-EN.pdf"]
if with_levels:
    parts += ["Level-Easy-p35-64-EN.pdf", "Level-Challenge-p65-94-EN.pdf"]
parts += ["Activity-Pages-p95-107-Answer-Key-EN.pdf", "Page-109-Thank-You-Sources-EN.pdf"]

out = pymupdf.open()
if os.path.exists(cover_pdf):
    out.insert_pdf(pymupdf.open(cover_pdf), from_page=0, to_page=0)
else:
    out.insert_pdf(orig, from_page=0, to_page=0)
toc = [[1, "Cover", 1]]
names = {"Front-Pages-p2-4-EN.pdf": "Welcome", "Flower-Pages-p5-34-EN.pdf": "30 Flowers",
         "Level-Easy-p35-64-EN.pdf": "Easy Level", "Level-Challenge-p65-94-EN.pdf": "Challenge Level",
         "Activity-Pages-p95-107-Answer-Key-EN.pdf": "Activities, Passport & Bonus",
         "Page-109-Thank-You-Sources-EN.pdf": "Thank You & Sources"}
for p in parts:
    toc.append([1, names[p], out.page_count + 1])
    out.insert_pdf(pymupdf.open(os.path.join(L, p)))
out.insert_pdf(orig, from_page=1, to_page=1)
toc.append([1, "Back Cover", out.page_count])
out.set_toc(toc)
out.set_metadata({"title": "Flowers Coloring Book Vol. 1 – Edition 2.0 (English)", "author": "Little Bloom Studio"})
name = "Flowers-Coloring-Book-Vol1-Edition2-EN-" + ("FULL.pdf" if with_levels else "COMBINED.pdf")
dst = os.path.join(L, name)
out.save(dst, garbage=4, deflate=True)
print(dst, out.page_count, "pages", round(os.path.getsize(dst) / 1e6, 1), "MB")
