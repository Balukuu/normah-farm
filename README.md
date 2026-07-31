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
robots.txt, sitemap.xml, .htaccess
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

Two ways to wire it up:

1. **A hosted form service** (Formspree or similar). Set
   `window.NORMAH_FORM_ENDPOINT` to the service's endpoint URL in a small
   inline `<script>` placed before `quote-form.js` loads on each page
   that has a form (`buyers.html`, `contact.html`).

2. **A PHP mail handler on cPanel/Apache shared hosting** (the default
   this build assumes, since that's the stated hosting target). Copy
   `assets/php/send-quote.php.example` to `assets/php/send-quote.php`,
   fill in `RECIPIENT_EMAIL` and `SITE_ORIGIN`, and confirm `mail()` is
   enabled on the host. This is the endpoint `quote-form.js` posts to by
   default if you set nothing else.

Test a real submission on the live host before considering the forms
done — `mail()` behaviour varies by hosting provider.

## Deployment (cPanel / Apache shared hosting)

1. Upload the entire contents of this folder to the account's web root
   (commonly `public_html/`).
2. Confirm `.htaccess` uploaded (some FTP clients hide dotfiles by
   default — check explicitly). It handles clean URLs (`/crops/maize`
   works alongside `/crops/maize.html`), cache headers, and gzip.
3. Confirm `mod_rewrite`, `mod_expires`, `mod_headers` and `mod_deflate`
   are enabled — standard on virtually all cPanel hosts, but worth a
   quick check if clean URLs don't resolve.
4. Update every `https://www.normahagrofarm.com/` occurrence (canonical
   tags, Open Graph URLs, JSON-LD, `sitemap.xml`, `robots.txt`) to the
   real live domain if it differs from this placeholder.
5. Set up `assets/php/send-quote.php` per the section above, or point
   `NORMAH_FORM_ENDPOINT` at a hosted form service.
6. Submit `sitemap.xml` to Google Search Console once the domain is live.

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
