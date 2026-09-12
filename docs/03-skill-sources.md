# 03 — Where skills come from

Six sources feed a Hermes profile. Knowing which one a skill came from tells you whether
it can be updated, and how to fix it when it breaks.

## 1. Bundled (builtin) — ships with Hermes

Seeded into the profile on install/update and tracked in `skills/.bundled_manifest`.
On this machine: **51 builtin** skills (github, pdf, xlsx, docx, powerpoint, obsidian,
maps, arxiv, hermes-agent, the autonomous-agent CLIs, the creative set, …).

```bash
hermes skills list                      # Source column shows "builtin"
hermes skills opt-out                   # stop seeding bundled skills into this profile
hermes skills opt-in                    # undo that
hermes skills list-modified             # bundled skills you edited (updates keep your version)
hermes skills diff <name>               # how your copy differs from stock
```

Editing a bundled skill is allowed but marks it *user-modified*; `hermes update` then
stops overwriting it. `hermes skills reset <name>` clears that flag.

## 2. Official optional skills

The Hermes repo also ships optional, niche skills (`optional-skills/<category>/<name>`)
that are not seeded by default.

```bash
hermes skills install official/<category>/<skill>
hermes skills repair-official           # backfill/restore them from repo source
```

## 3. The Hermes skills hub (registry search)

One command searches the ecosystem — skills.sh, GitHub, ClawHub, lobehub, browse.sh,
well-known endpoints, and vendor catalogs (nvidia, openai, **anthropic**, huggingface,
voltagent, gstack, minimax).

```bash
hermes skills search "lighting" --source anthropic
hermes skills search "mcp" --limit 20 --json
hermes skills browse                   # paginated full catalog
hermes skills inspect <identifier>     # preview before installing
hermes skills install <identifier> --category <folder> --yes
```

Verified identifiers on this machine:

| Identifier | Source | Trust |
|---|---|---|
| `anthropics/skills/skills/mcp-builder` | github | trusted |
| `skills-sh/<owner>/<repo>/<skill>` | skills.sh index | community |

**Caveat found in practice:** some community `skills-sh/...` identifiers that appear in
`hermes skills search` fail at install time with
`Error: Could not fetch '<identifier>' from any source.` When that happens, install from
the GitHub repo instead (source 4 below) — the content is identical, only the tracking
differs.

A hub install runs a safety scan (`skills-guard-v2`) and reports the verdict, the matched
rules, and the commit hash it pinned. Example from installing `mcp-builder`:

```
Decision: ALLOWED — Allowed (trusted source, caution verdict)
Scan provenance: fresh; scanner skills-guard-v2; hash sha256:30cb9efd…
rules: context_exfil, unpinned_pip_install
Installed: software-development/mcp-builder
```

The scan is informative, not a guarantee: read `scripts/` yourself before running a
skill from an unknown author. `--force` overrides a blocked verdict — don't, unless you
have read the files.

## 4. The Vercel `skills` CLI (skills.sh)

The ecosystem-wide installer at [skills.sh](https://skills.sh). Hermes is a first-class
agent target named **`hermes-agent`**, so installs land directly in the profile.

```bash
npx skills find "lighting"                       # search the registry
npx skills add anthropics/skills --list          # preview a repo's skills
npx skills add <owner/repo> --skill <name> -g -a hermes-agent --copy -y
```

Use it when a repo bundles many skills, when you want a `--list` preview, or when the
hub can't fetch an identifier. Downside: installs are **not** hub-tracked, so
`hermes skills check/update` ignores them (they show as Source `local`). Update them by
re-running `npx skills add …` or `npx skills update`.

It also prints a security panel per skill (Gen verdict, Socket alerts, Snyk risk) before
copying files — worth reading.

## 5. Hand-written skills

The skills you own — the highest-value ones, because they encode *your* procedures.

```bash
# via the agent (preferred: it writes frontmatter and validates):
#   skill_manage(action="create", name="...", content="---\nname: ...\n---\n...")
# manually:
mkdir -p "$LOCALAPPDATA/hermes/skills/<category>/<name>"
$EDITOR "$LOCALAPPDATA/hermes/skills/<category>/<name>/SKILL.md"
```

See [06-authoring-skills.md](06-authoring-skills.md).

## 6. Project-local skills

A repo can carry its own skills so a team shares them through git:

```
<project>/.hermes/skills/<name>/SKILL.md
<project>/.agents/skills/<name>/SKILL.md      # cross-agent convention
```

Project-local skills are **not** loaded in a session until the repo is trusted:

```bash
hermes skills trust            # in the project directory
hermes skills untrust          # revoke
```

This is the safest way to share skills with a team: they travel with the code, and
nothing runs until a human trusts the checkout.

Next: [04-install-recipes.md](04-install-recipes.md)
