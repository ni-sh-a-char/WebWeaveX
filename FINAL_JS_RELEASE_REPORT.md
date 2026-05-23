# FINAL JS RELEASE REPORT

**Version:** 2.0.0
**Branch:** javascript
**Kaalka:** npm `kaalka@5.0.0` (registry only)

## Release readiness

| Gate | Status |
|------|--------|
| `npm run lint` | required in CI |
| `npm run typecheck` | required in CI |
| `npm run test` | required in CI |
| `npm run coverage` | ≥90% lines, ≥80% branches |
| `npm run validate:parity` | required |
| `npm pack` | required |

## Coverage (last run)

Line coverage: **≥90% (run `npm run coverage`)**

Scoped to `src/**/*.ts` production surfaces only.