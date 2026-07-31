"""Builds the Open Graph / social card images for Normah Agro Farm:
a 1200x630 landscape card (Facebook/LinkedIn/Twitter) and a 1080x1080
square variant (WhatsApp/Instagram/LinkedIn post). Built with Pillow
directly from the brand tokens and the same fonts used on the site and
in the PDFs, rather than a screenshot, so it stays crisp at any size."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(BASE, "scripts", "fonts-for-pdf")
OUT_DIR = os.path.join(BASE, "assets", "img")
LOGO_MARK = Image.open(os.path.join(OUT_DIR, "icon-512.png"))  # real emblem, square canvas, transparent bg

INK = (16, 26, 18)
SEED = (30, 107, 58)
LEAF = (79, 158, 67)
CHAFF = (228, 190, 60)
LOAM = (107, 74, 44)
PAPER = (251, 252, 250)
ON_INK = (242, 245, 239)

ARCHIVO = os.path.join(FONT_DIR, "Archivo-Variable.ttf")
INSTRUMENT = os.path.join(FONT_DIR, "InstrumentSans-FromSite.ttf")
PLEX = os.path.join(FONT_DIR, "IBMPlexMono-Medium.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_season_band(draw, x, y, w, h):
    """The signature Season Band motif, simplified: two segments + chips."""
    a_w = int(w * 0.42)
    draw.rounded_rectangle([x, y, x + a_w, y + h], radius=6, fill=SEED)
    draw.rounded_rectangle([x + a_w, y, x + w, y + h], radius=6, fill=LEAF)
    # re-square the inner seam
    draw.rectangle([x + a_w - 8, y, x + a_w + 8, y + h], fill=LEAF if False else SEED)
    draw.rectangle([x + a_w, y, x + a_w + 6, y + h], fill=LEAF)
    # chips as small dots along the band
    chip_y = y + h + 22
    positions = [0.08, 0.18, 0.32, 0.5, 0.62, 0.72]
    for p in positions:
        cx = x + int(w * p)
        draw.ellipse([cx - 7, chip_y - 7, cx + 7, chip_y + 7], fill=CHAFF, outline=INK, width=2)


def draw_logo_mark(im, draw, cx, cy, r):
    size = int(r * 2.4)
    mark = LOGO_MARK.resize((size, size), Image.LANCZOS)
    im.paste(mark, (int(cx - size / 2), int(cy - size / 2)), mark)


def build_card(w, h, path, layout="landscape"):
    im = Image.new("RGB", (w, h), INK)
    draw = ImageDraw.Draw(im)

    # subtle vertical gradient for depth
    for i in range(h):
        t = i / h
        shade = tuple(int(INK[c] + (0 if t < 0.6 else (t - 0.6) * 40)) for c in range(3))
        draw.line([(0, i), (w, i)], fill=shade)

    margin = int(w * 0.07)

    if layout == "landscape":
        logo_r = int(h * 0.11)
        draw_logo_mark(im, draw, margin + logo_r, margin + logo_r, logo_r)
        wordmark_font = font(PLEX, int(h * 0.032))
        draw.text((margin + logo_r * 2 + 24, margin + logo_r - int(h*0.02)), "NORMAH AGRO FARM", font=wordmark_font, fill=ON_INK)
        draw.text((margin + logo_r * 2 + 24, margin + logo_r + int(h*0.03)), "AMURU DISTRICT, UGANDA", font=font(PLEX, int(h*0.024)), fill=LEAF)

        headline_font = font(ARCHIVO, int(h * 0.11))
        draw.text((margin, int(h * 0.42)), "Own-farm grain", font=headline_font, fill=ON_INK)
        draw.text((margin, int(h * 0.42) + int(h*0.13)), "from Amuru.", font=headline_font, fill=CHAFF)

        sub_font = font(INSTRUMENT, int(h * 0.045))
        draw.text((margin, int(h * 0.72)), "Six crops · two seasons · one traceable origin", font=sub_font, fill=ON_INK)

        band_y = int(h * 0.84)
        draw_season_band(draw, margin, band_y, w - margin * 2, int(h * 0.05))

    else:  # square
        logo_r = int(w * 0.13)
        draw_logo_mark(im, draw, w // 2, int(h * 0.22), logo_r)
        wordmark_font = font(PLEX, int(w * 0.045))
        wm_text = "NORMAH AGRO FARM"
        bbox = draw.textbbox((0, 0), wm_text, font=wordmark_font)
        draw.text(((w - (bbox[2]-bbox[0])) / 2, int(h * 0.37)), wm_text, font=wordmark_font, fill=ON_INK)

        headline_font = font(ARCHIVO, int(w * 0.095))
        for i, line in enumerate(["Own-farm grain", "from Amuru."]):
            bbox = draw.textbbox((0, 0), line, font=headline_font)
            tw = bbox[2] - bbox[0]
            draw.text(((w - tw) / 2, int(h * 0.46) + i * int(w * 0.11)), line, font=headline_font,
                      fill=CHAFF if i == 1 else ON_INK)

        sub_font = font(INSTRUMENT, int(w * 0.038))
        sub_text = "Six crops · two seasons · one traceable origin"
        bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        draw.text(((w - (bbox[2]-bbox[0])) / 2, int(h * 0.72)), sub_text, font=sub_font, fill=ON_INK)

        band_w = int(w * 0.8)
        draw_season_band(draw, (w - band_w) // 2, int(h * 0.82), band_w, int(h * 0.045))

    im.save(path, "PNG")
    print("wrote", path)


build_card(1200, 630, os.path.join(OUT_DIR, "og-card.png"), "landscape")
build_card(1080, 1080, os.path.join(OUT_DIR, "og-card-square.png"), "square")
