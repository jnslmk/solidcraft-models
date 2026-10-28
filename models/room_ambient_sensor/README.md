# Room ambient sensor enclosure

Ventilated **140 × 90 × 58.4 mm assembled** tabletop enclosure for a Wemos D1 mini, its existing perfboard/upright DHT22 assembly, attached SGP41 breakout, and separate MH-Z19B. Material: unfilled **PETG**. This is an indoor, non-weatherproof enclosure, not a certified sensor housing.

## Files and researched hardware

- Authoritative editable source: [`room_ambient_sensor.solidcraft`](room_ambient_sensor.solidcraft). Native named parameters and timeline features; no alternate generator.
- Populated native assembly: [`room_ambient_sensor_assembly.solidcraft`](room_ambient_sensor_assembly.solidcraft), with installed hardware references and inspection views; **not a printable assembly export**.
  The case-only file remains authoritative for printing; the assembly contains matching case geometry as an editable fit snapshot. Refresh both case components and repeat the fit checks after changing the printable design.
- Printable parts: [`../../exports/room_ambient_sensor/base.stl`](../../exports/room_ambient_sensor/base.stl) and [`lid.stl`](../../exports/room_ambient_sensor/lid.stl). Generated exports are intentionally untracked. Each STL is centered independently, at Z=0.
- Cited controller/DHT research: [`../../docs/room-sensor-board-research.md`](../../docs/room-sensor-board-research.md).
- Cited gas-sensor research: [`../../docs/room-sensor-gas-research.md`](../../docs/room-sensor-gas-research.md).

| Component | Published dimensions used, mm | What remains uncertain |
|---|---|---|
| Wemos D1 mini | Official PCB 34.2 × 25.6 | Mini-format identification is a photo inference. Clone, USB version and tall headers are not measured. Not for the 68.6 × 53.4 Uno-format D1 R2. |
| Connected prototyping shield | Default PCB **28.5 × 26**, 2.54 grid | **[INFERENCE]** Close-up resembles the standard D1 mini prototyping shield; seller size is not a measurement of this clone or its hand assembly. |
| DHT22 / AM2302 | Common white body 15.1 × 25 × 7.7; example breakout PCBs 37 × 16 or 40 × 23 | Default carrier height 40; exact breakout, mounting height and solder protrusions are unknown. |
| MH-Z19B | Nominal 33 × 20 × 9; Winsen terminal-equipped drawing **39.30 ±0.30 overall length** | Upright jumper housings and lead bends are additional. The white terminal is included even when unused. |
| SGP41 | Sensor package 2.44 × 2.44 × 0.85; generic breakout example 13 × 10.5 | Package is not the board. Reference geometry places the sensor on the underside of the blue four-pin breakout; dimensions, hole and actual air clearance remain photographic estimates. |

**Fit is provisional, not measured from the photograph.** Check the actual assembly against the occupied envelopes below before a full print. Online component drawings cannot establish the custom stack or loose wire geometry.

## Layout and mounting

Coordinates refer to the native base; X left/right, Y USB/antenna, Z print-up. The base is centered about X/Y. Its floor is Z=0–2.4, inner side walls X=±67.6, Y=±42.6. In the case-only source the lid sits beside it at X=160 for editing/printing; in the populated assembly it is seated. Do not print the entire side-by-side native layout as one object on a smaller plate.

