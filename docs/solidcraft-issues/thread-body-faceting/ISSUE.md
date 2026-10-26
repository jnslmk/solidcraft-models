# Modeled internal thread facets unrelated exterior cylinder and changes reported bounds (0.21.0)

Investigated 2026-10-25. **Known upstream issue; do not file a duplicate.** No issue or comment has been submitted from this repository.

## Investigation outcome and upstream tracking

- **Exact match:** [#3311, points 2–3](https://github.com/tangency-labs/solidcraft/issues/3311), open when checked, describes whole-body faceting, loss of other cylindrical bores, and difficulty with later fillets/chamfers.
- [#1250](https://github.com/tangency-labs/solidcraft/issues/1250) remains open; its [maintainer explanation](https://github.com/tangency-labs/solidcraft/issues/1250#issuecomment-6192324099) documents the faceted boolean. [#1395](https://github.com/tangency-labs/solidcraft/pull/1395) improves performance, not the resulting surface representation.
- [#4087's triage](https://github.com/tangency-labs/solidcraft/issues/4087#issuecomment-6352707615) explicitly confirms faceting of every curved face and recommends cosmetic threads while editing, modeling last only when needed for printing.
- [#3992](https://github.com/tangency-labs/solidcraft/issues/3992), open when checked, pauses kernel work while a replacement kernel is evaluated and asks users not to open new kernel issues/PRs/discussions. This is not a crash/data-loss report.

**Root cause confirmed in source:** in v0.21.0 (`65d288227ee212bb8633b173c6a0a125cafd0501`), [`FeatureKind::Thread`](https://github.com/tangency-labs/solidcraft/blob/65d288227ee212bb8633b173c6a0a125cafd0501/crates/doc/src/eval.rs#L6001-L6039) returns without modifying geometry for cosmetic threads, but modeled threads call `kernel::faceted_boolean` on the **whole input body** with tolerance `pitch * 0.005`. [`faceted_polys` / `faceted_boolean`](https://github.com/tangency-labs/solidcraft/blob/65d288227ee212bb8633b173c6a0a125cafd0501/crates/kernel/src/polybool.rs#L310-L404) tessellate curved input faces at that tolerance and reconstruct a body with planar faces only. This is an explicit implementation limitation, not an unexpected fallback or viewport-only effect.

For this 1.5 mm pitch, the body-faceting tolerance argument is **0.0075 mm**. It is not a guarantee of printed fit, an exact bound on every final coordinate, or the separate [thread-groove station/chord sampling](https://github.com/tangency-labs/solidcraft/blob/65d288227ee212bb8633b173c6a0a125cafd0501/crates/doc/src/eval.rs#L523-L535). Reducing a display/export mesh setting cannot restore analytic cylinders already replaced in the model.

Current `main`, checked at `2cf05388f1bc74979aa2e3529d213f1856c49715`, still has the [same thread call](https://github.com/tangency-labs/solidcraft/blob/2cf05388f1bc74979aa2e3529d213f1856c49715/crates/doc/src/eval.rs#L6841-L6880) and [whole-body faceting path](https://github.com/tangency-labs/solidcraft/blob/2cf05388f1bc74979aa2e3529d213f1856c49715/crates/kernel/src/polybool.rs#L310-L404). This is a source comparison, **not a runtime test of a newer build**.

**Disposition:** keep the native endcap unchanged. Cosmetic threads preserve editable analytic geometry but do not supply printable thread grooves. For the required printed thread, finish analytic operations first and model the thread last; this postpones the editing limitation, **not** the final faceting. Preserving unrelated analytic faces requires upstream kernel work; no model-level precision fix is claimed.

## Controlled comparison added 2026-10-25

New isolated headless probes add the previously missing measured pre-thread baseline and a cosmetic control. Neither the desktop document nor the attached endcap was opened or modified. The original two evidence files below remain unchanged.

| State | Positive x measured bound (mm) | Positive y measured bound (mm) | Logical face types |
| --- | ---: | ---: | --- |
| Before thread, after bore | 9.99984556213238 | 9.999763825245502 | 2 cylinders, 2 planes |
| Cosmetic thread | 9.99984556213238 | 9.999763825245502 | 2 cylinders, 2 planes |
| Modeled thread | 9.99820045062534 | 9.999731337406425 | 1,674 planes |

The cosmetic control preserves the complete measured body object, including volume **1460.0850040151802 mm³**, unchanged. The modeled thread yields **1378.7293780684506 mm³**; this volume reduction includes the intended groove and is not a measurement of exterior material loss.

The modeled positive-x/y measured extrema change by approximately **−0.00164511 / −0.00003249 mm** relative to the observed pre-thread baseline. Crucially, even the analytic baseline's reported extrema do not reach exactly ±10 mm. Therefore, the original nominal-to-final deviations below must **not** be attributed entirely to threading or interpreted as an independent exact measurement of exterior shrinkage. Loss of analytic surface representation is directly established by the face types and the source; the reported bounds also depend on measurement approximation.

Both probe runs and a saved-native reload exited 0, with no timeline errors/warnings and empty stderr. The reloaded modeled coupon matched its pre-save bounds, volume, area, face types, topology counts, and kernel counts exactly. Assertions checked the analytic baseline, unchanged cosmetic body, all-planar modeled body, changed measured extrema, clean timelines, and persisted geometry. No physical fit or export manifoldness was tested.

Reproduce in an isolated directory, using a finite-expiry process group and the workstation-wide heavy-verification lock as described in the parent README:

```sh
solidcraft-cli run cosmetic-probe.json --results --json-out cosmetic-results.json
solidcraft-cli run controlled-probe.json --results --save controlled-coupon.solidcraft --out controlled-coupon.step --json-out controlled-results.json
solidcraft-cli eval controlled-coupon.solidcraft --json-out reload-results.json
```

- `controlled-probe.json`: original coupon command sequence with one measured inspection inserted immediately before the thread.
- `cosmetic-probe.json`: same measured baseline with `modeled: false`; a control, not a printable-thread workaround.
- `investigation-results.json`: selected unchanged response objects from these new runs and the native reload, with provenance. Generated native/STEP files and full logs are disposable artifacts under `.codex-tmp/thread-faceting-20261025/`.

The remaining sections preserve the original report and distinguish its earlier evidence from the controlled comparison above.

## Environment

- SolidCraft CLI 0.21.0
- Linux x86_64
- Units: mm
- Minimal reproducer: headless JSON command script; no imported geometry or external files required
- Additional context: a self-contained, native-only saved endcap design and GUI screenshots (separate from the minimal coupon)

## Summary

Adding a modeled internal `M12.3x1.5` thread to a simple annular cylinder appears to facet the whole body, including the unrelated Ø20 exterior. The recorded final bounds no longer reach the nominal exterior radius of 10 mm, and the inspection reports only planar faces.

Is whole-body faceting an intentional limitation of modeled threads in 0.21.0, or should the unrelated analytic exterior be preserved? This report concerns an unexpected precision/geometry change, not thread-end fading or the acceptability of the thread profile itself.

The attached real endcap shows why preserving unrelated analytic surfaces matters for downstream editing, but it is **not** the coupon used for the small bounds deviation below. The endcap's recorded overall extents remained approximately **26.10000048 × 30.5 × 31.85 mm**; this report does not claim the same dimensional shrinkage for that model.

## Minimal reproduction

From this bundle directory, with `solidcraft-cli` 0.21.0 on `PATH`:

```sh
solidcraft-cli --version
solidcraft-cli run thread-probe.json --save coupon.solidcraft --out coupon.step --results
```

The supplied script is the existing successful coupon probe, preserved without changes to its command sequence:

1. Inspect the fresh document.
2. Create a radius-10 cylinder, height 6.5, base `[0, 0, 1.5]` (nominal z range 1.5–8).
3. Cut a Ø10.6762023679 bore, height 10, using the command's default base.
4. Apply a modeled `M12.3x1.5` thread, length 6.5, selecting the bore at `[5.33810118395, 0, 4.75]`.
5. Inspect the thread feature and measure the final document.

These describe the original probe; the new controlled comparison above was executed separately during investigation.

## Expected

The internal thread should not change the unrelated Ø20 exterior cylinder. Its nominal x/y bounds should remain ±10 mm and its unmodified exterior should remain analytic, unless whole-body approximation is an intentional, documented behavior.

## Actual recorded result

The existing successful CLI execution returned exit code 0. The thread feature reported `error: null`, `warning: null`, `suppressed: false`, and `rolled_back: false`.

The final `document.inspect` reported:

| Measurement | Recorded value |
| --- | --- |
| x minimum | -9.998200450625337 mm |
| x maximum | 9.99820045062534 mm |
| y minimum | -9.999731337406425 mm |
| y maximum | 9.999731337406425 mm |
| z minimum | 1.4999999999977045 mm |
| z maximum | 8.00000000000638 mm |
| Face types | `{"plane": 1674}` |
| Faces / edges / vertices | 1674 / 4183 / 2510 |

Thus the original measured x extent is approximately 19.9964009013 mm and y extent approximately 19.9994626748 mm, rather than the nominal 20 mm. The nominal-to-measured positive x/y shortfalls are approximately 0.00179955 / 0.00026866 mm. These are **not** measured pre-thread-to-post-thread differences; the controlled comparison above corrects that distinction.

The all-planar face classification establishes actual surface-representation loss rather than merely cosmetic viewport tessellation. The reduced reported extrema are consistent with approximation but do not independently establish exact exterior shrinkage. The inspection's separate `kernel` counts are preserved in the attachment; they differ from the top-level counts and are not treated as interchangeable.

## Real endcap context and downstream editing

The additional [saved unfinished native endcap](../shared/endcap_native_unfinished.solidcraft) contains **32 native timeline features, 14 sketches, and 1 body**. It is a self-contained editable SolidCraft design, **not an STL import or a native/mesh hybrid**. The final existing features are:

- #29 `Strap mouth fabric fillets`
- #30 `Plug tip corner fillets`
- #31 `Modeled M12.3x1.5 gland thread`
- #32 `Sew native threaded topology`

The intended final screw-recess breakout/seam fillets are **not included**. In the separate recorded endcap inspection after threading, the face classification was **9,834 planes and 1 cylinder**. That inspection is from an earlier checkpoint, not a new measurement of the attached saved file. It supports the concern about actual surface representation; the screenshots alone cannot distinguish kernel approximation from viewport tessellation.

![Native endcap overview with timeline and body](../shared/native-endcap-overview.png)

*Fully loaded GUI overview of the later saved native endcap. The tree provides design context; visible facet boundaries extend onto walls away from the gland thread. This is not a controlled before/after image or the minimal coupon.*

![Underside showing the two screw-access recesses](../shared/screw-access-underside.png)

*Underside overview locating both screw-access recesses and the adjacent exterior walls, unrelated to the internal gland thread.*

![Close-up of a screw-recess breakout at the exterior flank](../shared/screw-breakout-detail.png)

*Close-up of one recess where the cut breaks through the outside flank. This is the area intended for the missing finishing fillet, not a screenshot of a completed fillet.*

For downstream work, retaining unrelated analytic surfaces would avoid replacing a simple wall/curve with many small planar patches and edges when selecting and blending these breakout regions. However, **threading is not established as the sole cause of the unfinished fillet**: fillet attempts failed both before and after the thread, and the source analytic/native blend was also unsupported. Later constant-radius, adaptive, and taper attempts did not produce the desired seam fillet. Those geometric/capability diagnostics must not all be described as kernel panics. The images locate the editing problem; they do not independently prove a crash or STL topology defect.

The modeled thread was accepted as a practical tradeoff for this design. Investigation confirms that whole-body approximation is intentional in the current implementation and tracked upstream; preserving unrelated analytic surfaces remains unresolved.

## Opening the native context and attaching the report

1. Extract the complete per-issue ZIP, keeping `thread-body-faceting/` and its sibling `shared/` directory together so the relative links in this report work.
2. Open `shared/endcap_native_unfinished.solidcraft` directly in SolidCraft. No STL, STEP, source-generation script, or external model reference is needed.
3. Allow the native timeline to rebuild if required: the 32 features include an expensive modeled `nativeThread`. Opening is not claimed to be instantaneous or proof of a reusable cached result.
4. Inspect the unrelated walls and the screw-recess breakout regions shown above. Because the final seam fillet is absent, merely opening this file is **not** a reproduction of a fillet panic; use that report's original checkpoint and operation commands for the crash case.

For the faceting/bounds reproduction, run the coupon commands, not the larger endcap; prefer the controlled probes above for a measured before/after comparison. The complete per-issue ZIP bundles this issue's JSON evidence, native context model, and screenshots. Use it as supplementary evidence for existing #3311 if requested; do not open a duplicate. No issue/comment has been submitted.

## Evidence and limitations

- `thread-probe.json`: self-contained original successful JSON command sequence.
- `observed-results.json`: selected existing output objects (thread feature inspection and final body measurements) from the successful `thread-001.log`; explicitly an excerpt, not a newly generated run.
- The original successful probe did **not** record a measured pre-thread body inspection; its ±10 mm baseline is nominal input, not an observed value. The new controlled probe records that missing baseline.
- The similarly named `coupon.json` in the original working files is another input script, not result data. Its associated `coupon-v1` attempt returned lock exit code 75 and its log was empty; neither supplies evidence for this report.
- The shared native model and screenshots are later real-design context, not replacements for `thread-probe.json` or evidence of a measured coupon before/after pair.
- No local re-execution was performed during the original packaging. The later isolated comparison above exercises only installed 0.21.0, this thread size, and cosmetic versus modeled behavior; cross-platform behavior, other sizes, and newer-build runtime behavior remain untested. Whole-body faceting is now confirmed in source.
- No claim is made here about end fading, thread-profile correctness, or failure of a boolean operation. Accepting the modeled thread geometry for a particular design does not resolve the unrelated exterior-precision question.

The original two JSON attachments remain sufficient to rerun the original coupon. The added controlled probes and investigation results provide a measured baseline, cosmetic control, and persistence evidence. The native endcap and screenshots remain separate downstream-editing context.
