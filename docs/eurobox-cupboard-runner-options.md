# Eurobox cupboard: smaller timber runner options

Researched 2026-10-25. Research only; no CAD or procurement changes. Prices are observed listing/index values, not quotations or confirmation of local availability.

## Geometry constraint

The [current cupboard plan](eurobox-cupboard-plan.md#envelope-and-layout) uses runners **24 mm projecting into the bay × 44 mm vertically × 420 mm long**, in a 316 mm clear bay. Its approximate crate reference has a 264 mm-wide foot base, a roughly 299 mm-wide body, and an underside bearing face 12 mm above the feet. The plan explicitly requires physical confirmation and establishes no load capacity.

Keep projection and vertical height separate when comparing stock:

- **24 mm projection** leaves a 268 mm opening, nominally 2 mm clearance per side around centered 264 mm feet.
- **25 mm projection** leaves 266 mm, only 1 mm nominal clearance per side. It is close, but not an exact replacement; tolerances, skew while sliding and actual mouldings matter.
- **20 mm projection** leaves 276 mm. It also removes 4 mm of inward bearing reach per side compared with the current runner. Narrower rails do not preserve the existing bearing automatically, even if foot clearance increases.
- **29 mm projection** leaves 258 mm, smaller than the modeled foot base: the unmodified beech stock below cannot simply be turned flat that way.

These opening/clearance figures are arithmetic from the plan, not measured product fit. To preserve the current geometry exactly, finish stock to **24 mm projection**. Reducing vertical height is a separate change requiring a suitable connection and load assessment; the current two-screws-per-end allowance is not validated for a 20 mm-high runner.

## Three useful retail candidates

Dimensions in the orientation column mean **projection × vertical height**, not the retailer's dimension order.

| Candidate | Retail specification and observed price | Potential runner orientation | Evidence and limitations |
|---|---|---|---|
| [HORNBACH Konsta Rechteckleiste, article 5485736](https://www.hornbach.de/p/konsta-rechteckleiste-kiefer-fichte-roh-2000-x-25-x-20-mm/5485736/) | 2000 × 25 × 20 mm; pine/spruce, knot-free, bare surface, indoor use. **€6.95 per piece** including VAT, shipping potentially extra. | **25 × 20 mm** unmodified; finish the 25 mm dimension to **24 mm** for the existing projection. Four 420 mm runners fit within a 2 m piece with ordinary cutting allowances. | **Fetched official product page.** Page lists width 25 mm, thickness 20 mm, length 2000 mm, materials Kiefer/Fichte and quality Astfrei. This is the closest ready-section match found, but 25 mm projection reduces foot clearance as above. Not structurally graded/rated in the fetched specification. |
| [BAUHAUS Rechteckleiste, article 20784807](https://www.bauhaus.info/rechteckleisten/rechteckleiste/p/20784807) | **100 cm × 29 mm × 20 mm, beech; €6.00 per piece / €6.00 per metre**, VAT included and online shipping extra according to indexed text. | **20 × 29 mm** unmodified, sacrificing 4 mm bearing reach; alternatively finish the 29 mm dimension to **24 mm** and use **24 × 20 mm**. Two 420 mm runners fit within a 1 m piece with ordinary cutting allowances. | **Indexed official URL only.** Exact-URL/site searches returned the product number, dimensions, wood species, price displayed as “6,-” and unit price “1 m = 6,- €”. Direct fetch returned BAUHAUS's connection security check, not the product specification. Price/spec are therefore index corroboration, not a successful live-page fetch. Surface treatment, grading and stock availability were not verified. |
| [HORNBACH Neuhofer Rechteckleiste, article 8867588](https://www.hornbach.de/p/rechteckleiste-buche-roh-950-x-29-x-20-mm/8867588/) | 950 × 29 × 20 mm; beech, knot-free, bare surface, indoor use. **€5.90 per piece / €6.21 per metre**, VAT included, shipping potentially extra. | **20 × 29 mm** unmodified, with the same reduced-bearing warning as BAUHAUS; or finish to **24 × 20 mm**. Two 420 mm runners fit within a 950 mm piece with ordinary cutting allowances. | **Fetched official product page.** Exact section, species, surface and price confirmed. Page explicitly said **not orderable online**; any collection availability requires checking the user's store. No structural grade or runner load rating was given. |

The HORNBACH page's general furniture-building marketing is not a runner load rating. Neither source supplies a permissible loaded-crate weight, deflection limit or validated fixing design. No load rating or user-local availability is claimed here. Inspect actual straightness, section dimensions and defects before selecting timber; verify real crate contact and the smaller-section fastening arrangement before batch cutting or loading.

## Source/evidence trail

- [Current shelf geometry and safety assumptions](eurobox-cupboard-plan.md), especially “Envelope and layout”, “Cut list and stock” and “Connections and safety”.
- [HORNBACH 5485736 official listing](https://www.hornbach.de/p/konsta-rechteckleiste-kiefer-fichte-roh-2000-x-25-x-20-mm/5485736/): fetched successfully; price and specification above appeared in the page body. Its automatically selected store was not treated as the user's location.
- [HORNBACH 8867588 official listing](https://www.hornbach.de/p/rechteckleiste-buche-roh-950-x-29-x-20-mm/8867588/): fetched successfully after discovery in the [official Neuhofer category](https://www.hornbach.de/c/holz-fenster-tueren/S3985/f/Marke=Neuhofer). Product page confirmed €5.90, 950 × 29 × 20 mm, beech, knot-free and bare surface, and “Nicht online bestellbar”. Store-specific stock was not treated as user-local availability.
- [BAUHAUS 20784807 official listing](https://www.bauhaus.info/rechteckleisten/rechteckleiste/p/20784807): direct fetch blocked by “Sicherheitsprüfung ihrer Verbindung”. Indexed official-page snippets were cross-checked with searches `site:bauhaus.info "100 cm x 29 mm x 20 mm"`, `https://www.bauhaus.info/rechteckleisten/rechteckleiste/p/20784807 Preis EUR Buche`, and `site:bauhaus.info/rechteckleisten "29 mm x 20 mm" "€"`. Respectively these exposed the dimensions/species, article/price, and matching unit price.
