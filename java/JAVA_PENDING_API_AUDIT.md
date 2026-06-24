# JAVA_PENDING_API_AUDIT

**Final convergence audit (Session 29) of the 4 previously "portable-pending" APIs. Each is resolved
to a hard disposition — PORT or BLOCK — with runtime frontier, observable output, dependencies,
blocker analysis, and implementation estimate. No API remains in an undecided/unknown state.**
Python canon `9625f4a`; method = runtime call graph + empirical execution (not import closure).

Outcome: **1 BLOCKED** (`run_canonical_pipeline`), **3 PORT-APPROVED** (`RuntimeKernel`,
`get_runtime_kernel`, `run_autonomous_extraction`).

---

## 1. `run_canonical_pipeline` — DECISION: **BLOCKED** (inherits extraction blocker)

**Runtime frontier.** `run_canonical_pipeline(UniversalInput) → _detect_kind(inp)` then dispatch:
```
kind == "web"        → extract_web(target, …)                      [Playwright — blocked]
kind == "repository" → extract_repository(target)                  [filesystem os.walk — blocked]
kind == "document"   → Path(target).read_text(); extract_document_runtime(text)   [filesystem read]
kind == "multimodal" → extract_multimodal(target)                  [OCR — blocked]
else (default/text)  → extract({"source": target})                 [lxml — CASE B blocked]
→ RuntimeKernel(runtime_type).run_pipeline(sources={"extraction": extraction_payload, …})
→ ExtractionResult(kind, …, graph, fingerprint)
```
**Observable output.** Empirically, `run_canonical_pipeline(UniversalInput(source="hello world some
text"))` (the default/text kind) produces a 1.40 MB serialized result that **contains `raw_text` and
`fingerprint`** — i.e. the lxml-derived fields of `extract()` (`content.text`/`links`/`raw_text` and
the global fingerprint computed over them) flow straight into the pipeline result.
**Dependencies.** Every dispatch branch terminates in a formally-blocked engine: lxml (`extract`),
Playwright (`extract_web`), filesystem (`extract_repository`, `read_text`), OCR (`extract_multimodal`).
There is **no input kind** for which the observable output avoids a blocked engine.
**Blocker analysis (4-part).** (A) concrete: `source="hello world"` → `extract()` → output embeds
`raw_text`/`fingerprint`. (B) observable: those fields are top-level in `ExtractionResult` and feed its
fingerprint. (C) why Java can't: byte-exact requires reproducing libxml2 (see
JAVA_EXTRACTION_FINAL_VERDICT) — non-portable. (D) frontier reduction fails: the pipeline's purpose is
to *run* an extractor; no observable surface excludes the extractor output. Per the directive's
aggregator rule ("if a child is blocked, inherit the blocker"), the lxml/Playwright/OCR/fs children
block the aggregator.
**Implementation estimate.** N/A — blocked. Unblocks only when its children unblock (upstream canon:
portable parser + fetch/OCR/snapshot injection contracts).

---

## 2. `RuntimeKernel` — DECISION: **PORT-APPROVED** (portable; no blocker)

**Runtime frontier.** `RuntimeKernel(runtime_type)` → `initialize_runtime`; `run_pipeline(sources,
tick, phases, options)` schedules the canonical phases `[semantic, synchronization, memory, execution,
reconstruction]` via `schedule_kernel_phases` → `dispatch_runtime_phase` → the phase bridges
`run_semantic_phase`/`run_sync_phase`/`run_memory_phase`/`run_execution_phase`/
`run_reconstruction_for_extraction`, then `build_kernel_state`/`merge_kernel_state`,
`build_kernel_topology`, `coordinate_kernel_phases`, `enforce_kernel_policy`,
`enforce_runtime_boundary`, `replay_kernel_state`, `merge_runtime_graph`.
**Observable output.** Empirically, `RuntimeKernel("browser").run_pipeline(sources={}, tick=0)` returns
a **deterministic, fully JSON-serializable** dict with keys `{boundary, bounded, coordination, graph,
phases, policy_enforcement, registry, replay, runtime_type, schedule, state, topology}`.
**Dependencies.** Forbidden-dependency scan of `core/kernel/*` = **clean** (no bs4/lxml/`ast`/
Playwright/OCR/`sys.platform`/network). The five phase bridges wrap the `*_for_extraction`
orchestrators that are **already certified in Java** (semantic S25, sync S10, memory S20, execution S9,
reconstruction S16). With `sources={}` (or any caller-controlled sources) no extractor is invoked —
unlike `run_canonical_pipeline`, the kernel does **not** call `extract()`; the extraction payload is an
*input* the caller supplies.
**Blocker analysis.** No blocker. The output is deterministic and serializable; the only dependencies
are pure kernel-bridge logic plus already-ported orchestrators.
**Implementation estimate.** ~15–18 kernel bridge modules (scheduler, policy, topology, coordination,
boundary, registry, replay, state, dispatcher, lifecycle, bus, context + 5 phase bridges) → reuses 5
certified runtime families + `UnifiedRuntimeIr`/`RuntimeGraph`. **1–2 sessions.** Parity surface =
`run_pipeline(...)` output (the class itself is not serializable; certify via its produced dict, as
`UniversalInput` was certified via its value).

