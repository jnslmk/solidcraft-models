# Eurobox cupboard — small-runner variant

Separate twelve-level variant; the original ten-level cupboard and its plan/BOM remain unchanged. Editable native design: `models/eurobox_cupboard/cupboard_small_runners.solidcraft`. Timber-only export: `exports/eurobox_cupboard/cupboard_timber_small_runners.stl`.

## Layout and contact

Default envelope: **1124 W × 420 D × 2000 H mm**, three **316 mm clear bays**, eight 44 × 44 mm uprights and four continuous 44 × 44 mm rails. No shelves or back panel. Replace the original 24 × 44 mm ribs with **72 pine runners, 20 mm across the bay × 20 mm vertical × 420 mm long**: two per level, twelve levels per bay. There are **84 timber parts and 36 crate references, 120 bodies in total** in the intended assembly.

Each bay holds, bottom first, **220, 170, 170, 170, 170, 120, 120, 120, 75, 75, 75, 75 mm** crates. Total mix: **3 × 220, 12 × 170, 9 × 120 and 12 × 75 mm**. Current crate references are native simplified Euroboxes, not imported STEP solids. Approximate reference dimensions and contact assumptions do not establish real AUER moulding fit.

At default bay width, runner-edge gap is **316 − 2 × 20 = 276 mm**. Against the assumed **264 mm foot width**, that gives **6 mm per side**, versus the original 2 mm. The native simplified crate's 5 mm wall leaves a nominal **280 mm-wide × 380 mm-deep underside bearing floor**: only **2 mm overlap per side** over the runners at the default bay, versus 6 mm over the original 24 mm-wide ribs. At 312 mm bay width, bearing overlap and foot clearance are each 4 mm per side. A 320 mm bay would give zero bearing overlap and is excluded. Actual bearing geometry and remaining overlap must be checked on real crates; greater foot clearance is not proof of adequate support. Runner tops are nominally **12 mm above crate feet** (`slide_drop`) to contact the assumed underside bearing face.

## Elevations

All dimensions are mm, Z+ upward, feet at z=0, front toward Y−. `head_gap = 20` is clearance from each non-top crate to the underside of the next runner. Runner bottom = crate feet − 8; runner top = crate feet + 12.

| Level, bottom first | Crate height | Crate feet | Runner bottom | Runner top | Clearance to next runner / top rail |
|---|---:|---:|---:|---:|---:|
| 1 | 220 | 64 | 56 | 76 | 20 |
| 2 | 170 | 312 | 304 | 324 | 20 |
| 3 | 170 | 510 | 502 | 522 | 20 |
| 4 | 170 | 708 | 700 | 720 | 20 |
| 5 | 170 | 906 | 898 | 918 | 20 |
| 6 | 120 | 1104 | 1096 | 1116 | 20 |
| 7 | 120 | 1252 | 1244 | 1264 | 20 |
| 8 | 120 | 1400 | 1392 | 1412 | 20 |
| 9 | 75 | 1548 | 1540 | 1560 | 20 |
| 10 | 75 | 1651 | 1643 | 1663 | 20 |
| 11 | 75 | 1754 | 1746 | 1766 | 20 |
| 12 | 75 | 1857 | 1849 | 1869 | 24 |

Bottom rails occupy z=0–44 and top rails z=1956–2000. Highest crate top is **1932**, leaving **24 mm** below the top rails at default height.

## Parameters

| Parameter | Default | Intended range / relationship |
|---|---:|---|
| `bay_w` | 316 | 312–316 mm; overall width and rail length = 3 × bay_w + 4 × 44; 320 mm excluded because nominal bearing overlap is zero |
| `frame_d` | 420 | 410–430 mm; runner length follows depth |
| `frame_h` | 2000 | 2000–2050 mm; uprights follow height |
| Post / rail section | 44 × 44 | Fixed purchased section |
| Runner section | 20 × 20 | Fixed purchased section, not a fit parameter |
| `slide_drop` | 12 | Nominal underside bearing offset above feet |
| `head_gap` | 20 | Nominal clearance below the next runner |
| `lap_depth` | 22 | Half the fixed 44 mm post thickness |

