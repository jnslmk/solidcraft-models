# Sliding AUER Eurobox cupboard assembly

Updated editable copy: **`cupboard_slide.solidcraft`**. The earlier `cupboard.solidcraft` was open in the user's unbridged SolidCraft desktop session and was left untouched; open the `cupboard_slide.solidcraft` copy to see this change.

## Current design

The [plan and cut list](../../docs/eurobox-cupboard-plan.md) and [BOM](../../docs/eurobox-cupboard-bom.csv) describe the **1124 W × 420 D × 2000 H mm** layout, with three 316 mm clear bays. Twenty-one boxes are supported on 24 × 44 mm ribs; there are no shelf boards or back panel. Crate feet extend 12 mm below the rib tops and sit in the gap between them. The ribs support a flat underside face modeled 12 mm above the feet, allowing the boxes to slide between the supports.

The assembly has **75 solids/components**: 8 uprights, 4 continuous rails, 42 ribs and 21 imported AUER crate references (**54 timber parts**). The four 44 × 44 × 1124 mm rails span the full width at front/rear, top/bottom. Each rail meets four posts in complementary half-laps: **16 joints total**, with 44 mm-wide, 22 mm-deep notches. Depth is across the front-to-back timber thickness: rails retain the outer half and posts the inner half, keeping the outer faces flush and the whole frame envelope unchanged. These are square half-laps, not dovetails. One upright is grounded; rigid groups fix the remaining components. These are fixed layout references, not animated drawers. Retaining screws, rib screws, wall connections and shims remain BOM items rather than modeled geometry; no shop screw holes or chamfers are modeled.

## Parameters and interfaces

- `bay_w`: default **316 mm**, allowed range 316–320 mm. Overall width and continuous rail length = 3 × bay_w + 4 × 44 mm. At default, rib-edge gap is 268 mm and the modeled 264 mm-wide foot base has 2 mm clearance per side.
- `slide_drop`: **12 mm**, rib-top elevation above crate feet per the approximate STEP underside face.
- `frame_d`: default 420 mm, range 410–430 mm.
- `frame_h`: default 2000 mm, range 1950–2050 mm.
- Fixed purchased sections: posts/rails 44 × 44, ribs 24 × 44 mm. `crate_z1` through `crate_z7` derive crate feet elevations from box heights, handling gaps, rib heights and slide drop.
- `lap_depth = post / 2`: derived **22 mm** for the fixed 44 mm posts; nominal joint clearance is zero, not an adjustable fit range. Fit the cuts to the actual timber.
- Crate feet/bottom elevations: **88, 460, 782, 1054, 1276, 1448, 1620 mm**. Rib tops are 12 mm above those elevations and contact the modeled flat underside faces.

Source STEP envelopes are approximately **299 × 399 mm**, with a **264 × 364 mm** lowest foot perimeter and an underside bearing face modeled at +12 mm. At 316 mm bays, the crate body has 8.5 mm nominal side clearance; the opening between ribs is 268 mm, leaving 2 mm side clearance around the foot base. This is approximate third-party geometry, not certified real-box fit or load capacity; check the actual crate before cutting or loading.

**The backless frame requires separate wall bracing against racking and tipping.** The procurement BOM includes wall-bracing connection allowances; select their rating and fixings for the actual wall/load before use. Anti-tip straps alone do not establish anti-racking stiffness. Physical sliding/contact, loaded deformation, fixing capacity and safe withdrawal remain untested.

Glue the half-laps and use suitable retaining screws; pilot drill and follow the screw maker's edge-distance and spacing rules. Joinery does not replace the required wall bracing or establish a load rating.

Units are mm, Z+ vertical, feet at z=0, front toward Y−. This is timber furniture with purchased PP crates, not a printable part; print pose/PETG defaults do not apply. Native nominal densities are spruce 0.45 and PP 0.90 g/cm³. Do not treat approximate CAD mass as weighed product mass.

## Reference rights and deliverables

AUER references originate from [Gergely DEGI's GrabCAD collection](https://grabcad.com/library/euro-containers-boxes-auer-1), via the [local STEP files](../auer_euroboxes/README.md). They are marked `[similar]`; the author warns non-main dimensions may differ from real products. Imported Y-up solids were transformed upright and parameter-positioned.

The native document embeds restricted third-party geometry and remains **Git-ignored**. Do not commit or redistribute it without suitable permission; the inspected terms cover non-commercial internal use, not unrestricted redistribution. This README and independently dimensioned plan/BOM may be tracked.

Ignored geometry export: `exports/eurobox_cupboard/cupboard_timber_slide.stl`, furniture-only, excluding purchased crates. It is an assembled geometry reference, not a recommendation to print or fabricate the rack in one piece. Half-lap inspection/checkpoint evidence is disposable under `.codex-tmp/half-lap-decc0bfc/`.

The design change replaces the segmented width members with four continuous half-lapped rails while preserving the frame envelope, 42 support ribs and 21 crate references. No structural certification is claimed.

Verification after the half-lap conversion: saved and reopened the native design with **194 clean timeline features and 75 bodies**; no floating components or joint conflicts. All 16 mating interfaces have matching **44 × 44 mm faces**, opposite normals and **22 mm lap depth**; all 16 post/rail pairs were checked for interference, with none and no unchecked pairs. Every post and continuous rail matched its independently calculated volume and bounds within **0.00001 mm / mm³**. Bay width 316–320 mm, depth 410–430 mm and height 1950–2050 mm were exercised at both endpoints and returned to defaults. All 42 ribs and 21 crate references retained their original default volumes and bounds. Isometric and assembled/exposed joint-detail views were inspected.

At default dimensions, total timber volume remains **56,945,152 mm³**, with **1124 × 420 × 2000 mm** bounds. The regenerated binary STL has 1416 triangles and matches that volume within **0.1 mm³** and those bounds. These numerical checks establish nominal geometry, not physical timber fit or structural capacity.
