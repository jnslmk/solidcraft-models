# SolidCraft model instructions

## Source and layout

- The editable native `.solidcraft` design is authoritative; exports are deliverables, not source.
- Keep designs in `models/<snake_case_family>/`. Add a family README when adding a real model, documenting purpose, driving parameters and ranges, fixed/mating interfaces, tolerances, material, and print pose.
- Keep generated exports in `exports/<family>/`; they are untracked. Keep durable general documentation and research in `docs/`.
- Add scripts alongside a model only for intentional reproducible generators or checks. State whether a generator creates or edits a design; avoid a second, drifting definition of an existing native model.
- The official checking skill also supports plain JSON saved designs for readable diffs. Distinguish a saved design from a command script; do not rename formats blindly or replace native source with a partial script.
- Put disposable experiments, recovery copies, and inspection screenshots under ignored `.codex-tmp/<task>/`, creating the directory on use. Publish images only when requested.

## Load the applicable official skills

Read these project-local instructions before the corresponding work:

- **Create a part or new geometry:** `.agents/skills/solidcraft-modeling/SKILL.md`.
- **Resize, repair, or extend an existing design:** `.agents/skills/solidcraft-editing/SKILL.md`; follow its pointer to modeling command references as needed.
- **Create, change, or port any design:** also `.agents/skills/solidcraft-checking/SKILL.md` for constraint, parameter-range, and saved-design checks.
- **Assemblies, joints, or motion:** also `.agents/skills/solidcraft-mechanisms/SKILL.md`.

These are the official v0.21.0 skill trees. Their optional Python helpers and external comparison dependencies are not baseline project requirements; use them when the task warrants them.

## Connect and preserve the working design

1. Before connecting or troubleshooting control, read `docs/solidcraft-control-research.md`. Match documentation and tool schemas to the installed release.
2. For interactive work, use the MCP connection bridged to the user's desktop design. In v0.21.0, bare `solidcraft-cli mcp` creates a separate headless session; it does not edit the visible document.
3. Inspect the active design, saved path, dirty state, parameters, timeline, sketches, and baseline measurements before mutation. If the target is ambiguous, resolve it first. Ask before opening another design over dirty desktop work.
4. Preserve pre-existing file changes and unsaved work. Before mutation, take `edit.checkpoint` in its own call; preserve a recoverable on-disk baseline under `.codex-tmp/<task>/` when needed. Never reset, restore, or overwrite unrelated user work.
5. Edit in place through parameters, expressions, constraints, and native timeline operations. Preserve relative design intent: derive alignment, spacing, and symmetry from their driving geometry rather than independent coordinates. Inspect dependents before deleting features.
6. Use small reversible edits and inspect the outcome before retrying a failed operation. Restore only the agent's changes; reconcile intervening user edits before rollback.
7. Serialize mutations of a shared MCP design. Parallel independent work needs independent CLI sessions and separate design/output files, not concurrent calls into the same desktop document.

Discover actual commands and argument schemas through the connected tools instead of guessing names, IDs, or units. If using embedded skill documents, request `skill_reference` with explicit `file: "SKILL.md"` for each skill.

## Modeling conventions

- Default physical dimensions to **mm** and material to **PETG**, unless the model specifies otherwise. Record fit allowances rather than assuming nominal CAD clearance proves a printed fit.
- Use explicit unit-bearing parameter expressions where supported. Native document display units and command argument units are separate concerns: discover each command's length/angle convention, especially degrees versus radians.
- Keep named driving parameters, their allowed ranges, real sketch constraints, and dependent features editable. Constrain sketches intentionally; explain any remaining degrees of freedom.
- Design printable parts in their intended print pose: build plate at `z=0`, **Z+** as the print direction. Document exceptions and the relationship between assembly pose and print pose.
- Preserve fixed mating interfaces; surface consequential interface or manufacturing tradeoffs before changing them.

## Verify and deliver changed models

1. Predict the affected dimensions, clearances, bounds, body count, and volume or other meaningful geometric invariants before editing. Check the resulting geometry, not only parameter values or feature success.
2. Inspect timeline errors/warnings and sketch constraint state. Resolve failures and investigate warnings with measurements; a successful boolean can still produce the wrong solid.
3. Measure every changed functional interface and relevant assembly contact. Compare with independent expectations using documented tolerances; exclude duplicate printable bodies.
4. Exercise driving parameters through their documented range endpoints and back to the intended default, checking dependent dimensions and relationships at each state. Preserve the user's original state throughout.
5. Inspect an isometric view plus orthographic, interior, or section views needed to expose the changed geometry. Screenshots complement numerical checks, not replace them.
6. Save the agreed design to its intended path, with overwrite authorization established. Verify the persisted design by reload and repeat relevant checks. If reopening would discard unsaved user state, keep that session intact and inspect a saved copy in an independent CLI session instead.
7. Export **STL** by default; export STEP when requested. Retain the editable design, verify exports correspond to the saved geometry, and report paths, checks, tolerances, and any untested physical-fit assumptions.

Keep undecided design work identifiable. Commit or push only when requested; no deployment or automatic-push policy is inherited from sibling repositories.
