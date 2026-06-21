# JAVA_SESSION_14_BLOCKER_AUDIT

**Phase 8 — blocker state (machine-derived, re-proved).**

## New blocker findings this session

| API | blocker | type | implementable when |
| --- | --- | --- | --- |
| `stream_extract` | imports `core.extract.pipeline` → bs4/lxml | import-time, behavioral | upstream bs4 lazy-import |
| `capture_websocket_frames` | live Playwright `page` attribute coupling | runtime, platform | browser-fixture harness (cross-lang Deferred) |

`run_live_runtime` is **not** blocked — it is certified via projection parity (its output is
self-referential and so not serializable as a single blob, but every computed value is byte-exact).

## Remaining global blockers (42 APIs of 62 remaining)

| Blocker class | APIs | % of remaining | mitigation |
| --- | ---: | ---: | --- |
| bs4 import barrier (eager `core.semantic`/`core.evidence` `__init__`) | ~26 | ~42 % | upstream lazy-import (highest leverage) |
| lxml/bs4 HTML-parse (executed) | ~6 | ~10 % | lxml Soup engine |
| network | ~4 | ~6 % | boundary injection |
| OCR / browser / PDF / platform | ~6 | ~10 % | fixtures / defer |

## Single highest-leverage blocker (unchanged)

The **bs4 import barrier** — now ~42 % of remaining surface (incl. `stream_extract`). Upstream
lazy-import of bs4 in `core.semantic`/`core.evidence` `__init__` is the highest unlocked-APIs/effort
lever. Java cannot fix it.

## Clean surface remaining (~18 APIs, zero new substrate)

reconstruction (4), memory (4), identity (3), connectors-other (3), interaction (2), auth (1),
repository (1). → ~84/128 with no upstream change.
