# Rolling Eurobox cupboard

Editable source: `rolling_cupboard.solidcraft`. A new, independent single-column layout; the existing three-bay cupboard is unchanged. Ten 400 × 300 mm purchased crates: **four 120 mm high below six 75 mm high**. Front is Y−, Z is up, floor at Z=0. This is furniture, not a printable part; materials are spruce/pine, plywood, purchased PP crates and metal/TPE casters.

## Dimensions and construction

- Timber frame: **356 W × 448 D mm**; total height including casters/pads: **1479 mm**. External simplified bracing increases the plan envelope to **364 × 452 mm**. This is not a verified caster swivel/brake envelope.
- Four **24 × 44 × 1300 mm** posts, 24 across X and 44 along Y. Posts run Z=135–1435.
- Top/bottom rectangular rings: four **24 × 44 × 356 mm** front/rear rails and four **24 × 44 × 400 mm** side rails. Rings occupy Z=91–135 and 1435–1479. Rails are modeled as flush butt joints, not overlapping or notched stock. Their connection hardware is not designed or represented.
- Twenty **20 × 20 × 448 mm** longitudinal pine runners, two per crate. Four **80 × 80 × 18 mm** plywood corner pads at Z=73–91 spread the caster plates onto both bottom-ring members.
- Four swivel casters: two front braked and two rear unbraked. Verified product envelope: 50 mm wheel diameter, 73 mm overall mounting height, 60 × 60 mm plate, 46 mm listed hole spacing, 6.2 mm mounting holes, 80 kg rating per caster. Hole pattern/bolts are not modeled. Twin 18 mm wheel tracks, fork, swivel and brake are simplified original geometry; 12 mm wheel trail and 3 mm plate thickness are assumptions, not supplier dimensions. The supplier's rating is **not** a cupboard load rating.
- Rear and both sides have conceptual **20 × 2 mm metal X tension straps**, separated at their crossings. Strap anchorage, tensioning and sizing need a connection design. The front stays open. Bracing is necessary because the earlier cupboard depended on wall restraint; these drawn straps do not establish structural adequacy.

Approximate timber procurement: **four 2500 mm lengths of 24 × 44 mm**, each yielding one 1300 mm post plus one 356 mm and one 400 mm ring rail; **five 2000 mm lengths of 20 × 20 mm**, each yielding four 448 mm runners. These patterns allow 3 mm saw kerf and 20 mm end trimming, but no defective-stock allowance. Add plywood pads and suitable joint/runner/caster/bracing hardware after connection design.

## Crate support and editable dimensions

`bay_w` defaults to **308 mm**, intended range **304–308**; `frame_d` is **448 mm**, range **440–460**; `head_gap` is **29 mm**, range **29–34**. Replacing the uppermost two deep crates frees 90 mm, distributed over ten handling gaps to retain the **1479 mm** overall height. Section sizes, caster height and crate heights are fixed purchased interfaces, not fit knobs. Geometry uses expression-driven primitives with no unconstrained sketches. Ten crate slots are explicit timeline features; changing the crate count requires adding/removing levels and revising the derived top elevation, not merely changing a count parameter.

Runner top is 12 mm above each crate's lowest feet. Feet elevations, bottom first: **143, 300, 457, 614, 771, 883, 995, 1107, 1219, 1331 mm**. The next runner underside and final top ring have **29 mm** vertical clearance above each crate. Highest crate top is Z=1406. The 400 mm-deep crates are centered in the frame.

The simplified original crate has a nominal 300 × 400 mm top rim, 280 × 380 mm bearing underside, 260 × 360 mm foot ring, and an assumed 12 mm bearing height. Its cavity is 270 × 370 mm, walls 5 mm; foot relief extends 1 mm into the nominal 5 mm floor, leaving a central 4 mm floor. It is not measured manufacturer mould geometry and not the previous model's detailed crate. At default bay width, the 268 mm opening between runners gives **4 mm foot clearance and 6 mm underside overlap per side**. At 304 mm, these become 2 mm and 8 mm. Maximum rim-to-post side clearance is 4 mm per side at default, 2 mm at minimum.

**Measure the real crates before cutting:** underside contact, foot/rim clearance, moulding tolerances and loaded sliding are unknown. Nominal crate dimensions alone cannot establish a safe bearing surface. Runner fasteners must be selected for 20 mm stock without splitting. No working-load rating, safe drawer extension, anti-tip provision, joint/fastener capacity, braking performance or loaded stability has been established. A 1.48 m-high narrow rolling frame can tip with an extended loaded box; CAD bracing and caster brakes are not proof against tipping. Do not treat this layout as construction-approved.

## Product sources

- [Hornbach KONSTA planed spruce 24 × 44 × 2500, article 1000459](https://www.hornbach.de/p/konsta-kantholz-fichte-gehobelt-2500-x-44-x-24-mm/1000459/).
- [Hornbach KONSTA pine 20 × 20 × 2000, article 5485724](https://www.hornbach.de/p/konsta-quadratstab-kiefer-roh-2000-x-20-x-20-mm/5485724/) — same runner stock as the previous small-runner cupboard.
- [Tarrox braked swivel caster 6644769](https://www.hornbach.de/p/tarrox-transport-geraete-lenkrolle-feststellbar-mit-platte-60-x-60-mm-bis-80-kg-50-x-73-x-18-mm/6644769/), quantity two.
- [Tarrox unbraked swivel caster 6644766](https://www.hornbach.de/p/tarrox-transport-geraete-lenkrolle-mit-platte-60-x-60-mm-bis-80-kg-50-x-73-x-18-mm/6644766/), quantity two.
- [Manufacturer nominal 400 × 300 × 75/120 mm Euroboxes](https://www.alutec.net/produkte/eurobehaelter-kunststoffbehaelter/). No downloaded third-party CAD is embedded.

## Checks and deliverables

`check.py` is a read-only check of the authoritative saved native design, not a generator. It walks the three adjustable dimensions to their endpoints and back, checks clean timelines, crate bounds/volumes, runner contact elevations and clearances, timber dimensions/volumes, and caster pad/plate placement. Run under a session-owned expiring process group and the workstation heavy-verification lock:

```sh
timeout --signal=TERM --kill-after=10s 15m flock -w 60 "${XDG_RUNTIME_DIR:-/tmp}/omp-heavy-verification-${UID}.lock" uv run --no-project models/rolling_eurobox_cupboard/check.py
```

Native model: **74 bodies**, **130 timeline features**, no sketches. Inspection images and numerical evidence are disposable under `.codex-tmp/rolling-eurobox-20261027/`. Generated assembly and timber-only STL files are under `exports/rolling_eurobox_cupboard/`; these are assembly-layout references, not a recommendation to print the cupboard. Native source remains authoritative.

Verified on 2026-10-27 after replacing the uppermost two deep crates: saved-native reload and all eight parameter-walk states passed the geometry check. All four 120 mm and six 75 mm crate bounds/volumes and all twenty runner elevations matched independent expectations. The frame remains 1479 mm high. The ten crates and 32 timber members had no solid interference. The revised isometric view was inspected, both STL exports were regenerated, and the saved updated model remains open in the user's SolidCraft window. These are CAD checks, not physical or structural validation.
