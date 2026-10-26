# SolidCraft kernel transition: truck, SMLib and Solidcore

Research checked 2026-10-25 against official source, GitHub issues/PRs and the live Solidcore progress site. This is a source/documentation assessment, not a local execution of either alternative backend. No installation, build, CAD session, saved model or remote issue was changed.

## Bottom line

SolidCraft is evaluating a real replacement of its truck-backed geometry layer, not merely changing viewport tessellation. Solidcore is a **Rust port of NVIDIA's SMLib**, not an independently designed kernel. The integration experiments currently use the **C++ SMLib fork behind C shims**; the Rust port is intended to replace operations as differential parity is established. Neither the installed 0.21.0 nor the inspected stable 0.22.0/current-main source has switched to this backend. There is no demonstrated fix yet for this repository's modeled-thread faceting or screw-seam fillet panic.

## 1. What #3992 actually changes

[#3992](https://github.com/tangency-labs/solidcraft/issues/3992) is open and says kernel work is paused during evaluation. It asks contributors not to open new kernel issues, PRs or discussions, including booleans, blends, threads, import/export and tessellation. Existing kernel PRs were made drafts rather than discarded; reproductions are intended to feed the replacement kernel's regression suite. **Crashes and data loss remain explicitly welcome.** Work outside the kernel continues.

The older [#1597 roadmap](https://github.com/tangency-labs/solidcraft/issues/1597) points contributors toward Solidcore, but its 62%-ported figure is dated October 16 and is not current. It gives no delivery date. The later #3992 policy supersedes its broader invitation to file ordinary kernel reports.

The concrete integration work is [draft PR #4012](https://github.com/tangency-labs/solidcraft/pull/4012), tracking `kernel-smlib`. It explicitly says it **will not be merged as it stands**; work lands directly on that branch. The inspected branch head was [`1b7b9d8d88233c18071fe8d6f4da418a315935a6`](https://github.com/tangency-labs/solidcraft/commit/1b7b9d8d88233c18071fe8d6f4da418a315935a6), dated October 23. An open tracking PR is not evidence that the shipping app has adopted the backend.

## 2. The current SolidCraft kernel

SolidCraft's current kernel is **truck plus substantial SolidCraft-owned geometry code**, wrapped by `crates/kernel`. The application is not mesh-only: its geometry includes analytic and spline curves/surfaces and B-rep topology. SolidCraft implements additional booleans/fallbacks, blends, offsets, import/export and history/provenance around truck. See the [architecture](https://github.com/tangency-labs/solidcraft/blob/2cf05388f1bc74979aa2e3529d213f1856c49715/docs/architecture.md), [kernel boundary](https://github.com/tangency-labs/solidcraft/blob/65d288227ee212bb8633b173c6a0a125cafd0501/crates/kernel/src/lib.rs), and [current Boolean implementation](https://github.com/tangency-labs/solidcraft/blob/2cf05388f1bc74979aa2e3529d213f1856c49715/crates/kernel/src/ops.rs).

The latest stable release observed was **v0.22.0**, at [`0537623a75798f30e53ec976a61704defdf03011`](https://github.com/tangency-labs/solidcraft/releases/tag/v0.22.0). Its [Cargo dependencies](https://github.com/tangency-labs/solidcraft/blob/0537623a75798f30e53ec976a61704defdf03011/Cargo.toml) still include vendored truck components. The same is true of inspected `main`, [`2cf05388f1bc74979aa2e3529d213f1856c49715`](https://github.com/tangency-labs/solidcraft/tree/2cf05388f1bc74979aa2e3529d213f1856c49715). This checks source, not a locally installed/running 0.22.0.

Two different problems affect this repository:

- **Thread-body faceting is an explicit modeling path.** The [v0.22.0 thread evaluator](https://github.com/tangency-labs/solidcraft/blob/0537623a75798f30e53ec976a61704defdf03011/crates/doc/src/eval.rs#L6345-L6362) still calls `faceted_boolean` on the whole body with tolerance `pitch * 0.005`. The [polygon Boolean](https://github.com/tangency-labs/solidcraft/blob/65d288227ee212bb8633b173c6a0a125cafd0501/crates/kernel/src/polybool.rs#L310-L404) tessellates curved faces and reconstructs planar faces. It is not a display defect; finer rendering settings cannot restore the lost analytic surface representation. See the [local controlled investigation](solidcraft-issues/thread-body-faceting/ISSUE.md).
- **The fillet panic is a geometric failure with inadequate internal error handling.** The [vendored intersection-curve implementation](https://github.com/tangency-labs/solidcraft/blob/2cf05388f1bc74979aa2e3529d213f1856c49715/vendor/truck-geometry/src/decorators/intersection_curve.rs) contains unwraps of surface-projection results and an unimplemented second derivative. SolidCraft's kernel panic guard can contain a panic, but containment does not make the requested geometry succeed. The [local saved failing case](solidcraft-issues/kernel-intersection-panic/ISSUE.md) remains separate evidence; neither threading as its sole cause nor a replacement-kernel fix has been established.

“Exact B-rep” means surfaces and trims are represented geometrically rather than solely as flat triangles. It does **not** mean infinite-precision arithmetic or that every operation is supported. Both the current kernel and the proposed replacement use tolerances.

## 3. What Solidcore is, and what is actually implemented

The [pinned README](https://github.com/tangency-labs/solidcore/blob/337cbe6504a4955b6f1f58328f85f91a4636dc30/README.md) identifies Solidcore as an Apache-2.0 Rust port of SMLib from NVIDIA's `usd-brep`. Its scope includes analytic/NURBS geometry, topology, intersections, booleans, blends, shell/offset, sweeps, healing and mass properties. Upstream OCCT translators, USD/Hydra integration and Python bindings are out of scope. SolidCraft-side STEP work is therefore not automatically supplied by Solidcore.

The [core](https://github.com/tangency-labs/solidcore/blob/337cbe6504a4955b6f1f58328f85f91a4636dc30/crates/solidcore/src/lib.rs) uses B-rep-owned arenas and typed IDs; an explicit [`Kernel`](https://github.com/tangency-labs/solidcore/blob/337cbe6504a4955b6f1f58328f85f91a4636dc30/crates/solidcore/src/kernel.rs) carries tolerances, caches and deterministic RNG state instead of relying on upstream global state. The project forbids unsafe code in its kernel and targets deterministic results, controlled errors and WebAssembly. Its README also warns that recursive geometry algorithms still need an enlarged wasm stack. These policies are useful engineering safeguards, **not proof of geometric robustness or a universal no-panic guarantee**.

Its stated differential target is identical topology and numerical agreement with C++ within `1e-9` relative on tested inputs. This is **not** a universal dimensional accuracy or manufacturing tolerance. Matching a reference implementation can also reproduce that reference's bugs.

### Current progress, not the stale roadmap percentage

The [live progress page](https://tangency-labs.github.io/solidcore/), retrieved during this investigation, reports:

| Metric | Live report |
| --- | ---: |
| Units with ports, green or partial | 261 / 261 |
| Green units | 232 |
| Partial units | 29 |
| Upstream lines in green units | 86.1% |
| End-to-end primitive checks passing | 9 / 9 |

These are **upstream-published results, not tests run here**. The live report can lag the repository head. The source revision inspected was [`337cbe6504a4955b6f1f58328f85f91a4636dc30`](https://github.com/tangency-labs/solidcore/commit/337cbe6504a4955b6f1f58328f85f91a4636dc30). The checked-in [`PROGRESS.md` / `STATUS.md`](https://github.com/tangency-labs/solidcore/blob/337cbe6504a4955b6f1f58328f85f91a4636dc30/plan/STATUS.md) explicitly identify older generated snapshots; they should not be substituted for the live result.

The [primitive checks](https://tangency-labs.github.io/solidcore/solids.html) exercise public pure-Rust construction and compare manifoldness, Euler characteristic, volume, area and bounds against analytic expectations. That is stronger than module-presence claims. However, the same page's **real-model corpus is still unpopulated**.

More importantly, the progress page's independent surface/surface intersection corpus records 119 cases: Rust has 78 pass, 21 incomplete, 10 wrong topology, 1 error and 9 deferred. It also records 110 Rust/C++ comparisons, all identical. These two observations are compatible: **differential parity is not independent geometric correctness**. This is directly relevant to intersection-heavy booleans and fillets.

The README still calls the API **experimental, 0.0.x**, with integration, deferred paths and known mismatches limiting coverage. Full port coverage is not end-to-end CAD readiness.

## 4. The migration is staged, not a direct kernel toggle

[Solidcore #342](https://github.com/tangency-labs/solidcore/issues/342) specifies the actual boundary:

1. SolidCraft talks to the forked **C++ SMLib**, statically linked behind C shims that catch exceptions and return statuses.
2. SolidCraft owns the transferred **schema-4 B-rep records**, not SMLib handles.
3. The safe-Rust Solidcore port takes over operations once differential parity is established.

The records preserve regions/shells, face parameter domains, edge intervals, per-use UV trim curves (**pcurves**), analytic geometry, per-body/edge/vertex tolerances, canonical ordering and operation history. Pcurves matter because a 3D edge alone does not describe its trimmed boundary on each incident surface, particularly around periodic seams. Canonical order and history matter because downstream features refer to persistent faces and edges, not just visually similar solids.

[PR #4012](https://github.com/tangency-labs/solidcraft/pull/4012) reports primitive round-trips, operation comparisons and a naming guard over 154 saved designs. These are maintainer-reported branch results, not an assurance that arbitrary native designs migrate unchanged. [#2661](https://github.com/tangency-labs/solidcraft/issues/2661) explicitly identifies gaps in backend-independent regression coverage: its historical kernel mutation sample caught only 15% with the black-box suites. The figure is a sampled coverage finding, not a direct application failure probability.

### Performance evidence and remaining defects

A [maintainer's comparison](https://github.com/tangency-labs/solidcraft/pull/4012#issuecomment-6312433187) on 411 operations reported:

| Boolean kernel | Median | Worst | Total |
| --- | ---: | ---: | ---: |
| truck | 8.8 ms | 6.2 s | 44.0 s |
| C++ SMLib | 1.8 ms | 25 ms | 1.1 s |

This times the **Boolean alone**, excluding conversion overhead. It is a reported C++ SMLib experiment, **not a Rust Solidcore benchmark or a promised app-wide speedup**. That run also exposed failures and incorrect mass properties, so throughput is not enough to establish parity.

- [Solidcore #383](https://github.com/tangency-labs/solidcore/issues/383) remains open. Its latest inspected maintainer comment says the tangency validator bug was fixed in the **SMLib fork**, and the Rust port needs the same change. Treat the initial failure count as historical, not proof that the fixed fork still fails those cases.
- [Solidcore #384](https://github.com/tangency-labs/solidcore/issues/384) remains open for incorrect mass properties on some Boolean results. Follow-up discusses integration across trim-curve knots and asking for accuracy outside the documented API range; it also reports check-dependent volume differences. The current evidence does not justify declaring it fixed.

## 5. What this means for our models

| Concern | Assessment |
| --- | --- |
| Whole-body thread faceting | A better curved Boolean backend could remove the reason for the fallback, but the SolidCraft thread feature must also stop using its faceted tool/cut path. **Replacing the backend alone is not proof of a fix.** No reviewed end-to-end thread regression demonstrates analytic exterior preservation through Solidcore. |
| Screw-access seam fillet panic | Removing truck would remove this specific truck call path. It would not prove that the new backend can construct the requested fillet; test the saved pre-fillet checkpoint and exact operation. |
| Saved native design | Keep it authoritative. Migration must preserve timeline evaluation, tolerances, persistent naming and relevant geometry, not merely open or display the cached shape. Do not overwrite the original with an experimental rebuild. |
| Practical choice now | Keep current native files and the controlled reproducers. Do not treat a newer stable release or a Solidcore port percentage as acceptance evidence. Use isolated saved copies for any future alternate-backend evaluation. |

The most useful future acceptance cases are already here: the analytic coupon with an internal thread, and the saved pre-fillet endcap plus exact failing operation. For a candidate backend, require retained unrelated analytic surfaces, independently appropriate dimensional checks, valid printable topology, controlled errors, and saved/reloaded native behavior. Until those paths are exercised, improvement on these models remains **unverified**, not promised.

## Verification boundary

GitHub issue/PR states, release metadata, source paths, migration contracts, live progress and upstream-published results were inspected. No alternative kernel was built or run; no benchmark or test result is presented as locally reproduced. The earlier controlled 0.21.0 coupon run remains documented separately in the faceting report. No desktop model was touched.