1. **Rotate the intact Wemos/perfboard/DHT/SGP41 stack onto its edge**, rather than detaching the sensors to fit. The photographed-flat stack is rotated −90° about Y, with local origin placed at **[16.2, 0, 23.4]**. Wemos USB-to-antenna direction runs along Y, USB toward −Y and antenna toward +Y. The formerly upright DHT projects toward −X into the ventilated cool bay. This does not inherently require desoldering; flexible wires are rerouted laterally between the same modeled endpoints, not left as the tall loose arch. **Wire colours do not establish electrical pin mapping; mapping is unverified.**
2. Put the controller stack between the central guide rails. Guides remain **10 mm high above the floor (top Z=12.4)**. Two insulating supports are **8 mm high (top Z=10.4)**, matching the rotated shield's lower edge. Two lower face locators surround its unobstructed front bare PCB edge with **0.35 mm per-face clearance**. The former **42 × 36** footprint was a conservative stack reservation, **not the actual modeled PCB**.
3. The DHT carrier passes through the top-entry opening in the **X=−26…−24** thermal baffle. Opening **22 mm across Y**, open above Z=9.4. Earlier carrier/sensor reservation **X=−49…−2, Y=−10…10, Z=12…36** is not a measurement of the populated reference geometry. Keep the white sensing grille uncovered, with at least 3 mm local air clearance. The baffle redirects the main heat plume but does not stop heat conduction through the existing PCB or guarantee temperature accuracy.
4. Seat the MH-Z19B on its two PCB ledges at X=50.6, support **Z=5.4**, ledge centres **Y=−13.4 and +6.6**. Four releasable catches capture the **32.5 × 20 PCB** at its exposed end corners; the former loose cradle side/end walls have been removed. The terminal-equipped envelope remains **39.3 mm long**; the gold chamber is **26.53 × 19.5**. An installed 7-way plug would need extra axial space if you switch from the photographed jumper wiring.
5. **No screws, inserts, straps or ties are needed for primary retention.** The complete controller/DHT/SGP stack snaps in at the perfboard's top edge; the MH snaps act only on accessible PCB end lands, never the gold chamber. All screw posts, pilots, lid clearance holes, tie slots and underside strap channels have been removed from both native sources.
6. The SGP41 remains on its existing carrier; there is no second clamp or invented mounting-hole pattern. Reserve approximately 16 × 16 × 12 around that breakout within the parent-stack bay. The reference sensor is on the breakout underside: verify its real sensing face and a short open lateral air path, provisionally ≥3 mm. If the real stack blocks it, a hardware change may be needed; the fit model does not silently detach or reorient it. Enclosure ventilation cannot fix an occluded sensor package.
7. Keep the antenna pointing toward +Y, with a **15 mm conductor-free region** around its exposed end: no gas chamber, wire coil or metal fasteners. The new retention parts are plain PETG, not an RF shield; actual Wi-Fi performance is untested.

The USB/RESET service window has a **40 mm-wide × 26 mm-high rectangular lower portion**, starting Z=5.4; a 45° pitched upper opening reaches Z=51.3. It admits the USB overmould and a reset tool without relying on unknown switch coordinates. Removing the lid provides full switch/connector access. There is about 21.6 mm axial space from the provisional controller's USB-side edge to the inner wall; long plug strain reliefs can project through the large window. Check the actual cable and avoid sharp bends outside the case. The opening is not a cable strain-relief clamp.

Route excess jumper length along the available front/back perimeter space, not over the DHT grille, gas windows, antenna or lid rim. Do not force the original arch down. A 5 mm low baffle passage at Y=18…30 provides an optional wire route; it is not a cable clamp. Reroute wires if their natural bend exceeds the available clearance.

### Releasable snap retention

- **Lid:** four independent PETG cantilevers project **22 mm** from the inner plate, **1.2 mm** thick. Three are 6 mm wide; the fourth is 3 mm wide to use the intact land between antenna and side vents. Assembled catch centres are **X=−23 and −13 at the USB/front wall (−Y), and X=−23 and `rear_latch_x=case_length/4−5.5` at +Y**. The lid's print-pose Y coordinates are reversed because fitting it rotates it 180° about X. Registration tabs brace only the first 2 mm of three tongues; the remaining lengths have actual free space to bend inward.
- Each lid hook has a **45° lead-in, 0.7 mm radial undercut engagement**, **0.35 mm beam/wall clearance**, and an externally accessible release window. The windows are **8 × 1.5 mm** for the wide catches and **4 × 1.5 mm** for the narrow catch; their upper edge allows **0.30 mm lid lift** before retention contact. Press the hook inward with a roughly 1 mm flat tool while lifting that corner, then release the remaining catches. Do not lever against a vent rib.
- **Connected ESP stack:** two **1.2 mm-thick** vertical cantilevers at the perfboard's Y ends catch its upper bare PCB edge. They retain the entire electrically connected Wemos/perfboard/DHT/SGP assembly, without separating those modules or clamping components/solder. The rear beam is derived from **`max(perfboard_end_y, 10.16 mm)+pcb_clearance`** so it clears the SGP header spacer throughout the checked shield-size range. Push the two hooks away from the PCB (±Y) to remove the intact stack.
- **MH-Z19B:** four **1.2 mm-wide floor-plane cantilevers**, each **18.4 mm free length**, support integral upright catches at **Y=−19.2…−17.6 and +10.7…+12.3**. Through-floor reliefs leave **1.8 mm clear space on either side**, and an end gap: these are genuinely flexible beams, not floor-bonded bumps. Their tops stand 0.2 mm above the 2.4 mm floor. Push the posts outward in X, preferably one end pair at a time, while lifting the PCB. The front/rear bare lands remain at least **0.935/0.835 mm** away from the chamber ends; terminal and jumper bodies are not capture surfaces.
- PCB catches have **0.7 mm edge overlap**, **0.35 mm lateral clearance**, **0.25 mm vertical clearance** above the PCB, and 45° insertion ramps. Seat the PCB edges on their supports, not the sensor packages. Release access is from above with the lid removed. Four **1.2 mm-diameter × 3 mm-high** MH PCB end locators leave 0.35 mm axial clearance without touching the white terminal.

