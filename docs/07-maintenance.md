# 07 — Maintenance, backups, troubleshooting

A skills profile drifts: upstream repos change, bundled skills get edited, duplicates
appear. This is the routine that keeps it honest.

## Weekly-ish

```bash
hermes skills check        # are hub-installed skills stale?
hermes skills update       # update them
hermes skills audit        # re-scan installed hub skills for safety
hermes skills list | tail -1   # totals line
python scripts/verify_installed.py   # does the catalog still match the machine?
```

`npx skills update` handles the Vercel-CLI copies (the ones `hermes skills` reports as
Source `local`); `hermes skills update` handles the hub ones. They don't overlap — this
is the practical cost of using both installers, and it is worth it.

## Snapshot / restore / migrate

```bash
hermes skills snapshot export skills-snapshot.json    # everything you have, with sources
hermes skills snapshot import skills-snapshot.json    # rebuild on a new machine
```

Do this before any big experiment, and before reinstalling Hermes. The snapshot is the
fastest disaster recovery there is; the catalog in this repo is the curated *reference*,
the snapshot is the actual *state*.

## A safe pruning routine

```bash
# 1. what is installed, by category
python scripts/scan_installed.py --markdown | head -60

# 2. what has never been used (usage counters live next to the skills)
python - <<'EOF'
import json, os, pathlib
root = pathlib.Path(os.environ["LOCALAPPDATA"]) / "hermes" / "skills"
usage = root / ".usage.json"
data = json.loads(usage.read_text(encoding="utf-8")) if usage.is_file() else {}
for name, info in sorted(data.items(), key=lambda kv: str(kv[1]))[:25]:
    print(f"{name:42} {info}")
EOF

# 3. remove what's clearly never going to run
hermes skills uninstall <name>        # hub-installed
rm -rf "$LOCALAPPDATA/hermes/skills/<folder>"   # CLI-copied / hand-written
```

Prune the 9 country dossiers you'll never use before you prune anything else — they are
the largest low-value block in the current catalog (Saudi + UAE are the keepers).

## Troubleshooting

| Symptom | Diagnosis | Fix |
|---|---|---|
| `hermes: command not found` | shell not picking up the venv bin | call it by full path: `…\hermes-agent\venv\Scripts\hermes`, or add to PATH |
| `Invalid agents: hermes` | wrong agent name for the Vercel CLI | use `-a hermes-agent` |
| `Could not fetch '<identifier>' from any source` | community `skills-sh/...` id not resolvable | install from the GitHub repo with `npx skills add <owner>/<repo>` instead |
| Skill installed but not listed | installed into a **different profile** | check `hermes profile`, then reinstall with the right profile active |
| Skill listed but never triggers | description too vague, or the session predates the install | rewrite the description; start a new session |
| Duplicate rows for one skill | installed twice (hub + CLI) | delete the untracked copy (Source `local`) |
| Hub skill refuses to update after you edited it locally | marked user-modified | `hermes skills reset <name>` (keeps your edit, restores update tracking) |
| Install blocked by a scan verdict | `skills-guard-v2` found something | read `scripts/` yourself; only then `--force`, never blind |
| Everything is slow on first run | Defender scanning Node/Python first launches | exclude the profile folder, or accept the one-time cost |
| Agent forgets a lesson between sessions | it belongs in a skill or memory, not in chat | write it into the skill's Pitfalls, or save a durable memory fact |

## Health checks worth knowing exist

```bash
hermes doctor                 # environment diagnosis
hermes status                 # components
hermes skills list             # source / trust / enabled per skill
hermes skills list-modified    # bundled skills you edited (updates keep yours)
hermes skills diff <name>      # what you changed vs stock
hermes skills reset <name>     # clear user-modified, rejoin the update train
hermes skills config           # interactively enable/disable individual skills
hermes skills opt-out / opt-in # stop/resume seeding bundled skills
hermes curator                  # the usage-tracking curator
hermes backup                   # profile backup
```

## Rebuilding this environment from scratch

1. Install Git, Node, Python, `gh`, Hermes → [01-environment.md](01-environment.md)
2. `hermes setup` and confirm `hermes doctor` is clean
3. **Offline path (no network needed):** `git clone` this repo and
   `python scripts/install_from_repo.py --apply` — the 47 skills are vendored in `skills/`
4. **Online path:** `python scripts/install_catalog.py` (dry run) → `--apply`
5. `python scripts/verify_installed.py` → must print *catalog satisfied*
6. `hermes skills list | tail -1` → note the totals; they should match this profile's
7. Start a new session so the fresh index loads

Previous: [06-authoring-skills.md](06-authoring-skills.md)
