# -*- coding: utf-8 -*-
"""Builds the two-page Product Specification PDF and the longer Buyer Pack
PDF for Normah Agro Farm, from data/crops.json. Uses the same three brand
typefaces as the website (Archivo, Instrument Sans, IBM Plex Mono) and the
same six-token palette."""
import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, NextPageTemplate, PageBreak, KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE, "data", "crops.json")
FONT_DIR = os.path.join(BASE, "scripts", "fonts-for-pdf")
DOCS_DIR = os.path.join(BASE, "assets", "docs")
LOGO_PATH = os.path.join(BASE, "assets", "img", "logo.svg")

with open(DATA_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

# ---- brand tokens ----
INK = colors.HexColor("#101A12")
SEED = colors.HexColor("#1E6B3A")
LEAF = colors.HexColor("#4F9E43")
CHAFF = colors.HexColor("#E4BE3C")
LOAM = colors.HexColor("#6B4A2C")
MIST = colors.HexColor("#E5EAE1")
PAPER = colors.HexColor("#FBFCFA")
ON_INK = colors.HexColor("#F2F5EF")

# ---- fonts ----
# reportlab's TTFont parser reads raw sfnt files, not the woff2 container the
# website serves, so decompress the two woff2 webfonts to .ttf once here.
from fontTools.ttLib import TTFont as FTFont

def ensure_ttf(woff2_path, ttf_path):
    if not os.path.exists(ttf_path):
        f = FTFont(woff2_path)
        f.flavor = None
        f.save(ttf_path)
    return ttf_path

archivo_ttf = ensure_ttf(
    os.path.join(BASE, "assets", "fonts", "archivo-variable.woff2"),
    os.path.join(FONT_DIR, "Archivo-Variable.ttf"),
)
instrument_ttf = ensure_ttf(
    os.path.join(BASE, "assets", "fonts", "instrument-sans.woff2"),
    os.path.join(FONT_DIR, "InstrumentSans-FromSite.ttf"),
)

pdfmetrics.registerFont(TTFont("Archivo", archivo_ttf))
pdfmetrics.registerFont(TTFont("InstrumentSans", instrument_ttf))
pdfmetrics.registerFont(TTFont("PlexMono", os.path.join(FONT_DIR, "IBMPlexMono-Regular.ttf")))
pdfmetrics.registerFont(TTFont("PlexMono-Medium", os.path.join(FONT_DIR, "IBMPlexMono-Medium.ttf")))

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

styles = {
    "h1": ParagraphStyle("h1", fontName="Archivo", fontSize=22, leading=26, textColor=SEED, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Archivo", fontSize=14, leading=18, textColor=INK, spaceBefore=10, spaceAfter=6),
    "eyebrow": ParagraphStyle("eyebrow", fontName="PlexMono", fontSize=8.5, leading=11, textColor=SEED, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="InstrumentSans", fontSize=9.5, leading=14, textColor=INK),
    "body_dim": ParagraphStyle("body_dim", fontName="InstrumentSans", fontSize=8.5, leading=12, textColor=LOAM),
    "cell": ParagraphStyle("cell", fontName="InstrumentSans", fontSize=8.5, leading=11, textColor=INK),
    "cell_mono": ParagraphStyle("cell_mono", fontName="PlexMono", fontSize=8, leading=11, textColor=INK),
    "cell_head": ParagraphStyle("cell_head", fontName="PlexMono", fontSize=7.5, leading=10, textColor=ON_INK),
    "footer": ParagraphStyle("footer", fontName="PlexMono", fontSize=7, leading=9, textColor=LOAM),
    "verify": ParagraphStyle("verify", fontName="PlexMono", fontSize=7, leading=10, textColor=LOAM),
}


def season_label(codes):
    if not codes:
        return "Planned"
    return " & ".join(c for c in codes)


def crop_row(crop):
    def val(key, fallback="TBC — verify"):
        field = crop.get(key)
        if not field:
            return fallback
        v = field.get("value")
        return v if v else fallback

    return [
        Paragraph(crop["name"], styles["cell"]),
        Paragraph(season_label(crop.get("seasons", [])), styles["cell_mono"]),
        Paragraph(val("plantingWindow"), styles["cell_mono"]),
        Paragraph(val("harvestWindow"), styles["cell_mono"]),
        Paragraph(crop.get("primaryMarket", ""), styles["cell"]),
        Paragraph(val("packaging"), styles["cell_mono"]),
    ]


def draw_header_footer(canvas, doc, title):
    canvas.saveState()
    # header band
    canvas.setFillColor(INK)
    canvas.rect(0, PAGE_H - 22 * mm, PAGE_W, 22 * mm, fill=1, stroke=0)
    canvas.setFillColor(CHAFF)
    canvas.rect(0, PAGE_H - 22 * mm, PAGE_W, 1.2 * mm, fill=1, stroke=0)

    canvas.setFillColor(ON_INK)
    canvas.setFont("Archivo", 13)
    canvas.drawString(MARGIN, PAGE_H - 14 * mm, "NORMAH AGRO FARM")
    canvas.setFont("PlexMono", 8)
    canvas.setFillColor(LEAF)
    canvas.drawString(MARGIN, PAGE_H - 18.5 * mm, "AMURU DISTRICT, UGANDA")

    canvas.setFont("PlexMono", 8)
    canvas.setFillColor(ON_INK)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 14 * mm, title)

    # footer
    canvas.setFillColor(LOAM)
    canvas.setFont("PlexMono", 7)
    canvas.drawString(MARGIN, 12 * mm, "normahagrofarm.com  ·  sales@normahagrofarm.com [VERIFY]")
    canvas.drawRightString(PAGE_W - MARGIN, 12 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(colors.Color(0.06, 0.10, 0.07, alpha=0.15))
    canvas.line(MARGIN, 16 * mm, PAGE_W - MARGIN, 16 * mm)
    canvas.restoreState()


def build_spec_table():
    header = [Paragraph(h, styles["cell_head"]) for h in
              ["Crop", "Season(s)", "Planting window", "Harvest window", "Primary market", "Packaging"]]
    rows = [header]
    for crop in DATA["crops"]:
        if crop.get("status") == "planned":
            continue
        rows.append(crop_row(crop))

    col_widths = [23 * mm, 16 * mm, 27 * mm, 27 * mm, 34 * mm, 27 * mm]
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SEED),
        ("TEXTCOLOR", (0, 0), (-1, 0), ON_INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 1, SEED),
        ("LINEBELOW", (0, 1), (-1, -2), 0.5, colors.Color(0.06, 0.10, 0.07, alpha=0.12)),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, MIST]),
    ]))
    return t


