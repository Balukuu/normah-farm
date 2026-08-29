# Normah Agro Farm — website

Static, no-build-step marketing site for Normah Agro Farm Ltd, built to
the "Field Ledger" design system: six brand colour tokens, three typefaces
(Archivo for display, Instrument Sans for body, IBM Plex Mono for every
number on the site), and a scroll-linked Season Band as the signature
visual device. Plain HTML/CSS/vanilla JS — no framework, no bundler, no
`npm install`. It is meant to still work, untouched, in three years.

## What's in this folder

```
index.html                  Home
crops/index.html            What we grow — index + comparison table
crops/<crop>.html           Six crop detail pages (maize, soya-beans, rice, sesame, sorghum, millet)
farm.html                   The Farm
quality.html                Quality, Handling & Traceability
buyers.html                 For Buyers (incl. the request-a-quote form)
growers.html                For Growers
impact.html                 Community & Sustainability
about.html                  About
field-notes/                Field Notes index + 3 draft posts
contact.html                Contact (incl. general enquiry form)
assets/css/                 tokens.css, base.css, components.css, pages.css
assets/js/                  season-band.js, reveal.js, quote-form.js, nav.js
assets/fonts/               Self-hosted Archivo, Instrument Sans, IBM Plex Mono (woff2, latin subset)
assets/img/                 Logo, favicons, corridor map SVG, OG cards, photo placeholders live inline in HTML
assets/docs/                crop-specifications.xlsx, the two PDFs
assets/php/send-quote.php.example   Starting point for a cPanel mail handler
data/crops.json             Single source of truth for crop data
scripts/                    Python build scripts for the xlsx/PDFs/OG cards (not needed to run the site — only to regenerate the docs)
robots.txt, sitemap.xml, CNAME, .nojekyll
.htaccess                   Apache/cPanel config — inert on the current GitHub Pages host, kept in case of a future Apache deployment
SHOT-LIST.md                Every photo placeholder, what to shoot and when
CONTENT-GAPS.md             Every [VERIFY] in the build, grouped, with who needs to answer
```

## Editing content

Every page is a plain, hand-authored HTML file — there is no templating
engine, so header/nav/footer markup is repeated on every page rather than
included from one place. This is a deliberate trade-off for a client with
no in-house dev team (see Stack Option A in the build brief): editing a
paragraph means opening that one file and changing the text, with no
build step to run afterward.

**If you change the header, footer, or navigation**, you're changing it
on 19 files. Use your editor's find-and-replace across the folder rather
than editing pages one at a time.

**`[VERIFY]` markers.** Anywhere you see an HTML comment like
`<!-- [VERIFY] ... -->` or a `Verify` badge, that content is a safe
placeholder, not a confirmed fact — see `CONTENT-GAPS.md` for the full,
organised list before removing any of these.

## Editing `data/crops.json`

This file is the intended single source of truth for crop specifications
— seasons, planting/harvest windows, moisture targets, packaging, etc. —
and it feeds:
- `assets/docs/crop-specifications.xlsx` (via `scripts/build-xlsx.py`)
- `assets/docs/Normah-Agro-Farm-Product-Specification.pdf` and
  `Normah-Agro-Farm-Buyer-Pack.pdf` (via `scripts/build-pdfs.py`)

**It does not automatically update the HTML.** Because this is a
no-build static site, `crops/*.html`, `crops/index.html`, `buyers.html`
and the Season Band markup on `index.html` all hand-encode the same data
as HTML/CSS (so the site works with JavaScript disabled — see below).
If you change a value in `crops.json`, also update the matching HTML by
hand, and re-run the two build scripts so the spreadsheet and PDFs match:

```bash
python scripts/build-xlsx.py
python scripts/build-pdfs.py
```

Both require Python 3 with `openpyxl` (xlsx) and `reportlab` +
`fonttools` + `brotli` (PDFs) installed — `pip install openpyxl reportlab
fonttools brotli`.

To regenerate the OG social cards after a brand change:
```bash
python scripts/build-og-cards.py
```
(requires `Pillow`).

## Wiring the quote & enquiry forms

