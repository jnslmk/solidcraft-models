# Room ambient sensor: Wemos board and DHT22 fit research

Researched 2026-10-28. Dimensions are mm. Scope: controller, upright temperature/humidity module, perfboard stack, connectors and enclosure keepouts; the separate gas sensors are covered elsewhere.

## Identification and evidence limits

- **User identification is authoritative: this is a Wemos D1 board.** The photograph `/home/jonas/Downloads/PXL_20261028_093930665.jpg` shows a compact blue board, a projecting ESP-module PCB antenna, a USB cable at the opposite end, and a small perfboard carried above the controller on tall headers. **[INFERENCE]** This is a **D1 mini-format ESP8266/CH340 board or compatible clone**, not the Uno-sized D1 R1/R2. The exact Wemos revision, clone vendor and USB connector cannot be read reliably from this view.
- **[INFERENCE]** The upright white slotted sensor on a separate dark PCB is a DHT22/AM2302 **breakout assembly**. It is not merely the bare four-lead white sensor, and not the larger wired AM2302 enclosure. The upright PCB adds height below the white body, plus solder/header projections.
- **[INFERENCE]** The close-up resembles a standard **D1 mini prototyping shield**, rather than an arbitrary 42 × 36 perfboard. Wemos' official shield photograph shows the corresponding compact shield form; a seller gives approximately **28.5 × 26**, with a **2.54 mm grid**. [15, 16] This is a source-based identification, not a measurement or proof of clone identity. Hand-assembled header heights, solder protrusions, DHT placement and wire bends remain unverified.

## Controller variants: do not exchange these footprints

| Assembly | Published nominal size | Evidence/confidence and applicability |
|---|---|---|
| **LOLIN/Wemos D1 mini v3.1.0** | **34.2 × 25.6 PCB footprint** | **High** for the official board: Wemos technical-specification table; Micro-USB and CH340-driver link are on the same page. No assembled height is specified. [1] |
| **LOLIN D1 mini v4.0.0** | **34.2 × 25.6 PCB footprint** | **High** for official v4: same footprint, but **USB-C** and an extra LOLIN I²C connector. Official dimension drawing is linked. Do not use its connector geometry for an older/clone board. [2] |
| **AZDelivery D1 mini V3, ESP8266-12F/CH340C** | **34 × 26 × 8** advertised module dimensions | **Medium–high** for that seller's board, not this specimen. A useful common clone reference. Page explicitly names CH340C and Micro-USB; advertised 8 mm height must **not** substitute for the photographed socket/perfboard stack. [3] |
| **Wemos D1 R2 / Uno-format** | **68.6 × 53.4** | **Medium**, seller specification rather than original Wemos mechanical drawing. Approximately twice the mini's length; Uno-like outline/header arrangement differs visibly. Not the photo's likely form. R1/R2 are not interchangeable mounting patterns; no R1 mechanical fit is asserted. [4] |
| **NodeMCU LoLin V3 versus Amica V2** | Common seller nominal **58 × 31 × 13** versus **48 × 26 × 13** | Comparison only, **not the corrected enclosure assumption**. AZDelivery identifies LoLin as CH340 and Amica as CP2102; these are long NodeMCU boards, unlike the mini. The sizes appear in seller-indexed product descriptions; rendered pages currently omit dimensional tables, so do not use these as precision mechanical drawings. [5, 6] |

**Chip is not board:** Espressif specifies the ESP8266EX silicon package as **5 × 5 QFN32**; that is neither the ESP-12 module nor the D1 mini development board and is irrelevant as a board-fit dimension. [7, §1.2] A CH340 marking identifies the USB bridge, not a unique PCB outline: both compact D1 minis and larger NodeMCU variants use it. [1, 3, 5]

## DHT22 / AM2302 package and breakout dimensions

