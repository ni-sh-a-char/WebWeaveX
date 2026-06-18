# JAVA_SESSION_13_CERTIFICATION

**Entire `core.causality` family — 5 APIs, ~18 sub-engines, byte-exact.** Branch `java`.
Python canon `origin/python` @ `9625f4a` (2.1.0).

## Implemented APIs (5) — full family, no cherry-pick

| API | Java | Python canon |
| --- | --- | --- |
| `run_causality_runtime` | `io.webweavex.causality.CausalityRuntime#runCausalityRuntime` | `causality_orchestrator` (fans to ~18 engines + IR) |
| `replay_causal_runtime` | `…#replayCausalRuntime` | `causal_replay_engine` |
| `run_causality_for_extraction` | `…#runCausalityForExtraction` | orchestrator + IR-to-graph + unified-graph merge |
| `save_causal_memory` | `…#saveCausalMemory` | `causal_memory_engine` (FS + Kaalka + json.dumps) |
| `load_causal_memory` | `…#loadCausalMemory` | `causal_memory_engine` (FS + Kaalka + json.loads) |

All ~18 sub-engines + the causal IR + reused runtime-graph IR-merge ported. **ZERO new
substrate** — reuses StableSerialize/Kaalka/PyJson/PyJsonParse/PyRepr/Normalization/
`ExecutionRuntime.buildUnifiedRuntimeGraph`. No stubs.

## Proofs

- **Dependency:** [`JAVA_SESSION_13_DEPENDENCY_PROOF.md`](JAVA_SESSION_13_DEPENDENCY_PROOF.md) — 25 modules / 0 forbidden.
- **Traceability:** [`JAVA_SESSION_13_TRACEABILITY.md`](JAVA_SESSION_13_TRACEABILITY.md) — no orphan.
- **Parity:** [`JAVA_SESSION_13_PARITY_PROOF.md`](JAVA_SESSION_13_PARITY_PROOF.md) — **44/44** byte-exact (44 vectors / 22 sections, incl. 17 engine-level).
- **Coverage:** [`JAVA_SESSION_13_COVERAGE_PROOF.md`](JAVA_SESSION_13_COVERAGE_PROOF.md) — **96.35 % → 96.38 %** (CausalityRuntime 96.5 %).
- **Governance:** [`JAVA_SESSION_13_GOVERNANCE_AUDIT.md`](JAVA_SESSION_13_GOVERNANCE_AUDIT.md) — validator PASS 61/128.
- **Blocker:** [`JAVA_SESSION_13_BLOCKER_AUDIT.md`](JAVA_SESSION_13_BLOCKER_AUDIT.md) — no causality blocker.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 56 | **61** |
| Remaining (of 128) | 72 | **67** |
| Total tests | 602 | **646** |
| Instruction coverage | 96.35 % | **96.38 %** |
| `PROVEN_FLOOR` | 56 | **61** |

`mvn clean verify` BUILD SUCCESS (646/0/0). Manifest unchanged. All tests parity-backed.

## Next

[`JAVA_SESSION_14_PLAN.md`](JAVA_SESSION_14_PLAN.md): `core.streaming` (4 APIs, zero substrate).
Mission active — 61/128.
