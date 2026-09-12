---
name: villa-lighting-design
description: Design and review villa lighting, inside and outside.
version: 0.1.0
author: Ali (Alihkhawaher), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [lighting, villa, gypsum-ceiling, architectural-review, SBC, IES, interior-design]
    related_skills: [pdf, xlsx, docx, maps]
---

# Villa Lighting Design & Review

Design, check and review interior + exterior lighting for villas: layered schemes,
lux targets, lumen-method verification, LPD compliance against the Saudi Building
Code, gypsum-board ceiling detailing (cove / recessed / linear), fixture schedules,
and a submittal review pass on architectural and interior packages.
Technical basis is IES/CIBSE practice; regulatory basis is SBC (601 energy, 201
architectural, 401 electrical, 801 fire) plus SASO labelling. It does not replace a
licensed engineer's stamped design or a Dialux/AGi32 photometric report — it
produces the targets, the schedule, the calcs and the review findings.

## When to Use

- "Design the lighting for this villa / majlis / bedroom / facade."
- "Review this lighting layout / fixture schedule / photometric study."
- "Check the gypsum ceiling detail for these downlights / cove / curtain pocket."
- "How many lux should the kitchen/driveway/pool have?"
- "Check LPD / energy compliance for the lighting."
- Reviewing an architectural or interior design package for lighting-related gaps
  (ceiling heights, coordination, glare, maintenance access).
- Don't use for: commercial/industrial high-bay design, stage/show lighting,
  roadway lighting, or producing stamped photometric files.

## Procedure

Work in this order; each step ends with a checkable output.

1. **Brief and inventory.** Collect per space: use, dimensions (L×W×H), ceiling
   type and height, finishes (reflectance: white ceiling ≈0.8, mid wall ≈0.5,
   wood floor ≈0.2), window/wall orientation, sight-lines, furniture plan,
   client mood references. Output: a space table — one row per room. No design
   before this table exists.

2. **Set illuminance targets.** Take maintained lux from
   `references/illuminance-targets.md` (interior + exterior). Adjust ±1 step for
   age of occupants, task severity, and dark/bright finishes. Output: a target
   lux column on the space table.

3. **Choose the layers per space.** Every space gets: ambient (general),
   task (where a task happens), accent (art, niches, wall texture), decorative
   (chandelier, pendant). A space with only one layer is incomplete — say so in
   review. Output: layer matrix.

4. **Pick luminaires and check the photometry.** For each layer fix mounting,
   beam angle, CCT, CRI, output, dimming and IP. Then verify with the lumen
   method using `scripts/lux_check.py` (see `references/calculation-and-lpd.md`).
   Output: computed lux per room, and a written pass/fail against the target.

5. **Ceiling coordination.** Detail every ceiling element against
   `references/gypsum-ceiling-detailing.md`: cove geometry, recessed pocket
   depth, cut-outs, board thickness, backing for heavy fixtures, clearances to
   AC diffusers, smoke detectors, sprinklers, access panels. Output: dimensioned
   ceiling detail + a coordination-conflict list.

6. **Exterior and facade.** Apply `references/exterior-lighting.md`: ingress
   protection, glare shielding, uplight control, wet-zone safety, KSA climate
   derating. Output: exterior fixture list with IP/IK and mounting heights.

7. **Controls and circuits.** One scene per space minimum; astronomic time
   clock + motion for exterior and stairs; no dimmer below the fixture's
   compatible range. Output: control narrative + circuit/load schedule.

8. **Energy and compliance.** Total connected lighting load, LPD vs the adopted
   SBC 601 edition, SASO efficiency of lamps/drivers, emergency lighting where
   SBC 801/means-of-egress requires. Output: compliance line with the code
   clause cited.

9. **Deliverables.** Fixture schedule (`templates/fixture-schedule.csv`),
   lighting layout per ceiling plan, ceiling details, control narrative,
   calculation sheet, and for reviews a findings report.

## Reviewing a Submitted Package

Use `references/review-checklist.md` end to end, and read the submittal with the
`pdf` skill, check schedules in the `xlsx` skill, and issue the findings in
`docx`. Rules that catch most real defects:

- Every fixture tag on the plan must appear in the schedule with a maker, model,
  wattage, lumens, CCT, CRI, beam, cut-out, IP, driver and dimming method.
  Missing one of those is a finding, not a nitpick.
- Lux claims without a calculation or photometric file are unverified — request
  the file (`.ies`/`.ldt`) or recompute with `scripts/lux_check.py`.
- Recessed fixtures in an insulated ceiling must be IC-rated, or the ceiling
  detail must show an air gap; otherwise it is a fire and heat-derating finding.
- Anything hung from gypsum board above ~10 kg needs framing or a backing plate
  called out on the detail.
- Glare not addressed (UGR, shielding angle, or view angle from the seating
  position) is the single most common interior defect.
- Emergency/egress lighting absent in corridors and stairs is a code finding.

## Pitfalls

1. **Kelvin mixing.** One space, one CCT family (2700–3000 K residential).
   Mixed CCT reads as cheap and is the easiest thing for a client to notice.
2. **Lux at the wrong plane.** Residential maintained illuminance is generally
   quoted on the horizontal task plane (0.75–0.8 m for tables, floor+0.1 m for
   circulation). State the plane with the number.
3. **Ignoring maintenance factor.** Use MF 0.8 interior, 0.6–0.7 exterior before
   claiming compliance; a dirty KSA facade loses output fast.
4. **Cove with no bounce path.** An indirect cove needs a lit surface and
   clearance; a strip tucked into a 40 mm slot lights nothing.
5. **Cut-out vs. actual fixture.** Recessed depth and cut-out must match the
   schedule — 90 mm cut-outs with a 120 mm can is a site variation waiting to
   happen.
6. **Mains-voltage LED on a dimmer it does not support.** Confirm trailing-edge/
   leading-edge compatibility, or specify a protocol (0-10 V, DALI, wireless).
7. **Exterior uplight.** Unshielded uplights on the facade throw light into the
   sky and back into bedrooms — shield and aim them.
8. **SBC numbers drift between editions.** Always cite the edition and clause
   you actually checked; do not quote an LPD value from memory.

## Verification

- `python scripts/lux_check.py --demo` returns computed lux per room and an LPD
  line, with no room below target.
- Every fixture tag on the layout resolves to exactly one schedule row, and
  every schedule row appears on a layout (bidirectional match).
- Every room in the space table has a target lux, a layer matrix row, and a
  computed lux value.
- Every ceiling detail has a dimension and a coordination clearance drawn.
- Every compliance claim names the code edition and clause it was checked against.

## Files

- `references/illuminance-targets.md` — interior + exterior lux/CCT/IP targets.
- `references/gypsum-ceiling-detailing.md` — cove, recessed, linear, weights,
  clearances, board specs.
- `references/exterior-lighting.md` — facade, landscape, pool, security, KSA climate.
- `references/calculation-and-lpd.md` — lumen method, room index, MF, LPD worked example.
- `references/review-checklist.md` — the full submittal review sequence.
- `scripts/lux_check.py` — lumen-method + LPD calculator (stdlib only).
- `templates/fixture-schedule.csv` — schedule columns.
