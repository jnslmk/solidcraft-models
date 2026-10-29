# Two-piece plant support — 174 mm pot

`plant_support_174.solidcraft` is the editable, authoritative native design.
It contains two instances of the same half, rotated 180° around Z. Four sloping
struts connect the pot collar to a centred stem ring. Both rings split together,
so installation does not require threading the plant through a closed ring.

## Print and assemble

- Print **two copies** of `exports/plant_support/plant_support_half.stl`.
  Do not print an STL of the assembled model: its touching interfaces must remain
  separate. The accompanying half STEP is an export, not a second source.
- Material: **PETG**, 0.4 mm nozzle, 0.2 mm layers, at least four perimeters and
  25–35% infill. PLA is not recommended for the repeatedly flexed latches.
- Print in the supplied upright pose, pot ring and snap tongue on **Z = 0**;
  Z+ is the print direction. Each half is approximately **201 × 112 × 126 mm**.
  Use a brim if necessary without joining the two halves. The struts lean about
  36° from vertical and the stem-ring spans are short bridges.
- Enable build-plate-only supports beneath the **6 mm inward rim-rest overhangs**.
  The receiver has a short 2.2 mm channel-roof bridge; do not fill its channel
  with supports. Remove support/brim residue before assembly.
- Put one half on each side of the pot and stem, in the same orientation as the
  assembly. Rotate the second half 180° in plan, **not upside down**. Align the
  small stem-ring tongues and pot-ring latches, then press the halves together
  horizontally until both pot-ring barbs click into their side windows.
- To remove, press both exposed barbs inward toward the pot to clear the catches
  and separate the halves. No screws, loose pins, adhesive, or assembly tools.
  Avoid squeezing or levering against the living stem.

## Fit, interfaces and assumptions

- The nominal **174 mm outside pot diameter** gets a **175 mm collar bore**:
  0.5 mm radial clearance. This is a locating collar, not a friction clamp.
  Four inward rim rests reach radius 81.5 mm and sit on the top of the pot rim,
  preventing the collar from sliding down a tapered pot. Their underside is at
  Z = 8 mm. Check that the actual rim provides bearing beneath these rests.
- The upper ring has a **10 mm inner diameter**, 18 mm outside diameter and
  6 mm axial height. Its underside is Z = 120 mm, **112 mm above the rim-rest
  seating plane**, with the top at Z = 126 mm. The height is an assumption because
  the supplied sketch has no height dimension.
- The lower ring is 4.5 mm thick radially and 8 mm high. Two 4.5 × 6 mm struts
  belong to each half; the rim rests are 10 mm wide tangentially and 2 mm thick.
- Each half has one 20 mm free-length, 1.6 mm thick, 6 mm high cantilever tongue,
  a ramped barb, and one complementary receiver. The receiver is open underneath
  for printing; the oppositely oriented latches and stem alignment sockets
  constrain relative vertical motion once assembled.
- `fit = 0.3 mm` provides side and roof clearance, a 2.2 mm receiver channel,
  and 0.5 mm radial barb engagement. Stem alignment tongues are 1.6 × 3 mm with
  2 mm engagement and the same per-side clearance. Estimated snap root strain
  for approximately 0.5 mm tip deflection is about 0.3%; this is a geometric
  estimate, not a measured PETG fatigue or retention rating.
- Physical pot fit, latch force, layer adhesion and long-term creep are **not
  print-tested**. Ceramic ovality and slicer compensation can consume the stated
  clearance. Tune the named clearance parameters to the printer, not the nominal
  pot diameter. The stem opening must leave space for growth and must not pinch
  the plant; increase it if the actual stem approaches 10 mm.
- Intended for gently locating an indoor plant, not lifting the pot, supporting
  heavy branches, or resisting wind. It does not prevent the whole pot tipping.

## Editable parameters

Favourite parameters appear in the native Parameters table. Change one at a time
within these checked ranges; simultaneous extreme combinations are not qualified.
Other dimensions are fixed design interfaces, not independently qualified knobs.