`assets/js/quote-form.js` handles both the buyer request-a-quote form
(`buyers.html#quote`) and the general enquiry form (`contact.html`). It
validates fields client-side, then POSTs a JSON payload to an endpoint —
**no form on this site sends anywhere until you set that endpoint.**

The site is static and hosted on GitHub Pages, which cannot run the PHP
mail handler (`assets/php/send-quote.php.example` is kept only in case
of a future move to Apache/cPanel hosting — it does not work here).
Forms POST to **Formspree** instead:

1. Create a form at [formspree.io](https://formspree.io) for each of the
   two forms (or reuse one endpoint for both, if you're on a plan with a
   submission cap you'd rather share).
2. Each `<form data-normah-form>` in `buyers.html` and `contact.html`
   already carries `data-endpoint="https://formspree.io/f/YOUR_FORM_ID"`
   — replace `YOUR_FORM_ID` with the real id Formspree gives you (marked
   with a `[VERIFY]` comment right above each form tag).
3. `quote-form.js` sends `Accept: application/json` so Formspree responds
   with JSON instead of redirecting — no further code changes needed.

Test a real submission once the ids are set — Formspree's free tier has
a monthly submission cap, worth checking before launch.

## Deployment (GitHub Pages)

The site is deployed via GitHub Pages with a custom domain,
`normahfarms.co.ug`, set in the `CNAME` file at the repo root.

- **Clean URLs work natively** — GitHub Pages serves `/about` directly
  from `about.html` with no redirect and no build step, so every internal
  link on the site already omits the `.html` extension. `.htaccess` (an
  Apache/cPanel artifact) does nothing here; it's kept only for a
  possible future move off GitHub Pages.
- `.nojekyll` at the repo root skips GitHub's default Jekyll build step,
  since this is plain hand-authored HTML with no templating.
- Canonical tags, Open Graph URLs, JSON-LD and `sitemap.xml` all point at
  `https://normahfarms.co.ug/` — update all of these together if the
  domain ever changes (grep for the old domain across `*.html`,
  `sitemap.xml`, and `robots.txt`).
- Set up the Formspree endpoints per the section above before considering
  the forms done.
- Submit `sitemap.xml` to Google Search Console once the domain is live.

## Design rationale (short version)

- **Palette:** the six tokens in `assets/css/tokens.css` come straight
  from the existing Normah logo (two greens, one yellow) plus two
  additions grounded in the place itself — a soil brown (`--loam`) and a
  cool green-grey paper tone (`--mist`) instead of the ubiquitous warm
  cream. Nothing else was added; the QA pass greps the CSS for stray hex
  values.
- **Type:** Archivo's expanded width axis reads as signage/agricultural
  infrastructure rather than editorial display type; Instrument Sans
  carries body copy without competing for attention; every number on the
  site — acreage, tonnage, dates, moisture — sets in IBM Plex Mono, which
  is what makes the site read as operational rather than promotional.
- **Signature element:** the Season Band renders the two real growing
  seasons as a literal horizontal timeline with crops as chips at their
  position — because that's what the farm's own planting calendar looks
  like, not a decorative device borrowed from elsewhere. It has a full
  static fallback (works with JS off, respects reduced-motion) and a
  scroll-linked enhancement on the home hero.
- **The one aesthetic risk:** dropping photography entirely, everywhere
  it isn't yet real. Every photo slot is a labelled placeholder rather
  than stock imagery of a smiling farmer holding grain — a common
  category default this brief explicitly ruled out. The risk is that an
  unphotographed site reads as unfinished; the bet is that a buyer
  audience reads honest placeholders as more credible than a generic stock
  shot of someone else's farm, and the placeholders double as a shot list
  the client can actually execute (see `SHOT-LIST.md`).

## Known limitations to flag at handover

- The logo is a built-from-description placeholder (see `CONTENT-GAPS.md`
  item 1) — swap in the client's real logo file before launch.
- Contact phone/WhatsApp, exact farm GPS coordinates, and several crop
  specification fields are provisional — see `CONTENT-GAPS.md` in full.
- No automated test suite; QA was manual (see the build brief's QA
  checklist, Section 12, which this build was checked against before
  handover).
