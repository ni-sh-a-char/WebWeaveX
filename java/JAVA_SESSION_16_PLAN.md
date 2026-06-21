# JAVA_SESSION_16_PLAN

**Phase 11 — next slice. Mission active: 67 / 128.**

## Selected target: `core.reconstruction` orchestrator (2 APIs)

`run_reconstruction_runtime`, `run_reconstruction_for_extraction`
(`core.reconstruction.runtime_reconstruction_orchestrator`).

### Profile (measured this session)

- **24 modules / 1407 lines / 0 forbidden** — CLEAN.
- Output is **serializable** (NOT self-referential, unlike `run_live_runtime`) — direct byte-exact
  parity, no projection needed.
- Fans out to ~18 reconstruction sub-engines: `reconstruct_runtime` (already proven),
  `reconstruct_browser_runtime`, `reconstruct_application_runtime`, `reconstruct_runtime_session`,
  `build_runtime_environment`, `reconstruct_runtime_memory`, `rebuild_runtime_state`,
  `reconstruct_runtime_topology`, `reconstruct_runtime_identity`, `reconstruct_connector_runtime`,
  `build_runtime_timeline`, `build_runtime_replay`, `clone_runtime_environment`,
  `fabricate_runtime_reality`, `validate_reconstructed_runtime` (already proven),
  `recover_reconstructed_runtime`, `capture_reconstruction_snapshot`,
  `compile_reconstruction_runtime_ir` + `reconstruction_runtime_ir_to_graph`.
- `run_reconstruction_for_extraction` adds snapshot save/load + `build_runtime_graph` merge
  (reuse `ExecutionRuntime.buildUnifiedRuntimeGraph`).

### Plan

Dedicated full session (this is a large fan-out, comparable to causality/live). Read all ~18
engines → one `io.webweavex.reconstruction.ReconstructionRuntime` class → vectors with engine-level
sections → byte-exact test. Reuse existing `RuntimeReconstruction`/`RuntimeValidation` where the
engine is already ported.

### Expected gain

- **67 → 69** (+2).

### Queue after reconstruction

memory (4) → identity (3) → connectors-other (3) → interaction (2) → auth (1) →
repository (1). ≈ 14 more clean APIs → ~83/128 with no upstream change. Then Tier 2 (bs4-decouple
~26) + Tier 3 (lxml extraction ~10) need upstream-canon changes.

**Mission not complete — 67 / 128. Continue.**
