# LED profile endcaps

SolidCraft recreations of `models/led_profiles/endcap.py` and
`endcap_wired.py` in the sibling `build123d-models` repository. The native
`.solidcraft` documents are the authoritative editable models here; generated
print/exchange exports belong in `exports/led_profiles/`.

- `endcap.solidcraft`: standard endcap with a relieved flange and open-channel plug.
- `endcap_wired.solidcraft`: longer flange providing cable-turning room between
  the gland and the tube's wiring cavity.

The source code and freshly generated reference solids take precedence over
older comments or tables in the sibling repository. In particular, the plug
wall is **1.6 mm**, plug fit allowance is **0.22 mm diametral**, and the wired
chamber's peripheral shell is **2.21 mm**.

## Editing the native designs

| Driving parameter | Default | Verified range | Effect |
|---|---:|---:|---|
| `plug_depth` | 16 mm | 8–30 mm | Changes insertion depth; preserves flange, mating clearances and tip treatments |

These are **hybrid native designs**, not full procedural ports of every
build123d slider. Each embeds a precision fixed core and a separately movable
tip, preserving the source's faded helical thread and intricate blends that
SolidCraft 0.21.0 could not reliably rebuild with its native curved booleans.
A fully constrained native U-channel sketch and extrusion join them, with
extension length `plug_depth - 7 mm`; the tip follows `plug_depth - 16 mm`.
The embedded geometry is self-contained: reopening does not need the sibling
repository or disposable STEP fragments.

Only `plug_depth` is supported as a resize control. Other recorded hardware
dimensions are fixed references, not independent shape-changing parameters.
Changing gland size/clearance, screw layout, strap dimensions or plug wall
requires reworking the matching precision geometry, not changing a reference
number in the table. The original build123d sliders are not all reproduced.

## Fixed mating geometry

All dimensions are in mm. XY is the tube's cross-section, centred on the gland
axis; Z is along the tube, from the endcap's outside face toward its plug.

| Interface | Standard | Wired |
|---|---:|---:|
| Flush stadium-shaped flange, X × Y | 26.1 × 30.5 | 26.1 × 30.5 |
| Flange thickness | 15.85 | 25.85 |
| Plug insertion depth | 16 | 16 |
| Total height in print pose | 31.85 | 41.85 |
| Open-channel plug wall | 1.6 | 1.6 |
| Plug fit allowance, diametral | 0.22 | 0.22 |
| Gland thread | M12 × 1.5 | M12 × 1.5 |
| Female major diameter including print allowance | 12.3 | 12.3 |
| Thread start / threaded length | 1.5 / 6.5 | 1.5 / 6.5 |
| Screw spacing | 22 | 22 |
| Screw clearance diameter | 2.65 | 2.65 |
| Screw access diameter / depth | 4.85 / 4 | 4.85 / 14 |
| Strap slot, axial × transverse | 12.25 × 1.5 | 12.25 × 1.5 |
| Cable chamber floor / axial run | — | 15.85 / 10 |

The two screw axes are at `(−11, −0.55)` and `(11, −0.55)` in XY.
They accept M2 × 16 DIN 965 countersunk screws, with 90° seats recessed down
the access bores. Both caps preserve the same screw reach into the aluminium.
The strap slot is centred at Y=−11.4, spanning Z=1.8…14.05, and opens through
both curved flanks. It accepts the source's 12 × 1 mm strap with clearance.

The standard cap's centred gland is **not a cable route into the tube**:
the intervening opening is narrower than the source's 6.7 mm cable. Use the
wired variant when that route is required. These caps do not establish an IP
rating or a sealed lamp assembly.

## Material and printing

Preserve the source family's **ASA** material choice for outdoor UV and the
40–60 °C tube environment; do not silently substitute PETG and assume the same
fit. Print with the outside flange face on the bed at Z=0 and the plug growing
in +Z. The gland thread is vertical. The source recommends layer height
≤0.25 mm (pitch/6). Gland clearance is +0.30 mm on major diameter; the plug's
0.22 mm diametral allowance gives 0.11 mm per side before printing effects.
These are modeled allowances, not a physical-fit guarantee. Printed gland fit,
strap durability, screw retention and strength require real-part qualification.

## Verification

Both persisted native files were reopened and walked through
`plug_depth = 16 → 8 → 30 → 16 mm`. Every state retained one body with one
shell, a fully constrained eight-curve sketch, and no parameter or timeline
errors/warnings. Bounds and centre of mass were checked within 0.005 mm of
independently generated source expectations; tessellated volume and area were
checked within 0.1%. Defaults remain 16 mm in the saved documents.

| Model | Delivered STL triangles | Largest bidirectional sampled source-surface distance |
|---|---:|---:|
| Standard | 46,524 | 0.02500 mm |
| Wired | 45,846 | 0.02475 mm |

The surface comparison used vertices and face centroids against an independent
source mesh tessellated at 0.005 mm nominal tolerance. No sampled distance
exceeded 0.03 mm; this is sampled surface verification, not an exact Hausdorff
or Boolean-XOR proof. Adaptive OCCT mass integration of native-derived STEP
agreed with source volume within 0.001 mm³ for both defaults. Ordinary
non-adaptive volume integration and coincident-face XOR classification were
unreliable after STEP reparameterization, so exact XOR equality is not claimed.

Both STLs have one connected, closed edge- and vertex-manifold shell with
consistent outward winding. They require no welding or mesh healing.
Re-exporting from the persisted native files reproduced the delivered STL
bytes exactly. Isometric, top, underside and cutaway renders were inspected,
including the gland threads, recessed screw seats, relief/chamber and plug.
The user's desktop document was left untouched.

Run the retained regression check from the repository root:

```sh
uv run --no-project models/led_profiles/check.py
```

It checks the saved defaults, depth-range endpoints and restoration, plus the
delivered STL topology and volume. Run CAD work under the workstation's
heavy-verification lock and a finite process-group expiry.

## Re-exporting after an edit

**Do not use SolidCraft 0.21.0's direct STL for these parts:** its tessellation
leaves microscopic thread-face seam defects. Export STEP from the saved native
document, then use the topology-aware OCCT tessellator below. This exporter
defines no geometry and rejects a nonmanifold result rather than repairing it.
Its optional CAD dependencies are isolated by `uv`; normal native editing and
the regression check do not require them.

```sh
mkdir -p .codex-tmp/endcap-export
part=endcap # or endcap_wired
solidcraft-cli run --in "models/led_profiles/$part.solidcraft" \
  --out ".codex-tmp/endcap-export/$part.step"
uv run --script models/led_profiles/export_stl.py \
  ".codex-tmp/endcap-export/$part.step" "exports/led_profiles/$part.stl"
```

The intermediate STEP is disposable, not another source definition. The
delivered STLs are for the default 16 mm insertion depth; export again after
saving a different depth.
