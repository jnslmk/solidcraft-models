# solidcraft-models

Editable parametric CAD designs made with [SolidCraft](https://github.com/tangency-labs/solidcraft).

## Layout

```text
models/           native designs, grouped by model family
exports/          generated print/exchange files and renders (ignored)
docs/             general documentation and research
.agents/skills/   project-local official SolidCraft skills
```

Use `models/<snake_case_family>/` for a model or related parts. Keep each
part/assembly's authoritative `.solidcraft` document there, with a family
`README.md` describing its purpose, important parameters, interfaces, material,
tolerances, print orientation and verification. Add intentionally repeatable build
scripts or geometry checks alongside the design only when needed.

## Models

- [Notched plate sketch](models/notched_plate/README.md)
- [LED profile endcaps](models/led_profiles/README.md): standard and wired variants

Write generated artifacts to `exports/<family>/`. Retain editable source; STL is
the default print export, with STEP when requested. Temporary screenshots and
checkpoints belong in ignored `.codex-tmp/<task>/`, created when needed.

## Working with an agent

[AGENTS.md](AGENTS.md) defines the modeling and verification workflow. Four
release-matched official skills are installed locally: modeling, editing,
checking and mechanisms. Agents should read the relevant local `SKILL.md` files;
clients with project skill discovery can discover `.agents/skills/` directly.
See [.agents/README.md](.agents/README.md) for provenance and updates.

For a visible desktop connection with SolidCraft **0.21.0**, start:

```sh
solidcraft --control 7878
```

Configure your external MCP client to launch:

```sh
solidcraft-cli mcp --connect 127.0.0.1:7878 --allow-path /absolute/path/to/this/repository
```

Replace the path with an existing directory. A dedicated existing artifact
folder is a narrower grant; `--allow-path` includes hidden files. Both binaries
must be available to the client. No MCP client configuration is installed by
this repository setup.

In 0.21.0, omitting `--connect` creates a separate headless document. SolidCraft's
built-in Assistant already supplies its own CAD connection instead; it may not
load this repository's agent instructions. For setup details, alternatives and
version caveats, see [the control research](docs/solidcraft-control-research.md).
