# Room ambient sensor enclosure

Compact side-ventilated **108 × 74 × 44.4 mm assembled** tabletop enclosure for a Wemos D1 mini, its existing perfboard/upright DHT22 assembly, attached SGP41 breakout, and separate MH-Z19B. Material: unfilled **PETG**. This is an indoor, non-weatherproof enclosure, not a certified sensor housing.

## Files and researched hardware

- Authoritative editable source: [`room_ambient_sensor.solidcraft`](room_ambient_sensor.solidcraft). Native named parameters and timeline features; no alternate generator.
- Populated native assembly: [`room_ambient_sensor_assembly.solidcraft`](room_ambient_sensor_assembly.solidcraft), with installed hardware references and inspection views; **not a printable assembly export**.
- The case-only file is authoritative for printing. The populated assembly is a fit reference and must have matching case geometry before using it to assess fit.
- Printable parts: [`../../exports/room_ambient_sensor/base.stl`](../../exports/room_ambient_sensor/base.stl) and [`lid.stl`](../../exports/room_ambient_sensor/lid.stl). Generated exports are intentionally untracked. Both are centered independently in XY, with minimum Z=0; regenerate after editing the case.
- Cited controller/DHT research: [`../../docs/room-sensor-board-research.md`](../../docs/room-sensor-board-research.md).
- Cited gas-sensor research: [`../../docs/room-sensor-gas-research.md`](../../docs/room-sensor-gas-research.md).

| Component | Published dimensions used, mm | What remains uncertain |
|---|---|---|
| Wemos D1 mini | Official PCB 34.2 × 25.6 | Mini-format identification is a photo inference. Clone, USB version and tall headers are not measured. Not for the 68.6 × 53.4 Uno-format D1 R2. |
| Connected prototyping shield | Default PCB **28.5 × 26**, 2.54 grid | **[INFERENCE]** Close-up resembles the standard D1 mini prototyping shield; seller size is not a measurement of this clone or its hand assembly. |
| DHT22 / AM2302 | Common white body 15.1 × 25 × 7.7; example breakout PCBs 37 × 16 or 40 × 23 | Default carrier height 40; exact breakout, mounting height and solder protrusions are unknown. |
| MH-Z19B | Nominal 33 × 20 × 9; Winsen terminal-equipped drawing **39.30 ±0.30 overall length** | Upright jumper housings and lead bends are additional. The white terminal is included even when unused. |
| SGP41 | Sensor package 2.44 × 2.44 × 0.85; generic breakout example 13 × 10.5 | Package is not the board. Reference geometry places the sensor on the underside of the blue four-pin breakout; dimensions, hole and actual air clearance remain photographic estimates. |

**Fit is provisional, not measured from the photograph.** Check the actual intact assembly and wiring in the populated native model before a full print. Online component drawings cannot establish the custom stack, solder clearances or loose wire geometry.

## Layout and mounting

The case is **108 × 74 × 42 mm** externally; with the 2.4 mm lid the closed height is **44.4 mm**. Coordinates refer to the native base: X left/right, Y front/rear, and Z upward. The floor occupies Z=0–2.4; inner walls are at **X=±51.6, Y=±34.6**. The case-only source is authoritative and keeps the lid beside the base for editing/export; the populated assembly is a fit reference, not a printable assembly export.

The intact Wemos/perfboard/DHT22/SGP41 stack remains rotated onto its edge, −90° about Y, at **[16.2, 0, 23.4]**. No sensor or board detachment/desoldering is assumed. The highest default hardware is at Z=36.4, leaving **5.6 mm headroom** to the lid underside at Z=42. At the 28 mm perfboard-width endpoint the highest PCB is Z=38.4, leaving 3.6 mm. These are modeled clearances, not proof that a particular hand-built assembly fits.

