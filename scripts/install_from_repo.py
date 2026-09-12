#!/usr/bin/env python3
"""Install the skills vendored in this repository into a Hermes profile (offline).

Dry run by default - nothing is written until you pass --apply.

Usage:
    python scripts/install_from_repo.py                       # show what would be copied
    python scripts/install_from_repo.py --apply                # copy them in
    python scripts/install_from_repo.py --apply --force        # overwrite existing copies
    python scripts/install_from_repo.py --apply --only architecture/villa-lighting-design

Layout expected (this repo):
    skills/<category>/<skill>/SKILL.md
    skills/software-development/<skill>/SKILL.md
    skills/_sources/...            <- licenses, never copied

Target (Hermes profile):
    %LOCALAPPDATA%\\hermes\\skills\\<category>\\<skill>\\...

No network access, no package manager: this is the air-gapped path.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scan_installed import default_root  # noqa: E402

SKIP_DIRS = {"_sources"}


def discover(source: pathlib.Path) -> list[tuple[str, pathlib.Path]]:
    """Return (relative_target, skill_dir) for every skill in the vendored tree."""
    found = []
    for skill_md in sorted(source.rglob("SKILL.md")):
        rel = skill_md.parent.relative_to(source)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        found.append((str(rel).replace("\\", "/"), skill_md.parent))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=pathlib.Path, default=pathlib.Path("skills"),
                    help="vendored skills folder in this repo (default: ./skills)")
    ap.add_argument("--root", type=pathlib.Path, default=None,
                    help="target skills root (default: the active Hermes profile)")
    ap.add_argument("--only", action="append", default=None,
                    help="limit to these skill folders (repeatable, substring match)")
    ap.add_argument("--force", action="store_true", help="overwrite existing skills")
    ap.add_argument("--apply", action="store_true", help="actually copy")
    args = ap.parse_args()

    if not args.source.is_dir():
        print(f"error: no vendored skills at {args.source}", file=sys.stderr)
        return 2
    root = args.root or default_root()

    copied, skipped, planned = 0, 0, 0
    for rel, src in discover(args.source):
        if args.only and not any(o.lower() in rel.lower() for o in args.only):
            continue
        dst = root / rel
        exists = (dst / "SKILL.md").is_file()
        if exists and not args.force:
            print(f"  skip   {rel}  (already installed)")
            skipped += 1
            continue
        if not args.apply:
            print(f"  would  {rel}  ->  {dst}")
            planned += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  copied {rel}  ->  {dst}")
        copied += 1

    print(f"\ntarget: {root}")
    if args.apply:
        print(f"copied {copied}, skipped {skipped} existing.")
        if copied:
            print("Start a NEW Hermes session — the skill index is built at session start.")
            print("Then check: hermes skills list | tail -2")
    else:
        print(f"dry run: {planned} skill(s) would be copied, {skipped} already present.")
        print("re-run with --apply to copy them in.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())