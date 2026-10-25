# AUER 400 × 300 mm Euro containers: reusable CAD availability

Research checked **2026-10-25**. Scope: standard solid-walled, open-top AUER Euro containers for cupboard layout; lids, ESD-labelled products and generic Euro-format crates are distinguished below. Sources were inspected through static pages, page source and public metadata/file-list APIs. No browser, account login, CAD application, model import or large archive download was used.

## Decision

**Updated decision, 2026-10-25: replace the restricted downloads with independently constructed native layout models.** Redistribution requirements rule out embedding the GrabCAD solids in the current cupboard. See the [native Eurobox model](../models/auer_euroboxes/README.md) and [updated cupboard](../models/eurobox_cupboard/README.md). Their geometry is original native construction from catalogue dimensions plus documented assumptions, not traced or converted third-party CAD. All six nominal heights are covered parametrically. Undocumented interfaces remain unverified; this is not manufacturer-certified geometry or blanket legal clearance. The source/access research below records the earlier reuse investigation; its download/reuse recommendations are historical, not the current workflow.

These are **not manufacturer-certified geometry**. The author explicitly marks them `[similar]` because dimensions beyond AUER's main dimensions may not correspond to reality. Use them as approximate layout/visual references, not as the source of exact rim-contact, rail, snap-fit or fabrication geometry. No public first-party 3D CAD download was found in the official category, inspected product pages or discoverable contact/catalogue links; that is **not proof that AUER has no CAD or cannot supply it on request**. [A1–A4, G1]

## 1. First-party AUER availability

| Official source checked | What was actually visible | CAD conclusion |
| --- | --- | --- |
| [Solid Euro container category][A1] | Product table/configurator, main dimensions, description, product-detail mechanism and links to related container families. | No public STEP, IGES, native CAD or mesh download located in the inspected page/source. |
| [EG 43/17 HG, 400 × 300 × 170 mm][A2] | Product dimensions and material; Product information includes safety/conformity items, PPWR certificate, **Hinge hole template**, and **Print version**. | No public 3D download located. The linked hinge template is a 2D PDF, not a complete container model. |
| [EG 21512 HG detail page][A3] | Same product-information pattern, including its own hinge template and print version. This is a smaller footprint, checked only to understand the official download convention. | No public 3D download located there either; not itself a candidate for this cupboard. |
| [Contact us][A4] | Enquiry form; page source links [PDF product catalogue][A5] and a [browseable 2023 catalogue][A6]. | A manufacturer enquiry is the direct route to ask for unpublished CAD. These catalogue links are not 3D CAD links; the full catalogue was not downloaded for this research. |
| [Official EG 43 hinge template PDF][A7] | One-page drawing titled **“Lochbild Eurobehälter EG43”**, with hole-pattern dimensions, PP material and drawing information. | Useful only for its stated hole-pattern purpose. It does not establish the rim cross-section or complete exterior geometry. |

Targeted web searches for AUER plus CAD, STEP, IGES, downloads and 3D data did not reveal an additional first-party 400 × 300 model portal. Search coverage is not exhaustive; country-specific/account-only resources and CAD supplied privately remain unknown.

**Useful enquiry:** request neutral STEP (preferred) or IGES for the exact purchased `EG 43/...` height, handle configuration and base design; ask whether the supplied model represents the current moulding revision and whether a dimensioned rim/support cross-section and relevant tolerances are available. No enquiry was sent during this research.

## 2. Best match: Gergely DEGI's AUER range on GrabCAD

