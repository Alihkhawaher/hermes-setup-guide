#!/usr/bin/env python3
"""Install the skills listed in catalog/skills-catalog.json.

Dry run by default - nothing changes until you pass --apply.

Usage:
    python scripts/install_catalog.py                     # print what WOULD run
    python scripts/install_catalog.py --apply              # run the installers
    python scripts/install_catalog.py --apply --group "Design & creative"
    python scripts/install_catalog.py --apply --include-optional

Each catalog group carries its own `method` and `command`:
  - method "hermes": hub install (tracked, updatable via `hermes skills update`)
  - method "npx":    Vercel skills CLI copy (lands as Source: local)
  - method "manual": skipped with a pointer to the docs
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shlex
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scan_installed import default_root  # noqa: E402


def missing_folders(group: dict, root: pathlib.Path) -> list[str]:
    out = []
    for entry in group.get("skills", []):
        folder = entry.get("folder", "")
        if folder and not (root / folder / "SKILL.md").is_file():
            out.append(folder)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", type=pathlib.Path,
                    default=pathlib.Path("catalog/skills-catalog.json"))
    ap.add_argument("--root", type=pathlib.Path, default=None)
    ap.add_argument("--group", action="append", default=None,
                    help="only this group (repeatable, substring match)")
    ap.add_argument("--include-optional", action="store_true")
    ap.add_argument("--apply", action="store_true", help="actually run the commands")
    args = ap.parse_args()

    root = args.root or default_root()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    ran, skipped, failed = 0, 0, 0

    for group in catalog.get("groups", []):
        name = group.get("group", "")
        if args.group and not any(g.lower() in name.lower() for g in args.group):
            continue
        required = bool(group.get("required", True))
        if not required and not args.include_optional:
            print(f"\n=== {name}  [optional - skipped, use --include-optional]")
            continue
        missing = missing_folders(group, root)
        print(f"\n=== {name}")
        if not missing:
            print("    all present, nothing to do")
            continue
        print(f"    missing {len(missing)}: {', '.join(missing[:6])}"
              f"{' …' if len(missing) > 6 else ''}")
        method = group.get("method", "")
        if method == "manual":
            print("    manual group - follow docs/06-authoring-skills.md")
            skipped += 1
            continue
        command = group.get("command")
        if not command:
            print("    no command in catalog entry - skipping")
            skipped += 1
            continue
        print(f"    $ {command}")
        if not args.apply:
            skipped += 1
            continue
        # run through the platform shell; npx needs a real shell on Windows
        proc = subprocess.run(command, shell=True)
        if proc.returncode == 0:
            ran += 1
            print("    -> ok")
        else:
            failed += 1
            print(f"    -> FAILED (exit {proc.returncode})")

    print(f"\n{'applied' if args.apply else 'dry run'}: "
          f"{ran} command(s) run, {skipped} skipped, {failed} failed")
    if not args.apply:
        print("re-run with --apply to execute")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
