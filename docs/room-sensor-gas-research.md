# Room sensor: gas-sensor mechanical and enclosure research

Research date: 2026-10-28. Dimensions in mm. Identification clue: `/home/jonas/Downloads/PXL_20261028_093930665.jpg`; no physical measurements were supplied. **Official component dimensions are not measurements of the photographed assembly.** Proposed clearances below are enclosure-design allowances, not manufacturer requirements.

## MH-Z19B CO₂ module

### Defensible dimensions and identification

The gold chamber, terminal socket and exposed header rows in the photograph are consistent with the MH-Z19B family. The photograph does not authenticate its manufacturer or revision. Winsen's official page gives **33 × 20 × 9 nominal**, but the **v1.7 mechanical drawing explicitly distinguishes terminal and pin versions**. Do not use the 33 mm headline length as the connector-equipped footprint. [W1, W2]

| Feature | Dimension / observation | Confidence and limitation |
|---|---|---|
| Gold chamber footprint | **26.53 ±0.25 × 19.50 ±0.25** | High: terminal-version drawing, W2 p4. Not the PCB/connector envelope. |
| PCB/end-tab length | **32.50 ±0.30** | High: W2 p4, both versions. |
| Terminal-equipped overall length | **39.30 ±0.30** | High: W2 p4. White socket projects past PCB. Relevant to photographed module even though its socket is unused. |
| Common headline module height | **9 nominal** | High as W1's nominal figure; solder, pin and attached connector heights must be added independently. |
| Bare pin-version overall vertical extent | **16.50** in drawing | High for W2 p4 drawing, not applicable as a measured height of this modified assembly. |
| Side header spacing | **2.54 ±0.10** pitch; **29.50 ±0.25** between opposing row centerlines | High: W2 p4. These are electrical pin locations, **not mounting-hole patterns**. |
| Photographed wiring | Upright black female jumper housings on both end pin rows; unused white socket remains fitted | High as visual observation. Exact jumper heights, wire bend radii and required loop height unknown. |

### Connectors, diffusion windows and retention

- Winsen documents a **7-position terminal** and separate pin-header connection arrangements. Terminal pin 3 is GND, 4 is Vin, 5 RXD, 6 TXD; other terminal pins are reserved. The header version exposes additional functions. Do not confuse the two pin maps or assume a JST series solely from appearance. The terminal drawing labels a 1.25 mm spacing, but does not identify a purchasable connector series. [W2 pp4–5]
- The official structure illustrations show **rectangular pale diffusion-window areas on the chamber top and side**. Keep both unobstructed; do not treat the circular embossed top feature as a screw boss. The photographed top window is partly obscured by the jumper housing/wires; the photograph alone cannot confirm its complete unobstructed area. [W2 p3; photo]
- Manufacturer instruction: **avoid pressure on the gilded plastic chamber from any direction** during installation/use; a small enclosure must be well ventilated, especially at the diffusion window. Keep away from heat, direct sunlight and other heat radiation. This is not a clamping surface or a mounting-screw location. [W2 §9.1–9.3]
- Support the **PCB underneath, away from solder/pins**, with loose locating stops and a removable keeper that cannot squeeze the chamber or cover either window. Avoid a tight snap-fit around the gold body. The exposed end holes are occupied electrical terminals, not available mounting holes. [Design recommendation based on W2 and photo]
- **Proposed body bay: 41 × 22 × 12 clear**, measured above the PCB support datum; this covers the published terminal envelope with assembly clearance, but not the upright jumper housings. Reserve **25 mm clear height above that support datum for the local module-plus-jumper area**, with an additional open wire-routing path above/alongside it. This 25 mm is a provisional allowance, **not a verified wire-loop envelope**; preserve the original leads without sharp folding. [Design allowance]
- Leave **at least 3 mm unobstructed local air space** around diffusion faces and put adjacent case slots directly beside them; do not make the sensor breathe through a long narrow internal tunnel. No quantitative minimum window clearance/free vent area is specified in W2; 3 mm is a design starting value, not a sensor specification. If the terminal is later used, allocate a separate **15 mm insertion/service zone beyond the socket mouth**, then check the actual mating plug. In the photographed jumper-only configuration that service zone need not enlarge the enclosure. [Design allowance]
- W1 and W2 disagree on some electrical/environmental values (for example average current and temperature range). Treat these as revision-dependent, not interchangeable guarantees. Both specify 150 mA peak; place the module away from the DHT22 and SGP41 rather than assuming negligible heat because its average consumption is modest. [W1, W2]

