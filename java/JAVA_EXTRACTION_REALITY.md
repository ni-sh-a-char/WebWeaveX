# JAVA_EXTRACTION_REALITY

**Phase 5 — "what extraction actually works today", from code only.** Machine-derived from
`PARITY_MANIFEST.json` (Python/JS/Dart columns), the validator MAPPING (Java column), and the
relative-aware dependency tracer (blocked + why). Not from documentation.

## Connector-runtime extraction — **usable today in Java** (9 APIs, byte-exact)

| API | manifest | Py | JS | Dart | Java | usable? |
| --- | --- | :-: | :-: | :-: | :-: | --- |
| `extract_database_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_api_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_runtime_streams` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_telemetry_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_container_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_ide_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_kubernetes_runtime` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |
| `extract_document_runtime` | Partial* | ✓ | ✓ | — | ✓ | **yes** |
| `extract_paginated_content` | Complete | ✓ | ✓ | ✓ | ✓ | **yes** |

*Partial in the cross-language manifest only because Dart lacks it; Java is byte-exact to Python.

Example (deterministic, no live connection):
```java
Map<String,Object> snap = Map.of("namespaces", List.of("prod","default"),
                                 "pods", List.of(Map.of("name","api-7d")));
Map<String,Object> rt = KubernetesConnector.extractKubernetesRuntime(snap);
// rt = {namespaces:[default,prod], pods:[{name:api-7d}], ..., bounded:true}
```

## Clean but not yet ported (portable today — queued)

| API | subsystem | blocker | note |
| --- | --- | --- | --- |
| `extract_repository` | repository | none (FS) | path-canonicalization harness (R-2) |
| `extract_infinite_scroll` | interaction | none | fixture-page driven |
| `capture_dom_mutations` | streaming | none | snapshot transform (live source deferred) |
| `capture_websocket_frames` | streaming | none | snapshot transform |

## Blocked in canonical Python (cannot reach byte-exact Java without upstream change)

| API | blocker (code evidence) |
| --- | --- |
| `extract`, `extract_async`, `extract_docs`, `extract_repo` | BeautifulSoup+lxml (executed) + LLM + network |
| `extract_web` | BeautifulSoup + Playwright browser |
| `extract_recursive`, `crawl_async` | full extraction stack (bs4+network+OCR+PDF+DOCX+browser) |
| `crawl` | network (`requests`) |
| `stream_extract` | BeautifulSoup (transitive via `extract()`) + LLM + network |
| `universal_extract` | BeautifulSoup + OCR + PDF + DOCX |
| `extract_multimodal` | Tesseract OCR + PIL |
| `extract_native` | `sys.platform` host branch |
| `analyze` (source-mode) | BeautifulSoup via `extract()` |

## Bottom line

**Extraction that works in Java today = the 9 deterministic connector/document/pagination
APIs.** The HTML/web/crawl/multimodal extraction surface is blocked in the **Python canon**
itself (real parser/OCR/network/browser runtimes), not by a Java gap. See
[`JAVA_PARITY_RISK_REGISTER.md`](JAVA_PARITY_RISK_REGISTER.md) for the unblock sequence.
