# FINAL SPECIFICATION MIGRATION REPORT

**Measured:** 2026-05-29T15:29:39.413067+00:00

**Status:** STARTED

## Created

- `specification/README.md` — authority model
- `specification/vectors/manifest.json` — vector families

## Pending

- Re-home `validation/vectors/*` → `specification/vectors/*` with `source: webweavex-spec`
- Add `specification/contracts/` and `specification/schemas/` from `docs/specs/`
- JS validators consume `specification/` only (Phase 4)
- Python validators consume same `specification/` (independent CI)
