#!/usr/bin/env python3
"""Stage the Odoo 19 copy of the course module.

The 18.0 tree is never edited for 19. This copies it and applies what Odoo 19
needs for this module - the same rules as .claude/rules/odoo19.md:

* manifest version prefix 18.0 -> 19.0 (Odoo refuses a module from another series);
* ``_sql_constraints`` -> ``models.Constraint`` class attributes. Odoo 19 ignores
  ``_sql_constraints`` SILENTLY: the module installs and the constraint is never
  created. Only a test that expects the constraint to fire catches it.

    port19.py <src module dir> <dst module dir>
"""

import re
import shutil
import sys
from pathlib import Path

CONSTRAINTS = re.compile(r"\n    _sql_constraints = \[\n(?P<body>.*?)\n    \]\n", re.S)
ENTRY = re.compile(r'\(\s*"(?P<name>\w+)",\s*"(?P<sql>[^"]+)",\s*"(?P<msg>[^"]+)",\s*\)', re.S)


def convert(match):
    parts = []
    for entry in ENTRY.finditer(match.group("body")):
        parts.append(
            f"\n    _{entry['name']} = models.Constraint(\n"
            f'        "{entry["sql"]}",\n'
            f'        "{entry["msg"]}",\n'
            "    )\n"
        )
    if not parts:
        raise SystemExit("port19: could not parse a _sql_constraints block")
    return "".join(parts)


def main(src, dst):
    src, dst = Path(src), Path(dst)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))

    manifest = dst / "__manifest__.py"
    text, count = re.subn(r'"version": "18\.0\.', '"version": "19.0.', manifest.read_text("utf-8"))
    if count != 1:
        raise SystemExit("port19: manifest version not found")
    manifest.write_text(text, "utf-8")

    for path in (dst / "models").glob("*.py"):
        text = path.read_text("utf-8")
        new, count = CONSTRAINTS.subn(convert, text)
        if count:
            path.write_text(new, "utf-8")
            print(f"  {path.name}: {count} constraint block(s) converted")
    print("staged", dst)


if __name__ == "__main__":
    main(*sys.argv[1:3])