- The two controller supports are **8 × 4 × 8 mm**, with tops at Z=10.4 under the perfboard. The redundant long guide rails are removed. The stack's two end catches retain its bare upper PCB edge; release them away from the PCB in ±Y.
- The MH-Z19B centre follows `co2_x=case_length/2−wall−17 mm` (**34.6 mm** default). Its two ledges support the PCB at Z=5.4, centred at Y=−13.4 and +6.6. Four outward-releasable catches act on the exposed PCB end lands, not the gold chamber or white terminal. Each floor-plane beam has **12 mm free length**, 1.2 mm width, **1.8 mm lateral relief on both sides**, and the floor's 2.4 mm thickness. The beams are left integral with the floor by final U-shaped relief cuts; they are not cut away and rejoined. The catch feet overlap the intact floor by 1 mm before those cuts, avoiding the coplanar beam-join failure at the widest case setting.
- Four lid tongues retain the solid 2.4 mm plate. They project 22 mm in print pose, with 0.35 mm beam/wall clearance and 0.7 mm hook engagement. The rear positive-X latch follows `rear_latch_x=case_length/2−22.5 mm` (**31.5 mm** default); release the hooks through the outside windows before lifting. Snap fit depends on actual board thickness, clear solder/component-free lands, printer calibration and PETG behavior.
- Four jumper wires connect the modeled modules. Red/Brown pass through the baffle's front carrier opening at Y≈−10.2 and around the DHT's left end before reaching the rear; they do not pass through its PCB. Rear lanes are `Y=case_width/2−6.5 mm` (**30.5 mm**) for Red/Brown and `Y=case_width/2−5 mm` (**32 mm**) for Orange/Yellow, clear of the USB opening and lid tongues. Actual leads may need rerouting or shortening; no desoldering is assumed. Wire colours do not establish electrical pin mapping.
- The USB opening is at the front: rectangular portion **X=5…21, Z=5.4…29.4 mm**, with a 45° pitched roof reaching **Z=37.4 mm**. The modeled overmould passes through it; check the actual plug and cable bend. This is not a strain-relief clamp. Remove the lid for unrestricted reset/connector access.
- Ventilation comprises **20 end-wall slots, eight front/rear side-group slots, and six antenna-end slots**. Openings are 4 mm wide, extending from Z=6 to Z=32 at defaults. The thermal baffle remains at X=−26…−24, with a 22 mm-wide, top-entry DHT opening above Z=9.4. Keep the SGP sensing face, DHT grille, and MH sampling openings exposed; leave at least 3 mm local sensing-face clearance and roughly 10 mm outside the case.
- **RF tradeoff:** the tighter layout brings the metal MH chamber to approximately **11.6 mm from the modeled antenna trace**, so the former general 15 mm metal reservation is not retained. The new jumper routes remain at least 15.25 mm from that trace in the default fit proof. Actual Wi-Fi performance must be checked with the real hardware; this enclosure is not an RF qualification.

Component dimensions and identities remain provisional where noted above: the controller format is inferred from photographs, the connected shield and sensor carriers are not measured, and wire bends are only reference geometry. Measure the actual intact assembly and check the populated native model before committing to a full print. Preserve local air access to each sensing face and avoid placing the enclosure tight against a wall.

### Edge finishing

Both native sources have matching **1.5 mm outside vertical corner fillets** on the base and lid, plus **0.4 mm × 45° chamfers** around their exterior build-plate perimeters. The lid's chamfer is on its upper exterior face when assembled. These are four named, editable timeline features, driven by `outer_corner_radius` and `print_edge_chamfer`.

The rounds soften handling corners; the chamfers provide a small first-layer edge allowance. Both treatments remove material only. The upper base rim/lid seating planes, registration features, snap hooks and flexures, board supports, USB opening, and vents remain unchanged. No internal rounds were added at flexure roots or close-fitting electronics interfaces. The straight wall remains 2.4 mm thick; the maximum 2 mm outside corner radius stays within that wall's corner stock. Print calibration and physical fit remain untested.

## Editable parameters and clearances

All lengths are millimetres. These are independent documented ranges, not input validation. Values outside them are not covered by this design contract.

| Parameter | Default | Range | Notes |
|---|---:|---:|---|
| `case_length` | 108 | 108–116 | External X dimension; rear latch derives from `case_length/2−22.5`. |
| `case_width` | 74 | 74–82 | External Y dimension. |
| `case_height` | 42 | 42–46 | Base height; closed height is 2.4 mm greater. |
| `mh_snap_length` | 12 | 12–14 | MH-Z19B PCB catch beam length. |
| `pcb_snap_t` | 1.2 | 1.0–1.2 | PCB catch beam thickness. |
| `snap_engagement` | 0.7 | 0.5–0.7 | Hook engagement; affects required insertion deflection. |
| `pcb_clearance` | 0.35 | 0.25–0.4 | PCB fit clearance. |
| `lid_clearance` | 0.35 | 0.25–0.60 | Per-side lid tongue/registration clearance. |
| `co2_width` | 23 | 22–26 | MH support ledge length; catches follow the actual 20 mm PCB. |
| `perfboard_width` | 26 | 26–28 | Installed PCB height; stack datum and catches follow it. |
| `perfboard_length` | 28.5 | 28.5–30.5 | Stack end-catch alignment. |
| `perfboard_z` | 13.4 | 12.5–14 | Local photographed-flat stack separation. |
| `lid_snap_t` | 1.2 | 1.0–1.4 | Lid tongue thickness. |
| `lid_snap_length` | 22 | 20–24 | Tongue projection and mating release-window elevation. |
| `pcb_top_gap` | 0.25 | 0.15–0.40 | Gap above the PCB to the retaining hook. |
| `outer_corner_radius` | 1.5 | 1–2 | Outside vertical corner fillets on both printable parts. |
| `print_edge_chamfer` | 0.4 | 0.2–0.6 | Exterior build-plate perimeter, 45°; does not change the lid seat. |
| `dht_carrier_height` | 40 | 37–40 | Assembly-only provisional carrier estimate. |

