# AUER Toolbox Pro bottom coupling — first-party source investigation

Checked **2026-10-29**. Scope: manufacturer technical downloads, product HTML/JavaScript and available product information, including mating wall mount and transport trolleys. No patent search, third-party CAD tracing, physical measurements or model changes were performed.

## Conclusion

**A useful first-party vector drawing exists, but no complete dimensioned bottom-coupling specification or manufacturer CAD download was found in the inspected routes.** The two officially linked handle drilling-pattern PDFs contain scaled orthographic box elevations with visible bottom lugs. Their vector coordinates support drawing-derived exterior projection dimensions. They do **not** uniquely determine the three-dimensional lug/undercut, real bearing patches, mating clearances or production tolerances.

The previous four `24 × 24 × 10 mm` pads and any `3 mm` runner bearing overlap are not validated by these sources. Conversely, dismissing the PDFs merely because the feet are not individually annotated would discard useful evidence: their projected feet are approximately **51.6 mm long × 23.5 mm short-direction extent × 10.0 mm downward**. These are **derived projection envelopes**, not a manufacturer-stated foot size or proof that an extruded solid with those dimensions is correct.

All downloaded sources and derived inspection artifacts are under `.codex-tmp/auer-coupling-dimensions/`; `source-manifest.json` records principal URLs and the catalogue/API limitations.

## 1. Actual linked engineering drawings

Both [TB 4311 F1][tb4311] and [TB 4316 F1][tb4316] link these PDFs under “Drilling pattern, optional handle.” Their German product-page equivalents link the same files.

| Official source / local file | Drawing content, page 1 | Explicit dimensions, in mm |
|---|---|---|
| [`tb_43_osg_hole.pdf`][osg] | “Lochbild Toolboxen 43”, “optionaler Griff seitlich”, drawing number `TB OSG`. Long-face and narrow-side elevations of an unspecified taller Toolbox 43, both showing bottom projections; open-box isometric view. | Side hole chain **42.25 + 32 + 151.5 + 32 + 42.25 = 300**; hole diameter **4.5**; vertical references **15.9** and **11.2**. These annotate optional-handle holes, not feet. |
| [`tb_43_ovg_hole.pdf`][ovg] | “Lochbild Toolboxen 43”, “optionaler Griff vorne”, drawing number `TB OVG`. Two long-face elevations of an unspecified shallower Toolbox 43, both showing bottom projections; open-box isometric view. **No narrow-side or underside view.** | Front hole chain **117 + 166 + 117 = 400**; hole diameter **4.5**; vertical references **18** and **13**. These annotate optional-handle holes, not feet. |

Metadata extracted from the actual downloaded PDFs:

- One A2 page each: **1683.78 × 1190.56 PDF points**, rotation 0; PDF 1.3, unencrypted.
- Creator and producer: **CATIA V5**; author `Michael_Perl`.
- PDF creation dates: **2019-03-12 10:07:32 +01:00** (OSG), **2019-03-12 11:52:39 +01:00** (OVG). Title blocks say drawing created **09.03.2017**.
- Title-block main scale **1:2**; the isometric view is separately marked **1:3**. Do not measure the isometric at 1:2.
- Extracted vector drawing-path counts: **13,617 OSG**, **10,040 OVG**; **zero embedded raster images** in either. The exterior linework is consequently available as PDF vectors, not merely photograph pixels. Many curves are represented by short vector line segments; this is not native solid CAD.
- Both title blocks list material **PP** and general tolerance reference **DIN 16742-TG3**. Current selected product tables list **ABS**. The PDFs do not label their depicted box as TB 4311 or TB 4316, do not establish a current revision match, and do not supply individually applicable coupling tolerances. That limits transferring an old generic Toolbox 43 silhouette into a current product fit claim.

The title-block text “MODIFICATIONS ONLY BY CAD” is a drawing-management note, **not** a link to downloadable CAD or a reuse licence.

