# FINAL SPECIFICATION AUTHORITY CERTIFICATION

**Measured:** 2026-06-08T07:07:48.310535+00:00

**Status:** PASS

specification/ is the sole authority. Neither implementation defines the other.

| Check | Result | Detail |
|-------|--------|--------|
| Forbidden canonicity claims (active docs/src/validation) | PASS | 0 hits |
| specification/vectors tagged `webweavex-spec` | PASS | specification/vectors/manifest.json |
| Equivalence harness reads specification/vectors | PASS | runUniversalEquivalence.ts |

Both `origin/python` (pip) and `javascript` (npm) products conform to `specification/`; the equivalence harness checks JavaScript against the specification vectors, not against Python.
