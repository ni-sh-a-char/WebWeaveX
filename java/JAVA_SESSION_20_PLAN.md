# JAVA_SESSION_20_PLAN

**Phase A final slice. Mission active: 90 / 128.**

## Target: `core.memory` orchestrator (2 APIs) — last clean surface

`run_runtime_memory`, `run_memory_for_extraction`
(`core.memory.runtime_memory_orchestrator`).

### Profile (measured S19)

- **37 modules / 1634 lines / 0 forbidden**, import OK, output **SERIALIZABLE** (verified — not
  self-referential) → direct byte-exact parity.
- Largest orchestrator yet; fans out to the memory sub-engines (history/index/lineage/merge/
  convergence/diff/federation/replication/snapshot/policy/graph-memory + semantic memory engines).
- Dedicated full session (read all engines → one `io.webweavex.memory.RuntimeMemoryRuntime` class →
  vectors with engine-level sections → byte-exact test). Reuse existing memory classes where the
  engine is already ported.

### Expected gain

- **90 → 92** — completes Phase A. Clean surface then **exhausted**.

### After S20 — Phase B preparation only

Per `JAVA_BLOCKER_HIERARCHY_V2.md`, the next campaign is the **bs4-decouple** (Tier 2, ~9 APIs +
Tier-5 fallout) via an upstream lazy-import of BeautifulSoup in `core.semantic`/`core.evidence`
`__init__`. Author `JAVA_BS4_DECOUPLE_PLAN.md` before any implementation. Then Phase C (lxml Soup
engine, Tier 3).

**Mission not complete — 90 / 128. Continue.**
