# FINAL PACKAGE TREESITTER EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 6 |
| PASS | 3 |
| FAIL | 3 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/treesitter/__init__.py` — barrel_export_mismatch:['detect_language', 'parse_universal_ast']
- `core/treesitter/tree_sitter_loader.py` — py=None js=SUPPORTED_LANGUAGES.includes is not a function
- `core/treesitter/universal_ast_engine.py` — py=None js=Cannot find package 'fast-json-stable-stringify' imported from C:\Projects\WebWeaveX\src\browser\authenticatedRuntime.ts

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
