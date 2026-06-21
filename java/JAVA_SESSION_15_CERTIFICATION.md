# JAVA_SESSION_15_CERTIFICATION

**`recover_modal_runtime` — byte-exact.** Branch `java`. Canon `origin/python` @ `9625f4a`
(2.1.0). Phase 0 verified `HEAD == origin/java` (`a619ddc`); matrix/validator/ranking rebuilt live.

## Scope decision

The reconstruction priority cluster has **3 unproven clean APIs**: `recover_modal_runtime`
(standalone, `core.adaptive`, 1 module) and `run_reconstruction_runtime` /
`run_reconstruction_for_extraction` (one shared orchestrator, **24 modules / 1407 lines / ~18
engines**). To keep every commit a *complete* unit (no partial ports), this session certifies the
standalone `recover_modal_runtime`; the large reconstruction orchestrator is scheduled as its own
slice ([`JAVA_SESSION_16_PLAN.md`](JAVA_SESSION_16_PLAN.md)).

## API

| API | Java | Python canon | dependency |
| --- | --- | --- | --- |
| `recover_modal_runtime` | `io.webweavex.adaptive.ModalRecovery#recoverModalRuntime` | `core.adaptive.modal_recovery_engine` | 1 module, **0 forbidden** |

`recover_modal_runtime(page=None, html)` is a pure function of `html` (the live-`page` click +
`_test_modals` reset are test-hook side effects affecting no return value). Faithful port incl.
Python `str.strip("#.[]")` semantics in `_selector_in_html`. **Zero new substrate. No stubs.**

## Proofs (machine-derived)

| Gate | Result |
| --- | --- |
| Dependency | 1 module / 0 forbidden — CLEAN |
| Parity | `CrossLanguageParityS15Test` **9/9** byte-exact (`stable_serialize` + `compute_kaalka_hash`); empty/each-selector/first-wins/no-match/case-insensitive/unicode |
| Coverage | **96.40 % → 96.405 %** (increased) |
| Governance | validator **PASS 67/128**; matrix 67; MAPPING +1; `PROVEN_FLOOR` 66→67; manifest unchanged |
| Full suite | `mvn clean verify` **689/0/0** BUILD SUCCESS |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 66 | **67** |
| Remaining (of 128) | 62 | **61** |
| Total tests | 680 | **689** |
| Instruction coverage | 96.40 % | **96.405 %** |
| `PROVEN_FLOOR` | 66 | **67** |

Mission active — 67/128.