**Printed-fit limits:** snap dimensions assume the modeled bare lands really are clear of solder, components and coating buildup. That is not established by the photograph. Measure those lands and board thicknesses before printing, and make a small PETG beam/hook coupon using these section dimensions and your own extrusion compensation before fitting electronics. Do not force an unmeasured clone into a snap.

The conservative small-deflection estimate is **ε ≈ 1.5·t·δ/L²**. At defaults, lid bending uses δ=1.05 mm and an effective 17 mm root-to-hook length: **0.65% strain**; the combined independent lid endpoints reach **1.40%**. MH floor beams give **0.56% default**, **1.02% at the combined endpoints**. The worst connected-stack estimate is below **0.34%** (rear spacer clearance included). These are geometric estimates, **not PETG fatigue, creep or interlayer-strength qualification**; the tall MH posts also load their roots torsionally. With the lid printed flat, its upright tongue roots bend across layer interfaces; avoid brittle/wet filament and repeated over-deflection. Do not leave the beams flexed/preloaded in service, and do not call this a shock-rated mount.


## Inspecting the populated assembly

The assembly has **9 native components**: Enclosure base, Enclosure lid, Wemos D1 mini, Connected perfboard, DHT22 upright module, SGP41 attached breakout, MH-Z19B wired module, Interconnection leads, and USB power cable. The base is grounded; **8 as-built rigid joints** hold the installed placements. Its **76 bodies comprise 2 printable case bodies and 74 hardware/reference bodies**. Hardware shapes, two pairs of Dupont housings, four coloured 1.2 mm jumper wires, and USB plug/cable are fit references, not fabrication-ready electronics models.

- Open the populated `.solidcraft` file for the **installed** fit. Base opacity **0.23** and lid **0.12** expose the contents without removing the case.
- Select saved views **Populated fit isometric**, **Populated fit top**, or **DHT side clearance** for repeatable inspection.
- Use exploded views **Lid lifted for inspection** (lid +70 Z) or **Connected hardware outside enclosure** (hardware +75 Z, lid +145 Z). These are display-only offsets, not installed positions; return to the assembled state before judging fit.
- Default adjustable estimates include `perfboard_width=26` (26–28), `perfboard_length=28.5` (28.5–30.5), `perfboard_z=13.4` (12.5–14, local photographed-flat datum), and `dht_carrier_height=40` (37–40). Shield local centre Y is −4.5; installed `stack_z=wall+8 mm+perfboard_width/2`. Changing these estimates can change clearances; the defaults do not certify the real hand assembly.


## Editable driving parameters

All lengths are mm. Ranges are documented design limits, not enforced input validation. Vary them independently; `wall`, stack placement, rear latch position, lid placement and vent count are fixed/derived design quantities.

