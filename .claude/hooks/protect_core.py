#!/usr/bin/env python3
"""PreToolUse hook: refuse any edit inside the Odoo core checkout (./odoo).

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call and
shows stderr to Claude, which then knows why and can inherit instead.
"""

import json
import os
import sys

payload = json.load(sys.stdin)
path = payload.get("tool_input", {}).get("file_path", "")
project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
core = os.path.realpath(os.path.join(project, "odoo"))

if path and os.path.realpath(os.path.join(project, path)).startswith(core + os.sep):
    print(
        f"Blocked: {path} is Odoo core, which is read-only in this workspace. "
        "Change the behaviour from a module in addons-custom/ (inherit the model or view).",
        file=sys.stderr,
    )
    sys.exit(2)
sys.exit(0)