Feet elevations recur by adding the previous crate height + head_gap + runner height − slide_drop, i.e. previous height + 28 mm. The base feet elevation remains 64 mm. With this layout, **1996 mm** is the mathematical minimum frame height for 20 mm top clearance; the intended adjustable range starts at 2000 mm.

## Cut list and timber procurement

| Part | Quantity | Finished size, mm |
|---|---:|---|
| Uprights | 8 | 44 × 44 × 2000 |
| Continuous rails | 4 | 44 × 44 × 1124 |
| Runners | 72 | 20 × 20 × 420 |

Main frame: **ten 2500 mm lengths of 44 × 44 mm spruce**; eight give one upright each, two give two rails each. Runner stock: **eighteen 2000 mm lengths of KONSTA raw pine 20 × 20 mm**, Hornbach article **5485724**; cut **four 420 mm runners per length**. These default cut patterns allow 3 mm saw kerf and 20 mm end trimming; no damaged-stock allowance is included. At parameter extremes, the same counts fit (two 1124 mm rails per 2500 mm length and four 430 mm runners per 2000 mm length).

The [variant BOM](eurobox-cupboard-small-runners-bom.csv) prices timber only: main frame **€97.50**, runners **18 × €5.35 = €96.30**, total **€193.80**. This is **€42.30 above** the original €151.50 timber subtotal. Prices are planning inputs, not a supplier quotation; delivery, cutting, finish, hardware, wall fixings and crates are excluded.

## Connections and safety

The main frame retains **16 complementary square half-laps**, 44 mm wide × 22 mm deep, across the front-to-back thickness: rails retain the outer half and posts the inner half. Fit nominal zero-clearance cuts to actual timber; glue and select suitable retaining screws with pilot drilling and manufacturer-approved edge distances and spacing. The variant does not redesign or certify these joints.

**Runner fastening needs a connection design for 20 × 20 mm stock.** Do not carry over the old two-screws-per-end / 240-screw rib allowance as approved hardware. Select fastener type, diameter, length, number, pilot diameter and spacing for the actual pine, end/edge distances and required load; avoid splitting and opposing screw collisions at shared posts. Hardware quantities and prices remain unknown until this is resolved.

**The backless cupboard requires rated wall bracing against racking and tipping; it is not an unbraced freestanding rack.** Anti-tip straps alone do not establish anti-racking stiffness. Select connections and substrate-specific anchors for the loaded frame and actual wall. Level and support all eight feet.

Before batch cutting or loading, physically confirm the actual crate foot width, underside bearing geometry, remaining runner overlap, sliding/withdrawal clearances and loaded contact; assess timber bending, fixing capacity and wall restraint. No load rating, fastening certification, extension stops or safe cantilevered-box loading is established. Physical verification remains outstanding.

## CAD verification

Saved and reopened the variant with **472 clean timeline features, 120 bodies and no sketches**. All 36 crate heights, centers and feet elevations, and all 72 runner elevations and volumes matched independent expectations within **0.00001 mm / 0.01 mm³**. All eight posts and four continuous rails retained baseline volumes and bounds. Bay width 312–316 mm, depth 410–430 mm and height 2000–2050 mm were exercised at endpoints and returned to defaults.

Six representative crate/two-runner sets spanning the selected heights, modified eighth level and highest level were checked for solid interference: no intersections and no unchecked pairs. This excludes penetration, not inadequate bearing or real loaded-fit issues. Nominal bearing overlap is derived from the native 280 mm underside floor and remains only **2 mm per side** at default. Front and isometric views were inspected.

The regenerated timber STL has **1776 triangles**, volume **50,413,312 mm³** within **0.1 mm³**, and **1124 × 420 × 2000 mm** bounds, matching the saved timber geometry. Evidence and baseline are under `.codex-tmp/cupboard-small-runners-20261025/`. These checks do not validate physical contact, fastening capacity or a safe working load.

All 72 runners use the frame's wood appearance (`#cda574`), including the copied upper levels; the saved model's isometric view was inspected after applying this appearance.
