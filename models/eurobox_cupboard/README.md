# Sliding AUER Eurobox cupboard assembly

Editable source: **`cupboard_slide.solidcraft`**, now containing independently constructed native Eurobox geometry rather than imported GrabCAD solids. The older `cupboard.solidcraft` and backups remain private, ignored legacy files; they are not the current design.

## Current design

The [plan and cut list](../../docs/eurobox-cupboard-plan.md) and [BOM](../../docs/eurobox-cupboard-bom.csv) describe the **1124 W × 420 D × 2000 H mm** layout, with three 316 mm clear bays. Thirty boxes are supported on 24 × 44 mm ribs; there are no shelf boards or back panel. Crate feet extend 12 mm below the rib tops and sit in the gap between them. The ribs support a flat underside face modeled 12 mm above the feet, allowing the boxes to slide between the supports.

Only **75, 120, 170 and 220 mm** crate heights are selected. Each column uses **220, 170, 170, 170, 170, 120, 120, 75, 75, 75 mm** bottom to top, for an assumed total mix of **3 × 220, 12 × 170, 6 × 120 and 9 × 75 mm** crates. The highest crate ends at z=1921, leaving **35 mm clearance** below the top rail underside at z=1956. The frame envelope, eight uprights and four continuous rails are unchanged.

The ten-row assembly has **102 solids/components**: 8 uprights, 4 continuous rails, 60 ribs and 30 native crate approximations (**72 timber parts**). The four 44 × 44 × 1124 mm rails span the full width at front/rear, top/bottom. Each rail meets four posts in complementary half-laps: **16 joints total**, with 44 mm-wide, 22 mm-deep notches. Depth is across the front-to-back timber thickness: rails retain the outer half and posts the inner half, keeping the outer faces flush and the whole frame envelope unchanged. These are square half-laps, not dovetails. One upright is grounded; rigid groups fix the remaining components. These are fixed layout models, not animated drawers. Retaining screws, rib screws, wall connections and shims remain BOM items rather than modeled geometry; no shop screw holes or chamfers are modeled.

## Parameters and interfaces

- `bay_w`: default **316 mm**, allowed range 316–320 mm. Overall width and continuous rail length = 3 × bay_w + 4 × 44 mm. At default, rib-edge gap is 268 mm and the assumed 260 mm-wide foot base has 4 mm clearance per side.
- `slide_drop`: **12 mm**, assumed rib-top elevation above crate feet, shared with the native crate construction; not a product measurement.
- `frame_d`: default 420 mm, range 410–430 mm.
- `frame_h`: default 2000 mm, range **1990–2050 mm**. At 1990 mm, the top rail underside is z=1946, leaving 25 mm above the highest crate.
- Fixed purchased sections: posts/rails 44 × 44, ribs 24 × 44 mm. `crate_z1` through `crate_z10` derive crate feet elevations from box heights, handling gaps, rib heights and slide drop.
- `lap_depth = post / 2`: derived **22 mm** for the fixed 44 mm posts; nominal joint clearance is zero, not an adjustable fit range. Fit the cuts to the actual timber.
- Crate feet/bottom elevations: **88, 360, 582, 804, 1026, 1248, 1420, 1592, 1719, 1846 mm**. Rib tops are 12 mm above those elevations and contact the modeled flat underside faces; rib bottoms are 32 mm below the feet. Each non-top crate has 20 mm overhead clearance to the next rib.

Native crate envelopes are **300 × 400 mm**, with an independently assumed **260 × 360 mm** foot perimeter and a bearing plane at +12 mm. At 316 mm bays, the envelope has 8 mm side clearance; the 268 mm opening between ribs leaves 4 mm side clearance around the feet. The default 280 mm-wide bearing underside overlaps each rib by 6 mm, before local rib projections. `crate_wall` is 5 mm, tested over 3–5 mm; body width is `270 mm + 2*crate_wall`. At the combined widest bay/thinnest wall limits, bearing overlap remains 2 mm. These are assumed CAD interfaces, not certified real-box fit or load capacity. The [crate README](../auer_euroboxes/README.md) distinguishes catalogue dimensions from original simplified details, including the deliberate internal-height mismatch.

**The backless frame requires separate wall bracing against racking and tipping.** The procurement BOM includes wall-bracing connection allowances; select their rating and fixings for the actual wall/load before use. Anti-tip straps alone do not establish anti-racking stiffness. Physical sliding/contact, loaded deformation, fixing capacity and safe withdrawal remain untested.

