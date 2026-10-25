# Modeled internal thread facets unrelated exterior cylinder and changes its bounds (0.21.0)

Draft for upstream discussion; **not submitted**.

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

These are commands for a maintainer to run; no CAD operation was rerun while preparing this report.

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

Thus the measured x extent is approximately 19.9964009013 mm and y extent approximately 19.9994626748 mm, rather than the nominal 20 mm. The radius shortfall at the positive x/y extrema is approximately 0.00179955 / 0.00026866 mm. The absolute deviation is small, but it is on an exterior surface that the internal thread should not affect.

The all-planar face classification, together with the reduced x/y extrema, supports the observed whole-body faceting rather than merely a cosmetic viewport tessellation change. The inspection's separate `kernel` counts are preserved in the attachment; they differ from the top-level counts and are not treated as interchangeable.

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

The modeled thread was accepted as a practical tradeoff for this design. The upstream question remains whether unrelated analytic surfaces can be preserved; if whole-body approximation is required, please document its scope and tolerance so users can plan downstream edits.

## Opening the native context and attaching the report

1. Extract the complete per-issue ZIP, keeping `thread-body-faceting/` and its sibling `shared/` directory together so the relative links in this report work.
2. Open `shared/endcap_native_unfinished.solidcraft` directly in SolidCraft. No STL, STEP, source-generation script, or external model reference is needed.
3. Allow the native timeline to rebuild if required: the 32 features include an expensive modeled `nativeThread`. Opening is not claimed to be instantaneous or proof of a reusable cached result.
4. Inspect the unrelated walls and the screw-recess breakout regions shown above. Because the final seam fillet is absent, merely opening this file is **not** a reproduction of a fillet panic; use that report's original checkpoint and operation commands for the crash case.

For the faceting/bounds reproduction, run the original **coupon commands above** from `thread-body-faceting/`, not against the larger endcap. Attach the complete per-issue ZIP to the upstream report: it bundles this issue's original JSON evidence, the native context model, and the screenshots. This is preparation only; no issue has been submitted.

## Evidence and limitations

- `thread-probe.json`: self-contained original successful JSON command sequence.
- `observed-results.json`: selected existing output objects (thread feature inspection and final body measurements) from the successful `thread-001.log`; explicitly an excerpt, not a newly generated run.
- The nominal ±10 mm baseline follows from the radius-10 cylinder input. This successful probe did **not** record a measured pre-thread body inspection, so the baseline is not presented as an observed before/after measurement pair.
- The similarly named `coupon.json` in the original working files is another input script, not result data. Its associated `coupon-v1` attempt returned lock exit code 75 and its log was empty; neither supplies evidence for this report.
- The shared native model and screenshots are later real-design context, not replacements for `thread-probe.json` or evidence of a measured coupon before/after pair.
- No local re-execution was performed while packaging. Cross-platform behavior, other thread sizes, cosmetic threads, and whether this is an intentional implementation tradeoff are unknown.
- No claim is made here about end fading, thread-profile correctness, or failure of a boolean operation. Accepting the modeled thread geometry for a particular design does not resolve the unrelated exterior-precision question.

The two original JSON attachments remain sufficient to rerun and compare the coupon; the additional native model and screenshots make the downstream editing context inspectable without substituting a large-model reproduction for the minimal case.