| Parameter | Default | Checked range | Relationship |
|---|---:|---:|---|
| `case_length` | 140 | 136–152 | X envelope, MH supports/catches, lid, rear latch land and vents follow it |
| `case_width` | 90 | 86–98 | Y envelope, baffle and lid snap mating faces follow it |
| `case_height` | 56 | 54–64 | Base/baffle and release-window elevation; assembled height adds 2.4 |
| `lid_clearance` | 0.35 | 0.25–0.60 | Beam/registration clearance **per side**, not total gap |
| `co2_width` | 23 | 22–26 | Width of the two PCB support ledges; actual 20 mm PCB catches stay fixed |
| `perfboard_width` | 26 | 26–28 | Supported PCB height and top catches follow the intact stack |
| `perfboard_length` | 28.5 | 28.5–30.5 | PCB end catch/locator alignment |
| `perfboard_z` | 13.4 | 12.5–14 | Connected-stack separation; snaps follow the PCB's X position |
| `lid_snap_t` | 1.2 | 1.0–1.4 | Lid flexure radial thickness |
| `lid_snap_length` | 22 | 20–24 | Lid projection and matching release-window elevation |
| `snap_engagement` | 0.7 | 0.5–0.9 | Lid/PCB hook overlap; changes required assembly deflection |
| `pcb_clearance` | 0.35 | 0.25–0.50 | Per-face PCB clearance, not preload |
| `pcb_snap_t` | 1.2 | 1.0–1.4 | Connected-stack and MH flexure thickness |
| `mh_snap_length` | 18.4 | 17–20 | Free MH floor-plane beam length; roots/slots follow it |
| `pcb_top_gap` | 0.25 | 0.15–0.40 | Clearance above PCB to catch underside |

`wall=2.4` is fixed. Lid plate thickness is 2.4, with eight 2 mm registration tabs and four flexible latch tongues. **There is no screw interface or gravity-only primary mount.** Obsolete `post_x`, `post_y` and `co2_length` parameters have been removed. The 15-row table is present in both native files; the assembly additionally checks its 37–40 mm `dht_carrier_height` estimate.

## Print and use

- Print **one base and one lid**, separately, with their flat exterior faces on the plate at **Z=0; Z+ is print direction**. Lid registration tabs and latch tongues face upward while printing; flip the lid 180° about X when fitting it. STL bounds are **140 × 90 × 56** and **140 × 90 × 24.4**, respectively; the latter includes the 22 mm tongues, not a thicker closed enclosure.
- Starting settings: 0.4 mm nozzle, 0.2 mm layers, 4 perimeters, 5 solid top/bottom layers, 15–20% infill; use your filament's PETG profile. Ensure the 1.0–1.4 mm beams are solid perimeter paths, not sparse infill. These are unqualified starting settings.
- No generated supports are intended: side slots bridge **4 mm**, release windows bridge **8 mm maximum**, the USB roof is pitched 45°, and baffle carrier entry is open at the top. Default hook projection is **1.05 mm for lid/MH and 1.46 mm at the stack's spacer-clearing rear catch**; combined independent endpoints reach **1.50/1.40/1.81 mm**, respectively. Inspect these small ledges in the slicer and test the coupon; add locally removable support if your printer cannot hold them cleanly. Do not let a brim, elephant-foot expansion or supports fuse the MH relief slots; clean them before installing electronics. Avoid supports against sensing faces.
- Nominal vent geometry: 4 mm openings / 2 mm ribs, with lower and upper rails; lid exhaust is 18 slots at the default size, each 4 × 58. Broad ventilation sacrifices spill/dust protection. Leave roughly 10 mm or more around external sampling openings; do not place the case tight against a wall or cover it.
- Air freshly printed parts before installing gas sensors. Do not use internal glue, silicone, solvent cleaning residues or foam against the sensor openings. Sensirion does **not** qualify this PETG filament as outgassing-free.
- Position out of direct sunlight and away from radiators. Compare enclosed DHT readings against open-air readings after thermal equilibrium; no unmeasured firmware offset is supplied. MH-Z19B internal temperature is not the room-temperature reference. Physical fit, thermal bias, VOC baseline, cable bend and RF performance remain hardware acceptance checks.

## Verification

Both native sources were saved and successfully reopened through the installed desktop after the snap cutover:

