# Attribution & upstream sources

The `skills/` folder in this repository vendors skill files so the setup works
**offline**. Each skill keeps its original `SKILL.md` and supporting files unchanged;
licenses are reproduced under [`skills/_sources/<upstream>/`](skills/_sources/).

| Upstream | Commit pinned | License | Skills vendored here |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | `34040c9c568585f6929bedeaad110ad08f079624` | Apache-2.0 (per-skill `LICENSE.txt`) | `canvas-design`, `frontend-design`, `theme-factory`, `software-development/mcp-builder` |
| [Abhinavbwj/Skills-Architects](https://github.com/Abhinavbwj/Skills-Architects) | `30a0845dddcaebd765fc396059573d02e99c5b63` | MIT | the 29 `architecture/` skills: foundations, theory, concept, spatial planning, typology, programming, codes, envelope, services, sustainability, structural, fire, acoustics, accessibility, construction documentation, materials, daylighting, the calculator, and the 10 country dossiers |
| [AlpacaLabsLLC/skills-for-architects](https://github.com/AlpacaLabsLLC/skills-for-architects) | `e7e364497b2a47c088db2e47de6660344fcaf92d` | MIT | the 12 `aec-products/` skills: specs, master schedule, product research/match/pair, presentation, palettes, EPDs, site reports, minutes |
| [curiositech/some_claude_skills](https://github.com/curiositech/some_claude_skills) | `6713fc7a6451c8dee5903b98cd2063ff4cbf7317` | MIT | `design/interior-design-expert` |
| this repository | — | MIT | `architecture/villa-lighting-design` (original work) |

## Apache-2.0 compliance (anthropics/skills)

Redistribution of the Anthropic-authored skills is under Apache License 2.0. The
license text is vendored at [`skills/_sources/anthropics-skills/LICENSE.txt`](skills/_sources/anthropics-skills/LICENSE.txt).
Files are redistributed **unmodified**; no `NOTICE` file was published upstream. If you
modify them here, record the change — Apache-2.0 §4(b) requires modified files to carry
prominent notices of change.

## Keeping vendored copies honest

Vendored files are snapshots. To refresh them from upstream:

```bash
# native hub (updates the profile copy, then re-vendor with the script below)
hermes skills check && hermes skills update

# or re-copy from the live profile into the repo
python - <<'EOF'
import pathlib, shutil, os
src = pathlib.Path(os.environ["LOCALAPPDATA"]) / "hermes" / "skills"
dst = pathlib.Path("skills")
for cat in ("architecture", "aec-products", "design", "software-development"):
    for skill in sorted((src / cat).iterdir()):
        if (skill / "SKILL.md").is_file():
            shutil.copytree(skill, dst / cat / skill.name, dirs_exist_ok=True)
print("re-vendored")
EOF
```

Then update the commit column above — a pinned commit you didn't actually re-check is
worse than no pin at all.

## Provenance note

Every skill here was installed and run on the machine described in
[docs/01-environment.md](docs/01-environment.md), and its install path was verified with
`hermes skills list`. Security posture at install time: Gen "Safe" / Socket clean for all;
Snyk rated seven of them Medium risk (bundled scripts + web-fetch steps — read
`scripts/` before running those). See [docs/05-catalog.md](docs/05-catalog.md) for the
per-skill notes.