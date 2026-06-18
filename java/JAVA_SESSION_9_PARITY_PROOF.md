# JAVA_SESSION_9_PARITY_PROOF

**Phase 2 — actual parity results (executed, not narrated).**

## S9 vector inventory (golden_vectors_s9.json)

| Metric | Value |
| --- | ---: |
| Vector sections | 22 |
| **Total S9 vectors** | **89** |

Per section: build_runtime_sandbox 8, execute_runtime_action 9, replay_runtime_execution 4,
simulate_runtime_execution 4, run_execution_runtime 8, run_execution_for_extraction 5,
apply_runtime_transition 11, build_runtime_policy 2, enforce_runtime_policy 4,
validate_runtime_permissions 6, track_runtime_mutations 7, enqueue_runtime_action 2,
dequeue_runtime_action 2, schedule_runtime_execution 2, begin_runtime_transaction 2,
commit_runtime_transaction 1, build_runtime_workers 2, federate_runtime_execution 2,
coordinate_runtime_execution 2, recover_runtime_execution 2, build_runtime_action 2,
build_unified_runtime_graph 2.

## S9 parity test (CrossLanguageParityS9Test) — surefire output

```
Tests run: 89, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.168 s
  -- in io.webweavex.parity.CrossLanguageParityS9Test
```

| Metric | Value |
| --- | ---: |
| Parity tests (S9) | **89** |
| Pass | **89** |
| Fail | **0** |
| Error | **0** |
| Skipped | **0** |

Each test asserts **two** byte-exact equalities — `stable_serialize` and `compute_kaalka_hash`
of the Java output vs the Python-recorded value (2 × 89 = 178 byte-exact assertions).

## Full suite (mvn clean verify)

```
Tests run: 454, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

| Metric | Value |
| --- | ---: |
| Total tests | **454** |
| Pass | **454** |
| Fail / Error | **0 / 0** |

**Verdict: PASS.** 89/89 S9 parity tests green; 454/454 full suite green; oracle is canonical
Python 2.1.0 (`origin/python` @ `9625f4a`).