- **Case:** **115 healthy timeline features, 11 fully constrained sketches, exactly two solids.**
- **Assembly:** **343 healthy timeline features, 19 fully constrained sketches, 9 components, 8 rigid joints, no floating components or joint conflicts; 2 printable plus 74 hardware/reference bodies.** Original wiring, hardware component topology, three named views and two exploded views are preserved.
- **Installed geometry:** shield PCB bounds **[1.2, −18.75, 10.4]…[2.8, 9.75, 36.4]**, Wemos PCB **[14.6, −17.1, 10.6]…[16.2, 17.1, 36.2]**. The shield rests at Z=10.4 and MH PCB at Z=5.4. Highest hardware remains Z=36.4, leaving **19.6 mm to the lid plate**. Lid tongues descend to Z=34 only near the perimeter; they do not redefine whole-board headroom.
- **Clearance proof:** **180 conservative envelope/case pairs** checked against the actual saved base/lid shapes, with **zero interference and no unchecked proxy pairs**: 70 hardware boxes against both case bodies, plus 20 local cubic-spline control hulls against both. Each hull includes four consecutive wire control points, expanded by the 0.6 mm cable radius; local B-spline convex-hull containment avoids both an unsafe sampled-wire claim and the excessive whole-route bounding box. The closed base/lid pair is also interference-free. Supporting/retaining contact surfaces are intentional; the hooks leave the specified unloaded axial gaps.
- **Flexure geometry:** actual B-rep side planes confirm all four MH beams have **1.8 mm lateral relief on both sides**, not merely a nominal slot parameter. The printed-fit/strain limitations above still apply.
- **Visual inspection:** case print-pose isometric/interior top and transparent installed assembly views. Temporary proof solids were deleted before saving/exporting; the desktop ends on the transparent installed isometric view.

Default base measured **75,070.721 mm³** versus **75,070.733 mm³ analytic**; lid **21,208.376 mm³** versus **21,208.376 mm³ analytic**. Both sources have matching printable geometry. Outside dimensions remain **140 × 90 × 58.4 closed**.

**Regression result:** the saved case passed all **46 states / 15 endpoint walks**, including actual catch points and both regenerated, centered, connected, closed, consistently oriented edge/vertex-manifold STLs. The saved assembly passed all **49 states / 16 endpoint walks**, preserving all bodies, component placements and joints and restoring defaults. A first endpoint run exposed rectangular end-locator join failures at 136 mm case length and 22 mm support width; the native locators were replaced by the round posts described above. The final full assembly walk passed after removing redundant curved-wire mass integrations; the finite supervisor allowance below covers the exercised runtime.


`check.py` independently integrates the box/triangle/cylinder unions (including USB/vent overlap), checks all 15 parameter endpoint walks (46 states) and measured native catch points, and validates both STL print poses, mesh topology and volumes. `check_assembly.py` checks all 16 assembly parameter walks (49 states), component/joint topology, installed placements, support heights, catch points and plate headroom. All body bounds and identity occurrence transforms are checked at every state; independent full world-property reports are compared at initial/restored defaults, avoiding duplicate integration of curved-wire mass properties at every endpoint. The conservative collision and B-rep relief proofs above were exercised separately. Tolerances are **0.002 mm** for dimensions and **0.02%** for volume. Neither check is a thermal, airflow, electrical, RF or PETG durability simulation, nor a measurement of the actual hardware.

The currently installed CLI writes a newer native format than the desktop can read: use it for read-only checks, **not `--save` on these sources**, until the executable versions match. Continue native edits/saves through the desktop MCP bridge.

`check.py` is a read-only native regression/mesh check, not a design generator. It requires `solidcraft-cli`, Python and the generated STL exports; no third-party Python packages. From repository root, run under a finite, whole-group supervisor and the shared heavy-verification lock, for example:

```sh
systemd-run --user --collect --wait --pipe --working-directory="$PWD" \
  --unit="room-sensor-check-$(date +%s)-$$" \
  --property=RuntimeMaxSec=45m --property=KillMode=control-group \
  flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" \
  sh -c 'python3 models/room_ambient_sensor/check.py && python3 models/room_ambient_sensor/check_assembly.py'
```

Regenerate missing STL exports from the saved case-only native design, exporting only `Base` and only `Lid`. Translate each mesh to its own XY centre and minimum Z=0 (the native lid is beside the base at X=160); the delivered STLs are already centered. Never export the populated assembly wholesale for printing or include hardware/proof bodies. Do not replace either native source with a checking script.
