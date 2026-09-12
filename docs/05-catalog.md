# 05 — The catalog: what to install and why

The curated set for an architecture / villa-design practice working in Saudi Arabia,
on Windows, bilingually. Machine-readable twin: [`catalog/skills-catalog.json`](../catalog/skills-catalog.json).
Current state on this machine: **47/47 catalog entries present** —
`python scripts/verify_installed.py` says *catalog satisfied*.

> Philosophy: install for capability, prune for precision. Every skill adds a line to
> the per-turn index; near-duplicates make selection worse, not better. Everything below
> earned its place, and the "deliberately skipped" lists matter as much as the table.

## 1. AEC & architecture design system — 29 skills

**Source:** `Abhinavbwj/Skills-Architects` · **Method:** Vercel CLI (repo bundles 29 skills)

```bash
npx skills add Abhinavbwj/Skills-Architects --skill '*' -g -a hermes-agent --copy -y
```

| Group | Skills | Why |
|---|---|---|
| Design & practice | `architect-foundations`, `design-theory`, `concept-design`, `spatial-planning`, `building-typology`, `building-programming`, `material-selection`, `daylighting-design` | The front half of practice: theory → concept → programme → spatial layout |
| Codes & engineering | `building-codes`, `building-envelope`, `building-services`, `building-sustainability`, `structural-systems`, `fire-life-safety`, `acoustic-design`, `accessibility-design`, `construction-documentation` | Discipline-specific review criteria and numeric benchmarks |
| Calculator | `architect-calculator` | 7 Python scripts: area, cost, U-value, daylight, egress, structural load, energy |
| Geography | `geographic-foundations` + 10 dossiers | The router detects jurisdiction and loads the right national code file |

**The Saudi dossier is the reason this repo is in the catalog.** `country-saudi-arabia`
carries: the SBC 201–1001 nine-part series, Civil Defence requirements, the Saudi
Universal Accessibility Code, Mostadamah, the Vision-2030 giga-project regimes
(NEOM, Qiddiya, Red Sea, Diriyah, ROSHN), Amana/Baladiya permit workflows, SEEC
programmes, Royal Commission jurisdictions (Jubail, Yanbu, AlUla), Mecca/Medina Hajj
building rules, Aramco housing references, and climate overlays for the three national
climate zones. `country-uae` is included as the neighbour jurisdiction.

## 2. AEC products, specs & project records — 12 of 46 skills

**Source:** `AlpacaLabsLLC/skills-for-architects` · **Method:** Vercel CLI, explicit list

```bash
npx skills add AlpacaLabsLLC/skills-for-architects \
  --skill spec-writer --skill master-schedule --skill product-research \
  --skill product-spec-pdf-parser --skill product-match --skill product-pair \
  --skill slide-deck-generator --skill color-palette-generator \
  --skill epd-parser --skill epd-compare --skill site-visit-report \
  --skill meeting-minutes -g -a hermes-agent --copy -y
```

| Need | Skills |
|---|---|
| Specifications | `spec-writer` (CSI three-part outline specs), `master-schedule` |
| FF&E / fixture scheduling | `product-research`, `product-spec-pdf-parser`, `product-match`, `product-pair` |
| Client communication | `slide-deck-generator`, `color-palette-generator` |
| Sustainability | `epd-parser`, `epd-compare` (GWP comparison) |
| Records | `site-visit-report`, `meeting-minutes` |

**Deliberately skipped (34):** the 10 `nyc-*` zoning/property skills (jurisdiction-
specific to New York), and the `studio` / `project` / `workplan` / `tasklist` /
`timetracker` / `tool-catalog` framework — that set expects a scaffolded studio
workspace (`studio/`, `projects/`, TASKS.md, TIMELOG.md) and adds process overhead
without a firm to run it. Also skipped: the SIF/CSV interchange plumbing and the
image-pipeline utilities.

## 3. Design & creative — 4 skills

**Sources:** `anthropics/skills`, `curiositech/some_claude_skills`