- **Model:** [Euro containers / boxes (Auer)][G0].
- **Author:** **Gergely DEGI**, profile slug `gergely.degi-2`; created **2022-04-22**, according to the model's own metadata. This is a community upload, not an AUER publication. [G1]
- **Formats verified from actual file listing:** **77 `.STEP` files plus one `Eurobox - Auer (design table).pdf`** across all listed footprints. For **400 × 300**, there are **24 STEP files: six heights × four handle configurations**. No `.igs`/`.iges`, STL or native-CAD file appears in that listing. The website's combined **“STEP / IGES”** software label does **not** mean IGES files are present. [G2]
- **Coverage:** the description lists 400 × 300 × 75/120/170/220/270/320 mm as well as other footprints. Exact target-height filenames are independently present in the file list, so height coverage is not inferred from a search snippet. [G1, G2]
- **Access:** model metadata and file listing are public without an account. The tested 170 mm closed-handle STEP download endpoint returned **HTTP 401** anonymously. GrabCAD's own client code routes unauthenticated download actions to login. Treat actual file downloads as **account-gated**; successful download after login was not exercised. [G2, G3, G4]
- **Accuracy, author's statement:** “Auer only provide the main dimensions of their containers. The other dimensions on the models may not correspond to the reality. This is why I marked my boxes with the ‘similar’ flag.” That is a direct limit on geometrical trust, not merely a generic website disclaimer. [G1]
- **Rights:** no separate model-specific license was visible in the inspected description or file inventory. GrabCAD Terms §6.2 provides users a cross-license for their **own benefit and non-commercial, internal use**, including modification/derivatives; it is non-sublicensable/non-assignable/non-transferable. Do not interpret “free download” as public-domain or unrestricted redistribution/commercial permission. Keep downloaded third-party CAD out of a public repository unless permission has been established. [G1, G2, L1]

### Height-specific file selection

The following links are the **actual file-list download endpoints**, not promises of anonymous access. Log into [the model page][G0], open its files and select the named STEP file; the endpoints may still require the appropriate authenticated browser session. All filenames end in `[similar].STEP`. [G2]

| Nominal outer size, mm | Closed-handle filename in inventory | Listed STEP endpoint |
| --- | --- | --- |
| 400 × 300 × 75 | `40 x 30 x 7,5 - EG 43-75 HG (All closed) [similar].STEP` | [75 mm STEP][D75] |
| 400 × 300 × 120 | `40 x 30 x 12 - EG 43-12 HG (All closed) [similar].STEP` | [120 mm STEP][D120] |
| 400 × 300 × 170 | `40 x 30 x 17 - EG 43-17 HG (All closed) [similar].STEP` | [170 mm STEP][D170] |
| 400 × 300 × 220 | `40 x 30 x 22 - EG 43-22 HG (All closed) [similar].STEP` | [220 mm STEP][D220] |
| 400 × 300 × 270 | `40 x 30 x 27 - EG 43-27 HG (All closed) [similar].STEP` | [270 mm STEP][D270] |
| 400 × 300 × 320 | `40 x 30 x 32 - EG 43-32 HG (All closed) [similar].STEP` | [320 mm STEP][D320] |

For every height the same listing also contains **“Front side opened”**, **“Long side opened”**, and **“All opened”** versions, alongside **“All closed”**. Here these are the uploader's **handle-opening variants**, not open-front picking bins, perforated-wall boxes or lid variants. Their presence in CAD does not establish that AUER currently sells every combination, especially at 75 mm: match the current order configuration rather than treating the model inventory as a product catalogue. No lid model is present in this file inventory. [G1, G2, A1]

## 3. Alternative actual AUER model: 170 mm only

**[EG43/17 HG][H0]**, by **Eduard Osypchuk**, created **2020-10-30**. [H1]

