# Native Eurobox layout model

**`eurobox.solidcraft`** is the editable native source: one connected solid with 20 named primitive features, no imported BREP or mesh. It is an independently constructed Euro-format layout approximation, **not a tracing, conversion or exact reconstruction of the GrabCAD models**. The cupboard embeds native copies of this construction rather than STEP references. No creation generator is maintained; edit the saved native parameters/timeline.

## Dimensions and parameters

Length units are mm. The crate stands upright with its lowest foot at **z=0**, centered in X/Y; X is the **300 mm frontage**, Y the **400 mm depth**. Default height is **220 mm**. These are purchased **PP** containers, not printable PETG parts; this pose is the assembly pose, not a print recommendation.

| Parameter | Default | Exercised range | Basis |
|---|---:|---:|---|
| `crate_h` | 220 | 75–320 | AUER catalogue heights: 75, 120, 170, 220, 270, 320 |
| `foot_h` | 12 | 8–14 | Assumed underside bearing height, not measured product geometry |
| `wall` | 5 | 3–5 | Assumed straight wall thickness, not manufacturer mould data |

The nominal **300 × 400 mm external envelope** and **270 × 370 mm interior footprint** come from the [published AUER specifications](../../docs/auer-eurobox-400x300-specifications.md). All other details are explicit modeling assumptions:

- Straight-sided body: `(270 + 2 × wall) × (370 + 2 × wall)`, **280 × 380 mm** by default.
- Bottom bearing plane at `foot_h`; a **5 mm** floor above that plane.
- **260 × 360 mm** foot perimeter with **250 × 350 mm** relief. This was chosen to clear the cupboard's 268 mm runner opening; it is not a reverse-engineered AUER foot measurement.
- An **8 mm** stepped top rim reaching the nominal external envelope, twelve square **3 × 4 mm** exterior ribs, and two blind **90 × 20 × 2 mm** grip recesses on the short ends. These are original simplified details, not copied mould geometry.
- Square corners, no mould draft, logos, lids, open-handle variants or verified stacking engagement. The rim is a visual stacking-rim approximation, not a validated mating interface.

**Deliberate catalogue mismatch:** the modeled clear interior height is `crate_h - foot_h - 5 mm` (203 mm at default), not AUER's listed `crate_h - 5 mm`. The independently assumed underside/foot construction is for cupboard layout, not capacity or manufacturing reproduction. Do not infer printed fit, load capacity, or real-box bearing contact from it. Measure physical boxes before designing mating parts or cutting the rack.

## Cupboard interface

The [cupboard](../eurobox_cupboard/README.md) retains 316 mm bays, 24 mm-wide runners and a 12 mm bearing elevation. With the default native model:

- 300 mm maximum frontage leaves **8 mm side clearance**.
- A 268 mm runner gap around 260 mm feet leaves **4 mm foot clearance per side**.
- A 280 mm-wide bearing underside overlaps the runners by **6 mm per side**, before the local rib projections.
- 400 mm depth leaves **10 mm front/rear margin** in the 420 mm frame.

These are CAD relationships between original assumed shapes, not measured AUER tolerances. No timber geometry or support elevation changed in the replacement.

## Checks and exports

`check.py` is a read-only saved-design regression check, not a generator. It opens the native files in independent CLI sessions, exercises all six crate heights and foot/wall endpoints, checks analytic volume, center of mass, bounds and connectedness, and walks the cupboard's bay/depth/height/wall endpoints. It also rejects imported feature types and validates all six STL meshes using the existing repository mesh checker.

Run from the repository root, under a session-owned expiring process group:

```sh
timeout --signal=TERM --kill-after=10s 15m \
  flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" \
  uv run --no-project models/auer_euroboxes/check.py
```

Verified on 2026-10-25 with SolidCraft CLI 0.21.0: all saved-design/range checks passed; all six STL exports are closed, connected, outward-oriented, edge/vertex-manifold shells, with volumes within **0.1 mm³** of the analytic expectations. Native dimensional/center tolerances are **0.00001 mm** and volume tolerance **0.01 mm³**. Isometric, top and bottom views were rendered; isometric and bottom views were inspected. Export files are ignored deliverables:

- `exports/auer_euroboxes/eurobox_{75,120,170,220,270,320}.stl`

At default, the native crate volume is **2,046,772 mm³**. PP density is recorded as nominal **0.90 g/cm³**; model mass is not actual product weight.

## Third-party assets and rights boundary

The old `reference/` directory contains private GrabCAD STEP/PDF downloads by Gergely DEGI; it remains Git-ignored and unused by the new native models. The original download archive remains unchanged in `~/Downloads/`. Do not publish those files, old restricted native designs, backups or temporary baselines. Historical source/access/license research remains in [CAD availability](../../docs/auer-eurobox-cad-availability.md).

The new source contains original native construction and no downloaded CAD geometry. Rebuilding in another application alone does not clear third-party rights, and this is not a legal opinion or a guarantee concerning product-design rights or trademarks. AUER is used only to identify the purchased-box dimensions being approximated.
