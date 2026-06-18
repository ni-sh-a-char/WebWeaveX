# JAVA_PARITY_RISK_REGISTER

**Phase 8 — risk-ranked register of every remaining subsystem.** Derived from
`tools/rank_remaining_apis.result.json` (machine-derived forbidden-dependency classification)
+ the Session-6 runtime blocker audit. Risk = likelihood the subsystem cannot reach byte-exact
Java parity without an upstream change.

| Subsystem | Remaining APIs | Risk | Blocker | Dependency | Mitigation | Unlock impact |
| --- | ---: | --- | --- | --- | --- | ---: |
| **semantic / evidence** | ~12 (query_semantics, reason_semantically, run/replay_semantic_runtime, save/load_semantic_memory, query_documents, …) | **Critical** | transitive BeautifulSoup via eager `core.semantic`/`core.evidence` `__init__` | bs4 (import-time, **not executed** — proven S6) | Python-canon refactor: lazy-import bs4 in `core.semantic/__init__`, OR adopt a behavioral gate | **~26 APIs** flip forbidden→clean |
| **extraction (HTML/web)** | ~10 (extract, extract_async, extract_docs/repo, stream_extract, extract_web, crawl*, extract_recursive, analyze) | **Critical** | real BeautifulSoup/lxml parse + network + LLM | bs4+lxml (executed), requests/httpx, groq | Build an lxml+html.parser Soup engine (multi-session) + inject fetch/LLM at boundary | ~10 APIs (the core extraction surface) |
| **document/repository IR** | 3 (compile_document, compile_repository, query_repo) | **High** | same bs4 bridge as semantic | bs4 (import-time, not executed) | rides on the semantic refactor | 3 APIs |
| **native** | 2 (extract_native, run_native_cognition) | **High** | `sys.platform` host branch (+ bs4 import) | OS-coupled | permanent-deferred (host-dependent output) | 0 (irreducible) |
| **multimodal / OCR** | 2 (extract_multimodal, ingest_input) | **High** | Tesseract OCR + PIL | binary, non-deterministic | port deterministic graceful-degrade path only | 2 (partial) |
| **workflows** | 7 | **Low** | none (clean) | json.loads for `load_workflow_memory` (now built) | implement (next slice) | 7 |
| **execution** | 6 | **Low** | none | none | implement | 6 |
| **synchronization** | 6 | **Low** | none | json.loads (built) | implement | 6 |
| **evolution_runtime** | 6 | **Low** | none | json.loads (built) | implement | 6 |
| **causality** | 5 | **Low** | none | json.loads (built) | implement | 5 |
| **streaming** | 4 | **Low** | none | none | implement (capture_* fixture-driven) | 4 |
| **reconstruction** | 4 | **Low** | none | none | implement | 4 |
| **memory** | 4 | **Low** | none | json.loads (built) | implement | 4 |
| **identity** | 3 | **Low** | none | json.loads (built) | implement | 3 |
| **interaction** | 2 | **Low** | none | none | implement | 2 |
| **auth** | 1 | **Low** | none | none | implement | 1 |
| **repository (FS walk)** | 1 (extract_repository) | **Medium** | path-string/OS-separator | filesystem | path-canonicalization harness (R-2) | 1 |

## Headline risks

- **Critical #1 (highest unlock):** the eager-`bs4` import in `core.semantic`/`core.evidence`
  blocks **~26 behaviorally-clean APIs**. A one-line-per-module lazy-import refactor in the
  Python canon converts them all to clean. This is the single highest-leverage risk-reduction
  action in the whole mission. (Java-side cannot fix it — it is an upstream import structure.)
- **Critical #2:** the HTML extraction surface (~10 APIs) needs a genuine lxml+html.parser Soup
  engine — a real multi-session substrate build, plus boundary injection for network/LLM.
- **Everything else is Low risk** (clean, deterministic) — ~48 APIs are mechanically portable
  now, the `json.loads` substrate built this slice having removed the last shared blocker for
  the `load_*`/`decrypt_*` members.

## Recommended sequence (risk-weighted)

1. Sweep the **Low-risk clean clusters** (workflows → execution → sync → evolution → causality →
   streaming → reconstruction → memory → identity → interaction → auth) — ~48 APIs, no upstream
   change, substrate already in place. This is the bulk of the remaining mission.
2. **repository** with the path harness (1 API, Medium).
3. Escalate the **Critical #1** bs4-decoupling as an upstream canon change request (~26 APIs).
4. **Critical #2** Soup engine as a dedicated multi-session substrate build (~10 APIs).
5. Accept **native** (2) as permanent-deferred; **multimodal** (2) as graceful-degrade-only.