## 2. Drawing-derived projected foot coordinates

These values were obtained from the **OSG page 1 vector linework**, using its two orthographic elevations. They are **not explicitly annotated by AUER**. OVG's first front elevation independently gives essentially the same projected long-direction extents and downward height (within 0.01 mm at extraction precision), supporting a shared *visible front profile* between the depicted variants, not proving identical hidden geometry.

### Calibration and datums

PDF coordinates use points, with Y increasing down the page. At 1:2:

`points_per_model_mm = 72 / 25.4 / 2 = 1.4173228346`.

The annotated dimension chains also provide independent horizontal calibration:

- Front: full exterior width approximately `788.86 − 221.93 = 566.93 pt`; divide by **400 mm**, as independently anchored by OVG's `117 + 166 + 117` front chain.
- Narrow side: full exterior width approximately `1424.91 − 999.71 = 425.20 pt`; divide by **300 mm**, explicitly anchored by OSG's `42.25 + 32 + 151.5 + 32 + 42.25` chain.
- OSG front datum: outer left body `x₀ = 221.93 pt`, lower body edge `y₀ = 466.75 pt`.
- OSG narrow-side datum: outer left body `x₀ = 999.71 pt`, lower body edge `y₀ = 466.75 pt`.
- Convert horizontal locations with `(x_pdf − x₀) / points_per_model_mm`; downward projection with `(y_pdf − y₀) / points_per_model_mm`.
- The lowest lug line is approximately **480.92 pt**: `(480.92 − 466.75) / 1.4173228346 ≈ 10.00 mm`. This is **independent drawing evidence**, not an inference from stacking-height subtraction.

`X` below is long-face left-to-right in the front drawing; `S` is narrow-side left-to-right **as displayed in that drawing**, not an asserted front-to-rear CAD axis. Mirror/orientation correspondence must be resolved before assigning a global 3D coordinate system.

| Projected feature | Drawing-derived coordinate / size, mm | What this establishes |
|---|---:|---|
| Left long-face lug silhouette below body edge | **X 20.24–71.83**, span **51.59** | Exterior projection includes a sloping inner end and drafted/rounded outer end; not a square pad. |
| Right long-face lug silhouette below body edge | **X 328.18–379.77**, span **51.59** | Mirrored long-face counterpart. |
| First narrow-side hook silhouette below body edge | **S 5.50–28.99**, span **23.49** | Hooked/stepped projection; not a full solid rectangular foot. |
| Second narrow-side hook silhouette below body edge | **S 237.00–260.49**, span **23.49** | Same approximately 23.5 mm projected extent; the narrow-axis placement is not symmetric about the box midpoint. |
| Downward projection to lowest line | **10.00** | Visible vertical projection from the drawing's lower body edge. |
| Lowest horizontal front projection, left / right | **X 22.84–56.24** / **343.77–377.16**, span approximately **33.40** each | Extent of the lowest horizontal projected line, **not a proven full-width contact area**. |
| Lowest horizontal side projection, first / second | **S 6.40–23.38** / **237.90–254.88**, span approximately **16.98** each | Lowest horizontal projected line, **not a proven rectangular bearing patch**. |

The reported hundredths retain the extraction calculation for traceability. They are **not accuracy or manufacturing tolerance claims**. PDF endpoint rounding of about 0.01 pt corresponds to about 0.007 mm per coordinate; datum selection, curve segmentation, generic product revision, draft and hidden projections dominate real reproduction uncertainty. No defensible total fit-tolerance bound can be assigned from these documents. For an exterior-only visual reproduction, round the derived dimensions rather than implying hundredth-millimetre physical accuracy.

Saved artifacts:

