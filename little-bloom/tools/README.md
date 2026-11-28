# Build tools – Flowers Coloring Book Vol. 1, Edition 2.0

Everything needed to rebuild the PDFs is in this folder (fonts, cleaned line art, colour examples, original cover/back).
Requires Python 3 with `reportlab`, `pymupdf`, `numpy`, `pillow`.

| Script | Output (in `little-bloom/`) |
|---|---|
| `python3 build_front.py ../Front-Pages-p2-4-EN.pdf` | p. 2–4 |
| `python3 build_flowers.py ../Flower-Pages-p5-34-EN.pdf` | p. 5–34 flower pages + fact cards |
| `python3 build_levels.py ..` | p. 35–64 Easy and p. 65–94 Challenge |
| `python3 build_en.py ../Activity-Pages-p95-107-Answer-Key-EN.pdf` | p. 95–108 |
| `python3 build_109.py ../Page-109-Thank-You-Sources-EN.pdf` | p. 109 |
| `python3 combine.py` / `python3 combine.py --with-levels` | combined book |
| `python3 build_listing_images.py ../listing-images` | 10 Etsy listing images (2000×2000) |

## Adding new illustrations
- **Easy / Challenge:** save files in `little-bloom/illustrations/` as `easy_01_hibiscus.png` … `challenge_30_periwinkle.png` (only the number matters), then run `build_levels.py` and `combine.py --with-levels`.
- **Medium (p. 5–34):** replace `crops/fNN.png` (NN = flower number 01–30, e.g. `f28.png` for Rafflesia), remove that number from `NO_ART` in `build_flowers.py`, and re-run it.
- **Cover (current):** `python3 build_cover_from_art.py` uses your artwork `assets/cover_reference_art.jpg` (replace it with a higher-resolution export, ideally 2480×3508 px, and re-run) and writes `../cover.png` + `../cover.pdf`.
- **Alternative illustrated cover:** `python3 build_cover.py` (writes the same files, so copy the result if you want to keep both). A copy is saved as `../cover-alt-illustrated.png`.
- After changing the cover, re-run `combine.py` and `build_listing_images.py`.
