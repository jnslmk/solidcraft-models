# Sliding AUER Eurobox cupboard

Revised 2026-10-25: use the user-requested arrangement with each crate’s lowest feet hanging into the clearance between the 24 × 44 mm ribs; the ribs support the flat underside surface 12 mm above the feet. The cupboard is widened from the earlier direct-foot-bearing version. No shelf boards or back panel.

## Envelope and layout

**1124 W × 420 D × 2000 H mm**, open front and back, excluding wall connections and leveling shims. Three bays are **316 mm clear**, with four 44 mm upright lines. Eight uprights stand at z=0. Front posts occupy y=0–44; rear posts y=376–420. No plywood, doors, roof, drawer slides or wheels are included.

Boxes face 300 mm nominal width × 400 mm nominal depth. Nominal side clearance is **8 mm per side**; nominal front/rear margin is 10 mm. Imported STEP envelopes are approximately 299 × 399 mm, giving 8.5 mm side and 10.5 mm front/rear clearance. Community models are approximate: measure the real boxes before cutting.

The approximate STEP models show a 264 mm-wide × 364 mm-deep lowest foot/perimeter and a flat horizontal underside bearing face **12 mm above the lowest feet**. The ribs are raised so their tops meet that underside face. With a centered crate and ribs projecting 24 mm into each bay, the opening between rib edges is **268 mm**: the 264 mm foot base has **2 mm clearance per side** and hangs between the supports, while the wider flat underside face bears on the ribs. This depends on third-party approximate CAD geometry, not certified AUER dimensions. Confirm real mouldings and loaded contact before use; no load capacity is established.

## Crate elevations

Three identical columns hold 21 boxes. All dimensions below are mm. The rib top is 12 mm above the crate’s lowest feet, aligned with the modeled underside bearing face. Ribs remain **24 mm across the bay, 44 mm vertical**, not turned flat. Each box has 20 mm clearance to the next rib below its bearing plane.

| Level, bottom first | Box height | Crate feet / bottom | Rib bottom | Rib top / underside bearing face | Clearance above box to next support or top crossbar |
|---|---:|---:|---:|---:|---:|
| 1 | 320 | 88 | 56 | 100 | 20 |
| 2 | 270 | 460 | 428 | 472 | 20 |
| 3 | 220 | 782 | 750 | 794 | 20 |
| 4 | 170 | 1054 | 1022 | 1066 | 20 |
| 5 | 120 | 1276 | 1244 | 1288 | 20 |
| 6 | 120 | 1448 | 1416 | 1460 | 20 |
| 7 | 75 | 1620 | 1588 | 1632 | 261 |

Top crossbars occupy z=1956–2000. Bottom crossbars occupy z=0–44. The highest crate reaches z=1695.

## Cut list and stock

| Part | Quantity | Finished size mm |
|---|---:|---|
| Uprights | 8 | 44 × 44 × 2000 |
| Width crossbars | 12 | 44 × 44 × 316 |
| Crate support ribs | 42 | 24 × 44 × 420 |

Buy **nine 2500 mm lengths of each selected HORNBACH section**. For 44 × 44 stock, cut eight lengths into one 2000 mm upright and one 316 mm crossbar each; cut four more crossbars from the ninth. For 24 × 44 stock, cut five ribs from each of eight lengths and two ribs from the ninth. With 3 mm kerf and 20 mm stock-end trimming, both patterns fit. No damaged-stock allowance is included.

The [BOM](eurobox-cupboard-bom.csv) lists timber, connectors and wall restraints. Timber subtotal remains **€128.25** at the previously observed listings; hardware and other costs remain unpriced. Boxes are not included in construction procurement quantities.

## Connections and safety

Crossbars fit between posts with one steel furniture angle at each end. Each rib attaches to front and rear upright side grain with a planning allowance of two 4 × 60 mm screws per end. Check screw manufacturer's spacing/edge distances, pilot drill, and offset opposing paths at shared posts. No load rating is claimed.

**Without the back panel the timber frame requires separate wall bracing against racking and tipping; do not use it as an unbraced freestanding rack.** The BOM includes four wall-bracing connection allowances at upper/lower outer rear posts, in addition to two anti-tip restraint kits. Wall connections must actually resist lateral racking and tipping; their design/rating and wall fixings depend on substrate and loaded furniture. Simple straps alone do not establish that bracing. Hardware is not geometrically modeled.

Before batch cutting or loading, verify fit, contact, sliding/withdrawal behavior and clearance on real selected crates, and check loaded timber deformation and fixing capacity. No extension stops or safe cantilevered-box loading are implied.

## Native assembly and checks

See the [native assembly README](../models/eurobox_cupboard/README.md). The updated editable copy is **`models/eurobox_cupboard/cupboard_slide.solidcraft`** and contains **62 timber parts + 21 approximate crate references = 83 components**, no shelves or back panel. The earlier `cupboard.solidcraft` file was preserved because it was open in the user's unbridged desktop session; it is not this updated slide layout. Parameters: bay width 316 mm (tested 316–320), frame depth 410–430 mm and height 1950–2050 mm. Overall width = 3 × bay width + 4 × 44 mm.

The native document embeds restricted third-party references and remains Git-ignored. The native document is authoritative; no generator is maintained. CAD contact/interference and dimension checks do not establish structural capacity or physical fit. Timber-only reference export: `exports/eurobox_cupboard/cupboard_timber_slide.stl`.