def build_weighslip(rows, col_widths=(48 * mm, 40 * mm)):
    data = [[Paragraph(k, styles["body_dim"]), Paragraph(v, styles["cell_mono"])] for k, v in rows]
    t = Table(data, colWidths=list(col_widths))
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.Color(0.06, 0.10, 0.07, alpha=0.2), 1, (1, 2)),
        ("LINEABOVE", (0, 0), (-1, 0), 1.2, INK),
        ("LINEBELOW", (0, -1), (-1, -1), 1.2, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))
    return t


def build_spec_pdf():
    path = os.path.join(DOCS_DIR, "Normah-Agro-Farm-Product-Specification.pdf")
    doc = BaseDocTemplate(path, pagesize=A4,
                           leftMargin=MARGIN, rightMargin=MARGIN,
                           topMargin=28 * mm, bottomMargin=20 * mm,
                           title="Normah Agro Farm — Product Specification",
                           author="Normah Agro Farm Ltd")

    frame = Frame(MARGIN, 20 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 48 * mm, id="f1")

    def page1(canvas, doc_):
        draw_header_footer(canvas, doc_, "PRODUCT SPECIFICATION")

    def page2(canvas, doc_):
        draw_header_footer(canvas, doc_, "FARM & HANDLING")

    doc.addPageTemplates([
        PageTemplate(id="Page1", frames=[frame], onPage=page1),
        PageTemplate(id="Page2", frames=[frame], onPage=page2),
    ])

    story = []
    story.append(Paragraph("Product specification", styles["eyebrow"]))
    story.append(Paragraph("Grain from Amuru District, Uganda", styles["h1"]))
    story.append(Paragraph(
        "Own-farm grain from Amuru — six crops, two seasons, one traceable origin. "
        "Normah Agro Farm grows maize, soya beans, rice, sesame, sorghum and millet across two "
        "growing seasons on a single mechanised operation at Bana Trading Centre, Amuru District.",
        styles["body"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Crop specifications", styles["h2"]))
    story.append(build_spec_table())
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Fields shown as “TBC — verify” are provisional and pending client confirmation; "
        "see CONTENT-GAPS.md and data/crops.json in the website handover package.", styles["verify"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Planned addition", styles["h2"]))
    story.append(Paragraph(
        "Wheat is planned as a future crop and is not yet in production.", styles["body"]))

    story.append(NextPageTemplate("Page2"))
    story.append(PageBreak())

    story.append(Paragraph("The farm", styles["eyebrow"]))
    story.append(Paragraph("Bana Trading Centre, Amuru District", styles["h1"]))
    story.append(Paragraph(
        "Roughly 90 km west of Gulu town, bordering Adjumani and Nwoya districts, close to the "
        "South Sudan border and the Elegu/Nimule crossing.", styles["body"]))
    story.append(Spacer(1, 8))

    story.append(build_weighslip([
        ("Under cultivation today", "1,000+ acres"),
        ("Near-term growth plan", "Scaling toward 3,000+ acres"),
        ("Tractors", "4"),
        ("Combine harvesters", "2"),
        ("Grain warehouse", "450 sqm"),
        ("Growing seasons per year", "2"),
    ]))
    story.append(Paragraph(
        "Acreage figures are provisional pending client confirmation — see CONTENT-GAPS.md.",
        styles["verify"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Handling chain", styles["h2"]))
    chain_steps = [
        "Field and plot record", "Harvest", "Cleaning", "Drying and moisture check",
        "Grading", "Bagging", "Warehouse storage", "Dispatch documentation",
    ]
    chain_txt = "&nbsp;&nbsp;&raquo;&nbsp;&nbsp;".join(f"{i+1}. {s}" for i, s in enumerate(chain_steps))
    story.append(Paragraph(chain_txt, styles["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A silo with a processing area, a weighbridge and a washing/grading area are planned "
        "additions to this chain and are not yet built. Certification status (UNBS, phytosanitary, "
        "aflatoxin testing) is in progress — see the Quality, handling & traceability page for detail.",
        styles["body_dim"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Contact", styles["h2"]))
    story.append(build_weighslip([
        ("Kampala office", "Ntinda Ministers Village, Kampala"),
        ("Amuru farm", "Bana Trading Centre, Amuru District"),
        ("Email", "sales@normahagrofarm.com"),
        ("Web", "normahagrofarm.com"),
    ], col_widths=(40 * mm, 60 * mm)))

    doc.build(story)
    print("wrote", path)


def build_buyer_pack_pdf():
    path = os.path.join(DOCS_DIR, "Normah-Agro-Farm-Buyer-Pack.pdf")
    doc = BaseDocTemplate(path, pagesize=A4,
                           leftMargin=MARGIN, rightMargin=MARGIN,
                           topMargin=28 * mm, bottomMargin=20 * mm,
                           title="Normah Agro Farm — Buyer Pack",
                           author="Normah Agro Farm Ltd")
    frame = Frame(MARGIN, 20 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 48 * mm, id="f1")

    def page_any(canvas, doc_):
        draw_header_footer(canvas, doc_, "BUYER PACK")

    doc.addPageTemplates([PageTemplate(id="P", frames=[frame], onPage=page_any)])

    story = []
    story.append(Paragraph("Buyer pack", styles["eyebrow"]))
    story.append(Paragraph("Sourcing grain from Amuru, Uganda", styles["h1"]))
    story.append(Paragraph(
        "This pack combines Normah's product specification with capacity, logistics and "
        "documentation detail for buyers evaluating the farm as a supplier.", styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Crop specifications", styles["h2"]))
    story.append(build_spec_table())
    story.append(Spacer(1, 10))

    story.append(Paragraph("Capacity & availability", styles["h2"]))
    story.append(Paragraph(
        "Availability follows the two-season calendar above; see each crop's season assignment for "
        "timing. Standard packaging is 50 kg woven polypropylene bags "
        "(TBC — verify bulk/container options with the client).", styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Logistics", styles["h2"]))
    story.append(Paragraph(
        "Road route from Amuru to Kampala for domestic handling and onward logistics. Road route "
        "north on the Gulu–Elegu/Nimule corridor for South Sudan-bound shipments. Port options via "
        "Mombasa or Dar es Salaam for containerised export (TBC — verify preferred port and "
        "forwarding agent).", styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Documentation & terms", styles["h2"]))
    story.append(Paragraph(
        "Dispatch documentation traces every shipment to its batch and plot of origin. Export "
        "shipments require phytosanitary documentation, currently in progress. Payment terms and "
        "incoterms are confirmed per order (TBC — client to confirm).", styles["body"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Geography", styles["h2"]))
    story.append(Paragraph(
        "Amuru sits on the road corridor toward the Elegu/Nimule crossing into South Sudan, close to "
        "regional demand and Uganda's bimodal rainfall advantage over single-season producers.",
        styles["body"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Contact", styles["h2"]))
    story.append(build_weighslip([
        ("Kampala office", "Ntinda Ministers Village, Kampala"),
        ("Amuru farm", "Bana Trading Centre, Amuru District"),
        ("Email", "sales@normahagrofarm.com"),
        ("Web", "normahagrofarm.com"),
    ], col_widths=(40 * mm, 60 * mm)))

    doc.build(story)
    print("wrote", path)


build_spec_pdf()
build_buyer_pack_pdf()
