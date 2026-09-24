---
description: Write a failing test for a behaviour first, then make it pass
argument-hint: <module> <behaviour to test, in one sentence>
---

Test-first for: $ARGUMENTS

1. Find where the behaviour lives (model and method). Read the existing tests and the shared
   fixtures in `tests/common.py` if there is one; reuse them.
2. Write ONE test whose name states the behaviour (`test_<what_happens>`), tagged
   `post_install`, `-at_install`. Pass "today" into date logic instead of reading the clock.
3. Run only this module's tests and show me that the new test FAILS, with the assertion
   message. If it passes already, stop and tell me: the behaviour exists or the test is wrong.
4. Change the code, not the test, until it passes. Run the module's whole suite again.
5. Report: the test name, the failing line from step 3, the fix, and the final summary line.
   Never weaken or delete an existing test to get there.
