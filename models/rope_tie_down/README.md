# Printable wall-mounted horn cleat

Editable source: [`rope_tie_down_40.solidcraft`](rope_tie_down_40.solidcraft).
Printable export: [`../../exports/rope_tie_down/rope_tie_down_40.stl`](../../exports/rope_tie_down/rope_tie_down_40.stl) (generated, untracked).

A tapered oval horn bar on two mounting feet, inspired by the user's metal-cleat photograph. The feet are separate to avoid an elevated bridge during printing. The native design is authoritative; `check.py` only checks it.

## Wall screws and dimensions

Designed for the selected **Ø5 mm, 90° countersunk Torx wall screws**, assuming nominal Ø10 mm heads. Torx alone specifies the drive, not the head shape: check actual head dimensions before printing.

| Interface | Dimension, mm |
|---|---:|
| Screw-hole centres | **40** |
| Through-hole diameter | 5.5 |
| Countersink mouth diameter | 10.5 |
| Countersink depth / included angle | 2.5 / 90° |
| Overall length × width × stand-off | 120 × 26 × 30 |
| Oval bar thickness | 8 |
| Mounting-foot diameter | 24 |
| Clear space behind bar | 22 |
| Minimum gap between feet | 16 |
| Horn projection beyond each foot | 28 |

**Insert screws through the exposed oval bar face, through the feet and into the wall.** Heads seat in conical recesses on the exposed face. The mounting feet have plain clearance holes and flat contact faces; there are no deep cylindrical rear pockets. Use appropriate wall plugs/anchors for the substrate. The 30 mm body thickness consumes approximately 27.5 mm of screw length measured from the head's top to the mounting surface when the head is recessed 0.25 mm below the outer face; add the embedment required by the anchor manufacturer. Do not infer anchor suitability or a load rating from CAD dimensions.

The 0.5 mm shank clearance and 0.5 mm head-diameter allowance are nominal CAD allowances, not proven printed fits. Verify screw-head fit and avoid overtightening the plastic.

## Printing and use

Material: **PETG**, modeled at 1.27 g/cm³. Print the broad oval face **down on the bed**, mounting feet upwards, exactly as saved. Z=0 is the visible bar face; foot mounting faces are at Z=30. Screw axes are X=±20, Y=0. Countersinks open at Z=0 and narrow to the Ø5.5 bores at Z=2.5.

The horns start on the bed; holes are vertical and the foot flare is only about 7.43° from vertical. Countersinks narrow as printing progresses, so no support is intended. Inspect the slicer preview. Start with 0.2 mm layers, six perimeters, six top/bottom layers and 50% infill; consider a brim for horn-tip adhesion. Remove elephant foot from the countersink openings and smooth any rough rope-contact surfaces. No physical print or fit test has been performed.

Intended for ordinary small rope, with 4–8 mm as an untested starting assumption. **Unrated, light-duty utility part only**: not for climbing, overhead loads, safety-critical restraint or certified cargo securing. PETG can creep under heat, preload and sustained tension. Inspect fasteners and the part regularly. This is not structurally equivalent to the metal reference.

## Editable design and ranges

The native timeline uses two fully constrained sketches, oval-bar and tapered-post extrusions, edge/root blends and two countersunk hole features. No imported mesh or solid is used. Fixed constants: `post_d=18`, `foot_d=24`, `head_d=10.5`, `root_r=1.2`, `edge_r=0.8`, `bed_chamfer=0.4` mm. `post_taper` is derived from foot/post diameters and stand-off, including 1 mm buried root overlap. Changing fixed constants requires new checks.

| Driving parameter | Default | Checked endpoints |
|---|---:|---:|
| `hole_spacing` | 40 | 35–50 |
| `bar_length` | 120 | 110–130 |
| `bar_width` | 26 | 26–30 |
| `bar_t` | 8 | 8–10 |
| `mount_height` | 30 | 28–34 |
| `hole_d` | 5.5 | 5.2–5.8 |

Endpoints and return to default are exercised one parameter at a time, not for arbitrary combinations. Retain 40 mm spacing for the requested wall interface. Ranges are documented, not enforced by the application.

## Verification

Saved native geometry: one connected solid, 120 × 26 × 30 mm, volume 33,556.02 mm³, clean timeline at default, sketches at zero degrees of freedom. Saved-design reload and all six parameter walks pass bounds, symmetry and an independent ellipse/frustum/countersink volume estimate within 0.1%. Oval edge blends can report geometric rebinding during changed states; default returns clean. The exposed-face screw seats were visually inspected.

The STL is one closed, connected, consistently oriented edge- and vertex-manifold shell: 8,692 triangles, volume 33,525.18 mm³, within 0.1% of native. Exported rings verify centres ±20 mm, the 10.5 mm mouths, 5.5 mm bores and 24 mm foot faces to 0.0001 mm. Native bounds tolerance is 0.002 mm. These are digital checks, not manufacturing tolerances.

Run the read-only checks from the repository root:

```sh
timeout --signal=TERM --kill-after=10s 15m \
  flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-$(id -u).lock" \
  python3 models/rope_tie_down/check.py
```

Requires installed `solidcraft-cli` and Python stdlib only. Re-export the STL after editing the native design. The export check expects the delivered default wall-screw dimensions.