| Question | Verified result |
| --- | --- |
| Height/footprint | Description and CAD filenames identify **400 × 300 × 170 mm**. No other target heights are listed. [H1, H2] |
| Actual geometry files | `EG 43-17 HG Pojemnik.STEP` and `EG 43-17 HG Pojemnik.SLDPRT` (**SOLIDWORKS native**). The other two files are a JPG and a PDF; no actual IGES or mesh file is listed. [H2] |
| Download | [Listed STEP endpoint][H3] returned **HTTP 401** anonymously. Public metadata/file list are accessible; expect account-gated downloads. [H1–H3] |
| License | No separate model-specific license visible in inspected metadata/listing; the same GrabCAD non-commercial/internal-use cross-license applies. [H1, H2, L1] |
| Accuracy | No measured tolerance, scan provenance or manufacturer validation stated. There are source inconsistencies: the description says **ESD**, but gives **PP** and silver-grey colour and links a standard solid-container product; it says handles “Opened” despite `HG` naming. The accompanying PDF/JPG names reference **64-17**, not **43-17**. [H1, H2] |
| Recommendation | Secondary 170 mm comparison/layout candidate, **not a higher-confidence reference for fabrication**. Its description gives stack interior height **143 mm**, whereas current official EG 43/17 HG lists **155 mm**; this discrepancy means the old text cannot override the current product specification. Geometry itself was not downloaded or measured. [H1, A2] |

## 4. Other leads assessed, not substitutes for the AUER range

### Generic Euro-format mesh

[Euro stacking container 400 × 300 × 150 mm][S1], **Daniel Rosehill**, published **2026-07-25**. The description states **GLB/glTF 2.0**, real-world scale in **metres**, origin at base centre; the public API verifies **2,484 triangles** and `isDownloadable: true`. This is **not identified as an AUER box** and covers only **150 mm**, not one of the standard target heights above. The file format is the creator's stated upload format, **not an inspected downloadable-file manifest**; no STEP/IGES/native CAD was verified. [S1, S2]

Its visible license is **CC BY 4.0**; the API explicitly says author credit is required and commercial use allowed. An anonymous request to the download API returned **HTTP 401**, so public viewing and “downloadable” do not establish anonymous file access. The creator's Euro-module/VDA dimensional narrative is not independent evidence of fit to an AUER moulding. This may serve as a generic rendered layout prop, but is inferior to the matching-height STEP range for this cupboard and unsuitable as AUER rim geometry. [S1–S3]

### Hinged-lid gallery lead

[Ragnar Gallery: Auer Euro Container][R1], visibly attributed to **Petar Pandžić**, describes a **hinged-lid**, reinforced-base crate with latches. The page displays **“Pro Export”** and “Export to STEP, STL, GLB, or DXF, depending on the model.” It does **not** expose an actual file inventory, confirmed 400 × 300 dimensions/heights, model-specific license, dimensional validation, or an anonymous download link in the inspected static page. The format list is a **conditional platform export claim**, not verified files for this model; the exact login/subscription requirement remains unverified. Not selected: wrong default variant and insufficient evidence of dimensions/accuracy. [R1]

Search also surfaced model aggregators/mirrors and printable dividers/holders. They were not substituted for the original author's actual box files: accessories are not whole-box geometry, and a mirror's format snippet is weaker evidence than the original GrabCAD file manifest.

## 5. Historical reuse assessment (superseded)

1. **Reuse for layout:** download the appropriate-height STEP from Gergely DEGI's original listing after login, choose the correct handles, and check units, orientation and overall dimensions before positioning it. For SolidCraft, neutral **STEP/IGES** is preferable to a triangulated visualization prop; the pinned [SolidCraft v0.22.0 README][SC1] lists these among supported exchange formats, **“where supported.”** Actual import/support for these particular files has not been exercised. The verified AUER candidates supply STEP, not IGES.
2. **Do not stretch one detailed box to invent another height:** all six sizes already exist in the verified listing. Keep the model's approximate status explicit. For unavailable access, a simple nominal envelope can support early space allocation without re-creating ribs and fillets; it is not a measured box model.
3. **Do not design a supporting lip/rail from these files alone:** request current manufacturer geometry/drawings or measure a physical sample of the exact box configuration, especially rim overhang, underside bearing surface, corner radii, base/rib protrusions and insertion clearance. Nominal 400 × 300 dimensions and a plausible STEP surface do **not** guarantee real-world fit or load-bearing contact.
4. **Only model measured missing geometry if necessary:** the present evidence removes the need to build the complete range now. A manufacturer refusal, inaccessible/licence-incompatible files, failed import, or a genuinely missing measured interface would justify a narrowly scoped new model later—not speculative duplication today.

