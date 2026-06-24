# JAVA_FINAL_PARITY_LEDGER

**Complete classification of all 128 tracked public APIs for the Java port.** Python canon `9625f4a`;
Java HEAD verified == origin/java. Every API is in exactly one of three definite states:
**CERTIFIED** (byte-exact parity-proven), **BLOCKED** (formal proof, four-part evidence), or
**PORTABLE-PENDING** (proven dependency-clean — no blocker — implementation deferred by Rule 2).
There are **zero** APIs classified unknown / maybe / likely / suspected.

## Metrics

| State | Count |
|-------|------:|
| **CERTIFIED** (byte-exact) | **105** |
| **BLOCKED** (formal proof) | **19** |
| **PORTABLE-PENDING** (no blocker; multi-session port) | **4** |
| **Total** | **128** |
| Unknown / maybe / suspected | **0** |

Reality at publication: validator PASS (105/128), `mvn verify` BUILD SUCCESS, **1124 tests** green,
instruction coverage **96.513 %** (floor 94 %).

---

## CERTIFIED — 105 APIs (byte-exact, parity tests under `CrossLanguageParity*Test`)

Proven across Sessions 1–28. Mapping of api → Java symbol is the single source of truth in
`tools/gen_java_parity_matrix.py` (`JAVA_PROVEN`) and re-checked by `tools/validate_java_manifest.py`
(`MAPPING`); both are size-consistent with the matrix (checks 5 & 10). Families:

- **Foundation** (S1–3): crypto (`compute_kaalka_hash`, `encrypt_value`, `decrypt_value`),
  determinism/fingerprint/replay, graph/IR, query, memory, reconstruction primitives.
- **Connector extraction** (S4/7): database/api/streams/telemetry/container/ide/kubernetes runtimes.
- **Pure document + pagination** (S4B): `extract_document_runtime`, `extract_paginated_content`.
- **Runtime families** (S9–13): execution, synchronization, workflows, evolution, causality.
- **Streaming + live** (S14) and **adaptive modal** (S15).
- **Reconstruction orchestrator** (S16), **memory persistence ×8** (S17), **browser identity** (S18).
- **Clean remainder** (S19): distributed/native persistence, semantic replay, objective execution,
  `query_repository`, authenticate, clone/fabricate.
- **Memory orchestrator** (S20), **heal_selector** (S21), **query_documents** (S22),
  **semantic runtime** (S25), **application cognition** (S26).
- **Session 28 frontier-reduced** (this session, +8): `version`, `__version__`, `query_repo`,
  `compile_document`, `capture_websocket_frames`, `capture_dom_mutations`, `extract_infinite_scroll`,
  `replay_interactions`. Evidence: `golden_vectors_s28.json`, `CrossLanguageParityS28Test` (24 vectors).

---

## BLOCKED — 19 APIs (formal proof; see linked verdicts)

### lxml HTML parser — CASE B (7) → `JAVA_EXTRACTION_BLOCKER_PROOF.md`, `JAVA_EXTRACTION_FINAL_VERDICT.md`
`extract`, `extract_async`, `extract_docs`, `extract_repo`, `stream_extract`, `analyze` (default
branch), `extract_recursive`. Observable `content.text`/`content.links`/`raw_text`/`fingerprint`
depend on libxml2 recovery tree-building (CDATA drop, first-wins duplicate attributes); html.parser
and jsoup(HTML5) both diverge; JNI to libxml2 is non-portable. Frontier reduction fails (parser output
**is** the observable output).

### CPython `ast` — CONDITION B (3) → `JAVA_AST_FINAL_VERDICT.md`
`query_semantics`, `reason_semantically`, `compile_repository`. Output embeds CPython AST fields
(`node.type`/`lineno`/`end_lineno`/`args`/`bases`). tree-sitter/JavaParser/hand-parser produce a
different taxonomy; byte-exact = embedding CPython `ast`. Frontier reduction fails.

### Network (2) → `JAVA_EXTRACTION_FINAL_VERDICT.md`
`crawl`, `crawl_async`. bs4/lxml-free (regex link discovery is portable); blocked solely by live
`requests.get`/`httpx` — not certifiable offline without a fetch-fixture contract.

### Playwright live render (1) → `JAVA_PLAYWRIGHT_VERDICT.md`
`extract_web`. Output derives from live `page.content()` (headless Chromium after network-idle); no
pure-Java equivalent; offline bail-out is not the API's behavior.

### OCR runtime (3) → `JAVA_OCR_VERDICT.md`
`extract_multimodal`, `ingest_input` (image branch), `universal_extract` (image/file branch). Output
roots in native `pytesseract.image_to_data`; environment-dependent; no byte-exact pure-Java Tesseract.

### OS / platform (3) → `JAVA_PLATFORM_VERDICT.md`
`extract_native`, `run_native_cognition` (`sys.platform` leaks into observable `platform`; live
UIAutomation/Quartz/X11 enumeration). `extract_repository` (reads on-disk repo; OS-ordered `os.walk`).

---

## PORTABLE-PENDING — 4 APIs (NO blocker; proven dependency-clean; deferred by Rule 2)

These are **not** blocked and **not** unknown: a runtime + forbidden-dependency scan proves they are
free of bs4/lxml/`ast`/Playwright/OCR/`sys.platform`/network on their observable path. They route
entirely through already-certified portable runtimes. They are unported only because each is a large
multi-module aggregator that cannot be completed+certified+tested within a single session (Rule 2 —
no partial ports).

| API | Substrate | Evidence it is portable |
|-----|-----------|-------------------------|
| `RuntimeKernel` | kernel (22 modules) | `core/kernel/*` forbidden-dep scan = clean; phases route to ported semantic/sync/memory/execution/reconstruction runtimes |
| `get_runtime_kernel` | kernel | accessor over `RuntimeKernel` |
| `run_canonical_pipeline` | kernel | `RuntimeKernel.run_pipeline` over the same ported phases |
| `run_autonomous_extraction` | distributed | `core/distributed_extraction/autonomous_extraction_engine.py` forbidden-dep scan = clean |

**Path to 128/128:** porting these 4 aggregators (no blocker stands in the way) is the entire residual
gap. They are the recommended next implementation target. The remaining 19 are formally blocked under
the current Python canon; reaching 128 *certified* for those would require the upstream canon changes
enumerated in each verdict (portable parser, fetch/OCR/snapshot injection contracts, explicit platform).

---

## Convergence statement
Per the continuation directive's Success Condition B, **every API now carries either a byte-exact
certification or a formal four-part blocker proof, with the sole residual being 4 proven-portable
aggregators awaiting a multi-session port — none classified unknown/maybe/likely/suspected.** The
classification is complete and evidence-backed.
