# JAVA_SESSION_4B_DEPENDENCY_PROOF

**Pre-implementation gate.** For each Session-4B candidate API, the complete transitive
first-party import closure is computed from the canonical Python source
(`origin/python` @ `9625f4a`, materialized worktree) by an AST walker
(`_trace_imports.py`) that follows every `import`/`from … import` of `core.*`/`webweavex.*`
and flags any third-party dependency in the forbidden set:

`bs4 / BeautifulSoup`, `lxml`, browser (`playwright`, `selenium`, `pyppeteer`), OCR/image
(`pytesseract`, `PIL`, `cv2`), PDF (`pypdf`, `PyPDF2`, `pdfminer`, `fitz`), DOCX/binary
(`docx`, `openpyxl`, `pptx`), network (`requests`, `httpx`, `aiohttp`, `urllib`, `socket`,
`http`), LLM (`groq`, `openai`, `anthropic`).

> **Rule (mission):** if *any* forbidden dependency exists anywhere in the transitive
> closure, the API is **removed** from Session 4B. AST `ast.walk` includes
> **function-local** imports, so a lazily-imported dependency still disqualifies an API.

---

## Result summary

| Candidate API | Entry module | First-party modules | Forbidden hit | Verdict |
| --- | --- | ---: | --- | --- |
| `extract_document_runtime` | `core.documents.universal_document_extraction_engine` | 10 | none | ✅ **SURVIVES** |
| `extract_paginated_content` | `core.interaction.pagination_engine` | 1 | none | ✅ **SURVIVES** |
| `heal_selector` | `core.adaptive.selector_healing_engine` | 2 | **`bs4` (BeautifulSoup)** @ `core.adaptive.semantic_anchor_engine` | ❌ **REMOVED** |
| `ingest_input` | `core.ingestion.universal_ingestion_engine` | 9 | **`pytesseract` + `PIL` (OCR)** @ `core.ocr.ocr_engine` | ❌ **REMOVED** |

**Implemented this session:** `extract_document_runtime`, `extract_paginated_content`.

---

## 1. `extract_document_runtime` — ✅ SURVIVES

**Transitive first-party closure (10 modules):**
```
core.documents.universal_document_extraction_engine   (entry)
 ├─ core.documents.document_structure_engine
 ├─ core.documents.document_hierarchy_engine
 ├─ core.documents.citation_extraction_engine
 ├─ core.documents.reference_extraction_engine
 ├─ core.documents.document_table_engine
 ├─ core.knowledge.document_knowledge_graph_engine
 ├─ core.presentation.presentation_extraction_engine
 ├─ core.spreadsheets.spreadsheet_extraction_engine
 └─ core.ir.document_runtime_ir
```
**Non-first-party imports across the whole closure:** `__future__`, `re`, `typing` — **stdlib only**.

| Forbidden class | Present? | Evidence |
| --- | :---: | --- |
| 1. BeautifulSoup | ❌ no | no `bs4`/`BeautifulSoup` import in any of the 10 modules |
| 2. lxml | ❌ no | — |
| 3. browser runtime | ❌ no | no `playwright`/`selenium` |
| 4. OCR | ❌ no | no `pytesseract`/`PIL` |
| 5. PDF | ❌ no | no `pypdf`/`pdfminer` |
| 6. DOCX | ❌ no | no `docx`/`openpyxl` |
| 7. network | ❌ no | no `requests`/`httpx`/`socket`/`urllib` |
| 8. LLM | ❌ no | no `groq`/`openai` |

Pure `str`/`re`/`list`/`dict` transform over `(text, slides?, workbook?)`. No hashing
(`stable_serialize`/`compute_kaalka_hash`) inside the engine — the IR is an unhashed
aggregate dict; parity is proven on the serialized output (§Test strategy in the execution
plan).

## 2. `extract_paginated_content` — ✅ SURVIVES

**Transitive first-party closure (1 module):** `core.interaction.pagination_engine` —
self-contained. **Non-first-party imports:** `__future__`, `typing` only.

| Forbidden class | Present? |
| --- | :---: |
| 1–8 (all) | ❌ none |

Pure traversal over a caller-supplied **page object** (duck-typed `_test_url` / `_test_next_url`
/ `_test_paginate` / `click`, mirroring a Playwright page). The page is the live boundary in
production, but the function logic is deterministic and parity-provable against a deterministic
fixture page (no browser is imported by the module).

## 3. `heal_selector` — ❌ REMOVED (BeautifulSoup)

**Transitive closure:** `core.adaptive.selector_healing_engine` →
`core.adaptive.semantic_anchor_engine`, which imports **`from bs4 import BeautifulSoup`**
(`BeautifulSoup(html, "html.parser")`). Fails check #1. Per the rule, removed — even though the
selector logic is otherwise pure and the parse only fires on a non-empty `html` argument. This
confirms Risk **R-7** from `JAVA_EXTRACTION_RISKS.md`. `heal_selector` is deferred to the
html.parser-Soup slice.

## 4. `ingest_input` — ❌ REMOVED (OCR)

**Transitive closure (9 modules):** `core.ingestion.universal_ingestion_engine` →
(image branch) `core.multimodal.universal_multimodal_extraction_engine` →
`core.ocr.ocr_engine`, which imports **`pytesseract`** and **`PIL`**. Fails checks #4. The
import is **function-local** (`ingest_input` line 38, inside `if input_type == "image":`) and
`extract_multimodal(path)` is called there — a genuine behavioural dependency of the API's
contract for image inputs. Per the rule (AST includes function-local imports), removed.
Deferred to the vision/OCR layer (matrix session 7).

---

## Reproduction

```
git worktree add -f /tmp/wwx-python origin/python
cd /tmp/wwx-python && python _trace_imports.py _trace_result.json
# stderr:
#   extract_document_runtime: 10 modules -> CLEAN
#   extract_paginated_content: 1 modules -> CLEAN
#   heal_selector: 2 modules -> FORBIDDEN: bs4(BeautifulSoup)@core.adaptive.semantic_anchor_engine
#   ingest_input: 9 modules -> FORBIDDEN: pytesseract(OCR)@core.ocr.ocr_engine,PIL(OCR/image)@core.ocr.ocr_engine
```

The tracer (`_trace_imports.py`) and its JSON output are committed under `tools/` for audit.
