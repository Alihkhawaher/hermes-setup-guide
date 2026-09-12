# 02 — How skills work

A skill is a folder containing a `SKILL.md`: YAML frontmatter plus markdown
instructions. Hermes indexes every skill's **name + description** into the system prompt
(that index costs context on every turn), and loads the **body** only when the task
matches — that is the whole point: procedures cost nothing until they're relevant.

## Anatomy

```
skills/
└── architecture/
    └── villa-lighting-design/
        ├── SKILL.md                  ← required: frontmatter + instructions
        ├── references/
        │   ├── illuminance-targets.md
        │   └── gypsum-ceiling-detailing.md
        ├── scripts/
        │   └── lux_check.py          ← executable helpers the skill tells the agent to run
        └── templates/
            └── fixture-schedule.csv
```

- **The category is the parent folder name.** `skills/architecture/villa-lighting-design/`
  shows category `architecture`. A skill sitting directly in `skills/` has a blank
  category — functional, just flat. Categories are pure organisation; they do not affect
  loading.
- **`references/`** holds depth that would bloat the body (checklists, tables, domain
  rules). The skill body points at them; the agent reads them on demand.
- **`scripts/`** holds deterministic helpers (calculators, converters, validators).
  Prefer shipping a script over asking the model to re-derive logic every run.
- **`templates/`** holds skeletons to copy (schedules, report outlines, config files).

## Frontmatter

```yaml
---
name: villa-lighting-design
description: Design and review villa lighting, inside and outside.
version: 0.1.0
author: Ali (Alihkhawaher), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [lighting, villa, gypsum-ceiling]
    related_skills: [pdf, xlsx, docx]
---
```

| Field | Rule |
|---|---|
| `name` | lowercase-with-hyphens, ≤64 chars, matches the folder by convention |
| `description` | **the trigger.** Keep it under ~60 chars so it survives index truncation (the prompt clips at 57 chars + `…`). Start with what it does, not marketing |
| `platforms` | gate it honestly — a skill whose scripts use `osascript` is `[macos]` |
| `metadata.hermes.related_skills` | only names that actually exist locally, or the reference dangles |

The body then follows a predictable shape: **When to Use** (triggers + counter-triggers),
**Procedure** (numbered, each step ending in a checkable output), **Pitfalls**,
**Verification**, **Files**.

## Loading model

1. Session start → all skill *descriptions* are indexed into the prompt.
2. Task arrives → matching skills' *bodies* are pulled in; linked files are read on demand.
3. **The index is cached for the session** — a skill installed mid-session will not appear
   in that session's catalog. Start a new session (or `/new`) to see it. This is expected
   behaviour, not a failure.

## Cost awareness

Every installed skill adds a line to the per-turn index. A curated 50-skill catalog is
cheap; a hoarded 300-skill catalog degrades selection quality — near-duplicates compete
for the same trigger and the model picks worse. Install for capability, prune for
precision. (Hermes also ships a **curator** that tracks usage in
`skills/.usage.json`; see [07-maintenance.md](07-maintenance.md).)

## Skills vs MCP servers

They solve different problems and are often confused:

| | Skill | MCP server |
|---|---|---|
| What it is | instructions/procedures in markdown | a running process exposing tools |
| Cost | context only, loaded on demand | process + tool schemas in every request |
| Use for | "how to do this well", domain rules, checklists, calculations | live data access, accounts, hardware, external APIs |
| In Hermes | `hermes skills …` | `hermes mcp …`, or the `setup_mcp` tool that proposes a server as an inline consent card |

Rule of thumb: if the answer fits in a document, write a skill. If it needs to *call*
something, write an MCP server — and write a skill that explains when to use it.

Previous: [01-environment.md](01-environment.md) · Next: [03-skill-sources.md](03-skill-sources.md)
