# Rolling Eurobox and Toolbox Pro cupboard

Authoritative editable source: `rolling_cupboard_columns.solidcraft`. This two-column derivative was made by copying the [original single-column rolling model](../rolling_eurobox_cupboard/README.md) and editing the copy in place; the original `models/rolling_eurobox_cupboard/rolling_cupboard.solidcraft` is unchanged. No generator is required. The revised native model has **141 bodies and 310 geometric timeline features**, with no sketches.

Front is **Y−**, Z is up, and the floor is Z=0. All containers have their **400 mm sides running front-to-back along Y**, across two equally narrow bays. Toolbox cupboard occurrences are rotated **+90° about Z** from their unchanged standalone source orientation; their latches and front grip consequently face **X+**, not the cupboard front. These are purchased-container references in timber furniture, not printable enclosure designs.

## Layout and construction

- Default timber frame: **688 mm wide × 448 mm deep**, **1479 mm total height**. Frame width is `bay_w + tool_bay_w + 72`; exterior straps and caster motion are not included in this timber-frame width.
- **Left:** the original ten crates, bottom-to-top **four 120 mm and six 75 mm** boxes, retained on their original pairs of 20 × 20 mm runners.
- **Right:** seven closed Toolbox Pro cases, bottom-to-top **175, 120, 175, 120, 175, 120, 120 mm**: three TB 4316 and four TB 4311. See [the independent toolbox references](../auer_toolbox_pro/README.md) for published dimensions and approximation limits.
- Each toolbox rests directly on two **20 × 20 mm rails**, with no rectangular plywood panels above them. The lowest pair is `frame_d − 48` long (**400 mm** by default), fitting between the bottom front/rear frame rails; the other twelve rails are `frame_d` long (**448 mm**). The 14 existing `Tool_ledger_XX_Left/Right` bodies retain their names. Each rail top meets the modeled case feet at `tool_bottom`; its underside is 20 mm lower.
- Six posts form two bays, with top/bottom rings and middle rails. The four original caster assemblies are relocated to the frame; the original side and rear X straps follow its width. Their simplified geometry is retained, not structurally redesigned.
- Default X centres are **−166 mm** for the left column and **166 mm** for the toolboxes; the divider and toolbox Y centre are **0 mm**. Centres follow `crate_cx = −(tool_bay_w + 24)/2` and `tool_cx = (bay_w + 24)/2`.

## Editable dimensions and clearances

Dimensions are in millimetres. Purchased container sizes and section sizes are fixed interfaces, not fit knobs.

| Parameter | Default | Intended range / meaning |
|---|---:|---|
| `bay_w` | 308 | 304–308; clear left-bay width |
| `tool_bay_w` | 308 | 304–308; clear toolbox-bay width |
| `frame_d` | 448 | 440–460; frame depth |
| `head_gap` | 29 | 29–34; left-column handling gap |
| `tool_gap` | 21 | 21–26; case top to next rail underside |

At default widths, nominal container-to-post clearance is **4 mm per side** in each bay; at minimum widths it is **2 mm per side**. This is envelope clearance, not a physical-fit guarantee. `head_gap` also raises the top ring with the left crate stack, reaching **1529 mm overall height** at 34 mm; `tool_gap` changes only the right stack. Within the documented ranges, the smallest final toolbox-to-top-ring clearance is **19 mm** (`head_gap=29`, `tool_gap=26`).

For toolbox index `i = 0…6`, counted from the bottom:

```text
tool_bottom(i) = 135 + sum(previous toolbox heights) + i × (tool_gap + 20)
```

At defaults, the last case top is **Z=1386 mm**, below the top rail underside at **Z=1435 mm**, leaving **49 mm**. Each case top is **21 mm** below the next support rail underside.

The rotated modeled feet have centres **X=±125 mm, Y=±175 mm** relative to the case centre, and 24 × 24 mm contact patches at `tool_bottom`. Rails span Y=±`frame_d/2`, except the lowest pair is inset 24 mm at each end to clear the bottom frame. Their X extents are `tool_cx − tool_bay_w/2` to 20 mm inward and `tool_cx + tool_bay_w/2 − 20` to the right bay edge. The feet's outer X edges at ±137 mm give **3 mm lateral bearing overlap** at a 308 mm bay or **5 mm** at 304 mm; the full 24 mm foot depth is supported in the model. These small overlaps rely on approximate foot geometry, not measured product bearing surfaces.

**Cases must slide out closed before their lids are opened.** No in-cupboard lid-open or raised-handle clearance is provided. Side-facing latches and grips may require withdrawing the case for access. The full individual closed heights, not reduced coupled-stack heights, determine the rail spacing.

## Construction limitations

The toolbox shells, feet, bayonet features, hinges and catches are visual approximations, not measured bearing or mechanism geometry. Measure the actual boxes, foot contact, tolerances and loaded sliding behaviour before cutting timber; modeled overlap is **not a product bearing guarantee**, and printed-reference bearing strength is unverified. Rail fasteners, timber joints and support/load capacity have not been engineered. No load rating is assigned to the rails or cupboard.

The original caster, bracing and anti-tip limitations remain: caster product ratings do not establish a cupboard rating; strap anchorage/tensioning, timber joints and mounting hardware are not designed. Relocating the original casters and widening the bracing is not a stability calculation. A tall rolling cupboard can tip when loaded cases are withdrawn; brakes and drawn X straps are not an anti-tip system. No safe extension, loaded braking performance or structural capacity is established. **This model is not construction approval.** Refer to the [original model documentation](../rolling_eurobox_cupboard/README.md) for retained stock, caster sources and component assumptions; its single-column timber procurement quantities do not apply to this wider derivative.

## Checks and exports

`check.py` is the permanent **read-only** checker of the saved native models, not a generator. Run from the repository root under the workstation heavy-verification lock:

```sh
timeout --signal=TERM --kill-after=10s 15m flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" uv run --no-project models/rolling_eurobox_cupboard_columns/check.py
```

Verified on 2026-10-29 with SolidCraft CLI 0.26.1: the saved-native checker passed **9 standalone toolbox states and 12 cupboard states**, exercising the documented parameter endpoints and returning to defaults. All seven toolbox orientations, independent body volumes, direct rail contacts, modeled foot bearing and clean timelines matched expectations. The **109 functional bodies** (50 timber parts, 10 crates and 49 toolbox parts) had zero solid interferences; all 222 candidate pairs were checked. Isometric and front views of the revised desktop design were inspected. Assembly and timber-only STL exports were regenerated and their envelopes match the saved geometry within **0.001 mm**. Native geometry checks cannot establish physical fit or structural safety.

Assembly and `timber_only` STL exports are under `exports/rolling_eurobox_cupboard_columns/`; standalone toolbox exports are under `exports/auer_toolbox_pro/`. These are assembly-layout references, not furniture-print instructions. Native `.solidcraft` sources remain authoritative.