- `tb_43_osg_hole.pdf.paths.json`, `tb_43_ovg_hole.pdf.paths.json`: extracted vector paths and PDF coordinates.
- `derived-exterior-projections.json`: calculated projection bounds and calibration datums.
- `*.metadata.json`, `*.text.txt`: extraction metadata and text, including scales and explicit hole dimensions.
- `tb_43_osg_hole.png`, `tb_43_ovg_hole.png`: full-page renders.
- `*.orthographic.png`, `front-left-foot-detail.png`, `side-left-foot-detail.png`, `side-right-foot-detail.png`: inspection crops.

### What the elevations do not resolve

The views show a long trapezoidal projection and a short-direction **hook/step**, including a thin horizontal toe and upright/sloped webs. Two elevations constrain the exterior, but they are **projections, not sections**: near and far lugs, internal ribs and draft edges can overlap. There is no bottom plan, named lug datum, section through the hook, directly annotated toe/web thickness, exact undercut across the long direction, lock travel, clearance or complete 3D lug-to-corner correspondence.

Consequently, do not turn the two projected envelopes into four solid `51.6 × 23.5 × 10 mm` blocks, extrude the hook blindly across the long silhouette, or multiply the two lowest projected line lengths into a claimed support area. An exterior-only source-derived reference can use these projections while explicitly leaving hidden geometry unresolved; a complete mating interface needs a dimensioned section/CAD supplied by AUER or physical measurement.

## 3. Current product data and matching interfaces

Actual “Product safety and conformity information” controls were followed, rather than treating their icon as a technical drawing. In page JavaScript, `data-show="product_specification"` submits `prg_show=product_specification`; the resulting official PDF URLs are below. All five PDFs were downloaded and inspected. They reproduce product tables and safety text, **not coupling drawings**.

| Official product / generated first-party PDF | Published numbers relevant to scope | Coupling limitation |
|---|---|---|
| [TB 4311 F1][tb4311] / [PDF][pdf4311] | Exterior **400 × 300 × 120 mm**; stacking height **110 mm**; inlet **394 × 248 mm**; usable interior height **77 mm**. | No lug coordinates, toe thickness, contact footprint or mating tolerance. |
| [TB 4316 F1][tb4316] / [PDF][pdf4316] | Exterior **400 × 300 × 175 mm**; stacking height **165 mm**; inlet **394 × 248 mm**; usable interior height **132 mm**. | Same limitation. The 10 mm exterior-minus-stacking-height difference is not by itself a foot specification. |
| [TB WH 43 wall/floor mount][wall] / [PDF][pdfwall] | Exterior **400 × 300 × 30 mm**, nominal box footprint **400 × 300 mm**, weight **585 g**. Manufacturer states the same interlocking system used by the toolboxes. | Neither product HTML nor generated PDF links a mounting-hole/interface engineering drawing; no coupling-recess dimensions or hole coordinates. |
| [SK TB 43 hand trolley][hand] / [PDF][pdfhand] | Exterior **490 × 540 × 1120 mm**; load surface **440 × 323 mm**; nominal compatible footprint **400 × 300 mm**; load **160 kg**. | Overall loading-surface dimensions are not coordinates of its mating hooks. |
| [TB TR 43 FE transport trolley][transport] / [PDF][pdftransport] | Exterior **440 × 340 × 137 mm**; nominal compatible footprint **400 × 300 mm**; listed weight **795 g**. | Product description confirms coupling, but no detailed interface dimensions or engineering drawing download. |

The 160 kg hand-trolley rating must not be transferred to an independently reproduced foot or shelf support.

## 4. Manufacturer-side routes searched and limitations

