# Contributor Architecture Guide

## Module Map

| Module | Purpose | Entry Point |
|--------|---------|-------------|
| kernel | Canonical pipeline orchestrator | `lib/src/kernel/runtime_pipeline.dart` |
| determinism | Normalization, serialization, fingerprints | `lib/src/determinism/` |
| graph | Runtime graph construction and query | `lib/src/graph/runtime_graph.dart` |
| memory | Memory fabric, lineage, replay | `lib/src/memory/` |
| replay | Replay equivalence and validation | `lib/src/replay/` |
| reconstruction | Runtime identity rebuild | `lib/src/reconstruction/` |
| browser | Web extraction, SPA stabilization | `lib/src/browser/` |
| crypto | Kaalka v5, hashing | `lib/src/crypto/` |
| workflows | DAG scheduling, execution | `lib/src/workflows/` |
| execution | Runtime execution engines | `lib/src/execution/` |
| evolution | Runtime evolution engines | `lib/src/evolution/` |
| causality | Event chain analysis | `lib/src/causality/` |
| semantic | Semantic runtime | `lib/src/semantic/` |
| connectors | Database, API, streams | `lib/src/connectors/` |
| query | Graph/knowledge query dispatch | `lib/src/query/` |

## Data Flow

```
Input ? kernel/runtime_pipeline ? determinism/normalize ? graph/build
     ? memory/fabric ? replay/validate ? reconstruction/rebuild
```

## Adding a New Feature

1. Create module in `lib/src/<module>/`
2. Export from `lib/webweavex.dart`
3. Add tests in `test/<module>/`
4. Add parity test in `test/parity/`
5. Run: `dart analyze && dart test`
