# 04 — Install recipes (all verified)

Copy-paste recipes for every install path, with the quirks that actually bite.
Paths assume the `default` profile on Windows; substitute your profile root.

## A. One skill from a GitHub repo (native hub — preferred)

```bash
hermes skills search "mcp-builder" --source anthropic --json     # find the identifier
hermes skills inspect "anthropics/skills/skills/mcp-builder"     # preview
hermes skills install "anthropics/skills/skills/mcp-builder" \
      --category software-development --yes
```

Result on this machine:

```
Decision: ALLOWED — Allowed (trusted source, caution verdict)
Scan provenance: fresh; scanner skills-guard-v2; hash sha256:30cb9efd…
Installed: software-development/mcp-builder
```

- Identifier shape for GitHub-hosted skills: `<owner>/<repo>/<path-to-skill>`.
- `--category` picks the folder; omit it and the skill lands at the top level.
- Installs are **hub-tracked** → `hermes skills check` / `hermes skills update` work.

## B. Many skills from one repo (Vercel CLI)

```bash
cd "$LOCALAPPDATA/Temp"                                  # run from a neutral dir
npx skills add Abhinavbwj/Skills-Architects --list        # preview first
npx skills add Abhinavbwj/Skills-Architects --skill '*' \
    -g -a hermes-agent --copy -y                          # all skills, global, Hermes target
```

Selected skills:

```bash
npx skills add anthropics/skills \
    --skill canvas-design --skill frontend-design --skill theme-factory \
    -g -a hermes-agent --copy -y
```

| Flag | Meaning |
|---|---|
| `-g` | user-level install (`~/<agent>/skills`), not project-level (`./<agent>/skills`) |
| `-a hermes-agent` | the agent target — **`hermes` alone is rejected**; the valid name is `hermes-agent` |
| `--copy` | copy files instead of symlinking (Windows-friendly, and what you want for a profile) |
| `-y` | skip prompts (needed for scripted runs) |
| `--list` | show the repo's skills without installing |
| `--full-depth` | find `SKILL.md` files nested deeper than the standard containers |
| `--skill '*'` | every skill in the repo |

If the CLI reports `Invalid agents: hermes`, you used the wrong target name — it prints
the full valid list (aider-desk, claude-code, codex, cursor, **hermes-agent**, opencode,
windsurf, zed, …).

## C. From a skills.sh identifier via the hub

```bash
hermes skills search "arabic" --source skills-sh --json
# → identifier: skills-sh/sultanalsafran/agent-skills/arabic-presentations
hermes skills install "skills-sh/sultanalsafran/agent-skills/arabic-presentations" --yes
```

**Quirk:** community `skills-sh/...` identifiers can fail with
`Could not fetch … from any source.` When that happens use recipe B against the same
owner/repo — the skill content is identical, only update-tracking differs.

## D. From a raw URL

```bash
hermes skills install "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill>/SKILL.md" \
      --name <skill-name> --category <folder>
```

`--name` is required when the target SKILL.md has no `name:` frontmatter.

## E. By hand (your own skill)

```bash
SK="$LOCALAPPDATA/hermes/skills"
mkdir -p "$SK/<category>/<skill>"
cat > "$SK/<category>/<skill>/SKILL.md" <<'EOF'
---
name: <skill>
description: Keep this trigger line short and specific.
---
# <Skill>

## When to Use
- …
## Procedure
1. …
## Verification
- …
EOF
```

Better: ask the agent to create it (`skill_manage`), which writes validated frontmatter
and keeps references/scripts/templates in the right places.

## F. Whole-environment export / import

```bash
hermes skills snapshot export skills-snapshot.json     # what you have, with sources
hermes skills snapshot import skills-snapshot.json     # rebuild on another machine
```

This is the fastest way to reproduce this setup elsewhere — see
[07-maintenance.md](07-maintenance.md).

## Verification (after any install)

```bash
hermes skills list | grep -i "<skill>"          # enabled, and which source/trust
hermes skills list | tail -2                    # totals: hub/builtin/local + enabled/disabled
python scripts/verify_installed.py              # this repo's catalog vs reality
```

Two things that look like failures but aren't:

1. **The new skill doesn't appear in the current chat session.** The skill index is built
   at session start — open a new session.
2. **A skill shows a blank Category.** It was copied to the top level by the Vercel CLI.
   Functional; move the folder under a category if you care about tidiness
   (`hermes skills install --category` does this automatically).

## Duplicate names

Installing the same skill twice (once via `npx`, once via the hub) leaves two folders with
one `name:`. Only one is indexed. Detect and clean:

```bash
# find duplicate names across the tree
python - <<'EOF'
import pathlib, re, collections, os
root = pathlib.Path(os.environ["LOCALAPPDATA"]) / "hermes" / "skills"
names = collections.defaultdict(list)
for p in root.rglob("SKILL.md"):
    m = re.search(r"^name:\s*(.+)$", p.read_text(encoding="utf-8", errors="ignore"), re.M)
    if m: names[m.group(1).strip()].append(str(p.parent.relative_to(root)))
for n, paths in sorted(names.items()):
    if len(paths) > 1: print(n, "->", paths)
EOF
```

Keep the hub-tracked one (its Source column is `github`/`skills-sh`, not `local`) and
delete the other.

Previous: [03-skill-sources.md](03-skill-sources.md) · Next: [05-catalog.md](05-catalog.md)
