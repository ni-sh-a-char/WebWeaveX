# JAVA_PARITY_SURFACE_MAP

**Phase 1 — remaining parity surface grouped into families** (machine-derived from
`tools/rank_remaining_apis.result.json`). Each clean family shares a closure; the table drives
target selection by **parity-surface reduction ÷ new substrate**.

## Clean families (portable, 0 forbidden)

| Family (package) | APIs left | closure | reusable infra (already built) | new substrate | unlock value |
| --- | ---: | --- | --- | --- | ---: |
| `core.synchronization` | 6 | 25 m | StableSerialize, PyJsonParse, RuntimeGraph | none | high |
| `core.workflows` | 7 | 23 m | + json.loads | none | high |
| `core.evolution_runtime` | 6 | 25 m | + json.loads | none | high |
| `core.causality` | 5 | 25 m | + json.loads | none | high |
| `core.streaming` | 4 | 18 m | StableSerialize, Kaalka | none | medium |
| `core.reconstruction` | 4 | 24 m | RuntimeGraph, IR | none | medium |
| `core.memory` | 4 | 37 m | + json.loads | none | medium |
| `core.identity` | 3 | 28 m | + json.loads | none | medium |
| `core.interaction` | 2 | 19 m | InteractionGraph, Pagination | none | low |
| `core.connectors` (live_runtime) | 3 | 26 m | Connectors helpers | none | low |
| `core.auth` | 1 | 7 m | crypto/session | none | low |
| `core.repository` | 1 | 12 m | — | path-canon harness | low |

**Observation:** after the S8 `json.loads` and S9 execution slices, **every** remaining clean
family reuses already-built substrate (`StableSerialize` + `Kaalka` + `PyJson`/`PyJsonParse` +
`RuntimeGraph` + connector/IR helpers). **No clean family requires new substrate** except
`core.repository` (a path-canonicalization test harness). The remaining clean surface (~46 APIs)
is now a substrate-free mechanical sweep.

## Blocker families (forbidden — see `JAVA_BLOCKER_HIERARCHY.md`)

| Family | APIs | root blocker |
| --- | ---: | --- |
| semantic / evidence / memory(bs4) / modal / application / native-snapshot | ~26 | bs4 import barrier (eager `core.semantic`/`core.evidence` `__init__`) |
| HTML/web extraction | ~10 | lxml/bs4 parse + network + LLM + browser |
| OCR / multimodal | 2 | Tesseract |

## Highest parity-surface reduction

The **`core.synchronization`** / **`core.workflows`** families (6–7 APIs, 0 substrate) give the
largest immediate reduction. The single highest-leverage *blocker* removal remains the upstream
bs4-decouple (~26 APIs) — tracked in the blocker hierarchy, requires a Python-canon change.
