# FINAL VM EQUIVALENCE REPORT

**Status:** Partial — semantic VM link probe passes differential validation.

## Verified (specification/ canonical vectors → JavaScript)

| Probe | Result |
|-------|--------|
| `vm-semantic-link` | PASS — instruction execution, memory `a->b`, bounded |

## Not yet proven

- Full bytecode compilation parity
- Distributed execution VM
- Replay execution VM across full envelope surface
- Continuation VM state persistence

Run: `npx tsx validation/differential/validateVmEquivalence.ts`
