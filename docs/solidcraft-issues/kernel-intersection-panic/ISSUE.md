# Native fillet repeatedly panics in truck intersection_curve.rs before returning an unsupported-operation error

## Environment

- SolidCraft CLI 0.21.0 (installed binary reports `solidcraft-cli 0.21.0`)
- Linux x86_64; Linux 7.3.0-4-cachyos
- Headless CLI operating on native SolidCraft geometry

## Summary

A native fillet of the screw-access breakout seams of an endcap triggers repeated Rust panics in the vendored geometry kernel. The command eventually reports an unsupported blend/planar-face error. Unsupported geometry should produce a controlled diagnostic without panicking internally or repeatedly retrying the same panic path.

A separate attempt to join a native modeled-thread sleeve into the cap hit the same panic location. It is not established that both operations have the same root cause; this report's attachments focus on the fillet.

## Physical operation and downstream impact

The intended finishing operation rounds the **13 physical edges around the two screw-access recesses where their cuts break through the outer flanks** of the endcap. These are the screw-breakout seams, not the cable-gland thread edges and not the bed-contact rim. The original 14-pick command included one additional surface-parameter seam; the 13-edge isolation below preserves the physical finishing intent.

The unfinished result still lacks these seam fillets. Native downstream finishing is blocked: neither the original operation nor the isolated physical-edge selection produced the requested rounded breakouts. The primary bug here is the repeated internal panic, independently of whether this geometry is currently supported.

### Visual context (later native model, not the crash checkpoint)

![Current native endcap with model and feature tree](../shared/native-endcap-overview.png)

*Overview of the later saved native design. The model/tree locate the endcap and its thread; visible faceting is context, not evidence that the panic occurred.*

![Underside showing the two screw-access recesses](../shared/screw-access-underside.png)

*Underside overview: the two screw-access recesses are the regions of interest. The requested seam rounding is around their breakouts into the outside flanks, not around the whole bed-contact rim.*

![Closeup of one screw-access breakout into the outer flank](../shared/screw-breakout-detail.png)

*Closeup of one recess where the cut exits the outside flank. This identifies the intended missing finishing region; it is not an edge-selection overlay or a controlled before/after comparison.*

The accompanying [`endcap_native_unfinished.solidcraft`](../shared/endcap_native_unfinished.solidcraft) is a **later, different state**: native-only, 32 timeline features, 14 sketches and one body, with post-thread faceted topology. Its final features are #29 `Strap mouth fabric fillets`, #30 `Plug tip corner fillets`, #31 `Modeled M12.3x1.5 gland thread`, and #32 `Sew native threaded topology`. It does **not** contain the final screw-breakout seam fillet or its failing feature.

Use this saved design to inspect the intended part and unfinished regions, not as a replacement for `before-fillet.solidcraft` in the reproducer. Opening it may rebuild all 32 native features, including the expensive native thread; no instant/cached opening is promised. Neither these screenshots nor opening this later model proves the panic or STL topology, and no screenshot is a controlled before/after measurement.

## Reproducer

Extract the attached ZIP, keep the issue folder and sibling `shared/` folder together, and run from the `kernel-intersection-panic/` directory containing `operation.json`:

```sh
timeout --signal=TERM --kill-after=10s 120s \
  solidcraft-cli run operation.json --in before-fillet.solidcraft --results
```

This is one native `solid.fillet` command selecting 14 existing edges with radius expression `screw_seam_radius`. The native document contains the parameter and the pre-operation feature state. No STEP input, external component or source-project dependency is required.

The model has not yet been reduced to a small synthetic primitive example. `operation.json` preserves the failing edge selection exactly; some picks may include a coincident surface-parameter seam. Even if an edge selection is unsupported, the expected outcome is a structured rejection, not a kernel panic.

## Observed behavior

The original full-build invocation emitted repeated copies of:

```text
thread 'main' (...) panicked at vendor/truck-geometry/src/decorators/intersection_curve.rs:133:62:
called `Option::unwrap()` on a `None` value
```

