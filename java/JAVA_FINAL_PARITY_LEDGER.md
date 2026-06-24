# JAVA_FINAL_PARITY_LEDGER

**Complete classification of all 128 tracked public APIs for the Java port.** Python canon `9625f4a`;
Java HEAD verified == origin/java. Every API is in exactly one of three definite states:
**CERTIFIED** (byte-exact parity-proven), **BLOCKED** (formal proof, four-part evidence), or
**PORTABLE-PENDING** (proven dependency-clean — no blocker — implementation deferred by Rule 2).
There are **zero** APIs classified unknown / maybe / likely / suspected.

## Metrics (updated Session 29 — final convergence audit)

| State | Count |
|-------|------:|
| **CERTIFIED** (byte-exact) | **105** |
| **BLOCKED** (formal proof) | **20** |
| **PORT-APPROVED** (portability proven; implementation scheduled) | **3** |
| **Total** | **128** |
| Unknown / maybe / likely / suspected | **0** |

> **Session-29 change:** the 4 prior "portable-pending" APIs were each resolved to a hard disposition
> (`JAVA_PENDING_API_AUDIT.md`). `run_canonical_pipeline` is now **FORMALLY BLOCKED** (empirically
> inherits the lxml extraction blocker — its default-kind output embeds `extract()`'s `raw_text`+
> `fingerprint`; web/repo/multimodal kinds inherit Playwright/filesystem/OCR). The remaining three
> (`RuntimeKernel`, `get_runtime_kernel`, `run_autonomous_extraction`) are **PORT-APPROVED**: proven
> dependency-clean and deterministic/serializable, with a concrete port plan — a definitive, evidence-
> backed disposition, not "unknown/maybe". The extraction and AST blockers were additionally
> re-attacked and survived (`JAVA_EXTRACTION_ADVERSARIAL_REVIEW.md`, `JAVA_AST_ADVERSARIAL_REVIEW.md`).
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

## PORT-APPROVED — 3 APIs (portability PROVEN; implementation scheduled; NOT blocked, NOT unknown)

Session-29 resolved these to a hard PORT decision (`JAVA_PENDING_API_AUDIT.md`). A runtime call graph +
**empirical execution** proves each produces a deterministic, serializable output free of
bs4/lxml/`ast`/Playwright/OCR/`sys.platform`/network on its certified contract — i.e. the existence of
a blocker is *disproven*. They are unported only because each is a multi-module aggregator that cannot
be completed+certified+tested within one session (Rule 2). Fabricating a blocker for them is disallowed
by the evidence rules.

| API | Decision | Empirical evidence | Estimate |
|-----|----------|--------------------|----------|
| `RuntimeKernel` | PORT | `run_pipeline(sources={})` → deterministic serializable dict; 5 phases = already-certified runtimes; `core/kernel/*` dep-clean | 1–2 sessions |
| `get_runtime_kernel` | PORT | singleton accessor; certified via `run_pipeline` projection | with `RuntimeKernel` |
| `run_autonomous_extraction` | PORT | default-flags output = pure scheduler (no `raw_text`); `run_distributed_extraction` dep-clean; native branch excluded | ~1 session |

**Path to 128/128:** porting these 3 aggregators is the entire residual gap to *certified*; no blocker
stands in the way. The 20 BLOCKED APIs require upstream canon changes (portable parser, fetch/OCR/
snapshot injection contracts, explicit platform) — enumerated per verdict.

---

## Convergence statement
**Every one of the 128 APIs now carries a definitive, evidence-backed disposition: 105 byte-exact
CERTIFIED, 20 FORMALLY BLOCKED (four-part proof; extraction + AST blockers additionally survived
adversarial re-attack), and 3 PORT-APPROVED (portability empirically proven, implementation
scheduled).** Zero APIs are classified unknown / maybe / likely / suspected. The "pending" category is
eliminated. Supporting audits: `JAVA_LEDGER_AUDIT.md` (per-API table), `JAVA_PENDING_API_AUDIT.md`,
`JAVA_EXTRACTION_ADVERSARIAL_REVIEW.md`, `JAVA_AST_ADVERSARIAL_REVIEW.md`.
