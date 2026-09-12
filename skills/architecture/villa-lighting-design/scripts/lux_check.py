#!/usr/bin/env python3
"""Lumen-method + lighting power density check for villa lighting schemes.

Usage:
  python scripts/lux_check.py --rooms rooms.json
  python scripts/lux_check.py --demo

rooms.json shape:
{
  "rooms": [
    {
      "name": "Majlis",
      "length": 6.0, "width": 5.0, "height": 3.2,
      "work_plane": 0.75,
      "target_lux": 150,
      "fixtures": [
        {"tag": "L-01", "qty": 12, "lumens": 1000, "watts": 12, "uf": 0.56}
      ],
      "mf": 0.8,
      "lpd_limit": 12.0
    }
  ]
}

Per fixture: `uf` optional (defaults to 0.55). Per room: `mf` optional
(defaults 0.8); `lpd_limit` optional (W/m2). Exit code 1 if any check fails.
"""
import argparse
import json
import sys

DEFAULT_UF = 0.55
DEFAULT_MF = 0.8


def room_index(length, width, height, work_plane):
    hm = height - work_plane
    if hm <= 0 or (length + width) <= 0:
        return None, hm
    return (length * width) / (hm * (length + width)), hm


def check_room(room):
    length = float(room["length"])
    width = float(room["width"])
    height = float(room["height"])
    work_plane = float(room.get("work_plane", 0.75))
    target = room.get("target_lux")
    target = float(target) if target is not None else None
    mf = float(room.get("mf", DEFAULT_MF))
    area = length * width
    k, hm = room_index(length, width, height, work_plane)

    total_lm = 0.0
    total_w = 0.0
    rows = []
    for fixture in room.get("fixtures", []):
        qty = int(fixture.get("qty", 0))
        lumens = float(fixture.get("lumens", 0))
        watts = float(fixture.get("watts", 0))
        uf = float(fixture.get("uf", DEFAULT_UF))
        effective_lm = qty * lumens * uf * mf
        total_lm += effective_lm
        total_w += qty * watts
        rows.append({"tag": fixture.get("tag", "?"), "qty": qty, "uf": uf,
                     "effective_lm": round(effective_lm)})

    achieved = total_lm / area if area else 0.0
    lpd = total_w / area if area else 0.0
    limit = room.get("lpd_limit")
    return {
        "name": room.get("name", "unnamed"),
        "area": round(area, 2),
        "room_index": round(k, 3) if k else None,
        "mounting_height": round(hm, 2),
        "target_lux": target,
        "achieved_lux": round(achieved, 1),
        "target_pct": round(100.0 * achieved / target, 1) if target else None,
        "connected_w": round(total_w, 1),
        "lpd": round(lpd, 2),
        "lpd_limit": float(limit) if limit is not None else None,
        "lpd_ok": (lpd <= float(limit)) if limit is not None else None,
        "lux_ok": (achieved >= target) if target else None,
        "fixtures": rows,
    }


def report(results, verbose=False):
    fails = []
    header = (f"{'room':<22}{'area m2':>9}{'K':>7}{'target':>8}{'achieved':>10}"
              f"{'%':>7}{'W':>8}{'LPD':>8}{'limit':>8}  verdict")
    print(header)
    print("-" * len(header))
    total_w = 0.0
    total_area = 0.0
    for r in results:
        total_w += r["connected_w"]
        total_area += r["area"]
        verdict = []
        if r["lux_ok"] is False:
            verdict.append("LOW LUX")
            fails.append(f"{r['name']}: {r['achieved_lux']} lux < target {r['target_lux']}")
        if r["lpd_ok"] is False:
            verdict.append("LPD OVER")
            fails.append(f"{r['name']}: LPD {r['lpd']} > limit {r['lpd_limit']}")
        if r["lux_ok"] is None:
            verdict.append("no target set")
        print(f"{r['name'][:21]:<22}{r['area']:>9.2f}"
              f"{(r['room_index'] or 0):>7.2f}"
              f"{(r['target_lux'] or 0):>8.0f}"
              f"{r['achieved_lux']:>10.1f}"
              f"{(r['target_pct'] or 0):>7.1f}"
              f"{r['connected_w']:>8.1f}{r['lpd']:>8.2f}"
              f"{(r['lpd_limit'] or 0):>8.1f}  "
              + ("OK" if not verdict or verdict == ["no target set"] else ", ".join(verdict)))
        if verbose:
            for f in r["fixtures"]:
                print(f"    {f['tag']:<10} qty {f['qty']:>3}  UF {f['uf']:.2f}  "
                      f"effective {f['effective_lm']} lm")
    print("-" * len(header))
    if total_area:
        print(f"total connected {total_w:.0f} W over {total_area:.0f} m2 = "
              f"{total_w / total_area:.2f} W/m2 whole-villa check")
    if fails:
        print("\nFAILING CHECKS:")
        for f in fails:
            print(" - " + f)
        return 1
    print("\nAll rooms meet their target lux and LPD limit.")
    return 0


DEMO = {"rooms": [
    {"name": "Majlis", "length": 6.0, "width": 5.0, "height": 3.2,
     "work_plane": 0.75, "target_lux": 150, "mf": 0.8, "lpd_limit": 12.0,
     "fixtures": [{"tag": "L-01", "qty": 12, "lumens": 1000, "watts": 12,
                   "uf": 0.56}]},
    {"name": "Kitchen", "length": 4.5, "width": 4.0, "height": 3.0,
     "work_plane": 0.85, "target_lux": 300, "mf": 0.8, "lpd_limit": 12.0,
     "fixtures": [{"tag": "L-05", "qty": 10, "lumens": 1100, "watts": 12,
                   "uf": 0.60},
                  {"tag": "L-06", "qty": 4, "lumens": 700, "watts": 8,
                   "uf": 0.35}]},
    {"name": "Bedroom 1", "length": 5.0, "width": 4.0, "height": 3.0,
     "work_plane": 0.75, "target_lux": 100, "mf": 0.8, "lpd_limit": 12.0,
     "fixtures": [{"tag": "L-07", "qty": 6, "lumens": 800, "watts": 9,
                   "uf": 0.55}]},
    {"name": "Facade wash", "length": 20.0, "width": 1.0, "height": 6.0,
     "work_plane": 0.0, "target_lux": 30, "mf": 0.65, "lpd_limit": 10.0,
     "fixtures": [{"tag": "L-03", "qty": 8, "lumens": 2400, "watts": 24,
                   "uf": 0.25}]},
]}


def main():
    parser = argparse.ArgumentParser(description="Villa lighting lux and LPD check")
    parser.add_argument("--rooms", help="JSON file containing a rooms list")
    parser.add_argument("--demo", action="store_true", help="run the bundled example")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print per-fixture effective lumens")
    args = parser.parse_args()
    if args.demo or not args.rooms:
        data = DEMO
    else:
        with open(args.rooms, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    rooms = data.get("rooms", []) if isinstance(data, dict) else data
    if not rooms:
        print("no rooms found in input", file=sys.stderr)
        return 2
    return report([check_room(r) for r in rooms], verbose=args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