It ultimately returned:

```text
error: step 368 (solid.fillet): not supported yet: the blend is larger than the neighbouring faces (site 387) (the operation failed: not supported yet: both faces next to the edge must be planar)
```

`observed.stderr` is the original captured log, not a fabricated output from the reduced one-command invocation. The saved checkpoint plus extracted operation have been preserved for reproduction, but that packaged one-command invocation has not been rerun solely to reproduce the crash. A run of the one-command script would number its command differently from step 368.

## Expected behavior

Either a valid native fillet, or a prompt structured error explaining the unsupported edge/face condition, without Rust panic messages and repeated kernel retries.

## Attachments and how to use them

Attach the complete prepared ZIP with this report, preserving its issue-folder-plus-`shared/` layout so the relative evidence links resolve when extracted. Include:

- `before-fillet.solidcraft`: original saved native pre-operation checkpoint; **this is the crash input**, not the later context design.
- `operation.json`: exact original 14-pick failing fillet command.
- `observed.stderr`: original full-build panic and final error output, with provenance described above.
- `operation-real-edges.json`, `observed-real-edges.stderr`, and `source-seam-proof.json`: original 13-physical-edge isolation and source comparison described below.
- `later-constant-003.stderr` and `later-taper-003.stderr`: supplementary later controlled diagnostics, not crash reproducer logs.
- `../shared/endcap_native_unfinished.solidcraft`: editable later native design for context, with no final screw-breakout seam fillet.
- `../shared/native-endcap-overview.png`, `../shared/screw-access-underside.png`, and `../shared/screw-breakout-detail.png`: the captioned context screenshots above. Upload these images alongside the ZIP as well if inline GitHub rendering is desired; local relative image links alone will not upload them.
- `SHA256SUMS`: attachment checksums.

Use the original checkpoint and original commands below/above for panic investigation. Do not replay their edge coordinates against the later, faceted context model as though it were the same topology.

No backtrace was captured in the original run. The message suggests `RUST_BACKTRACE=1`; a maintainer may use that when reproducing. No upstream issue has been submitted by this preparation.

## Follow-up isolation

The original selection contained one cone parameter seam adjacent to only one
face. Removing that seam leaves 13 physical edges. Applying the native fillet
to those 13 edges also emitted the same kernel panic and failed; therefore
the observation is not confined to selecting that parameter seam.

Additional preserved attachments:

- `operation-real-edges.json`: reduced native selection (fillet plus inspection).
- `observed-real-edges.stderr`: original output from that investigation; initial
  unrelated source-oracle deprecation warnings are retained for provenance.
- `source-seam-proof.json`: independent source-model 14-versus-13 comparison;
  identical volume and zero Boolean difference showed that excluding the
  parameter seam did not omit a physical source blend.

The reduced native invocation is:

```sh
timeout --signal=TERM --kill-after=10s 120s \
  solidcraft-cli run operation-real-edges.json --in before-fillet.solidcraft --results
```

This packaged invocation has not been replayed just to reconfirm the panic.

## Later finishing attempts: controlled errors, not additional panic evidence

Later attempts on the evolving native design also left the seam finishing incomplete, but their diagnostics must not be conflated with the original panic:

- A constant-radius `0.03 mm` attempt reported `error: step 2 (solid.fillet): not supported yet: the blend is larger than the neighbouring faces` (`later-constant-003.stderr`, copied from the existing `finish003.stderr` capture).
- A later tapered attempt with requested maximum `0.03 mm` reported `error: step 2 (solid.fillet): not supported yet: each end of the edge must touch exactly one more face` (`later-taper-003.stderr`, copied from the existing `stitched_taper003.stderr` capture).

These are supplementary original diagnostic captures from different later states, not additional standalone reproducers or evidence that taper caused a panic. They show why simply reducing the requested radius or trying taper did not complete the desired finishing; the original 14/13-edge checkpoint evidence remains the basis of this panic report.
