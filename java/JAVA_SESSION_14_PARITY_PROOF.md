# JAVA_SESSION_14_PARITY_PROOF

**Phase 8 — actual parity results (executed).**

## S14 vectors (golden_vectors_s14.json)

| Metric | Value |
| --- | ---: |
| Vector sections | 12 |
| **Total S14 vectors** | **34** |

Comparison modes: direct `stable_serialize` + `compute_kaalka_hash` for the serializable APIs and
engines; **projection parity** for `run_live_runtime` (every non-cyclic output path compared to
the oracle); file-content byte-exact for `save_live_runtime`; root-normalized FS-walk for the
null-snapshot filesystem branch.

## S14 parity test (surefire)

```
Tests run: 34, Failures: 0, Errors: 0, Skipped: 0
  -- in io.webweavex.parity.CrossLanguageParityS14Test
```

## Full suite (mvn clean verify)

```
Tests run: 680, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

**Verdict: PASS.** 34/34 S14 + 680/680 full suite. Oracle = canonical Python 2.1.0
(`origin/python` @ `9625f4a`). No self-consistency tests.