| Parameter | Default | Checked range | Meaning |
|---|---:|---:|---|
| `pot_d` | 174 mm | 170–180 mm | Actual outside pot diameter |
| `pot_clearance` | 0.5 mm | 0.3–0.8 mm | Radial pot clearance |
| `stem_d` | 10 mm | 8–12 mm | Stem-ring bore |
| `support_h` | 120 mm | 100–140 mm | Z of stem-ring underside |
| `fit` | 0.3 mm | 0.25–0.4 mm | Snap/socket per-side clearance |

All sketch profiles are constrained to zero degrees of freedom. Coordinates and
loft sections use expressions tied to the driving radii and height. The second
half is a native copy/rotation of the completed first half, not duplicated geometry
instructions. Re-export only `SupportHalf` after changing the saved native design,
then print it twice.

### Integrated junctions

The latch mounts now sweep into the collar through expression-driven cubic
fairings with an 18 mm tangential run, instead of ending as isolated rectangular
blocks. Inner strut roots use 1.5 mm blends into the rim rests; the stem-ring
underside junctions use 0.75 mm blends, and exposed receiver-end corners use
1.2 mm rounds. These fixed parameters are `fairing_run`, `root_blend`,
`head_blend`, and `latch_blend`; they are not independently range-qualified.
The strut sections, pot/stem bores, spring tongues, engagement shoulders and
running clearances are unchanged.

Fairing extrusions run from Z = 0.01 to 7.99 mm, overlapping the collar through
its side rather than sharing its top/bottom planes. This 0.01 mm end relief
avoids a zero-area face in the CAD boolean without affecting the seating or
snap interfaces. The spline control points follow the pot radius. The printable
pose, supports, material and two-identical-halves assembly remain unchanged.


## Verification and export

`check.py` is a read-only regression check, **not a design generator**. It reloads
the saved native model, measures both bores, walks the five favourite parameters
to both endpoints and back, checks body bounds/health, and validates the printable
mesh. Native boolean joins can report sub-micron tool-displacement retries at the
anchors/fairings/rim rests; they are accepted only with checked geometry/volume.
`SoftReceiverEnds` also reports a split-edge rebind: the nearest surviving edge
piece was verified by independent STEP validity/intersection and the actual
channel/roof measurements, including across the parameter walk.

Refinement checks passed: persisted native reload, all 15 parameter-walk states,
175 mm pot and 10 mm stem bore measurements, zero-DOF sketches, and two closed
single-shell bodies. The actual 2.2 mm receiver channel and 0.3 mm roof clearance
were measured, with their parameter-dependent values checked at every walk state.
Isometric and top views were inspected. The final half STL has 2,806 triangles,
one connected manifold shell and volume 19,114.573 mm³; independent, valid STEP
solids measure 19,112.469 mm³ per half (native measurement: 19,112.693 mm³).

The native interference tool could not conclusively verify the contacting seams.
An independent OpenCASCADE STEP intersection found only two anchor-seam slivers:
0.0373 mm³ total, confined within 0.000365 mm across the mating plane, from the
documented boolean displacement retries. This is below the 0.002 mm CAD checking
tolerance and far below the 0.3 mm latch clearance; it is not a nominal designed
press-fit. No other solid overlap was found. Printed retention/fit remains
unverified.

Use a unique session-owned process group and a finite supervisor, holding the
workstation-wide slot until all CAD children have stopped, for example:

```sh
setsid flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" \
  timeout --signal=TERM --kill-after=10s 15m \
  python3 models/plant_support/check.py
```

Record the owning session, process group, expiry and cleanup command before
starting. Do not unlink the lock file or terminate another session's job.

The native direct STL has seam defects on this model, so use the existing
STEP-to-STL exporter under the same finite CAD lock. It tessellates the native
STEP and rejects a non-manifold mesh; it does not redefine or heal the design:

```sh
uv run --script models/led_profiles/export_stl.py \
  exports/plant_support/plant_support_half.step \
  exports/plant_support/plant_support_half.stl
```

The desktop's unrelated ambient-sensor document was left untouched. Inspection
images and disposable checks are kept under ignored `.codex-tmp/` only.
