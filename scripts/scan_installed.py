#!/usr/bin/env python3
"""Scan a Hermes skills root and emit a machine-readable inventory.

Usage:
    python scripts/scan_installed.py                    # -> catalog/installed-inventory.json
    python scripts/scan_installed.py --markdown         # also print a markdown table
    python scripts/scan_installed.py --root C:/path/to/skills --out inv.json

Stdlib only: works with any Python 3.8+ (no PyYAML needed - the frontmatter reader
below handles the subset Hermes skills actually use: scalars, quoted strings, and
`>` / `|` block scalars).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def default_root() -> pathlib.Path:
    """Skills root for the active profile on Windows, else ~/.hermes/skills."""
    local = os.environ.get("LOCALAPPDATA")
    if local and (pathlib.Path(local) / "hermes" / "skills").is_dir():
        return pathlib.Path(local) / "hermes" / "skills"
    return pathlib.Path.home() / ".hermes" / "skills"


def parse_frontmatter(text: str) -> dict:
    """Minimal frontmatter reader: top-level scalars + block scalars."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    lines = m.group(1).splitlines()
    data: dict = {}
    key = None
    buf: list[str] = []
    block = None

    def flush():
        nonlocal buf, key, block
        if key and block:
            data[key] = (" ".join(s.strip() for s in buf if s.strip())).strip()
        buf, key, block = [], None, None

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        is_child = line.startswith((" ", "\t"))
        if not is_child and ":" in line:
            flush()
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            if v in (">", "|", ">-", "|-", ">+", "|+"):
                block = v
            elif v:
                data[key] = v.strip("'\"")
            # empty value with no block marker = nested mapping; ignored on purpose
        elif is_child and block:
            buf.append(line)
    flush()
    return data


def scan(root: pathlib.Path) -> list[dict]:
    found = []
    for skill_md in sorted(root.rglob("SKILL.md")):
        rel = skill_md.parent.relative_to(root)
        parts = list(rel.parts)
        if any(p.startswith(".") for p in parts):        # skip .archive etc.
            continue
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"warn: cannot read {skill_md}: {exc}", file=sys.stderr)
            continue
        fm = parse_frontmatter(text)
        body = text[FRONTMATTER_RE.match(text).end():] if FRONTMATTER_RE.match(text) else text
        folder = skill_md.parent
        found.append({
            "name": fm.get("name") or folder.name,
            "category": "/".join(parts[:-1]) if len(parts) > 1 else "",
            "path": "/".join(parts),
            "description": fm.get("description", ""),
            "version": fm.get("version", ""),
            "platforms": fm.get("platforms", ""),
            "has_references": (folder / "references").is_dir(),
            "has_scripts": (folder / "scripts").is_dir(),
            "has_templates": (folder / "templates").is_dir(),
            "body_chars": len(body),
            "files": sum(1 for p in folder.rglob("*") if p.is_file()),
        })
    return found


def to_markdown(items: list[dict]) -> str:
    out = ["| Skill | Category | Files | Description |", "|---|---|---:|---|"]
    for it in sorted(items, key=lambda x: (x["category"], x["name"])):
        desc = " ".join(str(it["description"]).split())
        if len(desc) > 90:
            desc = desc[:87] + "..."
        out.append(f"| `{it['name']}` | {it['category'] or '—'} | {it['files']} | {desc} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=pathlib.Path, default=None,
                    help="skills root (default: the active Hermes profile)")
    ap.add_argument("--out", type=pathlib.Path,
                    default=pathlib.Path("catalog/installed-inventory.json"))
    ap.add_argument("--markdown", action="store_true", help="also print a markdown table")
    args = ap.parse_args()

    root = args.root or default_root()
    if not root.is_dir():
        print(f"error: skills root not found: {root}", file=sys.stderr)
        return 2

    items = scan(root)
    payload = {
        "skills_root": str(root),
        "count": len(items),
        "with_references": sum(1 for i in items if i["has_references"]),
        "with_scripts": sum(1 for i in items if i["has_scripts"]),
        "categories": sorted({i["category"] for i in items if i["category"]}),
        "skills": items,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"scanned {payload['count']} skills from {root}")
    print(f"  {payload['with_references']} ship references/, {payload['with_scripts']} ship scripts/")
    print(f"  categories: {len(payload['categories'])}")
    print(f"wrote {args.out}")
    if args.markdown:
        print()
        print(to_markdown(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
