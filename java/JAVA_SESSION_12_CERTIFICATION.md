# JAVA_SESSION_12_CERTIFICATION

**Entire `core.evolution_runtime` family — 6 APIs, ~17 sub-engines, byte-exact.** Branch `java`.
Python canon `origin/python` @ `9625f4a` (2.1.0).

## Implemented APIs (6) — full family, no cherry-pick

| API | Java | Python canon |
| --- | --- | --- |
| `build_runtime_evolution` | `io.webweavex.evolution.EvolutionRuntime#buildRuntimeEvolution` | `runtime_evolution_engine` |
| `evolve_selector_runtime` | `…#evolveSelectorRuntime` | `selector_evolution_engine` |
| `run_evolution_runtime` | `…#runEvolutionRuntime` | `runtime_evolution_orchestrator` (fans to ~17 engines + IR) |
| `run_evolution_for_extraction` | `…#runEvolutionForExtraction` | orchestrator + IR-to-graph + unified-graph merge |
| `save_evolution_runtime` | `…#saveEvolutionRuntime` | `runtime_memory_engine` (FS + Kaalka + json.dumps) |
| `load_evolution_runtime` | `…#loadEvolutionRuntime` | `runtime_memory_engine` (FS + Kaalka + json.loads) |

All ~17 sub-engines + the evolution IR + reused runtime-graph IR-merge ported. Only new helper:
`sha256hex32` (evolution-id hashing). No stubs. Reuses StableSerialize/Kaalka/PyJson/PyJsonParse/
PyRepr/Normalization/`ExecutionRuntime.buildUnifiedRuntimeGraph`.

## Proofs

- **Dependency:** [`JAVA_SESSION_12_DEPENDENCY_PROOF.md`](JAVA_SESSION_12_DEPENDENCY_PROOF.md) — 25 modules / 0 forbidden.
- **Traceability:** [`JAVA_SESSION_12_TRACEABILITY.md`](JAVA_SESSION_12_TRACEABILITY.md) — no orphan.
- **Parity:** [`JAVA_SESSION_12_PARITY_PROOF.md`](JAVA_SESSION_12_PARITY_PROOF.md) — **49/49** byte-exact (49 vectors / 23 sections, incl. 17 engine-level).
- **Coverage:** [`JAVA_SESSION_12_COVERAGE_PROOF.md`](JAVA_SESSION_12_COVERAGE_PROOF.md) — **96.29 % → 96.35 %** (EvolutionRuntime 96.8 %).
- **Governance:** [`JAVA_SESSION_12_GOVERNANCE_AUDIT.md`](JAVA_SESSION_12_GOVERNANCE_AUDIT.md) — validator PASS 56/128.
- **Blocker:** [`JAVA_SESSION_12_BLOCKER_AUDIT.md`](JAVA_SESSION_12_BLOCKER_AUDIT.md) — no evolution blocker.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 50 | **56** |
| Remaining (of 128) | 78 | **72** |
| Total tests | 553 | **602** |
| Instruction coverage | 96.29 % | **96.35 %** |
| `PROVEN_FLOOR` | 50 | **56** |

`mvn clean verify` BUILD SUCCESS (602/0/0). Manifest unchanged. All tests parity-backed.

## Next

[`JAVA_SESSION_13_PLAN.md`](JAVA_SESSION_13_PLAN.md): `core.causality` (5 APIs, zero substrate).
Mission active — 56/128.
