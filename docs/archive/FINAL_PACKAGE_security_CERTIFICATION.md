# FINAL PACKAGE SECURITY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 23 |
| PASS | 14 |
| FAIL | 9 |
| UNTESTED | 0 |
| Hash mismatches | 3 |
| State mismatches | 3 |

## Behavioral mismatches

- `core/security/hardening/__init__.py` — barrel_export_mismatch:['sandbox_text', 'timeout_guard', 'recursion_guard', 'memory_guard', 'decompression_guard']
- `core/security/hardening/parser_sandbox_engine.py` — py=None js=raw.slice(...).decode is not a function
- `core/security/hardening/ssrf_guard_engine.py` — py=None js=urlparse is not defined
- `core/security/payload_limits.py` — py=None js=safe.encode is not a function
- `core/security/remote_target.py` — py=None js=urlparse is not defined
- `core/security/safe_parser.py` — output_or_state_mismatch
- `core/security/ssrf_guard.py` — output_or_state_mismatch
- `core/security/url_validator.py` — output_or_state_mismatch
- `core/security/v4/__init__.py` — barrel_export_mismatch:['enforce_resource_budget_v4']

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