| Form | Nominal dimensions | Fit interpretation |
|---|---|---|
| Common bare four-lead DHT22 white body | **15.1 wide × 25 high × 7.7 deep**; **2.54 pin pitch** | Adafruit's sensor guide explicitly gives body size and pin pitch. **Medium–high** for this common package, not a guarantee for all Aosong revisions/clones. Leads and any breakout PCB are additional. [8] |
| Narrow three-pin breakout sold by ProtoSupplies | **37 × 16 PCB** | **Medium–high** for that product: seller explicitly labels these as PCB dimensions, not assembled depth. Includes a 3-pin `+ / OUT / −` header and external jumper cable. Similar general form to the photo, but not identified as the same PCB. [9] |
| IDUINO ST1173 DHT22 breakout | **40 × 23**, unspecified depth | **High** that the manufacturer's manual states this size; **low** that it matches the photograph. Shows why a generic “DHT22 module” cannot be assigned the bare sensor's footprint. Manual does not precisely define connector inclusion. [10] |

**Source conflicts:** an older Aosong-authored DHT22 sheet lists “small 14 × 18 × 5.5” / “big 22 × 28 × 5”; these are different package forms and do not establish the white body's size seen here. [11] The current Aosong AM2302 product page also provides a manufacturer outline graphic, confirming the four-pin slotted-body form, but does not identify the photographed breakout. [12] Adafruit's product-385 page currently lists **27 × 59 × 13.5**, conflicting with its own guide; do not silently use that outlier as the bare body's dimension. The guide's explicit 15.1 × 25 × 7.7 is the provisional common-package reference. [8, 13]

## Provisional CAD assumptions and fit allowances

These are **design reservations, not measured hardware sizes or guaranteed fit**. Axes below: controller length runs USB → antenna, width is across its two header rows, height is normal to its PCB. Keep them editable; do not turn this photograph into fixed hole coordinates.

| Reservation | Recommended starting value | Reason / limitation |
|---|---|---|
| Mini PCB surrogate | **35 × 27** | Rounds official 34.2 × 25.6 upward for an unidentified mini clone. This is the board object, before cavity allowance. |
| Clear board pocket | **37 × 29 minimum** | Adds 1 mm per side to surrogate; PETG fit recommendation, not supplier tolerance. Use removable edge retainers / a tray rather than an unverified hole pattern. Do not bear on components, solder or antenna. |
| Earlier perfboard / lower stack plan envelope | **42 × 36** | Conservative reservation around the compact board, shield edges, pins and jumper housings; retained as allowance history, **not the populated model's PCB dimensions**. The populated shield defaults to **28.5 × 26** from the standard-shield inference. [15, 16] |
| Upright DHT breakout reservation | **42 high × 24 wide × 12 deep**, above its attachment datum | Covers the cited 37 × 16 and 40 × 23 planar variants with a provisional depth allowance. Connector engagement and cable sweep remain additional; actual board might exceed this. |
| Entire controller/perfboard/upright solid-stack headroom | **65 above the lowest assembly point** | **[INFERENCE]** Allows roughly 20 mm for controller/stack plus 42 mm upright breakout and a small margin. The photo does not verify the 20 mm stack height. Measure the actual highest solid part and header/solder underside before locking it. |
| As-photographed loose wire-loop headroom | **80 initially**, measured from same lowest point | **[INFERENCE]** Separate reservation for the visible tall flexible loop, not a rigid-component dimension. It may need more; rerouting laterally is preferable to compressing it under the lid. Do not force the loop onto the DHT sensor or antenna. |
| Under-PCB insulation gap | **3 minimum below the lowest pin/solder projection**, not just below the PCB face | Engineering allowance; avoid solder points touching PETG under load. Support only verified bare PCB edges or mounting lands. |

The **42 × 36 × 65** solid-stack reservation is only the controller/sensor bay: it excludes the separate MH-Z19B, the antenna exclusion zone, USB plug/cable space, lid/floor/wall thickness, and the 80 mm wire-loop reservation. It is not an enclosure outside size. A very low-profile enclosure cannot preserve the pictured upright assembly without reorienting/rewiring it.

### USB, reset and servicing

