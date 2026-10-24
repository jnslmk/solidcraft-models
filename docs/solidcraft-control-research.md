# Controlling SolidCraft with an AI agent

Research checked 2026-10-24 against first-party documentation/source. Latest stable release observed: [v0.21.0](https://github.com/tangency-labs/solidcraft/releases/tag/v0.21.0). This is documentation/source research, not a locally exercised installation. Nothing was installed or configured.

## Recommendation

For an external coding agent working in this models repository, use **SolidCraft's bundled MCP server plus its bundled modeling skills**, with a short project instruction file to route the agent to those skills and record actual design conventions. These are complementary layers, not competing integrations. No third-party SolidCraft MCP implementation is needed. [MCP documentation](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/mcp.md), [official skills](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/README.md).

| Layer | Purpose | Recommendation |
|---|---|---|
| MCP | Executes CAD commands, inspects/measures geometry, produces images, saves/exports | Use the built-in `solidcraft-cli mcp`; explicitly connect it to the desktop when you want visible modeling |
| Agent Skills | Teach modeling/editing/checking workflows and tool pitfalls | Start with embedded documents; install complete skill folders only for client auto-discovery or bundled helper scripts |
| Project instructions | Choose the workflow and define this project's units, tolerances, deliverables and file conventions | Keep short and project-specific; do not copy SolidCraft's source-contributor `AGENTS.md` |

## Visible desktop control: released v0.21.0 setup

Obtain matching official `solidcraft` and `solidcraft-cli` executables. On Linux, the official portable tarball exposes both without needing a source build; native packages also contain both. An AppImage contains the CLI internally but its launcher runs the GUI and does not install a host `solidcraft-cli` command. Snap names the CLI `solidcraft.cli`. Flatpak adds network/token/filesystem sandbox considerations. For external-agent control, accessible native binaries are the simplest recommendation. [Package manifest](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/packaging/linux/nfpm.yaml), [packaging script](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/packaging/linux/package.sh), [AppImage launcher](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/packaging/linux/AppRun), [getting started](https://docs.solidcraft.io/guide/getting-started.html).

Launch the desktop app with its control bridge:

```sh
solidcraft --control 7878
```

Configure the external MCP client to spawn the following command over stdio; normally the client starts it, not a second interactive terminal:

```sh
solidcraft-cli mcp --connect 127.0.0.1:7878 --allow-path /home/jonas/git-projects/cad-and-3d/solidcraft-models
```

Example configuration shape used by Claude Desktop and other clients supporting `mcpServers` (each client has its own configuration location/schema):

```json
{
  "mcpServers": {
    "solidcraft": {
      "command": "/absolute/path/to/solidcraft-cli",
      "args": [
        "mcp", "--connect", "127.0.0.1:7878",
        "--allow-path", "/home/jonas/git-projects/cad-and-3d/solidcraft-models"
      ]
    }
  }
}
```

Replace the executable path with its installed location. App and CLI must run on the same machine for the documented screenshot-file bridge. Prefer absolute artifact paths, since bridged relative paths resolve in the app's working directory. [Released setup and client configuration](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/mcp.md).

**Important version trap:** v0.21.0's bare `solidcraft-cli mcp` operates a separate headless design, not the visible desktop document. Moving `main` already documents automatic desktop discovery, a default 27878 port and `--headless`; do not assume those new defaults exist in a downloaded v0.21.0 binary. Explicit `--control` plus `--connect` avoids that ambiguity. [v0.21.0](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/mcp.md#start-it), [main](https://github.com/tangency-labs/solidcraft/blob/main/docs/mcp.md#start-it).

### Access boundaries

The app bridge binds to loopback and authenticates using a per-launch token read automatically by the CLI. MCP file access is scoped; the current working directory is not automatically permitted. `--allow-path` grants an existing directory tree **including hidden files**. Use a dedicated existing artifact folder instead if the project contains secrets; avoid `--allow-any-path`. External-agent approvals and unrelated shell/network tools remain that client's responsibility, not SolidCraft's MCP sandbox. [Filesystem policy](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/mcp.md#which-files-the-agent-can-reach), [control token and limits](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/control-protocol.md).

## Skills: use the official four

| Skill | Use |
|---|---|
| [`solidcraft-modeling`](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/solidcraft-modeling/SKILL.md) | New parametric parts; numeric planning, staged construction and measurement |
| [`solidcraft-editing`](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/solidcraft-editing/SKILL.md) | Modify existing designs through parameters/timeline instead of rebuilding |
| [`solidcraft-checking`](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/solidcraft-checking/SKILL.md) | Constraint and parameter-range checks, saved-design regression workflows, optional reference comparisons |
| [`solidcraft-mechanisms`](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/solidcraft-mechanisms/SKILL.md) | Assemblies, joints and motion; load when applicable |

All four skill documents are embedded in v0.21.0 and exposed through the MCP `skill_reference` tool. For example, this is a **tool call**, not a shell command:

```text
skill_reference {"skill":"solidcraft-modeling","file":"SKILL.md"}
```

Use explicit `file:"SKILL.md"` for each skill. Omitting `file` defaults to `reference.md`, which modeling/mechanisms provide but editing/checking do not. Full skill installation is optional for MCP document access. Copy whole skill directories if installing: the checking scripts/template are not exposed through the embedded-document tool. Match copied skills to the installed application release. Official installation examples target Claude's global `~/.claude/skills/` or project `.claude/skills/`; other Agent Skills clients use their own documented directories. [Skill installation](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/skills/README.md#install), [embedded implementation](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/crates/mcp/src/skill_reference.rs).

## Project instructions: a small router, not a copied manual

The upstream `AGENTS.md` governs development of SolidCraft itself: Rust architecture, licensing/clean-room rules, CI, PRs and releases. It is not appropriate wholesale for an end-user CAD models repository. [Upstream contributor instructions](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/AGENTS.md).

Suggested project guidance, not an installed file or upstream template:

- Use SolidCraft MCP for interactive modeling. Load modeling or editing plus checking; load mechanisms for assemblies. Retrieve each skill with explicit `file:"SKILL.md"`.
- Inspect the active document first; preserve existing/unsaved work. Prefer parameter and timeline edits to rebuilding existing features.
- Plan intended dimensions, parameter relationships and expected measurements before construction. Discover actual commands/arguments rather than guessing.
- Build in stages, check timeline/solver errors, compare measured dimensions/volume/bounds with independent expectations, and inspect a final image before saving/exporting.
- Exercise intended parameter-range endpoints. Keep the editable design and appropriate reproducible build/check artifacts; record actual units, tolerances, output locations and required delivery formats when known.
- Do not let parallel agents mutate one shared MCP document; use independent CLI sessions for independent work.

These recommendations follow the official modeling, editing and checking skills above. MCP initialization supplies brief guidance, but enabling MCP does not automatically load every complete skill. Explicit routing helps. [Server initialization](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/crates/mcp/src/server.rs).

## Alternatives that may be simpler

**Inside SolidCraft:** the desktop Assistant already hands its selected agent an MCP server named `solidcraft-app` connected to the open design. Configure an installed ACP-capable agent/adapter or supported model endpoint in Preferences → AI; no separately registered SolidCraft MCP server is needed for that mode. ACP is the app-to-agent connection, not a replacement CAD engine. Its agent runs in an empty working directory, so do not rely on this repository's instruction file being loaded there. The embedded skills remain available. Default integrated permissions allow model edits but ask about file actions. [Assistant setup, tools and permissions](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/agent-chat.md).

**Repeatable headless generation:** a shell-capable coding agent can write a JSON command script and use `solidcraft-cli run script.json --out part.step`, without MCP. This uses the same engine commands and is a good fit for deterministic batch artifacts; it does not control a visible desktop document. MCP is the recommendation for conversational inspection/editing, not a requirement for every scripted part. [Script format](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/scripts.md).

**Browser app:** prefer the native `window.solidcraft` JavaScript API (`commands`, `execute`, `inspect`, `request`) to coordinate-click automation. It acts on the current tab and supports inspection/undo. Keep the tab active; files live in a browser virtual filesystem, not unrestricted host paths. It is not WebMCP and does not open a network listener. Use this if browser-only operation is the goal, not as an extra layer on top of a working desktop MCP setup. [Browser API](https://github.com/tangency-labs/solidcraft/blob/v0.21.0/docs/browser-api.md).

## Verification boundary

Release metadata, setup commands, skill availability and control alternatives were verified against official web documentation/source. No runtime connection, local application behavior, geometry, package installation or client-specific configuration was exercised. Runtime acceptance after a future setup: discover commands, create a small part in an empty test document, verify numerical dimensions/volume and an image, then save/reopen the editable design and export inside the allowed folder.
