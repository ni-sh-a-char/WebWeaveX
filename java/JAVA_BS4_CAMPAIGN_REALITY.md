# JAVA_BS4_CAMPAIGN_REALITY

**Tier-B reality reconstruction (S21) — corrects the premise of `JAVA_BS4_DECOUPLE_PLAN.md`.**
Canon `origin/python` @ `9625f4a`. All findings machine-derived (relative-aware trace + runtime
import-guard proof).

## CRITICAL FINDING: the bs4 block is an eager-import artifact, NOT a runtime dependency.

For every Tier-2 API, the `forbidden` count traces to **exactly two modules** —
`core.semantic.table_semantics_engine` and `core.semantic.ui_semantics_engine` — pulled
transitively by the **eager `core.semantic.__init__`**. The API's own runtime path does **not**
call BeautifulSoup.

**Proof (executed):** with `bs4` blocked at call time via an `__import__` guard,
`compile_document_ir("...")` runs to completion and returns its claims/steps — i.e. the document
IR is **runtime-pure**. The eager import only matters for *importing the module*, which Python
does successfully (bs4 is installed); it never affects the *output*.

### Consequence for the Java port

The Java side does not import Python modules — it reimplements the pure logic. So these APIs need
**no Python change** and **no bs4** in Java; they are byte-exact-certifiable today. The
`JAVA_BS4_DECOUPLE_PLAN.md` lazy-import campaign is therefore **not required for Java parity** (it
would only tidy the Python import graph). The **real** blocker is the *size* of the pure
semantic-IR NLP engines that must be reimplemented byte-exact.

## Per-API reality (Tier 2)

| API | engine | closure | runtime bs4? | real blocker |
| --- | --- | ---: | --- | --- |
| `query_documents` | document semantic IR | 276 mod / 6582 L | **no** (pure NLP) | port 6.5k-line IR engine |
| `query_semantics` | dispatch + above | 365 mod / 9445 L | **no** | reuses proven query_graph/knowledge + needs document/repo engines |
| `reason_semantically` | semantic reasoning | 341 mod / 8859 L | **no** | port 8.9k-line reasoning engine |
| `run_semantic_runtime` / `_for_extraction` | semantic orchestrator | large | **no** | port orchestrator + sub-engines |
| `run_application_cognition` | app cognition | forbidden=4 | partial (HTML app) | needs HTML/Soup for some paths |
| `extract_multimodal` | multimodal | 8 mod / 388 L | OCR/vision | **non-portable** (OCR) |
| `ingest_input` | ingestion | 9 mod / 447 L | FS + OCR | FS-coupled + multimodal |
| `heal_selector` | selector healing | 2 mod / 144 L | bs4 only for non-empty HTML | **DONE (S21)** for empty-HTML contract |

## Revised plan

1. **heal_selector** — empty-HTML portable contract **certified (S21, +1 → 93)**. The semantic
   anchor yields nothing for `html=""`, so the `dom_nodes` healing logic is bs4-independent and
   byte-exact. Non-empty-HTML anchor healing remains Tier-C (Soup engine).
2. **The pure NLP engines** (`document_semantic_ir` 6.5k L, `semantic_reasoning` 8.9k L, the
   semantic orchestrator) are **portable but multi-session** byte-exact ports. They are the genuine
   remaining high-value work — recompute the byte-exact semantic-IR engine (mirrors the Dart
   "recomputed semantic IR" effort). Each is its own multi-session campaign.
3. **OCR/multimodal/FS** (`extract_multimodal`, `ingest_input`) — non-portable runtime deps; defer
   with proof.

## Honest status

The cheap-unlock premise (lazy-import → ~13 APIs) was **wrong**: lazy-importing bs4 upstream does
not reduce the Java porting work at all, because the Java port never imports bs4 — it must
reimplement the pure NLP. The accurate ROI: each large semantic engine is a dedicated multi-session
byte-exact port. `heal_selector` (small, 144 L) was the one tractable Tier-2 win and is now done.
