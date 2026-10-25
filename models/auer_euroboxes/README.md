# AUER Eurobox references

Local third-party reference geometry for planning a cupboard around AUER's nominal **400 × 300 mm** solid Euro containers. These STEP files are downloaded source references, not generated exports or native parametric SolidCraft designs.

## Files and provenance

`reference/` contains 24 original STEP files: **75, 120, 170, 220, 270 and 320 mm** heights, each with closed, front-open, long-side-open and all-open handle configurations. The original `Eurobox - Auer (design table).pdf` accompanies them. Filenames are preserved, including the author's `[similar]` accuracy marker. CAD variants do not establish current product availability.

- Author: **Gergely DEGI**.
- Source: [Euro containers / boxes (Auer), GrabCAD](https://grabcad.com/library/euro-containers-boxes-auer-1).
- Intake date: **2026-10-25**.
- Download archive: `~/Downloads/euro-containers-boxes-auer-1.snapshot.5.zip`, retained unchanged; other footprints are not extracted here.
- Usage: GrabCAD's inspected terms provide non-commercial internal-use rights, not unrestricted redistribution. `reference/` is Git-ignored; do not commit or republish these assets without appropriate permission.

## Modeling limits

Intake verification: all 24 STEP files and the PDF match their archive members byte-for-byte. All STEP files have valid Part 21 opening/closing markers, with four variants for each of the six heights. Git ignore matching was verified for `reference/`. This does not validate geometry or CAD import.

The author warns that dimensions beyond AUER's main dimensions may differ from reality. Use these files for approximate layout, not validated rim/rail contact or fabrication geometry. No geometric tolerance or load rating is established by the files' presence.

The real boxes are **PP**, not the project's default PETG. These purchased-box references are not intended to be printed, so print pose is not applicable. Imported units, pose, body count and actual bounding dimensions remain to be checked in SolidCraft; file-integrity checks are not geometric validation.

When creating the cupboard design, keep the box height selection and side/rear/overhead clearances explicit. Preserve the purchased box's mating interfaces; measure rim underside, underside bearing footprint, ribs, corners and loaded deformation before designing close-fitting supports. Do not infer wall thickness or stacking pitch from catalogue interior dimensions.

See [manufacturer specifications and initial cupboard decisions](../../docs/auer-eurobox-400x300-specifications.md) and [CAD sources, licensing and accuracy limits](../../docs/auer-eurobox-cad-availability.md).
