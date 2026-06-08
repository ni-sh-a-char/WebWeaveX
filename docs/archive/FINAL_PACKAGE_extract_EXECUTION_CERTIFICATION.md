# FINAL PACKAGE EXTRACT EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 29 |
| PASS | 4 |
| FAIL | 14 |
| UNTESTED | 11 |
| Hash mismatches | 1 |
| State mismatches | 1 |

## Behavioral mismatches

- `core/extract/advanced/api_extractor.py` — py=None js=ParserRegistry.detect_language is not a function
- `core/extract/advanced/architecture_extractor_v2.py` — py=None js=ln is not defined
- `core/extract/advanced/dependency_extractor_v2.py` — py=None js=ln is not defined
- `core/extract/advanced/docs_extractor_v2.py` — py=None js=h is not defined
- `core/extract/advanced/repository_extractor_v2.py` — output_or_state_mismatch
- `core/extract/architecture_extractor.py` — py=None js=line is not defined
- `core/extract/dependency_extractor.py` — py=None js=deps.extend is not a function
- `core/extract/enrichment_engine.py` — py=KeyError: 'metadata' js=The requested module './facades/serializerFacade.js' does not provide an export named 'dumpsDeterministic'
- `core/extract/html_extractor.py` — py=None js=BeautifulSoup is not defined
- `core/extract/markdown_extractor.py` — py=None js=h is not defined
- `core/extract/metadata_extractor.py` — py=None js=src.splitlines is not a function
- `core/extract/pipeline.py` — py=None js=Cannot find module 'C:\Projects\WebWeaveX\src\security\hardening.js' imported from C:\Projects\WebWeaveX\src\extract\pipeline.ts
- `core/extract/repository_extractor.py` — py=None js=ln is not defined
- `core/extract/repository_intelligence.py` — py=None js=Counter is not defined

## UNTESTED

- `core/extract/facades/core_facade.py` — no_python_functions
- `core/extract/facades/document_facade.py` — no_python_functions
- `core/extract/facades/graph_facade.py` — no_python_functions
- `core/extract/facades/internet_facade.py` — no_python_functions
- `core/extract/facades/knowledge_facade.py` — no_python_functions
- `core/extract/facades/parser.py` — no_python_functions
- `core/extract/facades/parser_facade.py` — no_python_functions
- `core/extract/facades/repository_facade.py` — no_python_functions
- `core/extract/facades/security_facade.py` — no_python_functions
- `core/extract/facades/serialize.py` — no_python_functions
- `core/extract/facades/serializer_facade.py` — no_python_functions

**Certification:** NOT ELIGIBLE until PASS == TOTAL.
