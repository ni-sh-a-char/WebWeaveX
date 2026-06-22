# JAVA_BS4_DECOUPLE_PLAN

**Phase 7 — bs4-decouple campaign scope (preparation only; NO Python modified, NO decoupling
started).** Canon `origin/python` @ `9625f4a`.

## Goal

Unlock the **Tier-2 (bs4-coupled) APIs without any behavior change** by converting eager,
module-top BeautifulSoup imports into lazy (function-local) imports. This lets the Java port
dependency-prove and byte-exact-certify the bs4-*adjacent* APIs whose runtime path never actually
parses HTML for the inputs we test.

## Tier-2 target APIs (9) + their async wrappers

`query_documents`, `query_semantics`, `reason_semantically`, `run_semantic_runtime`,
`run_semantic_for_extraction`, `extract_multimodal`, `ingest_input`, `heal_selector`,
`run_application_cognition` (+ `crawl_async`/`extract_async` inherit). Plus the Tier-5 aggregators
that pull bs4 only through these become partially unblocked.

## Where BeautifulSoup actually enters (grep `import bs4|from bs4|BeautifulSoup` in `core/`)

| Module | Role |
| --- | --- |
| `core/semantic/table_semantics_engine.py` | HTML table → semantics |
| `core/semantic/ui_semantics_engine.py` | HTML UI → semantics |
| `core/browser/html_semantic_extraction_engine.py` | HTML → semantic extraction |
| `core/extract/html_extractor.py` | the extraction pipeline parser |
| `core/extraction/semantic_content_extraction_engine.py` | content extraction |
| `core/dom/dom_reconstruction_engine.py` | DOM rebuild |
| `core/application/{dashboard,form,navigation_semantic,ui_semantic}_*` | app-cognition HTML |
| `core/adaptive/semantic_anchor_engine.py` | selector-healing anchors |
| `core/security/safe_parser.py` | the shared safe HTML parser |

## Why these block import even when HTML is never parsed

`core/semantic/__init__.py` and `core/evidence/__init__.py` are **eager**: they import their
orchestrators/engines at package-import time, which transitively imports the bs4 modules above.
So `import core.semantic.X` triggers bs4 **even for the non-HTML APIs** (e.g. `query_semantics`
on a pre-parsed graph). This is the exact "eager-`__init__` barrier" confirmed across sessions.

## Candidate lazy-import points (upstream Python change — behavior-preserving)

1. **`core/security/safe_parser.py`** (highest leverage): move `from bs4 import BeautifulSoup`
   from module top into the parse function body. Every HTML module routes through here, so one
   change removes the import-time dependency for the whole subtree while keeping runtime behavior
   identical.
2. **`core/semantic/__init__.py` / `core/evidence/__init__.py`**: convert eager re-exports to
   `__getattr__`-based lazy module loading (PEP 562) so importing the package does not import the
   bs4 engines until an HTML API is actually called.
3. Per-engine: wrap `import bs4` inside the functions in the table list that parse HTML.

All three are **import-time-only** changes — no parsing logic, ordering, or output changes → parity
preserved (re-run the full S1–S20 byte-exact suite + the Python==JS==Dart cross-language suite to
confirm zero drift).

## Impact estimate

| Change | APIs unblocked (Java byte-exact, non-HTML paths) |
| --- | ---: |
| lazy `safe_parser` + lazy semantic/evidence `__init__` | **~9 Tier-2** directly |
| + Tier-5 aggregators that only needed bs4 | **~4–6 more** become reachable |
| **Total expected unlock** | **~13–15 APIs** → ~105–107/128 |

The genuinely HTML-parsing APIs (Tier 3 lxml/extract) still need the **Soup engine**
(`JAVA_LXML_EXTRACTION_PLAN.md`, Phase C) — that is a separate, larger effort.

## Constraints (per mission)

- **Do NOT modify Python yet.** This document is the scope only.
- The decouple is an **upstream-canon** change; once landed in `origin/python`, the Java side
  re-runs dependency proofs (expecting forbidden→0 + import OK) and certifies each unblocked API
  with the established pattern.
