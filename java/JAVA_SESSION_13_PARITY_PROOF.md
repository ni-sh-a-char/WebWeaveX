# JAVA_SESSION_13_PARITY_PROOF

**Phase 8 — actual parity results (executed).**

## S13 vectors (golden_vectors_s13.json)

| Metric | Value |
| --- | ---: |
| Vector sections | 22 |
| **Total S13 vectors** | **44** |

Public-API sections: run_causality_runtime 8, replay_causal_runtime 2,
run_causality_for_extraction 4, save_causal_memory 3, load_causal_memory 4 (incl. missing)
+ 17 engine-level sections.

## S13 parity test (surefire)

```
Tests run: 44, Failures: 0, Errors: 0, Skipped: 0
  -- in io.webweavex.parity.CrossLanguageParityS13Test
```

| Metric | Value |
| --- | ---: |
| Parity tests (S13) | **44** |
| Pass / Fail / Error / Skip | **44 / 0 / 0 / 0** |

Each `section()` assertion compares **both** `stable_serialize` and `compute_kaalka_hash`; save
asserts written file content byte-for-byte.

## Full suite (mvn clean verify)

```
Tests run: 646, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

**Verdict: PASS.** 44/44 S13 + 646/646 full suite. Oracle = canonical Python 2.1.0
(`origin/python` @ `9625f4a`). No self-consistency tests.
