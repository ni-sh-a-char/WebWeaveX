# JAVA_FINAL_PARITY_LEDGER

**Complete classification of all 128 tracked public APIs for the Java port.** Python canon `9625f4a`;
Java HEAD verified == origin/java. Every API is in exactly one of three definite states:
**CERTIFIED** (byte-exact parity-proven), **BLOCKED** (formal proof, four-part evidence), or
**PORTABLE-PENDING** (proven dependency-clean — no blocker — implementation deferred by Rule 2).
There are **zero** APIs classified unknown / maybe / likely / suspected.

## Metrics (Session 30 — FINAL, terminal)

| State | Count |
|-------|------:|
| **CERTIFIED** (byte-exact) | **108** |
| **BLOCKED** (formal proof) | **20** |
| **PENDING / PORT-APPROVED** | **0** |
| **Total** | **128** |
| Unknown / maybe / likely / suspected | **0** |

> **Session-30 change:** the 3 PORT-APPROVED aggregators were implemented and **CERTIFIED** byte-exact
> (`golden_vectors_s30.json`, `CrossLanguageParityS30Test`, 11 vectors): `RuntimeKernel.run_pipeline`
> (routes to the 5 already-certified runtime orchestrators; `boundary.size` reproduced via faithful
> `json.dumps`), `get_runtime_kernel` (projection parity), `run_autonomous_extraction` (pure
> distributed scheduler + 12 ported sub-engines, portable flag contract). The PENDING category is now
> **empty**. Every API is terminal: **108 CERTIFIED + 20 FORMALLY BLOCKED = 128**. `run_canonical_pipeline`
> remains the one kernel-adjacent API that is FORMALLY BLOCKED (inherits the lxml extraction blocker).
> Per-API table: `JAVA_LEDGER_AUDIT.md`.

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

### OS / platform / filesystem (3) → `JAVA_PLATFORM_VERDICT.md`
`extract_native`, `run_native_cognition` (`sys.platform` leaks into observable `platform`; live
UIAutomation/Quartz/X11 enumeration). `extract_repository` (reads on-disk repo; OS-ordered `os.walk`).

### Aggregator inheriting a blocker (1) → `JAVA_PENDING_API_AUDIT.md`
`run_canonical_pipeline`. Empirically its default-kind output embeds `extract()`'s `raw_text`+
`fingerprint` (lxml); web→`extract_web` (Playwright), repository→`extract_repository` (fs),
multimodal→`extract_multimodal` (OCR). **No input kind avoids a blocked child** → inherits the blocker.

---

## PORT-APPROVED → CERTIFIED — 3 APIs (Session 30: implemented + certified byte-exact)

The Session-29 PORT decision was executed. All three are now CERTIFIED (`golden_vectors_s30.json`,
`CrossLanguageParityS30Test`):

| API | Java symbol | Evidence |
|-----|-------------|----------|
| `RuntimeKernel` | `io.webweavex.kernel.RuntimeKernel#runPipeline` | routes to 5 certified runtimes; full kernel-bridge infra ported; `boundary.size` via faithful `PyJson.dumpsDefaultAscii` |
| `get_runtime_kernel` | `io.webweavex.kernel.RuntimeKernel#getRuntimeKernel` | singleton; certified via `run_pipeline` projection parity |
| `run_autonomous_extraction` | `io.webweavex.distributed.AutonomousExtraction#runAutonomousExtraction` | `run_distributed_extraction` + 12 distributed sub-engines ported; portable flag contract |

The PENDING / PORT-APPROVED category is now **empty**.

---

## Convergence statement (FINAL)
**Every one of the 128 APIs carries a terminal disposition: 108 byte-exact CERTIFIED and 20 FORMALLY
BLOCKED (four-part proof; extraction + AST blockers survived adversarial re-attack). Zero APIs are
PENDING, PORT-APPROVED, unknown, maybe, likely, or suspected.** The 20 BLOCKED require upstream Python
canon changes (portable parser, fetch/OCR/snapshot injection contracts, explicit platform) — enumerated
per verdict; they cannot be certified byte-exact under the pure-Java / cross-platform-deterministic
constraints. Supporting audits: `JAVA_LEDGER_AUDIT.md` (per-API table), `JAVA_PENDING_API_AUDIT.md`,
`JAVA_EXTRACTION_ADVERSARIAL_REVIEW.md`, `JAVA_AST_ADVERSARIAL_REVIEW.md`. **Mission complete.**
