# JAVA_SESSION_11_BLOCKER_AUDIT

**Phase 8 — blocker state (machine-derived, re-proved).** No blocker in workflows; the global
hierarchy is unchanged.

## Workflows — no blocker

All 7 workflow APIs passed the relative-aware dependency proof (0 forbidden). Full family
implemented and parity-proven. No API dropped.

## Remaining global blockers (42 APIs of 78 remaining)

| Blocker class | APIs | % of remaining | mitigation |
| --- | ---: | ---: | --- |
| bs4 import barrier (eager `core.semantic`/`core.evidence` `__init__`; never executed) | ~26 | ~33 % | upstream lazy-import (highest leverage) |
| lxml/bs4 HTML-parse (executed) | ~6 | ~8 % | lxml Soup engine (multi-session) |
| network | ~5 | ~6 % | boundary injection |
| OCR (Tesseract) | 2 | ~3 % | graceful-degrade only |
| browser (Playwright) | ~3 | ~4 % | fixture transforms |
| PDF/DOCX | 2 | ~3 % | defer |
| platform (`sys.platform`) | 2 | ~3 % | permanent-deferred |

## Single highest-leverage blocker (unchanged)

The **bs4 import barrier** — ~26 behaviorally-clean APIs blocked only by Python's eager package
`__init__`. Upstream lazy-import unblocks ~33 % of the remaining surface. Java cannot fix it.

## Clean surface remaining (~33 APIs, zero new substrate)

evolution (6), causality (5), streaming (4), reconstruction (4), memory (4), identity (3),
connectors-live (3), interaction (2), auth (1), repository (1). This is the actionable sweep
→ ~83/128 with no upstream change.
