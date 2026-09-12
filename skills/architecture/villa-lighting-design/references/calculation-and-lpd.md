# Lumen Method, Room Index, Maintenance Factor, LPD

## Lumen method

```
E (lux) = (N x Phi x UF x MF) / A
```

- `N` — number of luminaires
- `Phi` — lumens per luminaire (not per LED chip; use the photometric file's
  rated output)
- `UF` — utilisation factor, from the room index and surface reflectances
  (0.4–0.7 typical residential; 0.5 is a fair default for a mid-reflectance room)
- `MF` — maintenance factor: 0.8 interior, 0.6–0.7 exterior (dust, KSA climate)
- `A` — area of the room (m2)

Room index:

```
K = (L x W) / (Hm x (L + W))
```

- `L`, `W` — room length and width (m)
- `Hm` — mounting height above the working plane, i.e. ceiling height − 0.75 m
  (or − 0.0 m for circulation where the plane is the floor)

Typical `UF` from `K` (ceiling 0.7–0.8, walls 0.5, floor 0.2):

| K | UF |
|---|---|
| 0.6 | 0.40 |
| 0.8 | 0.48 |
| 1.0 | 0.54 |
| 1.5 | 0.62 |
| 2.0 | 0.66 |
| 3.0 | 0.70 |

Rearrange to size the count: `N = (E x A) / (Phi x UF x MF)`, round up, then
re-check the spacing against the ceiling grid.

## Worked example

Majlis 6.0 × 5.0 m, ceiling 3.2 m, target 150 lux, 12 W / 1 000 lm downlight,
UF 0.6, MF 0.8.

- A = 30 m2; Hm = 3.2 − 0.75 = 2.45 m; K = 30 / (2.45 × 11) = 1.11 → UF ≈ 0.56
- N = (150 × 30) / (1000 × 0.56 × 0.8) = 4500 / 448 = 10.0 → 12 fixtures on a
  4 × 3 grid for symmetry
- Achieved E = (12 × 1000 × 0.56 × 0.8) / 30 = 179 lux — above target, which
  leaves headroom for dimming the ambient layer down.

Run it instead of doing it by hand:

```bash
python scripts/lux_check.py --rooms rooms.json
python scripts/lux_check.py --demo
```

## Lighting power density (LPD)

```
LPD (W/m2) = total connected lighting watts / area (m2)
```

- Compute per space and for the whole villa. Use **connected/installed** load
  (driver input watts, not LED chip watts) — that is where designers under-declare.
- Compare against the LPD allowance of the SBC edition actually adopted for the
  project (SBC 601 governs energy conservation, with electrical power and lighting
  in its residential chapters). Do not quote a number from memory: open the
  edition, find the space-type table, and cite the edition and clause in the report.
- Saudi lighting-product energy efficiency labelling (SASO) governs the lamps and
  drivers sold; the LPD check governs the design.
- Where LPD is exceeded, the fixes in cost order: higher-efficacy fixtures, remove
  decorative redundancy, put task lighting on local controls, and only then argue
  a whole-building performance path.

## Uniformity and spacing sanity checks

- Uniform general grid spacing ≈ 1–1.2 × ceiling height to floor.
- Perimeter row ≈ 0.5 × grid spacing off the wall (600–900 mm typical).
- Wall-grazing accents: 300–600 mm off the wall, 600–900 mm apart.
- If the computed lux is met by a single row of high-output fixtures, it will look
  striped — go back to more, lower-output fixtures.