## SGP41: chip package is not breakout-board size

| Item | Defensible dimension | Confidence and limitation |
|---|---|---|
| **Official SGP41 sensor package** | **2.44 × 2.44 × 0.85**, 6-pin DFN, 0.8 terminal pitch | High: Sensirion datasheet §5. This is the tiny sensing component only. [S1] |
| Package gas opening | Typical **0.8 diameter**, offset on top surface | High: S1 §5. Do not dimension the enclosure around this tiny hole alone. |
| Common generic **GY-SGP41 breakout** | Seller nominal **13 × 10.5 PCB size** | Medium for that commercial board family; **low for exact match to photograph**. Retailer publishes this size; board images/colours/layouts vary. No original PCB manufacturing drawing found. [B1, B2] |
| Photographed blue breakout | One large mounting hole, four header solder joints, visible `SCL`/`SDA`/power labels | Visual observation only. Exact outer dimensions, PCB thickness, hole diameter/offset, header height, populated underside and revision **unverified**. |

The photograph shows the blue board's **silkscreen/header-solder side**, not a clearly identifiable exposed SGP41 sensing package. Its gas-facing orientation cannot be certified from this view; the populated sensor may face down toward the perfboard. **Do not add a top-facing case vent and assume it reaches the sensor.** Maintain a lateral air path beneath/around this breakout, or reorient its removable header-mounted board toward an outer vent if the physical assembly permits. [Photo inference]

The generic listings misleadingly call this a “CO₂” or “eCO₂” board. Sensirion specifies **VOC and NOx raw signals/indices**, not direct CO₂ measurement. Use seller listings only for candidate breakout dimensions, not sensor capabilities. [S1, B1]

### Air, thermal and material guidance

Sensirion's SGP4x design-in guide is the strongest enclosure source here: [S2]

- Place the sensor **close to the outer shell with a large, short opening**, ideally facing its sensing top toward that opening. Prefer the **coldest/lower part** of the device, away from CPU/Wi-Fi heat. The heated sensing element is temperature controlled, but warming nearby plastics increases their VOC emissions and can mask real room events. [S2 §§1–2]
- Isolate the sampling region from enclosure-internal VOCs where practical: a short local partition/vent plenum is preferable to a shared stagnant cavity above the ESP8266. A seal is discussed in S2, but **do not add arbitrary silicone, foam or glue**: material chemistry and curing matter, and S3 warns of harmful outgassing. For the already-stacked assembly, generous direct vents and an unobstructed local air path are more realistic than claiming a sealed sampling chamber. [S2 §2, S3 §§3, 7]
- Face the opening toward room air, not directly toward a wall/table; if it must face such a surface, Sensirion advises **about 10 mm or more** between the external sensor opening and that surface. [S2 §1]
- The SGP41 package consumes about **3 mA at 3.3 V** during measurement and has internal hotplates. S2's SHTxx guidance recommends separate sensing volumes where possible; otherwise roughly **20 mm separation plus thermal isolation**, with the temperature/humidity sensor lower than the gas sensor to avoid rising warm air. Applying that principle to this DHT22 is an engineering inference, **not a DHT22-specific certified clearance**. The existing compact stack limits separation; enclosure vents cannot eliminate conduction through the original assembly. [S1 §2.1; S2 §5]
- Protect from bright sunlight/artificial illumination; use shaded/louvered vents rather than a clear window aimed at the sensor. Operate without condensation; recommended SGP41 conditions are −10 to +50 °C and 0–90% RH. [S1 §§2.3, 2.6]
- The sensor has its own dust membrane: **no additional membrane is required**. Do not touch, remove, tape over or load its top; support only the breakout PCB. Additional fine filters slow gas exchange. [S2 §4; S3 §§5–6]
- Sensirion lists suitable examples such as PC, ABS, PTFE and PEEK, and warns that additives/adhesives can change compatibility. **The consulted documents do not qualify printed PETG or any specific filament.** Keep freshly printed parts, cleaning solvents and uncured adhesives away from the sensor; ventilate/air parts before installation and avoid internal glue where mechanical retention suffices. Do not claim a guaranteed PETG outgassing-free measurement. [S2 §2; S3 §§3–4, 7, 9]

