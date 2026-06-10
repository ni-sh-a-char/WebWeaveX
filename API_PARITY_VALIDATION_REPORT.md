# API_PARITY_VALIDATION_REPORT.md

> Regenerated from source on 2026-06-10. Three-way comparison measured directly from the
> real branch sources via `git show`, not from any prior report.
> Tools: `tools/dart_parity_audit.py` (Python↔Dart classification) and
> `tools/three_way_parity.py` (Python↔JavaScript↔Dart name-level presence).

## Sources compared (all measured live)

| Language | Source of truth | Public surface |
|----------|-----------------|----------------|
| Python | `origin/python:webweavex/__init__.py` `__all__` | **128** names (126 APIs + `version`, `__version__`) |
| JavaScript | `origin/javascript:src/index.ts` + `publicApi.ts` + `connectors/index.ts` | **126/126** canonical APIs present (229 total exports incl. helpers) |
| Dart | `lib/webweavex.dart` barrel + all `lib/**/*.dart` public symbols | classified below |

Version alignment: Python **2.0.1** · JavaScript **2.0.1** · Dart **2.0.1**.

## Three-way name-level presence (excluding `version`/`__version__`)

| Implementation | Canonical APIs present by name | Coverage |
|----------------|-------------------------------:|---------:|
| Python (definition) | 126 / 126 | 100% |
| **JavaScript** | **126 / 126** | **100%** (full reference) |
| **Dart (native symbol)** | **96 / 126** | **76.2%** (after `heal_selector` + `replay_interactions` ports) |

JavaScript is the proof-of-feasibility reference: it reaches 126/126 because Node.js can drive
real browsers (Playwright/Puppeteer), native OS/Electron/DevTools surfaces, and NLP/AST tooling
in-process. Dart cannot do these in-process — that gap is the source of every non-Complete row.

## Dart classification (`tools/dart_parity_audit.py`, regenerated this session)

```
Python total: 128   Counts: {Complete: 77, Partial: 36, Missing: 0, Deferred: 15}
```

| Status | Count | Meaning | Proof standard |
|--------|------:|---------|----------------|
| ✅ Complete | **77** | Native Dart impl, name-mapped, **cross-language proof-verified** | `computeDeterministicHash(dartOut) == Python compute_deterministic_hash(pyOut)` or save/load roundtrip |
| 🟡 Partial | **36** | Bounded Dart impl or proven core path only | primary/deterministic path proven; a sub-path (network/NLP/AST) not portable |
| ⚪ Deferred | **15** | Needs OS/desktop/Electron/DevTools/Playwright in-process | not feasible in Dart VM |
| ❌ Missing | **0** | Not implemented at all | — |

**Wave 3–4 changes (2026-06-10):** two APIs ported Deferred → Partial as native Dart, each proven
by deep-equality vectors against Python **2.0.1** (materialized from `origin/python`; the installed
Python is a broken 2.0.0):
- `heal_selector` — DOM-node strategies (`text_anchor`/`attribute_anchor`/`structural_fallback`) are
  full-fidelity (11 vectors, `selector_healing_api_vectors.json`); `semantic_anchor` HTML path bounds
  deeply nested inline markup.
- `replay_interactions` — the returned structure is a full-fidelity pure function of the interaction
  log (6 vectors, `interaction_replay_api_vectors.json`); the live-page action dispatch is the bounded edge.

`77 + 36 + 15 = 128` (with the `version`/`__version__` constants folded into Complete).
**Proof Coverage Audit (`COMPLETE_API_PROOF_MATRIX.md`):** all 75 functional Complete APIs are
cross-language proof-verified (49 VECTOR, 22 ROUNDTRIP, 4 CORE_VECTOR). **11 APIs were downgraded
Complete → Partial** in this audit because they had only a determinism/structural test and the
Dart contract/output diverges from Python (see `PARTIAL_API_AUDIT.md` Group 1). 96 APIs have a
Dart symbol; the gap to 77 Complete is the 11 downgrades + the 8 `FORCE_PARTIAL` semantic/query
sub-paths. The 30 APIs with no Dart symbol are the network-bounded Partials and the 15 Deferred.

## The 30 Python APIs with no native Dart symbol (all present in JS)

**Browser / network extraction (bounded-Partial candidates):**
`extract`, `extract_async`, `extract_repo`, `extract_docs`, `extract_recursive`,
`crawl`, `crawl_async`, `stream_extract`, `ingest_input`, `universal_extract`,
`extract_web`, `extract_repository`, `extract_multimodal`, `extract_document_runtime`,
`run_autonomous_extraction`.

**Live-browser DOM/runtime capture (Deferred — needs Playwright/DevTools):**
`extract_infinite_scroll`, `extract_paginated_content`,
`capture_websocket_frames`, `capture_dom_mutations`, `recover_modal_runtime`.
(`heal_selector` and `replay_interactions` were here; both are now native Dart Partials — see above.)

**Native OS / Electron / container / IDE (Deferred — no in-process Dart surface):**
`run_application_cognition`, `execute_runtime_objective`, `save_application_memory`,
`load_application_memory`, `extract_native`, `run_native_cognition`, `save_native_runtime`,
`load_native_runtime`, `extract_container_runtime`, `extract_ide_runtime`.

## Cross-language deterministic parity (executed)

`dart run validation/validate_parity.dart` → `crossLangMatch: true`, all 11 core vectors
hash-match the JavaScript reference (`hash_match`, `encrypt_match`, `decrypt_ok`,
`deterministic` all true). Runtime-family parity proven by ~145 hash vectors in
`validation/parity/*_api_vectors.json` asserted in `test/parity/`.

## Verdict

- **0 Missing** — every canonical API is either implemented (Complete), bounded with a proven
  core (Partial), or honestly Deferred for a documented platform reason.
- Dart trails JavaScript on the **30 browser/native/infra APIs** that require in-process
  capabilities the Dart VM does not have, plus the **11 audit-downgraded** contract-divergent APIs.
- Highest achievable next gains are the **11 downgraded APIs** (Group 1 of `PARTIAL_API_AUDIT.md` —
  several are portability **A**: port Python's exact field set/formula + add vectors) and the
  network-extraction surface. The native-OS/Electron/DevTools families remain genuinely Deferred.
