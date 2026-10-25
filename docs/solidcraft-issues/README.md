# SolidCraft 0.21.0 issue drafts

Prepared reports and portable evidence; **not submitted upstream**.

| Draft | Finding | Evidence status |
|---|---|---|
| [Kernel intersection panic](kernel-intersection-panic/ISSUE.md) | Repeated Rust `Option::unwrap()` panics during a native fillet; unsupported-operation error eventually returned | Original failing-run stderr plus saved native checkpoint and exact extracted command; extracted command not replayed |
| [Modeled thread changes unrelated curved surfaces](thread-body-faceting/ISSUE.md) | Native modeled thread facets the entire target body, including its outer cylinder | Minimal native coupon script and captured measurements |
| [Nonmanifold threaded STL export](stl-thread-seams/ISSUE.md) | Direct STL export has defective seam topology while OCCT tessellation of native-derived STEP is manifold | Saved native input, raw STL, validation and comparison evidence |

Each directory contains its report and attachments. Run repro commands from the
corresponding directory. CAD reproduction should use an isolated process group,
a finite expiry and the workstation-wide heavy-verification lock; avoid rerunning
crash cases merely to confirm already captured failures.

Before filing, check the current upstream issue list for duplicates and whether a
newer release fixes the behavior. These drafts describe the exercised 0.21.0
installation, not an assertion about the current upstream release.

## Screenshots and the current native design

The [shared evidence](shared/README.md) contains the saved
[`endcap_native_unfinished.solidcraft`](shared/endcap_native_unfinished.solidcraft)
and three captioned screenshots. The current native file has no final
screw-breakout seam fillet. It is visual/editable context, not a replacement for
the earlier panic checkpoint or the measured hybrid STL-export reproducer.

The model and screenshots are snapshotted in these bundles; maintainers do not
need access to this repository or its temporary files. No new CAD/crash
reproduction was run to update the reports.

## Ready-to-attach packages

Each ZIP contains its issue directory plus the sibling `shared/` directory, so
the relative model/image links work after extraction:

- [Kernel panic report and evidence](../../exports/solidcraft-issues/kernel-intersection-panic.zip)
- [Whole-body thread faceting report and evidence](../../exports/solidcraft-issues/thread-body-faceting.zip)
- [Nonmanifold STL report and evidence](../../exports/solidcraft-issues/stl-thread-seams.zip)

Paste the corresponding `ISSUE.md` into the upstream issue body and attach its
ZIP. For inline GitHub images, also upload the three shared PNGs and replace the
relative image URLs with the URLs GitHub supplies. ZIP archives are generated
deliverables under ignored `exports/`; durable drafts and evidence live here.
Check attachment integrity using the included `SHA256SUMS` files. Neither the
archives nor the drafts have been submitted upstream.
