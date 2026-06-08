# FINAL PACKAGE IDENTITY EXECUTION CERTIFICATION

**Measured:** 2026-06-04T11:00:07.792567+00:00

**Status:** FAIL

| Metric | Count |
|--------|-------|
| Modules tested | 20 |
| PASS | 7 |
| FAIL | 13 |
| UNTESTED | 0 |
| Hash mismatches | 0 |
| State mismatches | 0 |

## Behavioral mismatches

- `core/identity/browser_identity_orchestrator.py` — py=None js=_USER_AGENTS.includes is not a function
- `core/identity/fingerprint_persistence_engine.py` — py=None js=Path is not defined
- `core/identity/font_runtime_engine.py` — py=None js=_FONTS.includes is not a function
- `core/identity/identity_replay_engine.py` — py=None js=_USER_AGENTS.includes is not a function
- `core/identity/identity_rotation_engine.py` — py=None js=The requested module './browserProfileEngine.js' does not provide an export named 'PROFILE_IDS'
- `core/identity/language_runtime_engine.py` — py=None js=_LANGUAGES.includes is not a function
- `core/identity/media_device_runtime_engine.py` — py=None js=_DEVICES.includes is not a function
- `core/identity/navigator_runtime_engine.py` — py=None js=_USER_AGENTS.includes is not a function
- `core/identity/platform_runtime_engine.py` — py=None js=_PLATFORMS.includes is not a function
- `core/identity/session_identity_engine.py` — py=None js=object is not iterable (cannot read property Symbol(Symbol.iterator))
- `core/identity/timezone_runtime_engine.py` — py=None js=_TIMEZONES.includes is not a function
- `core/identity/user_agent_runtime_engine.py` — py=None js=_USER_AGENTS.includes is not a function
- `core/identity/webgl_runtime_engine.py` — py=None js=_WEBGL.includes is not a function

## UNTESTED


**Certification:** NOT ELIGIBLE until PASS == TOTAL.
