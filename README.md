# Hermes Agent — Environment & Skill Setup Guide

A reproducible recipe for a working **Hermes Agent** desktop environment on Windows,
plus the curated skill catalog installed on this machine: **what to install, from where,
and exactly how**.

Everything here was executed and verified on a real machine — every command in this
guide is one that was actually run, with its real output shape. Where a number or a path
appears, it came from a tool, not from memory.

## What's in here

| Doc | Covers |
|---|---|
| [docs/01-environment.md](docs/01-environment.md) | Prerequisites, install, profile layout, paths, health checks |
| [docs/02-how-skills-work.md](docs/02-how-skills-work.md) | SKILL.md anatomy, categories, load-on-demand, project vs global |
| [docs/03-skill-sources.md](docs/03-skill-sources.md) | Bundled, official, skills.sh, GitHub, ClawHub, hand-written, project-local, MCP |
| [docs/04-install-recipes.md](docs/04-install-recipes.md) | Every install command, verified, with its quirks |
| [docs/05-catalog.md](docs/05-catalog.md) | The curated catalog — what to install and why, group by group |
| [docs/06-authoring-skills.md](docs/06-authoring-skills.md) | Writing your own skill that actually triggers |
| [docs/07-maintenance.md](docs/07-maintenance.md) | Updates, audits, pruning, export/import, troubleshooting |

Machine-readable: [`catalog/skills-catalog.json`](catalog/skills-catalog.json) (what to
install) and [`catalog/installed-inventory.json`](catalog/installed-inventory.json)
(what is currently installed — regenerable).

## TL;DR

```bash
# 1. Hermes itself (see docs/01 for the full flow)
hermes setup

# 2. Health check
hermes doctor
hermes skills list

# 3. Install the curated catalog (dry run first, then apply)
python scripts/install_catalog.py
python scripts/install_catalog.py --apply

# 4. Verify against the manifest
python scripts/verify_installed.py
```

## The two install mechanisms (know the difference)

| Path | Command | Tracked for updates? | Use when |
|---|---|---|---|
| **Native hub** | `hermes skills install <identifier>` | **Yes** — `hermes skills check` / `update` | Default choice; identifiers like `anthropics/skills/skills/mcp-builder` |
| **Vercel `skills` CLI** | `npx skills add <owner/repo> --skill <name> -g -a hermes-agent --copy -y` | No — lands as a plain local skill | Multi-skill repo installs, `--list` previews, `find` search |

Both land in the same directory. A hub-installed skill shows its source in
`hermes skills list`; a CLI/manual copy shows `local`. The native path is preferred when
the skill exists in the hub, because only that one can be updated in place.

## Verified environment

- Windows 10 22H2, no admin rights, git-bash (MSYS) shell
- Hermes profile `default` → `C:\Users\Ali\AppData\Local\hermes\`
- Skills root → `C:\Users\Ali\AppData\Local\hermes\skills\`
- 108 skills enabled, 0 disabled; 51 bundled, 57 local
- Node 22 + `npx skills` 1.5.26, `hermes` CLI from the venv

## License

MIT — see [LICENSE](LICENSE).
