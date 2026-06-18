# JAVA_EXTRACTION_GOVERNANCE_AUDIT

**Phase 5 — audit of `PARITY_MANIFEST.json` for the extraction subsystem. Analysis only;
the manifest is NOT modified.**

The manifest is the **shared 128-API contract** across Python (canonical), JS, and Dart. Its
`classification` (Complete / Partial / Deferred) describes the **cross-language** parity
state of that triple — it is **not** a statement about Java, nor strictly about
determinism. This audit separates three things the manifest conflates, so the Java port
does not mis-target work:

- **(M) manifest class** — Complete / Partial / Deferred (P/JS/Dart).
- **(D) determinism** — is the Python function pure/deterministic given its inputs?
- **(J) Java parity feasibility** — can Java prove byte-exact parity *stub-free* now?

---

## 1. Extraction APIs in the manifest

26 manifest APIs are extraction-related (the `extract*`/`crawl*`/`analyze`/`stream_extract`/
`universal_extract`/`*_for_extraction` orchestrators, `compile_document`, `compile_repository`,
`ingest_input`, `query_documents`/`query_repository`, plus the native pair). The
already-Java-proven connector-runtime four (`extract_database/api/runtime_streams/telemetry`)
are excluded — they are DONE.

| API | (M) manifest | (D) deterministic? | (J) Java feasibility | Audit note |
| --- | --- | --- | --- | --- |
| `extract_document_runtime` | **Partial** | ✅ pure | **READY** | **Mis-low.** Partial only because `dart:false`; the Python fn is pure text→IR. Java can prove it now. |
| `compile_document` | Complete | ✅ pure | READY (large) | Correct. Already Complete P/JS/Dart. |
| `extract_paginated_content` | Complete | ✅ pure | READY | Correct. |
| `ingest_input` | Complete | ✅ pure | READY | Correct. |
| `heal_selector` | **Partial** | ✅ pure | **READY** | **Mis-low.** `dart:true` but `contract_parity:false`; the Python fn is pure. Java-provable. Tiny html.parser edge on `html` arg (Risk R-7). |
| `replay_interactions` | **Partial** | ✅ output-pure | **READY (output)** | **Mis-low** for the *returned log*; the live page side-effects are not in the output. |
| `run_live_runtime` | **Partial** | ✅ pure | **READY** | **Mis-low.** Aggregates the already-certified connector family; pure over `snapshot`. |
| `run_autonomous_extraction` | Partial | ✅ core-pure | READY (core) | Correct *as a whole* (optional native fan-out is Class E); base scheduler is pure. |
| `extract_repository` | Partial | 🟡 path-sensitive | READY-with-harness | **Partly correct.** Deterministic per-machine but embeds abs paths + OS separator → needs canonicalization harness (Risk R-2). |
| `compile_repository` | Complete | ✅ pure | READY | Correct (IR compiler, not the FS walk). |
| `query_documents` | Complete | ✅ pure | READY | Correct (document-family query). |
| `query_repository` / `query_repo` | Complete | ✅ pure | READY | Correct. |
| `extract` / `extract_async` | Partial | 🟡 core; ❌ entry | **BLOCKED (Soup)** | Correct. lxml Soup + (URL) network + (groq) LLM. |
| `extract_docs` / `extract_repo` | Partial | 🟡 | BLOCKED (Soup) | Correct — thin wrappers over `extract`. |
| `analyze` | Partial | ✅ graph / 🟡 source | BLOCKED (source) / READY (graph) | **Dual-mode** — manifest's single class hides that graph-mode is pure. |
| `stream_extract` | Partial | 🟡 | BLOCKED (Soup) | Correct — Soup-bound transitively (ANALYSIS §3.1). |
| `extract_recursive` | Partial | ❌ | BLOCKED (network) | Correct — mandatory crawl loop. |
| `crawl` / `crawl_async` | Partial | 🟡 core | BLOCKED (network) | Correct. |
| `universal_extract` | Partial | mixed | mixed | Correct — dispatcher; archive/repo/unsupported branches portable. |
| `extract_web` | Partial | 🟡 | BLOCKED (browser) | Correct — Playwright + html.parser. |
| `extract_infinite_scroll` | **Deferred** | 🟡 transform | BLOCKED (live source) | Correct as **source-deferred**; transform-core is fixture-provable. |
| `capture_dom_mutations` | **Deferred** | 🟡 transform | BLOCKED (live source) | Same — source-deferred, transform portable. |
| `capture_websocket_frames` | **Deferred** | 🟡 transform | BLOCKED (live source) | Same. |
| `extract_native` | **Deferred** | ❌ `sys.platform` | **DEFERRED permanent** | Correct — genuinely host-bound. |
| `run_native_cognition` | **Deferred** | ❌ `sys.platform` | **DEFERRED permanent** | Correct — host-bound (+ electron CDP). |
| `run_canonical_pipeline` | Partial | 🟡 by kind | PARTIAL | Correct — web kind inherits browser; doc/text/repo kinds pure. |