`wall=2.4 mm` is fixed. The controller stack stays in place as the case changes; the MH bay, its mounts and connecting wire endpoints follow `co2_x`. The assembly has nine components and eight as-built rigid joints; its case components are an editable fit snapshot, not linked external parts.

For the floor beams, **ε ≈ 1.5·t·δ/L²** gives **1.3125%** at defaults and **1.375%** at the worst independent range combination. These are geometric estimates only, not PETG fatigue, creep, layer-bond or repeated-use qualification. Print a small beam/hook coupon and measure the bare PCB lands before fitting electronics. Do not force a board into a catch or leave a flexure preloaded.

## Print and use

- Print one base and one lid separately in **PETG**, each in its existing native print pose with its flat exterior face on the build plate at Z=0. The parts are separate; do not export the populated assembly as a print. Confirm orientation, bounds, clearances, and snap details in the slicer against the current native source and regenerated exports.
- No support strategy or slicer settings are certified here. Inspect the vents, pitched USB roof, snap features and internal supports in the slicer; use only locally removable support if required and keep support/brim material out of fit and sensing interfaces.
- This is an indoor, non-weatherproof housing. Keep sampling openings clear, allow ambient air to reach the vents and sensor faces, and air out freshly printed parts before installing gas sensors. Avoid glue, silicone, solvent residue or foam near sensing openings. PETG outgassing and sensor response are not qualified.
- Position away from direct sunlight and heat sources. Compare enclosed temperature readings with open air after thermal equilibrium. Physical fit, cable routing, thermal bias, VOC baseline, airflow and RF performance remain hardware acceptance checks.

## Verification

The compact native sources and subsequent edge finishing were edited and saved through the desktop bridge; the populated source remains open afterward.

- **Native geometry after edge finishing:** 107 healthy case features / 11 fully constrained sketches / two solids; 335 healthy assembly features / 19 fully constrained sketches / 76 bodies. Default printable geometry matches between sources: base **46,302.918 mm³**, lid **20,138.088 mm³**. Independent union-minus-round/chamfer expectations are **46,303.046 / 20,138.094 mm³**, within the 0.02% volume tolerance. Outside bounds are unchanged. The eight rigid joints remain fully constrained, without conflicts or floating components.
- **Installed clearance, before edge finishing:** 70 conservative hardware boxes and 480 refined cubic-Bézier wire hulls were checked against both actual case solids: **1,100 hardware/wire-to-case pairs, zero interference, no unchecked pairs** after retrying one exhausted three-second pair budget. The base/lid pair was also clear. Wire hulls were expanded by 0.60001 mm to contain the 1.2 mm insulation; their boxes do not overlap unrelated hardware boxes. The antenna distance proof covers the new wires, not an all-metal RF keepout. The integral-floor beam repair and subsequent exterior rounds/chamfers remove material only, leaving the clearance-checked geometry a superset; they cannot introduce a new hard interference. This is not physical-fit qualification.
- **Visual inspection:** finished print-pose isometric plus installed transparent isometric and top views. The desktop ends on the saved populated assembly.
- **STLs:** each is one connected, closed, consistently outward-oriented edge/vertex-manifold shell. Bounds are **108 × 74 × 42 mm** for the base and **108 × 74 × 24.4 mm** for the lid; both are independently centred at Z=0. Mesh volumes match native geometry within 0.02%.

**Saved-source regression checks passed after edge finishing:** the case completed **52 states / 17 parameter endpoint walks**, and the populated assembly completed **55 states / 18 walks**, restoring all defaults. Checks cover timeline health without errors or warnings, fully constrained sketches, independent case volumes including the analytic round/chamfer subtraction, actual snap/USB geometry, PCB headroom, connected wire endpoints, component placements, eight rigid joints, and both centered manifold STLs. The supervised combined run completed successfully in **42 minutes**. Lid finishing is deliberately immediately after `Lid plate`, before its registration features and assembly placement: end-of-history corner picks produced geometry-fallback warnings when `case_length` changed. Physical print fit, release force, cable bend, thermal bias, VOC baseline and wireless performance remain untested hardware acceptance items.

The currently installed CLI writes a newer native format than the desktop can read: use it for read-only checks, **not `--save` on these sources**, until the executable versions match. Continue native edits/saves through the desktop MCP bridge.

`check.py` and `check_assembly.py` are read-only native checks, not design generators. Use them only after the saved native sources and exports reflect this geometry. From repository root, run under a finite, whole-group supervisor and the shared heavy-verification lock, for example:

```sh
systemd-run --user --collect --wait --pipe --working-directory="$PWD" \
  --unit="room-sensor-check-$(date +%s)-$$" \
  --property=RuntimeMaxSec=60m --property=KillMode=control-group \
  flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" \
  sh -c 'python3 models/room_ambient_sensor/check.py && python3 models/room_ambient_sensor/check_assembly.py'
```

Regenerate missing STL exports from the saved case-only native design, exporting only the base and lid. Center each mesh independently in XY and place its minimum Z at 0. Never export the populated assembly wholesale or include hardware/reference bodies. The currently installed CLI must not save either native source.
