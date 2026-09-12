# 01 — Environment

## Prerequisites

| Need | Why | Check |
|---|---|---|
| Windows 10/11 (no admin needed for a user-profile install) | Hermes runs from the user profile | `winver` |
| Git for Windows | brings `git-bash`, which Hermes uses as its shell on Windows | `git --version` |
| Node.js 18+ (22 LTS recommended) + `npx` | the Vercel `skills` CLI and most MCP servers run on Node | `node --version`, `npx --version` |
| Python 3.10+ | skill helper scripts; Hermes ships its own venv | `python --version` |
| GitHub CLI (`gh`) | installing skills hosted on GitHub, publishing your own | `gh --version`, `gh auth status` |

On this machine: Git 2.54, GitHub CLI 2.95, Node 22, `npx skills` 1.5.26, Hermes on the
bundled venv Python at
`C:\Users\Ali\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`.

> **Shell note (Windows):** the agent's `terminal` tool runs **git-bash (MSYS)**, not
> PowerShell. Use POSIX syntax in commands you hand to it. Native Windows programs do
> **not** get MSYS path translation — pass `C:/Users/Ali/...` style paths to `git`,
> `node`, `gh`, `python`, never `/c/Users/Ali/...`.

## Install

```bash
# 1. Install Hermes (or update it)
hermes --help          # present?
hermes update          # keep the binary current

# 2. Configure model / provider interactively
hermes setup

# 3. Verify everything
hermes doctor
hermes status
hermes skills list
```

`hermes setup` writes the profile config; `hermes doctor` is the single command that
tells you whether tools, providers, and the shell integration are healthy.

## Where everything lives (profile `default`)

| Path | What |
|---|---|
| `C:\Users\Ali\AppData\Local\hermes\` | profile root |
| `…\hermes\skills\` | **skills root** — every installed skill is a folder with a `SKILL.md` |
| `…\hermes\skills\<category>\<skill>\SKILL.md` | categorised skill (family layout) |
| `…\hermes\skills\<skill>\SKILL.md` | top-level skill (no category) |
| `…\hermes\skills\.usage.json` | per-skill usage counters |
| `…\hermes\skills\.bundled_manifest` | which skills shipped with Hermes |
| `…\hermes\skills\.curator_*.jsonl` | curator activity log |
| `…\hermes\hermes-agent\` | the Hermes source tree + its venv |
| `…\hermes\cron\` | scheduled jobs |
| `…\hermes\profiles\<name>\` | other profiles (each has its own skills/, cron/, memories/) |

Multiple profiles are fully isolated: installing into one does **not** affect another.
Never edit another profile's skills/cron/memories unless explicitly asked.

## Health checks

```bash
hermes doctor                  # full environment diagnosis
hermes status                  # component status
hermes skills list             # what's installed, source, trust, enabled/disabled
hermes skills check            # are hub-installed skills stale?
hermes logs                    # when something is wrong but doctor is happy
```

Machine-readable count check (the footer line tells you the totals):

```bash
hermes skills list | tail -2
# e.g. "0 hub-installed, 51 builtin, 57 local — 108 enabled, 0 disabled"
```

## Windows specifics worth knowing

- **No admin, no WSL2, no Docker Desktop** is a valid configuration. Hermes itself needs
  none of them; heavy sandboxed work is done in a headless QEMU VM instead (see the
  `devbox-vm-manager` project).
- **Long paths:** the skills root is inside the user profile, so long skill names with
  nested `references/` are fine, but keep names under ~40 chars.
- **Background work:** cron jobs and the messaging gateway only run while the Hermes
  gateway process is alive. Install it as a Startup-folder login item
  (no UAC required) if you want scheduled jobs to fire.
- **Antivirus:** Windows Defender can slow the first launch of Node-based MCP servers;
  exclude the profile folder if startup feels stalled.

Next: [02-how-skills-work.md](02-how-skills-work.md)
