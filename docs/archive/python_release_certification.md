# PYTHON RELEASE CERTIFICATION

**Measured:** 2026-06-08T12:50:27.550527+00:00

**Status:** PASS (technical) — publish blocked by version 2.0.0 already on PyPI

| Gate | Result |
|------|--------|
| pip install . (clean venv) | EXIT 0 |
| import webweavex (-W error) | 0 warnings, 137 names |
| pytest | 772 passed, 0 failed, 1 skipped |
| wheel + sdist build | both built |
| twine check | both PASSED |
| install wheel OUTSIDE repo | import + public API OK |

Certified on the `python` branch (post determinism-fix merge, commit 6f056d9).