- Put the USB end at an enclosure wall; keep its axis and insertion path clear. **Do not cut a “USB-C” opening merely because current Wemos documentation is v4**: v3 uses Micro-USB, and the photograph does not expose the receptacle sufficiently to prove its type. [1, 2]
- For an unidentified **Micro-USB plug**, reserve a provisional **14 wide × 10 high opening** and **25 axial clear space beyond the receptacle** for the plug overmould/strain relief, then a non-kinked cable route. These are engineering allowances, **not USB connector-standard dimensions or verified dimensions of this cable**. An open-sided cable notch in a removable lid avoids a need to thread a large plug through a tight aperture. Confirm the actual overmould before finalizing the port.
- Keep the board's reset switch accessible through a removable cover or a generous service opening located from the actual board. Do not invent reset-button coordinates from the official v4 board, and do not let retention clips press it. Provide vertical extraction room to unplug the stacked perfboard and jumper housings without levering the sensor body.
- The perfboard can hide USB/reset components. Retainers must capture the controller, not clamp the perfboard stack together by pressing on solder joints or connectors.

### Antenna keepout

Espressif recommends putting a module's PCB antenna beyond the carrier-board edge. If that is not possible, **the antenna and the 15 mm region beyond it must have no copper, tracks or components**, and the module must not be covered by a metal shell. This is a **baseboard RF-layout requirement**, not a specified 15 mm air gap from every plastic wall. [7, §1.6.2]

For this enclosure, conservatively keep the protruding antenna tip toward an outer PETG wall and reserve a **15 mm conductor-free zone around the exposed antenna region**: no MH-Z19B metal can, screws, brass inserts, metal mounting plate, perfboard copper or wire bundle alongside/over it. This is an enclosure-design interpretation of the source, not a tested RF guarantee. Do not stack the separate gas sensor over the antenna. Plain unfilled PETG is the intended material; keep carbon/metal-filled plastic away from RF. Antenna performance in the assembled enclosure still requires a real-device check.

### DHT thermal isolation and ventilation

Aosong specifically directs designers to keep the sensor far from heat-generating electronics, **below the heat source**, with good enclosure ventilation; reduce PCB copper heat conduction and leave a gap. It also warns about chemical vapours, strong sunlight/UV and condensation. [14, §8.2–8.4; 11, §8]

Consequences for this hardware:

1. The photographed DHT **above** the ESP/perfboard is mechanically compact but thermally unfavourable: **[INFERENCE]** rising warm air can bias room temperature and humidity. Ventilation alone cannot guarantee removal of that bias.
2. Best arrangement, if rewiring is allowed: place the DHT module at a lower, directly ventilated outer wall, separated from the ESP regulator and MH-Z19B. A starting **10–15 mm air separation** is a design allowance, **not an Aosong-specified minimum**. A thin PETG partition can divert the electronics' rising plume, but must not seal off the DHT pocket.
3. If preserving the upright stack is mandatory: place broad side openings directly opposite the DHT grille, provide lower air entry and upper exhaust, and avoid a solid shelf or cap immediately covering the slotted body. Allow **at least 3 mm air space around the grille** as a provisional mechanical allowance; no manufacturer-validated vent area or accuracy claim is available for this enclosure.
4. Do not glue the grille shut or mount the sensor against a thick wall. Avoid adhesives, sealants and solvent/cleaner vapours near the sensing element; keep it out of direct sunlight. No weatherproof or condensation-resistant claim follows from a ventilated PETG case.

## Populated native fit model

[`../models/room_ambient_sensor/room_ambient_sensor_assembly.solidcraft`](../models/room_ambient_sensor/room_ambient_sensor_assembly.solidcraft) models the **connected** Wemos/shield/upright-DHT/SGP41 stack, then rotates that entire stack −90° about Y into the enclosure; the sensors are not detached to obtain clearance. The blue SGP41 breakout carries its sensor on the underside in the reference model. Four flexible leads are routed laterally between the same modeled endpoints instead of preserving the photographed high arch; **colour does not verify electrical pin mapping**. USB overmould, lead bends and hand-soldered geometry are estimates, not supplier drawings.

Default shield dimensions are `perfboard_length=28.5` and `perfboard_width=26`, adjustable over 28.5–30.5 and 26–28 respectively. Local shield centre Y is −4.5; `perfboard_z=13.4` (12.5–14) describes its photographed-flat datum, while `dht_carrier_height=40` (37–40) accommodates the uncertain carrier. Installed stack origin is [16.2, 0, 23.4], with `stack_z=wall+8 mm+perfboard_width/2`; the default shield lower edge is Z=10.4. These ranges expose uncertainty, not guaranteed fit limits.

