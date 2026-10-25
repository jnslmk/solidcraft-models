# Sliding AUER Eurobox cupboard assembly

Updated editable copy: **`cupboard_slide.solidcraft`**. The earlier `cupboard.solidcraft` was open in the user's unbridged SolidCraft desktop session and was left untouched; open the `cupboard_slide.solidcraft` copy to see this change.

## Current design

The [plan and cut list](../../docs/eurobox-cupboard-plan.md) and [BOM](../../docs/eurobox-cupboard-bom.csv) describe the **1124 W × 420 D × 2000 H mm** layout, with three 316 mm clear bays. Twenty-one boxes are supported on 24 × 44 mm ribs; there are no shelf boards or back panel. Crate feet extend 12 mm below the rib tops and sit in the gap between them. The ribs support a flat underside face modeled 12 mm above the feet, allowing the boxes to slide between the supports.

The assembly has **83 solids/components**: 8 uprights, 12 crossbars, 42 ribs and 21 imported AUER crate references. One upright is grounded; rigid groups fix the remaining components. These are fixed layout references, not animated drawers. Screws, brackets, wall connections and shims remain BOM items rather than modeled geometry. Timber solids represent nominal stock envelopes, without shop chamfers or holes.

## Parameters and interfaces

- `bay_w`: default **316 mm**, tested 316–320 mm. Overall width = 3 × bay_w + 4 × 44 mm. At default, rib-edge gap is 268 mm and the modeled 264 mm-wide foot base has 2 mm clearance per side.
- `slide_drop`: **12 mm**, rib-top elevation above crate feet per the approximate STEP underside face.
- `frame_d`: default 420 mm, range 410–430 mm.
- `frame_h`: default 2000 mm, range 1950–2050 mm.
- Fixed purchased sections: posts 44 × 44, ribs 24 × 44 mm. `crate_z1` through `crate_z7` derive crate feet elevations from box heights, handling gaps, rib heights and slide drop.
- Crate feet/bottom elevations: **88, 460, 782, 1054, 1276, 1448, 1620 mm**. Rib tops are 12 mm above those elevations and contact the modeled flat underside faces.

Source STEP envelopes are approximately **299 × 399 mm**, with a **264 × 364 mm** lowest foot perimeter and an underside bearing face modeled at +12 mm. At 316 mm bays, the crate body has 8.5 mm nominal side clearance; the opening between ribs is 268 mm, leaving 2 mm side clearance around the foot base. This is approximate third-party geometry, not certified real-box fit or load capacity; check the actual crate before cutting or loading.

**The backless frame requires separate wall bracing against racking and tipping.** The procurement BOM includes wall-bracing connection allowances; select their rating and fixings for the actual wall/load before use. Anti-tip straps alone do not establish anti-racking stiffness. Physical sliding/contact, loaded deformation, fixing capacity and safe withdrawal remain untested.

Units are mm, Z+ vertical, feet at z=0, front toward Y−. This is timber furniture with purchased PP crates, not a printable part; print pose/PETG defaults do not apply. Native nominal densities are spruce 0.45 and PP 0.90 g/cm³. Do not treat approximate CAD mass as weighed product mass.

## Reference rights and deliverables

AUER references originate from [Gergely DEGI's GrabCAD collection](https://grabcad.com/library/euro-containers-boxes-auer-1), via the [local STEP files](../auer_euroboxes/README.md). They are marked `[similar]`; the author warns non-main dimensions may differ from real products. Imported Y-up solids were transformed upright and parameter-positioned.

The native document embeds restricted third-party geometry and remains **Git-ignored**. Do not commit or redistribute it without suitable permission; the inspected terms cover non-commercial internal use, not unrestricted redistribution. This README and independently dimensioned plan/BOM may be tracked.

Ignored geometry export: `exports/eurobox_cupboard/cupboard_timber_slide.stl`, furniture-only, excluding purchased crates. It is an assembled geometry reference, not a recommendation to print or fabricate the rack in one piece. Inspection/checkpoint evidence is disposable under `.codex-tmp/slide-between-ribs-20261025/`.

Verification on the updated headless copy covered all 21 crates and 42 rails for interference, support elevations and 20 mm vertical clearances, the tested bay-width endpoints and return to default, a clean 178-feature timeline, and a timber-only STL export. No structural certification is claimed.
