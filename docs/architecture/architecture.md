# Architecture

WebWeaveX is organized as deterministic runtime phases routed through a **universal runtime kernel**.

## Pipeline

```
Extract → Cognize → Synchronize → Evolve → Remember → Execute → Reconstruct
```

## Canonical packages

- `core/kernel/` — operational substrate and phase bridges
- `core/ir/unified_runtime_ir.py` — merged runtime cognition IR
- `core/browser/`, `core/native/`, `core/repository/` — extraction surfaces
- `core/semantic/`, `core/workflows/`, `core/synchronization/`, `core/evolution_runtime/`
- `core/connectors/`, `core/memory/`, `core/execution/`, `core/reconstruction/`
- `core/runtime_graph/` — universal federated graph merge
- `core/crypto/` — Kaalka persistence

## Design principles

1. **Deterministic** — SHA-256 IDs, sorted collections, tick-indexed history
2. **Bounded** — explicit caps on graphs, queues, replay depth
3. **Replay-safe** — identical inputs produce identical outputs
4. **Kaalka-secured** — encrypted persistence for operational state
