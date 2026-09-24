#!/usr/bin/env python3
"""PostToolUse hook: format and lint every Python file Claude edits in addons-custom/.

Formatting is applied silently. Lint problems that ruff cannot fix are sent back
to Claude (stderr + exit code 2) so it fixes them in the same turn. If ruff is not
installed the hook says so once per edit and lets the edit stand.
"""

import json
import os
import shutil
import subprocess
import sys

payload = json.load(sys.stdin)
path = payload.get("tool_input", {}).get("file_path", "")
project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
full = os.path.realpath(os.path.join(project, path)) if path else ""
addons = os.path.realpath(os.path.join(project, "addons-custom"))

if not full.endswith(".py") or not full.startswith(addons + os.sep):
    sys.exit(0)

ruff = shutil.which("ruff")
if not ruff:
    print("ruff is not installed (pip install ruff); skipped lint for " + path, file=sys.stderr)
    sys.exit(0)

subprocess.run([ruff, "format", "--quiet", full], cwd=project, check=False)
result = subprocess.run(
    [ruff, "check", "--fix", "--quiet", full], cwd=project, capture_output=True, text=True
)
if result.returncode:
    print(f"ruff found problems in {path}:\n{result.stdout}{result.stderr}", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
