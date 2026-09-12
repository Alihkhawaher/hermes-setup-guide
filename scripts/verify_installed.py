#!/usr/bin/env python3
"""Verify the skills in catalog/skills-catalog.json are actually installed.

Usage:
    python scripts/verify_installed.py                 # human report, exit 1 if required missing
    python scripts/verify_installed.py --json           # machine-readable
    python scripts/verify_installed.py --include-optional

Checks for the folder + a SKILL.md inside it. Presence only - it does not judge quality.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scan_installed import default_root  # noqa: E402  (same-directory helper)


def load_catalog(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(catalog: dict, root: pathlib.Path, include_optional: bool) -> list[dict]:
    results = []
    for group in catalog.get("groups", []):
        required = bool(group.get("required", True))
        if not required and not include_optional:
            continue
        for entry in group.get("skills", []):
            folder = entry.get("folder", entry.get("name", ""))
            target = root / folder
            results.append({
                "group": group.get("group", ""),
                "required": required,
                "skill": entry.get("name", pathlib.PurePath(folder).name),
                "folder": folder,
                "installed": (target / "SKILL.md").is_file(),
                "purpose": entry.get("purpose", ""),
            })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", type=pathlib.Path,
                    default=pathlib.Path("catalog/skills-catalog.json"))
    ap.add_argument("--root", type=pathlib.Path, default=None,
                    help="skills root (default: the active Hermes profile)")
    ap.add_argument("--include-optional", action="store_true",
                    help="also check groups marked required=false")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.root or default_root()
    if not args.catalog.is_file():
        print(f"error: catalog not found: {args.catalog}", file=sys.stderr)
        return 2

    results = check(load_catalog(args.catalog), root, args.include_optional)
    missing_required = [r for r in results if r["required"] and not r["installed"]]
    missing_optional = [r for r in results if not r["required"] and not r["installed"]]

    if args.json:
        print(json.dumps({
            "skills_root": str(root),
            "checked": len(results),
            "installed": sum(1 for r in results if r["installed"]),
            "missing_required": missing_required,
            "missing_optional": missing_optional,
        }, indent=2))
        return 1 if missing_required else 0

    print(f"skills root: {root}")
    group = None
    for r in results:
        if r["group"] != group:
            group = r["group"]
            print(f"\n[{group}]")
        mark = "OK  " if r["installed"] else ("MISS" if r["required"] else "opt ")
        print(f"  {mark} {r['skill']:<34} {r['folder']}")

    ok = sum(1 for r in results if r["installed"])
    print(f"\n{ok}/{len(results)} present"
          f"{'' if not missing_optional else f' · {len(missing_optional)} optional not installed'}")
    if missing_required:
        print("\nMISSING (required):")
        for r in missing_required:
            print(f"  - {r['skill']}  ->  expected at {root / r['folder']}")
        print("\nInstall with: python scripts/install_catalog.py --apply")
        return 1
    print("catalog satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