Glue the half-laps and use suitable retaining screws; pilot drill and follow the screw maker's edge-distance and spacing rules. Joinery does not replace the required wall bracing or establish a load rating.

Units are mm, Z+ vertical, feet at z=0, front toward Y−. This is timber furniture with purchased PP crates, not a printable part; print pose/PETG defaults do not apply. Native nominal densities are spruce 0.45 and PP 0.90 g/cm³. Do not treat approximate CAD mass as weighed product mass.

All support ribs, including the upper three levels, use the frame's wood color (`#cda574`).

## Reference rights and deliverables

The [independent crate model](../auer_euroboxes/README.md) uses published nominal AUER envelope/interior-footprint dimensions plus explicit assumptions for feet, bearing surfaces, walls, rim, ribs and blind grip recesses. It is not traced or converted from the third-party models. The saved assembly contains only native box, move and body-transfer features; all six imported base features, their dependent placements/transfers and the 30 old crate components were removed.

The current `cupboard_slide.solidcraft` no longer embeds downloaded CAD and is no longer Git-ignored. This does not establish blanket product-design/trademark clearance. Keep the original `cupboard.solidcraft`, restricted STEP/PDF downloads, backups and temporary baselines private and ignored.

Ignored exports: `exports/eurobox_cupboard/cupboard_timber_slide.stl` excludes crates; `exports/eurobox_cupboard/cupboard_slide.stl` includes the native crates. These are assembled geometry references, not recommendations to print or fabricate the rack in one piece. Half-lap inspection/checkpoint evidence is disposable under `.codex-tmp/half-lap-decc0bfc/`.

The design uses four continuous half-lapped rails while preserving the frame envelope, with 60 support ribs and 30 crate references. The ten-row revision changes crate references, rib quantities and support elevations, not half-lap geometry. Procurement requires ten main-frame stock lengths and twelve rib-stock lengths, costing **€97.50 + €54.00 = €151.50** at the previously observed timber prices; hardware remains unpriced. Rib screws require 240, with a purchase allowance of 250. No structural certification is claimed.

Historical checks after the earlier half-lap conversion: all 16 mating interfaces had matching **44 × 44 mm faces**, opposite normals and **22 mm lap depth**; all 16 post/rail pairs were checked for interference, with none and no unchecked pairs. Every post and continuous rail matched its independently calculated volume and bounds within **0.00001 mm / mm³**. Isometric and assembled/exposed joint-detail views were inspected. These checks concern the unchanged half-lap geometry, not verification of the selected-height revision.

Ten-row revision verification: saved and reopened **248 clean timeline features and 102 bodies**. All 30 crate heights, feet elevations and center positions, and all 60 rib elevations and volumes matched independent expectations within **0.00001 mm / 0.01 mm³**. Same-height crate volumes agree within **0.01 mm³**. Bay width 316–320 mm, depth 410–430 mm and height 1990–2050 mm were exercised at endpoints and restored to defaults. Front and isometric views were inspected.

The regenerated timber-only STL has **1632 triangles**, verified volume **64,928,512 mm³** within **0.1 mm³**, and bounds **1124 × 420 × 2000 mm**, matching the saved timber geometry. Evidence is under `.codex-tmp/crate-mix-20261025/`. Nominal geometry does not establish physical timber fit or structural capacity; real-box contact and loaded sliding remain untested.

Native-crate replacement verification: **436 clean timeline features and 102 bodies**, saved and reopened with matching volumes for every body. All 72 timber bodies retained their preceding volumes and bounds; timber geometry and elevations were not changed. The read-only [crate check](../auer_euroboxes/check.py) passed all six standalone crate heights, foot/wall endpoints, and the cupboard's frame/wall endpoints, checking all 30 crate bounds/volumes/centers and all 60 rib elevations/volumes. Thirty crate-plus-two-rib interference checks found no overlaps or unchecked pairs. The actual modeled underside and rib top planes were inspected at z=100 mm on the first row, with opposite normals; isometric and front assembly views were inspected. Physical fit remains untested.

Current mesh checks: six standalone crate STLs are closed connected manifold shells with analytic volumes within 0.1 mm³. Assembly and timber-only STL volumes/bounds were compared with the saved geometry. Native source provenance was checked in the saved container: no imported base/mesh feature remains. Disposable evidence is under `.codex-tmp/native-crates-20261025/`. No creation generator is maintained; native timelines are authoritative.
