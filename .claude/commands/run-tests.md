---
description: Install a module on a fresh test database, run its tests and summarise the result
argument-hint: <module> [18|19]
allowed-tools: Bash(dropdb --if-exists course18_test), Bash(./venv/bin/python odoo/odoo-bin:*), Bash(ruff check:*), Read, Grep
---

Run the tests of: $ARGUMENTS (default series 18).

1. `ruff check addons-custom/<module>`.
2. Drop `course18_test` and run the install + test command from CLAUDE.md with
   `--log-level=test`, saving the log to `/tmp/<module>_test.log`.
3. From the log report: the exit code, the `N failed, M error(s) of T tests` line, and for
   each failure or error the test name and the last 10 lines of its traceback. Ignore
   `duplicate key value violates unique constraint` lines that come from a test expecting it.
4. Do not change any file. If something failed, end with your diagnosis of the likely cause
   and the file you would change, and wait.