- Inspected current English TB 4311/TB 4316 item HTML, the German TB 4311 page, Pro family page, Toolbox overview, accessories index, wall/floor mount English/German pages, transport-trolley family/detail pages, and hand-trolley detail. Followed actual linked PDF and related-product controls. No `.step`, `.stp`, `.iges`, `.igs`, `.dxf` or native CAD link was exposed in the inspected product/download controls.
- Saved and inspected the site's actual `product_details.js`, `functions.js`, `main.js`, and shared functions. Product AJAX methods concern displayed product detail/variants, configurator components, colours and carts; no geometry/CAD endpoint was found in those inspected scripts. A read-only `ajaxGetTooltipProductDetails` request for product IDs **50127** and **50137** returned `{"error":true}`; this did **not** expose extra dimensions, and is not evidence that every possible manufacturer endpoint was exhausted. Responses are preserved locally.
- Followed [Service][service] → [Browse catalogue][catalogue], including the hidden `prg_txt=215` control. The actual destination was the AUER-branded [2023 English catalogue on Yumpu][yumpu] (German control redirected to document **67265597**). Direct retrieval returned HTTP **202 with an empty body**; a managed browser returned “ERROR: The request could not be satisfied.” Reader-mode retrieval exposed a **244-page** viewer shell/cover but not searchable technical pages or an accessible PDF download. Therefore this investigation **does not claim to have inspected the complete catalogue or excluded a drawing inside it**. Manufacturer FAQ still describes an option to download a catalogue PDF, but the current followed route was the Yumpu redirect, not a direct PDF.
- Manufacturer-scoped web searches for exact TB 4311, Toolbox Pro CAD/STEP/technical drawings, `/pdf/drawings/`, and TB WH 43 matching-interface drawings did not produce an additional first-party dimensional source. Search results are not proof that unpublished CAD does not exist.

**Exact remaining prerequisite for a complete, fit-accurate interface:** current-revision AUER bottom plan plus lug sections/clearances (or manufacturer CAD with suitable permission), or measurements of actual TB 4311/TB 4316 undersides. For simple shelf bearing, the actual lowest contact patches and their load behaviour still require validation; the projected lines above do not establish them.

## 5. Licensing and use

No manufacturer CAD file or CAD-specific reuse licence was found or downloaded. The public PDFs are AUER-authored engineering references linked from product pages, but public availability is **not** an open-source geometry/artwork licence. Keep downloaded PDFs/images as temporary research references unless redistribution permission is established; cite their origin when describing any drawing-derived model. Current AUER pages describe the bayonet system as **patented**; this note makes no patent-status, manufacturing-rights or freedom-to-operate conclusion. No unlicensed third-party CAD was used.

[tb4311]: https://www.auer-packaging.com/en/Tool-boxes-Pro/TB-4311-F1.html
[tb4316]: https://www.auer-packaging.com/en/Tool-boxes-Pro/TB-4316-F1.html
[osg]: https://www.auer-packaging.com/pdf/drawings/tb_43_osg_hole.pdf
[ovg]: https://www.auer-packaging.com/pdf/drawings/tb_43_ovg_hole.pdf
[wall]: https://www.auer-packaging.com/en/Toolbox-wall-mount/TB-WH-43.html
[hand]: https://www.auer-packaging.com/en/Hand-trolley-Tool-boxes/SK-TB-43.html
[transport]: https://www.auer-packaging.com/en/Tool-box-transport-trolleys/TB-TR-43-FE.html
[pdf4311]: https://www.auer-packaging.com/en/Product-safety-and-conformity-information/TB-4311-F1.pdf
[pdf4316]: https://www.auer-packaging.com/en/Product-safety-and-conformity-information/TB-4316-F1.pdf
[pdfwall]: https://www.auer-packaging.com/en/Product-safety-and-conformity-information/TB-WH-43.pdf
[pdfhand]: https://www.auer-packaging.com/en/Product-safety-and-conformity-information/SK-TB-43.pdf
[pdftransport]: https://www.auer-packaging.com/en/Product-safety-and-conformity-information/TB-TR-43-FE.pdf
[service]: https://www.auer-packaging.com/en/Service.html
[catalogue]: https://www.auer-packaging.com/en/Browse-catalogue.html
[yumpu]: https://www.yumpu.com/en/document/read/67269159/auer-packaging-product-catalogue-2023-en-wo
