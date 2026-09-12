# 06 — Writing a skill that actually triggers

Installing is the easy half. The skills that earn their context are the ones you write,
because they encode procedures nobody else has.

## Ask the agent to write it

```python
skill_manage(action="create", name="my-skill", category="architecture",
             content="---\nname: my-skill\ndescription: One-line trigger.\n---\n\n# My Skill\n...")
```

It validates frontmatter, lands the file in the right profile folder, and can add
`references/`, `scripts/`, `templates/` in follow-up calls. Then read the file yourself —
if the agent wrote it, you own reviewing it.

## Structure that works

```
skills/<category>/<name>/
├── SKILL.md
├── references/<topic>.md      depth that would bloat the body
├── scripts/<helper>.py        deterministic work the model shouldn't re-derive
└── templates/<file>           skeletons to copy
```

Body shape (battle-tested, and what review expects to see):

```markdown
# <Skill> Skill
2–3 sentences: what it does, what it does NOT do.

## When to Use
- bullet triggers, written the way you'd actually ask
- Don't use for: <counter-triggers>   ← prevents mis-triggering

## Procedure
1. Step, ending in a checkable output ("Output: a space table, one row per room")
2. …

## Pitfalls
1. Failure mode → what to do instead

## Verification
- The command you run to prove the job is done, and its expected shape

## Files
- references/… , scripts/… , templates/…
```

Rules that separate a skill that fires from one that rots:

1. **The `description` is the trigger, and it is all the model sees by default.** Keep it
   under ~60 characters (the index truncates at 57 + `…`). "Design and review villa
   lighting, inside and outside." beats "A comprehensive framework for…".
2. **One skill, one job.** If the When-to-Use list needs an "or", split it.
3. **Every procedure step ends in an artifact or a pass/fail.** "Consider the ceiling" is
   noise; "Output: a dimensioned ceiling detail + a conflict list" is a step.
4. **Put numbers in `references/`, rules in the body.** Tables of lux targets, code
   clauses, dimension ranges: references. The rule "never hang >10 kg from board alone":
   body.
5. **Ship scripts for anything deterministic** — calculators, converters, validators.
   Cheaper and more reliable than asking the model to redo arithmetic every run, and the
   script doubles as the skill's verification step.
6. **Write the pitfalls from your own failures.** A pitfall list is a scar log: the first
   time a job goes wrong for a silly reason, add the pitfall. Delete any pitfall that
   stops changing behaviour.
7. **Say what the skill does not do.** Boundaries prevent it from being pulled into the
   wrong task and prevent it from inventing authority it doesn't have (e.g. "does not
   replace a stamped photometric report").

## Testing your skill

There is no test harness for prose, but there is for the parts that matter:

```bash
# 1. frontmatter parses and the description is short enough
python - <<'EOF'
import pathlib, re, sys
p = pathlib.Path(r"C:\Users\Ali\AppData\Local\hermes\skills\architecture\my-skill\SKILL.md")
c = p.read_text(encoding="utf-8")
assert c.startswith("---"), "frontmatter must start at byte 0"
m = re.search(r"\n---\s*\n", c[3:]); assert m, "unclosed frontmatter"
head = c[3:m.start()+3]
desc = re.search(r"^description:\s*(.+)$", head, re.M)
assert desc, "no description"
print("description chars:", len(desc.group(1).strip()))
EOF

# 2. every shipped script runs
python skills/architecture/my-skill/scripts/helper.py --demo

# 3. it appears in the catalog (new session required - see pitfalls)
hermes skills list | grep my-skill
```

Then use it on a real task the same day. A skill that hasn't survived one real job is a
draft.

## Pitfalls learned the hard way

| Symptom | Cause | Fix |
|---|---|---|
| Skill invisible right after creating it | the index is cached at session start | start a new session (`/new`) |
| Two skills with the same `name:` | installed twice, from different sources | find duplicates, keep the tracked one (see 04-install-recipes.md) |
| Blank Category in `hermes skills list` | the Vercel CLI copies to the top level | file it under a category, or reinstall with `hermes skills install --category` |
| Skill never triggers | description too long/generic, or buried past char 57 | rewrite the description as a specific trigger |
| Skill triggers for everything | no "Don't use for" counter-triggers | add them |
| `related_skills` points nowhere | referenced a skill that isn't installed | only reference existing skills |
| Script fails on another machine | hardcoded absolute path | keep paths relative to the skill folder |

## Sharing a skill

- **With your future self:** it's already in the profile; `hermes skills snapshot export`
  captures it (see [07-maintenance.md](07-maintenance.md)).
- **With a team/repo:** put it in the project at `.hermes/skills/<name>/` and commit it;
  teammates run `hermes skills trust` once. Nothing loads until they do.
- **Publicly:** publish to a registry with `hermes skills publish`, or push a GitHub repo
  containing `skills/<name>/SKILL.md` — it then installs with
  `hermes skills install <owner>/<repo>/<path>` or `npx skills add <owner>/<repo>`.

Previous: [05-catalog.md](05-catalog.md) · Next: [07-maintenance.md](07-maintenance.md)
