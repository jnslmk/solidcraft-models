# Shared current-native endcap evidence

`endcap_native_unfinished.solidcraft` is a byte-for-byte snapshot of the design
saved from the fully loaded desktop document as
`models/led_profiles/endcap_native_unfinished.solidcraft`. It is not a mesh or
an imported-geometry replacement. Its native history includes the modeled
M12.3×1.5 thread and topology-stitch feature. The final screw-breakout seam
fillets are missing; the file is deliberately named unfinished.

Opening this file may rebuild its 32 native timeline features, including the
modeled thread, and can take substantial time. Do not interpret the loading
progress dialog as an observed crash. No new CAD execution was performed to
prepare these attachments.

## Screenshots

- `native-endcap-overview.png`: fully loaded SolidCraft desktop showing the
  native model, tree and many exterior face boundaries after the thread feature.
  Captured after saving as `endcap_native_unfinished`. This is not a controlled
  before/after pair.
- `screw-access-underside.png`: user-supplied underside overview showing the
  central thread and the two smaller screw-access recesses.
- `screw-breakout-detail.png`: user-supplied closeup of one screw recess meeting
  the outside flange wall. The intended missing fillet is along that breakout
  junction, not around the entire circular rim, central hole or bed perimeter.

These screenshots establish appearance and location. They do not independently
prove a Rust panic, nonmanifold topology, or measured geometric deviation.

## Which design reproduces which finding?

The current native file is supplemental real-part context, especially for the
whole-body faceting report. Use the original per-issue inputs for the recorded
failures:

- Kernel panic: `kernel-intersection-panic/before-fillet.solidcraft` and its
  extracted operation scripts. That is an earlier analytic pre-operation state,
  not this post-thread native checkpoint.
- Thread faceting: `thread-body-faceting/thread-probe.json` is the minimal native
  coupon; the current endcap demonstrates the same visible whole-body behavior.
- STL defect: `stl-thread-seams/evidence/endcap_hybrid_baseline.solidcraft` and the
  preserved raw/control STLs are the measured exporter reproduction. Topology of
  a new STL exported from this current native file has not been assessed here.

`manifest.json` records source provenance, sizes and SHA-256 digests; `SHA256SUMS`
verifies the attached model and images. Local source paths are provenance only:
all attached `.solidcraft` inputs are self-contained.
