# WebWeaveX Specification

**Authority model:** Neither Python nor JavaScript owns this specification. Both implementations must conform.

## Layout

| Path | Purpose |
|------|---------|
| `contracts/` | Public behavioral contracts (inputs, outputs, invariants) |
| `schemas/` | JSON/Zod/structural schemas shared by implementations |
| `vectors/` | Canonical behavioral vectors for certification |
| `behavior/` | Narrative behavioral expectations per subsystem |

## Certification

- **Python** validates against `specification/vectors/` (dev/CI tooling).
- **JavaScript** validates against `specification/vectors/` at `npm test` / `npm run validate` — **no Python runtime**.

## Migration

Vectors currently mirrored under `validation/vectors/` are being re-homed here with `source: webweavex-spec` (not `origin/python`).