## Recommended adjustable retention envelope

These are **provisional CAD parameters, not measured fits**:

1. **MH-Z19B:** reserve **41 × 22** plan envelope, with PCB-supported loose stops adjustable across **32–40 length / 19–22 width** according to what they touch. Retain the PCB, never compress the chamber. Allow **12 body height / 25 local wired height** above its support and a separate unobstructed wire-routing volume. Keep stops and keeper out of top/side window paths. No assumed fixed screw-hole attachment.
2. **Blue SGP41 breakout:** if a separate carrier is needed, reserve **16 × 16 × 12** for PCB, solder/header structure (excluding wires); use adjustable edge support spanning **10–15 mm** rather than a pin-perfect 13 × 10.5 pocket. Leave the sensing face and its surrounding airflow space open; reserve **3 mm minimum provisional air clearance** at that face, without inventing an official clearance spec. **Since this board is already attached to the perfboard, preferably retain the parent stack and provide only this keepout—do not add a second overconstraining clamp.** Do not commit its one visible hole to a screw until the hole and underside are measured.
3. **Must remain adjustable/unknown:** actual MH-Z19B variant, underside solder/pin projections, actual SGP41 breakout outline/thickness/hole coordinates, header seating heights, active gas-face orientation, and jumper loop height. None is made exact by the package datasheet. Photographic perspective and loose wiring prevent a fully verified physical-fit guarantee.

## Sources

- **[W1] Winsen manufacturer product page**, nominal module dimensions and revision-dependent operating data: https://www.winsen-sensor.com/sensors/co2-sensor/mh-z19b.html
- **[W2] Winsen MH-Z19B User's Manual v1.7, 2020-10-15**, p3 structure/window illustrations, p4 dimensioned drawings, pp4–5 pin maps, §9 handling/ventilation: https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19b-co2-manual(ver1_7).pdf — drawing pages inspected visually, not inferred from broken PDF table extraction.
- **[S1] Sensirion SGP41 datasheet v1.0, December 2021**, §§2, 5: https://sensirion.com/media/documents/5FE8673C/61E96F50/Sensirion_Gas_Sensors_Datasheet_SGP41.pdf
- **[S2] Sensirion Design-In Guide for Integrating SGP4x Gas Sensors v1.0, August 2020**, §§1–2, 4–5: https://sensirion.com/media/documents/C87B1A6C/616452A3/Sensirion_Gas_Sensors_Datasheet_GAS_SGP4x_Design-In_Guide_D1.pdf
- **[S3] Sensirion Handling and Assembly Instructions for SGPxx Gas Sensors v1.2, November 2020**, §§3–7, 9: https://sensirion.com/media/documents/C16AA7D5/6440F28E/GAS_AN_SGPxx_HandlingAndAssemblyInstructions_D1.pdf
- **[B1] Robot Pi Shop GY-SGP41 listing** (secondary commercial source, 13 × 10.5 size; not a mechanical manufacturing drawing): https://robotpishop.com/products/gy-sgp41-tvoc-co2-air-quality-gas-sensor-module
- **[B2] AliExpress generic GY-SGP41 listing/image** (secondary visual variant evidence, not evidence that this is the photographed PCB): https://fr.aliexpress.com/i/1005005632234038.html ; image https://ae-pic-a1.aliexpress-media.com/kf/S3d9e03725a6c42ea9ae50fbc8d3a2436U.jpg
