# Shot list

Every photo placeholder in the build, in one list. The site currently
renders each of these as a labelled `--mist` placeholder block (never a
stock photo) so nothing is misrepresented before real photography exists.
Each placeholder carries a `PHOTO REQUIRED` caption in the HTML that
matches the description below — search any file for that string to find
the exact spot.

Once a photograph is ready: save it as WebP, add `width`/`height`
attributes matching the image's real dimensions, keep `loading="lazy"` on
anything below the fold, write real (non-placeholder) `alt` text, and
delete the `.photo-slot` wrapper in favour of an `<img>` tag. See the
README's "Editing content" section for the exact markup pattern.

Shoot in both Season A (Mar–Jun) and Season B (Jul–Dec) wherever a season
isn't specified, so the site has real options for both halves of the year
rather than depending on a single visit.

| # | Page | Slot | What to shoot | When | Orientation |
|---|------|------|----------------|------|--------------|
| 1 | Home | Farm strip (mechanisation) | Combine harvester working a field | Season B harvest | Wide (16:9) |
| 2 | Home | For growers preview | Training or demonstration farming session | Any session date | Standard (4:3) |
| 3 | The farm | Location & climate | Wide establishing shot of Amuru fields | Either season, good light | Wide (16:9) |
| 4 | The farm | Mechanisation | Tractor pulling an implement (disc/planter/sprayer) mid-operation | Either season, active field work | Wide (16:9) |
| 5 | The farm | Water | Borehole and irrigation water tower | Any | Standard (4:3) |
| 6 | The farm | Storage | Warehouse interior, grain bagged and stacked | After a harvest, warehouse in use | Standard (4:3) |
| 7 | The farm | Housing & staff | Staff housing or team at work on the farm | Any, with people present (get consent) | Standard (4:3) |
| 8 | Maize (crop page) | Grown at Normah | Maize field | Season B, standing crop | Wide (16:9) |
| 9 | Soya beans (crop page) | Grown at Normah | Soya bean field | Either season, standing crop | Wide (16:9) |
| 10 | Rice (crop page) | Grown at Normah | Rice field, ideally showing irrigation | Season B | Wide (16:9) |
| 11 | Sesame (crop page) | Grown at Normah | Sesame (simsim) field | Season B | Wide (16:9) |
| 12 | Sorghum (crop page) | Grown at Normah | Sorghum field | Either season, standing crop | Wide (16:9) |
| 13 | Millet (crop page) | Grown at Normah | Millet field | Season A | Wide (16:9) |
| 14 | For growers | Mechanisation services | Normah tractor/implement working a neighbouring smallholder's plot | Any service visit | Standard (4:3) |
| 15 | For growers | Training & demonstration | Training or demonstration farming session, ideally with attendees visible | Any session date | Standard (4:3) |
| 16 | Impact | Soil-first agronomy | A rotation or cover-cropped field showing the practice, not just a green field | Either season | Wide (16:9) |
| 17 | Impact | Local employment | Farm staff at work (equipment operation, fieldwork, or warehouse) | Any, with consent | Standard (4:3) |
| 18 | Impact | Community engagement | A farm open day or community training session, people visible | Harvest-time open day if one is run | Standard (4:3) |
| 19 | Field notes — "Season B planting" | Post body | Planting operation in progress | Season B, planting window | Wide (16:9) |
| 20 | Field notes — "Inside the warehouse" | Post body | Warehouse interior, grain in bags | Post-harvest | Wide (16:9) |

**Not yet on the shot list because the infrastructure doesn't exist yet:**
the planned silo, weighbridge, walk-in bagging area, washing/grading area
and district pack houses (Masindi, Lira, Gulu, Amuru) have no photo slot
on the site — add one only once each is actually built, so the site never
implies a planned asset already exists.

**Dropped, 2026-08-29:** the About/Directors portraits (Hassan Mortada,
James Odera) and the "Farmer training day" post-body photo no longer have
a placeholder in the HTML — those sections now run text-only by request,
so there's nothing left to shoot for them.
