# JAVASCRIPT RELEASE CERTIFICATION

**Measured:** 2026-06-08T12:50:27.550527+00:00

**Status:** PASS (technical) — publish blocked by version 2.0.0 already on npm

| Gate | Result |
|------|--------|
| npm ci | EXIT 0 |
| npm run build | EXIT 0 |
| npm run typecheck | 0 errors |
| npm test | 399 passed (clean run) |
| coverage | 99.17/99.65/95.44/99.17 |
| npm pack | 9 files (dist+README+LICENSE+package.json), 0 non-product |
| clean-dir install | ESM+CJS 229 exports, Python-free |

Note: a single browser-continuation test timed out once under self-inflicted background contention; passes in 3.6s isolated; hardened with a 120s per-test budget (assertions unchanged).
