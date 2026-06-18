# JAVA_SESSION_12_PARITY_PROOF

**Phase 8 — actual parity results (executed).**

## S12 vectors (golden_vectors_s12.json)

| Metric | Value |
| --- | ---: |
| Vector sections | 23 |
| **Total S12 vectors** | **49** |

Public-API sections: build_runtime_evolution 2, evolve_selector_runtime 3,
run_evolution_runtime 9, run_evolution_for_extraction 4, save_evolution_runtime 3,
load_evolution_runtime 4 (incl. missing) + 17 engine-level sections.

## S12 parity test (surefire)

```
Tests run: 49, Failures: 0, Errors: 0, Skipped: 0
  -- in io.webweavex.parity.CrossLanguageParityS12Test
```

| Metric | Value |
| --- | ---: |
| Parity tests (S12) | **49** |
| Pass / Fail / Error / Skip | **49 / 0 / 0 / 0** |

Each `section()` assertion compares **both** `stable_serialize` and `compute_kaalka_hash`; save
asserts written file content byte-for-byte.

## Full suite (mvn clean verify)

```
Tests run: 602, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

**Verdict: PASS.** 49/49 S12 + 602/602 full suite. Oracle = canonical Python 2.1.0
(`origin/python` @ `9625f4a`). No self-consistency tests.