## Sources

All links below were checked or discovered in the cited primary page/file listings on **2026-10-25**. Individual download endpoints were extracted from those listings; only D170 and H3 were requested to check the GrabCAD anonymous-access gate. No file-body accuracy checks were performed.

- **AUER:** [A1] category; [A2] 170 mm product; [A3] smaller product/download convention; [A4] contact; [A5] PDF catalogue link; [A6] browseable catalogue link; [A7] hinge drawing.
- **Range model:** [G0] model page; [G1] author/description metadata; [G2] complete file inventory; [G3] tested download gate; [G4] first-party client login/download logic.
- **Licensing:** [L1] GrabCAD Terms, particularly §6.2 and the accuracy disclaimer in §14.
- **170 mm alternative:** [H0] model page; [H1] author/description metadata; [H2] complete file inventory; [H3] tested STEP download gate.
- **Other leads:** [S1] generic mesh page; [S2] generic mesh API metadata/license; [S3] tested mesh download API gate; [R1] hinged-lid gallery.
- **Import context:** [SC1] pinned SolidCraft README.

[A1]: https://www.auer-packaging.com/en/Euro-containers-solid.html
[A2]: https://www.auer-packaging.com/en/Euro-containers-solid/EG-4317-HG.html
[A3]: https://www.auer-packaging.com/en/Euro-containers-solid/EG-21512-HG.html
[A4]: https://www.auer-packaging.com/en/Contact-us.html
[A5]: https://www.auer-packaging.com/pdf/auer-katalog_en_eur.pdf
[A6]: https://www.yumpu.com/en/document/read/67269159/auer-packaging-product-catalogue-2023-en-wo
[A7]: https://www.auer-packaging.com/pdf/drawings/eg_43_hole.pdf
[G0]: https://grabcad.com/library/euro-containers-boxes-auer-1
[G1]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1?extended=true
[G2]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files
[G3]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=33d2632a034211aa3a280b4ab8902a2f
[G4]: https://grabcad.com/assets/production/app/community_frontend/application-2d10d710465e6257cf3ee4c4cb5123279881f5389e0484c2152e88f232651fd1.js
[L1]: https://grabcad.com/terms
[D75]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=fc4b93ffa2d0056667c4021d1c918d9d
[D120]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=eb04e6dfd7ac17dc46580367f51dfe7d
[D170]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=33d2632a034211aa3a280b4ab8902a2f
[D220]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=5ac38b2ebe76420479ab112f9a117407
[D270]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=89bf6305bbeef20a9cfbfdd300fe629e
[D320]: https://grabcad.com/community/api/v1/models/euro-containers-boxes-auer-1/files/download?cadid=f6a5ccf2ac420fc0ee18fb33d085bf70
[H0]: https://grabcad.com/library/eg43-17-hg-1
[H1]: https://grabcad.com/community/api/v1/models/eg43-17-hg-1?extended=true
[H2]: https://grabcad.com/community/api/v1/models/eg43-17-hg-1/files
[H3]: https://grabcad.com/community/api/v1/models/eg43-17-hg-1/files/download?cadid=f7e5532166046ddc85fbcabc851e5466
[S1]: https://sketchfab.com/3d-models/euro-stacking-container-400-x-300-x-150-mm-16559b386cac4646aaee842be6d45b7c
[S2]: https://api.sketchfab.com/v3/models/16559b386cac4646aaee842be6d45b7c
[S3]: https://api.sketchfab.com/v3/models/16559b386cac4646aaee842be6d45b7c/download
[R1]: https://app.ragnar.build/gallery/nh7djtv9q58n5knv8ecjc5rqg18g53td
[SC1]: https://raw.githubusercontent.com/tangency-labs/solidcraft/v0.22.0/README.md
