# JAVA_SUBSTRATE_LEVERAGE

**Phase 4 — ROI of every foundation substrate already built.** Which remaining APIs each one
unlocks. Machine-informed by the dependency closures.

| Substrate (Java) | What it provides | APIs it unlocks (remaining) | residual blockers on those |
| --- | --- | ---: | --- |
| `StableSerialize` + `Kaalka.computeKaalkaHash` | canonical hash/serialize — the comparison basis for **every** parity proof | all 91 | n/a (universal) |
| `PyJson` (`json.dumps`) | canonical dumps (compact/default, ascii/unicode) | execution (done), sessions (done), workflows, sync, identity, … | none |
| **`PyJsonParse`** (`json.loads`, S8) | round-trip decode for **every** `decrypt_*`/`load_*` | `load_sync_memory`, `load_workflow_memory`, `load_causal_memory`, `load_evolution_runtime`, `load_runtime_memory`, `load_browser_identity`, `load_live_runtime`, … (~12 `load_*`) | none — the families are otherwise clean |
| `RuntimeGraph` + `ExecutionRuntime.buildUnifiedRuntimeGraph` (IR merge) | graph build + heterogeneous IR merge | every `*_for_extraction` / `run_*` that merges a unified graph (workflows, sync, causality, evolution, reconstruction) | none |
| `Kaalka` action-ID path (`sha256(json.dumps)`) | deterministic IDs | execution (done); any engine using content-hash IDs | none |
| `connectors.Connectors` helpers | snapshot→envelope (`getList`/`getMap`/`sortedByStr`/`pyInt`) | `run_live_runtime`, `load/save_live_runtime`, streaming snapshot transforms | none |
| `PyRepr.str` (str(dict)) | Python `str()` for sort keys | any engine sorting by `str(item)` (kubernetes, scheduler, replay) | none |
| `PyText` (splitlines/strip) | CPython text ops | document/repository engines | repository: path harness |

## ROI summary

- **`PyJsonParse` (S8) was the highest-ROI build:** it was the *last shared blocker* for the
  `load_*`/`decrypt_*` members spread across ~6 clean families. With it in place, those families
  no longer need any new substrate.
- **Net effect:** the entire remaining **clean** surface (~46 APIs) is now buildable with **zero
  new substrate** (sole exception: `core.repository`'s path-canonicalization harness). Future
  slices are pure mechanical ports + parity vectors.
- The **only** remaining substrate of real size in the whole mission is the **lxml/html.parser
  Soup engine** required by the ~10 HTML-extraction APIs (a multi-session build) — and that is
  gated behind the bs4 *import* barrier for the ~26 semantic APIs, which is an upstream Python
  change, not a Java substrate.