```bash
npx skills add anthropics/skills --skill canvas-design --skill frontend-design \
    --skill theme-factory -g -a hermes-agent --copy -y
npx skills add curiositech/some_claude_skills --skill interior-design-expert \
    -g -a hermes-agent --copy -y --full-depth
```

| Skill | Why |
|---|---|
| `canvas-design` | Posters, presentation one-pagers, static art as PNG/PDF — ships ~40 licensed fonts |
| `frontend-design` | Visual direction that doesn't read as a template |
| `theme-factory` | 10 ready palettes + font pairings to dress decks and docs |
| `interior-design-expert` | Space planning, IES lighting layers, Munsell/NCS colour, furniture proportions, style consultation |

Anthropic's `brand-guidelines` (Anthropic's own branding), `web-artifacts-builder`
(claude.ai-specific), `algorithmic-art` and `webapp-testing` were skipped as duplicates
of capabilities you already have (`p5js`, `dogfood`).

## 4. MCP tooling — 1 skill (hub-installed)

```bash
hermes skills install "anthropics/skills/skills/mcp-builder" \
      --category software-development --yes
```

`mcp-builder` is the reference for building MCP servers (Python FastMCP / Node SDK) and
ships an evaluation harness. Installed through the **hub** on purpose, so
`hermes skills check` / `update` maintain it.

## 5. Hand-written — 1 skill (yours)

| Skill | What it encodes |
|---|---|
| `architecture/villa-lighting-design` | Interior + exterior villa lighting: lux targets and planes, lumen-method + LPD calculator (`scripts/lux_check.py`), gypsum-board ceiling detailing (cove/recessed/linear, loads, clearances), exterior IP/IK and pool safety, a submittal review checklist, and a fixture-schedule template |

Nothing in the ecosystem covered architectural lighting (every "lighting" skill on
skills.sh is 3D-engine lighting — three.js, Blender, Godot), and nothing covers gypsum
ceiling detailing. This is the gap that justified writing rather than installing.

## 6. Optional extras — install on demand

| Skill | For | Command |
|---|---|---|
| `financial-statements` | IS/BS/CF with variance analysis | `npx skills add anthropics/knowledge-work-plugins --skill financial-statements -g -a hermes-agent --copy -y` |
| `3-statement-model` | Fill linked model templates | `npx skills add anthropics/financial-services --skill 3-statement-model -g -a hermes-agent --copy -y` |
| `ifrs-accounting-standards-advisor` | IFRS treatment advisor | `npx skills add camiloespinoza/ifrs-accounting-standards-advisor -g -a hermes-agent --copy -y --full-depth` |
| `arabic-presentations` | RTL-correct Arabic PPTX | `npx skills add sultanalsafran/agent-skills --skill arabic-presentations -g -a hermes-agent --copy -y` |
| `rvt-to-ifc` | Revit/BIM conversion batch tools | `npx skills add datadrivenconstruction/ddc_skills_for_ai_agents_in_construction --skill rvt-to-ifc -g -a hermes-agent --copy -y` |
| `skill-creator` | Skill authoring + evals/benchmarks | `npx skills add anthropics/skills --skill skill-creator -g -a hermes-agent --copy -y` |

Known gap: **no Caseware skill exists anywhere** in the ecosystem (0 search results) —
if you want one, it must be hand-written like `villa-lighting-design`.

## Keeping the catalog honest

```bash
python scripts/scan_installed.py       # regenerate catalog/installed-inventory.json
python scripts/verify_installed.py     # catalog vs reality; exit 1 if anything required is missing
python scripts/install_catalog.py      # dry run: what WOULD be installed
python scripts/install_catalog.py --apply --include-optional
```

When you add a skill, add it to `catalog/skills-catalog.json` **and** to this page —
otherwise the manifest silently drifts from the machine.

Previous: [04-install-recipes.md](04-install-recipes.md) · Next: [06-authoring-skills.md](06-authoring-skills.md)
