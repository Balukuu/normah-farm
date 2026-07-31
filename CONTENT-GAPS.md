# Content gaps — client homework

Every `[VERIFY]` in the build, grouped by topic. Each one renders on the
live site as either a plain safe statement (with an HTML comment marking
what's unconfirmed) or a visible `Verify` / `In progress` badge — nothing
here is a guess dressed up as fact. Work through this list with the
client, update the source file named, then re-run the build scripts in
`/scripts` where noted so the site, spreadsheet and PDFs stay in sync.

## 1. Brand & domain
- **Live domain.** Every canonical URL, Open Graph tag and JSON-LD block
  currently assumes `https://www.normahagrofarm.com/` as a placeholder.
  Confirm the real domain, then find-and-replace it across all HTML files.
  *Who: client, on the actual hosting/domain purchase.*
- **Logo file.** `assets/img/logo.svg` is a built-from-description
  recreation of the mark described in the brief (wheat ear, green circle,
  yellow band) — the real logo file was never supplied to this build.
  Replace it in place with the client's actual vector artwork (same
  filename), then regenerate `favicon.ico`, `favicon-16x16.png`,
  `favicon-32x32.png`, `apple-touch-icon.png`, `icon-192.png` and
  `icon-512.png` in `assets/img/` from the new file — this build's
  environment had no SVG rasterizer available, so those were hand-drawn
  in Pillow to approximate the placeholder mark rather than generated
  from the SVG directly. Any favicon generator (e.g. realfavicongenerator.net)
  or `Inkscape`/`ImageMagick` will do this cleanly once the real logo exists.
  *Who: client, to supply the original logo file (AI/EPS/SVG).*
- **Company registration / TIN.** Removed from the footer at the client's
  request (was previously shown as "to be added"). Re-add if the client
  later wants it published.

## 2. Farm scale (Section 2 of the build brief — known contradictions)
- **Exact acreage.** The source profile states both "one square mile"
  (~640 acres) and "1,200 acres." The site publishes the safe figure
  "1,000+ acres" everywhere (`index.html`, `farm.html`, footer weigh-slip).
  *Who: client, to confirm the actual surveyed or claimed acreage.*
- **Expansion plan.** The profile states both "+2,000 acres in 5 years"
  and "expansion to 5,000 acres." The site publishes "scaling toward
  3,000+ acres" as the safe near-term figure (`farm.html`).
  *Who: client.*

## 3. Crop specifications (drives `data/crops.json`, the crop pages, the
   comparison table, `crop-specifications.xlsx`, and both PDFs)
- **Season assignment per crop.** The source profile confirms only that
  "roughly three crops" are intercropped per season, not which three. The
  season assignment currently shown (maize/soya/sorghum in both seasons;
  rice/sesame in Season B; millet in Season A) is a provisional agronomic
  estimate, flagged `verify: true` in `data/crops.json`, not a confirmed
  fact.
- **Planting and harvest windows** — shown only as qualitative placeholders
  ("early in each season," etc.), no exact dates.
- **Moisture target (%) per crop.**
- **Variety per crop.**
- **Minimum order per crop.**
- **Packaging** — shown as "50 kg woven polypropylene bags" as an
  industry-standard placeholder, not a confirmed Normah policy; bulk/
  container options unconfirmed.

  *Who: client's agronomy/operations team. Where to fix: edit
  `data/crops.json` (each field has a `"verify": true/false` flag), then
  run `python scripts/build-xlsx.py` and `python scripts/build-pdfs.py`
  to regenerate the spreadsheet and PDFs, and update the matching HTML
  in `/crops/*.html` and `/crops/index.html` by hand (there is no build
  step that does this automatically — see README).*

## 4. Quality & certification status (`quality.html`)
- UNBS product certification — current application status.
- Phytosanitary export certificate — current status.
- Aflatoxin testing regime and threshold levels.
- GlobalG.A.P. or equivalent — confirm whether this is being pursued at all.

  *Who: client's quality assurance / compliance contact. All five are
  shown as "In progress," never implied as complete.*

## 5. Buyer-facing commercial terms (`buyers.html`)
- Preferred export port (Mombasa vs. Dar es Salaam) and forwarding agent.
- Incoterms and payment terms supported.
- Sample request cost/shipping policy.

  *Who: client's sales/logistics contact.*

## 6. Contact details (`contact.html`, site footer, `assets/php/send-quote.php.example`)
- **Phone number** — confirmed: `+256 751 365 747`, live site-wide.
- **WhatsApp number** — confirmed: `+256 751 365 747`; the floating dock
  button on the site now links to `wa.me/256751365747`.
- **Sales inbox** — confirmed: `info@normahfarms.co.ug`, live site-wide.
- **Sending address** for the PHP mail handler (`no-reply@normahagrofarm.com`)
  still needs to be a real, deliverable address once the live domain is
  confirmed (see Section 1) — left as-is since it depends on that domain.
- **Farm's exact GPS coordinates** — `contact.html`'s embedded map and
  `LocalBusiness` JSON-LD currently use an approximate Amuru District
  centroid, not a surveyed location.

  *Who: client.*

## 7. Governance & team (`about.html`)
- External auditor / tax accountant engagement — confirm current status
  before publishing as fact.
- Headcount for procurement managers, agronomists, machine operators and
  mechanics — the brief names these roles but gives no per-role count
  beyond the totals (14 planned, 10 Ugandan nationals).

  *Who: client.*

## 8. Community & growers programme (`impact.html`, `growers.html`)
- Farm open days — actual frequency/status, not just "planned."
- Mechanisation services offered to third-party smallholders — current
  scope and any pricing.

  *Who: client.*

## 9. Regional trade context (home page corridor section)
- The sentence on Kenya's maize deficit and South Sudan's import
  dependence reflects general, widely published East African trade
  patterns, not a client-supplied figure. Before publishing, attach an
  actual citation (FAO, WFP, USDA FAS, or similar) so the claim is
  sourced rather than asserted.

  *Who: whoever signs off on the site's published claims.*

---

**Not included above, and deliberately never publishing:** the UGX
financial forecast table (lender document, contains arithmetic errors),
named third-party buyers and their volumes (Unga Millers, WFP), the
"best fertile soils in Africa" claim, any use of the word "organic," and
the shares-in-trust ownership detail. These are excluded by design, not
pending — see Section 2 of the original build brief for why.
