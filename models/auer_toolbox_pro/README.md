# AUER Toolbox Pro layout references

Authoritative editable sources: `tb_4311.solidcraft` and `tb_4316.solidcraft`. Each native design has **7 bodies and 22 geometric timeline features**, using expression-driven primitives rather than sketches. These are independent, approximate references for purchased boxes, not imported manufacturer CAD, printable replacement parts or enclosure-print designs. Their resting pose has its lowest surface at **Z=0**.

## Published dimensions

All dimensions are in millimetres. The F4 appearance is a **dark-grey case with a light-grey lid**.

| Native source | Product | Published exterior L × W × H | Published inlet | Published usable interior height |
|---|---|---:|---:|---:|
| `tb_4311.solidcraft` | TB 4311 F4 | 400 × 300 × 120 | 394 × 248 | 77 |
| `tb_4316.solidcraft` | TB 4316 F4 | 400 × 300 × 175 | 394 × 248 | 132 |

The inlet is not a guaranteed rectangular interior volume. Floor footprint, wall draft and local intrusions are not dimensioned by these catalogue values. Product codes do not directly encode the exterior heights.

Height is adjustable between the **two discrete product settings, 120 and 175 mm**; intermediate heights are not purchased-product variants supported by this model. Other published purchased dimensions remain fixed. No generator is needed: edit the native source directly.

## Approximation boundary

The original visual geometry represents the case, feet, recessed lid, folded U-shaped carry handle, front grip relief, front-corner latches and rear hinges. These local shapes and their positions are approximations, not measured mould geometry. The front grip relief does not represent an optional attached front handle.

Fixed visual assumptions are **10 mm feet, 23 mm floor elevation above the lowest surface, 20 mm lid thickness and 10 mm lid recess**. These are modelling choices, not manufacturer specifications; in particular, a published stacking-height difference does not establish the real foot height. The model does not reproduce exact bayonet coupling, seals, spring mechanisms or logo geometry. It does not establish functional catches, a working hinge, physical fit, support contact or compatibility with mating hardware. Measure real products before designing close-fitting parts or load-bearing supports.

The folded handle and closed lid remain within the nominal purchased envelope. No raised-handle or open-lid clearance is established.

## Sources and deliverables

See [the product research](../../docs/auer-toolbox-pro-research.md) for published values, first-party visual references and their limitations. Official selected products: [TB 4311 F4](https://www.auer-packaging.com/en/Tool-boxes-Pro/TB-4311-F4.html) and [TB 4316 F4](https://www.auer-packaging.com/en/Tool-boxes-Pro/TB-4316-F4.html).

STL references are under `exports/auer_toolbox_pro/` at the repository root. They are visual/layout exports, not a recommendation to print replacement boxes. The native `.solidcraft` files remain authoritative. The [two-column cupboard checker](../rolling_eurobox_cupboard_columns/check.py) passed **9 saved-native toolbox states** on 2026-10-29, including both discrete height settings and restoration. Exterior bounds, inlet dimensions, usable height and independently calculated body volumes matched; timelines were clean. Both isometric views and an interior section were inspected, and STL envelopes match within **0.001 mm**. Physical fit and printability are not validated.