---

## 2. Findings

**F1 — "Partial" ≠ "non-deterministic".** Six extraction APIs classed Partial are in fact
**pure and Java-parity-provable now**: `extract_document_runtime`, `heal_selector`,
`run_live_runtime`, `replay_interactions` (output), plus the graph-mode of `analyze` and the
scheduler-core of `run_autonomous_extraction`. Their Partial label reflects **Dart absence**
(`dart:false`) or an unaligned cross-language *contract*, not Python non-determinism. The
Java port should treat these as legitimate targets and **not** wait on the Soup engine.

**F2 — Deferred is two different things.** `extract_native`/`run_native_cognition` are
**permanently** deferred (`sys.platform`). But `extract_infinite_scroll`/
`capture_dom_mutations`/`capture_websocket_frames` are **source-deferred**: their Python
*transform* is a deterministic map over a supplied page/snapshot and **can** be parity-proven
against a committed fixture. The manifest's single "Deferred" bucket hides this distinction.

**F3 — No misclassification requiring a manifest edit.** Every extraction API is present and
its class is defensible from the cross-language (P/JS/Dart) viewpoint the manifest encodes.
The gaps are **interpretation gaps for the Java port**, not manifest errors. **Recommendation:
do not edit `PARITY_MANIFEST.json`** (policy §2: "it is not edited to suit Java"). Record the
Java-feasibility view in the matrix/validator instead.

**F4 — `extract_multimodal` is Complete but binary-bound.** It is classed Complete (P/JS/Dart)
yet its OCR boundary uses Tesseract. It is parity-safe only on its *graceful-degrade /
provided-snapshot* path; the live-image path is platform-bound. It belongs to the **vision/ocr
layer (matrix session 7)**, not this extraction session — flagged so it is not pulled in early.

---

## 3. Governance wiring required when the READY slice lands (no change this session)

Per [`JAVA_BRANCH_POLICY.md`](../JAVA_BRANCH_POLICY.md) §3/§6 and
[`tools/validate_java_manifest.py`](../tools/validate_java_manifest.py), each newly proven API
must, in the **same** change set, add: a `MAPPING` entry (api → Java FQN, golden file,
section), a golden-vector section, a `CrossLanguageParity*Test` that loads that file, an
`✅ Implemented (parity-proven)` matrix row, and the implemented package in the matrix package
list. The validator enforces 10 checks incl. bidirectional source↔matrix drift (check 10) and
`matrix_proven_count == len(MAPPING)` (check 5). The CI `PROVEN_FLOOR` (currently 21) must be
raised to the new count and **never** decreased.

**Manifest-level pre-conditions already satisfied** for the READY targets (all have
`python:true, javascript:true`): `extract_document_runtime`, `compile_document`,
`extract_paginated_content`, `heal_selector`, `ingest_input`, `run_live_runtime`. So adding
them to the Java proven set will **not** trip validator check 1 (proven API absent from
manifest). `extract_document_runtime` and `heal_selector` are `dart:false`/Partial in the
shared manifest — that is fine: the validator checks presence in the manifest and the Java
matrix, not the cross-language class.

**No governance object is modified by this analysis session.** All wiring is deferred to the
implementation slice that follows.