---

## 3. `get_runtime_kernel` — DECISION: **PORT-APPROVED** (co-ported with `RuntimeKernel`)

**Runtime frontier.** `get_runtime_kernel(runtime_type="browser")` → module-level singleton: returns the
cached `RuntimeKernel` (recreated when `runtime_type` changes).
**Observable output.** Returns a `RuntimeKernel` object — **not directly serializable** (empirically
`json.dumps(kernel)` → `TypeError`). Certified, like the class, via the projection
`get_runtime_kernel(t).run_pipeline(...)`.
**Dependencies.** Identical to `RuntimeKernel` (it constructs one). No blocker.
**Blocker analysis.** None — pure singleton accessor.
**Implementation estimate.** Trivial **once `RuntimeKernel` is ported** (same session): a static
accessor returning a memoized `RuntimeKernel`.

---

## 4. `run_autonomous_extraction` — DECISION: **PORT-APPROVED** (portable contract; native flag excluded)

**Runtime frontier.** `run_autonomous_extraction(tasks, …) → run_distributed_extraction(tasks, workers,
checkpoint, tick)` (optionally load/save `DistributedCheckpoint`, both already ported). Optional flags
add: `objective_execution`→`build_runtime_goal` (pure); `causal/semantic/workflow/sync/evolution/live/
federated/execution/reconstruction`→ the certified `*_for_extraction` orchestrators;
`native_extraction=True`→`extract_native` (**platform — blocked**).
**Observable output.** Empirically, `run_autonomous_extraction(tasks=[{task_id,url,priority,objective},
…])` (default flags) returns a **2.9 KB deterministic serializable** dict with keys `{adaptive_sync,
assignments, autonomous, bounded, checkpoint, cluster, distributed_graph, identity_routes, monitoring,
queue, schedule, session_routes, stream_federation, topology, workers}` — **no `raw_text`** (no
extractor runs); the `fingerprint`-style hashes are deterministic Kaalka hashes of the scheduler output.
**Dependencies.** `run_distributed_extraction` orchestrator forbidden-dep scan = clean (operates on task
*dicts* — URL strings, priorities — never fetches or parses page content). Reuses ported
`DistributedCheckpoint`. The only blocked sub-path is the optional `native_extraction=True` branch
(`extract_native` → `sys.platform`).
**Blocker analysis.** Not blocked on its portable contract (`native_extraction=False`, the default).
The native branch is excluded from the certified contract — the same precedent as `run_application_
cognition` (S26, certified for the `html=""` contract) and `run_semantic_for_extraction` (S25).
**Implementation estimate.** Port `run_distributed_extraction` + distributed engines (worker assignment,
deterministic queue, cluster/topology, identity/session routing, stream federation, adaptive sync,
monitoring); reuse `DistributedCheckpoint`. **~1 session.** Parity surface = the scheduler payload for
the portable flag contract.

---

## Disposition summary

| API | Decision | Reason | Estimate |
|-----|----------|--------|----------|
| `run_canonical_pipeline` | **BLOCKED** | inherits lxml/Playwright/OCR/fs child blocker on every kind (empirically embeds `extract()` `raw_text`+`fingerprint`) | — |
| `RuntimeKernel` | **PORT-APPROVED** | `run_pipeline` deterministic+serializable; phases route to 5 certified runtimes; kernel clean | 1–2 sessions |
| `get_runtime_kernel` | **PORT-APPROVED** | singleton accessor over `RuntimeKernel` | with #2 |
| `run_autonomous_extraction` | **PORT-APPROVED** | pure distributed scheduler (default/portable flags); native branch excluded | ~1 session |

**Result: the "portable-pending" category is eliminated.** One API moves to FORMALLY BLOCKED; three
move to PORT-APPROVED (definitive, evidence-backed, planned — not unknown/maybe/suspected). Honoring
the directive's "do not implement new APIs yet," the three PORT-APPROVED ports are scheduled, not
executed this turn; fabricating blockers for provably-portable APIs is disallowed by the evidence
rules (a PORT-APPROVED API has *disproven* the existence of a blocker).
