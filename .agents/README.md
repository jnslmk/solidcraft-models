# Official SolidCraft skills

The four packages in `skills/` are unmodified copies from
[SolidCraft](https://github.com/tangency-labs/solidcraft), tag **v0.21.0**, resolved
commit **65d288227ee212bb8633b173c6a0a125cafd0501**. They match the installed
`solidcraft-cli 0.21.0`.

Source inventory: [release skill tree](https://github.com/tangency-labs/solidcraft/tree/v0.21.0/skills).
Downloaded archive: <https://codeload.github.com/tangency-labs/solidcraft/tar.gz/refs/tags/v0.21.0>
(SHA-256 `b80471a1ee2270365dc8a8d3257499d41c998db9cbbc4c4a092eb083d66aee69`).
The packages contain 15 upstream files, including all references, checking
helpers, helper tests and the design-test template. `scripts/run.py` retains its
upstream executable bit. This is the sole project-local installation.

The upstream `LICENSE-MIT`, `LICENSE-APACHE` and `NOTICE` are preserved beside the
packages in `skills/`; SolidCraft contributors license this material under MIT
OR Apache-2.0. Upstream `ATTRIBUTION.md` lists no files in these skill trees.

## Updating to match the app

After upgrading SolidCraft, replace these trees with the matching release tag,
not the latest branch. Run from the repository root, set `tag` to the installed
release reported by `solidcraft-cli --version`, and record the new resolved
commit and archive hash above. This replaces only the four vendored packages;
keep repository-specific instructions outside them.

```sh
set -eu
tag=v0.21.0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl -fL "https://codeload.github.com/tangency-labs/solidcraft/tar.gz/refs/tags/$tag" -o "$tmp/source.tar.gz"
root="solidcraft-${tag#v}"
tar -xzf "$tmp/source.tar.gz" -C "$tmp" "$root/skills" "$root/LICENSE-MIT" "$root/LICENSE-APACHE" "$root/NOTICE"
for skill in solidcraft-modeling solidcraft-editing solidcraft-checking solidcraft-mechanisms; do
    rm -rf ".agents/skills/$skill"
    cp -a "$tmp/$root/skills/$skill" .agents/skills/
done
cp -a "$tmp/$root/LICENSE-MIT" "$tmp/$root/LICENSE-APACHE" "$tmp/$root/NOTICE" .agents/skills/
```

Confirm the tag's commit through the official repository's tag API
(`https://api.github.com/repos/tangency-labs/solidcraft/git/ref/tags/<tag>`;
resolve an annotated tag object if present), and use `sha256sum` on the downloaded
archive before the temporary directory is removed. Review the release's skill
inventory and licensing when updating; retain any new accompanying files.

## Optional helper dependencies

Reading the skills needs no Python environment. The checking helpers invoke
`solidcraft-cli` from `PATH`; STEP comparison additionally needs `build123d`
(OpenCASCADE), and the supplied helper tests/template use `pytest`. Upstream
shows isolated `uv run --no-project --with build123d ...` / `--with pytest`
commands in the checking skill. Those packages are optional external checking
tools, not SolidCraft runtime dependencies, and were not installed or run here.