The case's controller supports were raised from 3 to **8 mm above the floor (top Z=10.4)** and guides from 5 to **10 mm (top Z=12.4)**. MH-Z19B support height stays **Z=5.4**; its ledges are at Y=−13.4 and +6.6 to meet the short PCB, not the terminal extension. That support-only correction added 1,800 mm³; the subsequent snap-fit cutover removes screw/tie geometry and adds releasable PCB-edge retention for the intact stack and MH end lands. Enclosure outside dimensions do not change. The [model README](../models/room_ambient_sensor/README.md) documents the current snap geometry, tolerances, nine-component assembly, inspection views and exercised checks. No measured physical fit, thermal accuracy or RF performance follows from this reference model.


## Sources

1. Wemos, official **D1 mini v3.1.0** specifications, Micro-USB and documentation links: https://www.wemos.cc/en/latest/d1/d1_mini_3.1.0.html
2. Wemos, official **D1 mini v4** specifications and dimensional drawing link: https://www.wemos.cc/en/latest/d1/d1_mini.html ; drawing: https://www.wemos.cc/en/latest/_static/files/dim_d1_mini_v4.0.0.pdf (drawing text could not be extracted; no hole/connector coordinates were taken from it).
3. AZDelivery, **D1 Mini V3 ESP8266-12F/CH340C**, 34 × 26 × 8 and Micro-USB: https://www.az-delivery.de/en/products/d1-mini-v3
4. Open Impulse, **Wemos D1 R2 Uno** seller dimensions and photos: https://www.openimpulse.com/blog/products-page/product-category/wemos-d1-r2-uno-esp8266-wifi-development-board/
5. AZDelivery, **NodeMCU LoLin V3/CH340**: https://www.az-delivery.de/products/nodemcu-lolin-v3-modul-mit-esp8266
6. AZDelivery, **NodeMCU Amica V2/CP2102**: https://www.az-delivery.de/products/nodemcu
7. Espressif, **ESP8266 Hardware Design Guidelines v2.8**, §1.2 package, §1.6.2 / printed pp. 15–16 antenna guidance: https://documentation.espressif.com/esp8266_hardware_design_guidelines_en.pdf
8. Adafruit, **DHT11, DHT22 and AM2302 Sensors — Overview**, explicit body dimensions/pitch: https://learn.adafruit.com/dht/overview
9. ProtoSupplies, **DHT22 Humidity / Temperature Sensor Module**, PCB dimensions and connector description: https://protosupplies.com/product/dht22-humidity-and-temp-sensor-module/
10. IDUINO, **ST1173 User Manual**, manufacturer document mirrored by Reichelt, p. 2: https://cdn-reichelt.de/documents/datenblatt/B300/ST1173.pdf
11. Aosong, **DHT22 datasheet**, original manufacturer-authored document mirrored by SparkFun, §3 and §8: https://cdn.sparkfun.com/assets/f/7/d/9/c/DHT22.pdf
12. Aosong, current **AM2302** product page and manufacturer outline image: https://www.aosong.com/en/Products/info.aspx?itemid=2294&lcid=139 ; image: https://www.aosong.com/uploadfiles/2025/04/20250416093734276.jpg
13. Adafruit, product **385** page, dimensional conflict noted above: https://www.adafruit.com/product/385
14. Aosong, **AM2302 Product Manual**, manufacturer-authored document mirrored by Seeed, PDF pp. 9–10 / §8: https://files.seeedstudio.com/wiki/Grove-Temperature_and_Humidity_Sensor_Pro/res/AM2302-EN.pdf
15. Wemos, official **D1 mini prototyping shield**, product photograph used for form-factor comparison: https://www.wemos.cc/en/latest/d1_mini_shield/protoboard.html
16. Rozakos, **Protoboard Shield Wemos D1 Mini Double Sided**, seller reference for approximately 28.5 × 26 mm and 2.54 mm grid: https://www.rozakos.com/product/protoboard-shield-wemos-d1-mini-double-sided/
