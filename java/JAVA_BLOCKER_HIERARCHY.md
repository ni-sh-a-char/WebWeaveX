# JAVA_BLOCKER_HIERARCHY

**Phase 5 — machine-derived blocker hierarchy.** Every blocked API grouped by root cause
(`tools/rank_remaining_apis.result.json`). 42 of 91 remaining APIs are blocked in the **Python
canon** (not Java-side). Surface % = share of the 91 remaining.

| Rank | Blocker class | APIs | % of remaining | mitigation | est. unlock |
| ---: | --- | ---: | ---: | --- | ---: |
| **1** | **bs4 import barrier** (eager `core.semantic`/`core.evidence` `__init__` pulls BeautifulSoup; **never executed** — proven S6 runtime trace) | **~26** | **~29 %** | Python-canon: lazy-import bs4 in `core.semantic`/`core.evidence`, OR adopt a behavioral (runtime-trace) gate | **~26** |
| 2 | lxml/bs4 HTML-parse barrier (real, executed) | ~6 | ~7 % | build an lxml+html.parser Soup engine (multi-session substrate) | ~6 |
| 3 | network barrier | ~5 | ~5 % | inject fetch at the boundary; only the deterministic core is portable | partial |
| 4 | OCR barrier (Tesseract) | 2 | ~2 % | port graceful-degrade path only | partial |
| 5 | browser barrier (Playwright) | ~3 | ~3 % | fixture-snapshot transforms only | partial |
| 6 | PDF / DOCX binary | 2 | ~2 % | accept text divergence or defer | 0 |
| 7 | platform (`sys.platform`) | 2 | ~2 % | permanent-deferred (host-dependent) | 0 |

(Classes overlap: the ~10 full-extraction APIs trip several barriers at once.)

## Single highest-leverage blocker

**Rank 1 — the bs4 import barrier.** ~26 APIs (semantic, evidence, memory-bs4, modal,
application, native-snapshot, document/repository IR) are **behaviorally bs4-free** (Session-6
runtime trace: `compile_document` executes 238 modules with **0** bs4 call-hits) yet blocked by
Python's eager package `__init__` importing BeautifulSoup. A single upstream refactor — make
`core.semantic.semantic_orchestrator`'s `table_semantics_engine`/`ui_semantics_engine` imports
lazy — moves **~29 % of the remaining surface** from blocked → clean in one change.

This is a **Python-canon change**, outside the Java branch. It is recorded here as the #1
mission-level risk-reduction action. Until then, those 26 APIs stay blocked under the strict
import-based gate; the ~46 truly-clean APIs (no barrier) are the actionable sweep.
