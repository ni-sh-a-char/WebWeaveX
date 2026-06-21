# JAVA_SESSION_14_CERTIFICATION

**`core.streaming` + `core.connectors.live_runtime` clean subset — 5 APIs, byte-exact.**
Branch `java`. Python canon `origin/python` @ `9625f4a` (2.1.0).

## Implemented APIs (5)

| API | Java | certification |
| --- | --- | --- |
| `build_stream_timeline` | `io.webweavex.streaming.StreamingRuntime#buildStreamTimeline` | direct byte-exact |
| `replay_stream_events` | `…#replayStreamEvents` | direct byte-exact |
| `run_live_runtime` | `…#runLiveRuntime` | projection parity (self-referential output) |
| `save_live_runtime` | `…#saveLiveRuntime` | file-content byte-exact |
| `load_live_runtime` | `…#loadLiveRuntime` | roundtrip + missing byte-exact |

Reuses the 7 certified connector engines + live IR + 2 new internal sub-engines
(`extract_filesystem_runtime`, `extract_cicd_runtime`). **Zero new substrate.** No stubs.

Blocked/deferred (documented, not implemented): `stream_extract` (bs4), `capture_websocket_frames`
(Playwright page). `extract_runtime_streams` was already proven (S7).

## Proofs

- [`JAVA_SESSION_14_DEPENDENCY_PROOF.md`](JAVA_SESSION_14_DEPENDENCY_PROOF.md) — 0 forbidden on the 5 clean APIs.
- [`JAVA_SESSION_14_TRACEABILITY.md`](JAVA_SESSION_14_TRACEABILITY.md) — no orphan.
- [`JAVA_SESSION_14_PARITY_PROOF.md`](JAVA_SESSION_14_PARITY_PROOF.md) — **34/34** byte-exact (incl. projection + FS-walk).
- [`JAVA_SESSION_14_COVERAGE_PROOF.md`](JAVA_SESSION_14_COVERAGE_PROOF.md) — **96.38 % → 96.40 %**.
- [`JAVA_SESSION_14_GOVERNANCE_AUDIT.md`](JAVA_SESSION_14_GOVERNANCE_AUDIT.md) — validator PASS 66/128.
- [`JAVA_SESSION_14_BLOCKER_AUDIT.md`](JAVA_SESSION_14_BLOCKER_AUDIT.md) — 2 new documented blockers.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 61 | **66** |
| Remaining (of 128) | 67 | **62** |
| Total tests | 646 | **680** |
| Instruction coverage | 96.38 % | **96.40 %** |
| `PROVEN_FLOOR` | 61 | **66** |

`mvn clean verify` BUILD SUCCESS (680/0/0). Manifest unchanged.

## Next

[`JAVA_SESSION_15_PLAN.md`](JAVA_SESSION_15_PLAN.md): `core.reconstruction` (4 APIs). Mission active — 66/128.
