<p align="center">
  <strong>Deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
</p>

<p align="center">
  <a href="https://pub.dev/packages/webweavex"><img src="https://img.shields.io/pub/v/webweavex?style=flat-square" alt="pub"/></a>
  <img src="https://img.shields.io/badge/Dart-3.3%2B-0175C6?style=flat-square&logo=dart&logoColor=white" alt="Dart"/>
  <img src="https://img.shields.io/badge/parity-11%2F11-22c55e?style=flat-square" alt="Parity"/>
  <img src="https://img.shields.io/badge/tests-793%20passing-22c55e?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/coverage-97.25%25-22c55e?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/API%20parity-88%2F126-3b82f6?style=flat-square" alt="API parity"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="License"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Coffee"/></a>
</p>

---

## Contents

- [Overview](#overview) · [Why WebWeaveX](#why-webweavex) · [Features](#features)
- [Architecture](#architecture) · [Installation](#installation) · [Quick Start](#quick-start)
- Subsystems: [Extraction](#extraction-systems) · [Runtime](#runtime-systems) · [Memory](#memory-systems) · [Replay](#replay-systems) · [Reconstruction](#reconstruction-systems) · [Workflows](#workflows) · [Graph](#graph-intelligence) · [Determinism](#deterministic-systems)
- [API Reference](#api-reference) · [Examples](#examples) · [Performance](#performance)
- [Testing](#testing) · [Coverage](#coverage) · [CI/CD](#cicd) · [Pub.dev Release](#pubdev-release)
- [Contributing](#contributing) · [OSS Governance](#oss-governance) · [Security](#security) · [Roadmap](#roadmap) · [Vision](#vision)

---

## Overview

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents**
to understand, continue, reconstruct, replay, and reason about **authenticated operational
software systems**.

This **`dart`** branch is the native **pub.dev** implementation — not a scraper, not an LLM
wrapper, not AGI hype. It is byte-for-byte parity-aligned with the Python (PyPI) and JavaScript
(npm) implementations at the cryptographic and deterministic-serialization layers.

| Branch | Role |
|--------|------|
| [`main`](https://github.com/ni-sh-a-char/WebWeaveX) | Ecosystem portal |
| [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | **Canonical** PyPI runtime (2.0.1) |
| [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | npm runtime (2.0.1) |
| **`dart`** (this) | pub.dev runtime (2.0.1) |

Spec: [CANONICAL_RUNTIME_SPEC.md](docs/architecture/CANONICAL_RUNTIME_SPEC.md) · Matrix: [ECOSYSTEM_MATRIX.md](docs/architecture/ECOSYSTEM_MATRIX.md)

### Humans and AI agents

| Audience | Use |
|----------|-----|
| **Engineers** | Deterministic extraction, session continuation, replay audits |
| **AI agents** | Replay-safe memory, graph identity, operational continuity |

---

## Why WebWeaveX

Traditional tools capture HTML, not **operational runtime state**. WebWeaveX provides canonical
serialization, Kaalka-sealed sessions, replay equivalence, and reconstruction identities so that
**how software runs** — not just what HTML was returned — becomes a first-class, reproducible
artifact.

| Problem | With WebWeaveX |
|---------|----------------|
| Ephemeral browser state | Stabilized DOM + runtime fingerprints |
| Auth drift | Encrypted session continuation (authorized credentials) |
| Nondeterministic replays | `validateReplayEquivalence` |
| Lost operational context | Runtime graphs + memory fabric |

### What WebWeaveX is NOT

| Not | Reality |
|-----|---------|
| Scraper / crawler | Operational runtime substrate |
| AGI product | Bounded deterministic pipelines |
| Auth / CAPTCHA bypass | No credential cracking |
| LLM wrapper | Native Dart library |

---

## Features

- **Deterministic core** — `normalizeRuntimeValue → stableSerialize → UTF-8 → Kaalka v5 → base64`,
  byte-identical to Python and JavaScript (`computeDeterministicHash` produces matching hashes).
- **Runtime graphs** — sorted, fingerprinted node/edge graphs (`buildRuntimeGraph`, `graphFingerprint`).
- **Runtime memory fabric** — build, query, search, and lineage-track operational memory.
- **Replay equivalence** — prove two runtime envelopes are operationally identical.
- **Runtime reconstruction** — rebuild deterministic runtime identities from extraction envelopes.
- **Authenticated continuation** — Kaalka-encrypted session save/load (you supply credentials).
- **12 runtime-cognition families** — causality, semantic, synchronization, evolution, workflows,
  execution, memory-runtime, reconstruction-runtime, persistence, connectors, query, kernel/IR.
- **Cross-language parity vectors** — 11/11 core + ~145 runtime-API hash vectors under `validation/`.

---

## Architecture

```text
Input → Canonical pipeline → Graph + Memory → Replay check → Reconstruction
              ↓
     Normalization + Kaalka v5 (pub.dev kaalka)
```

Layered source layout (`lib/src/`):

| Layer | Packages |
|-------|----------|
| crypto | `kaalka_runtime`, `kaalka_v5_proc`, `time_key`, `hashing` |
| determinism | `normalization`, `dom_stabilization`, `fingerprint`, `stable_serialize` |
| graph | `runtime_graph`, `runtime_graph_replay`, `runtime_graph_reconstruction` |
| kernel | `runtime_pipeline`, `replay_pipeline`, `reconstruction_pipeline`, `kernel_runtime` |
| memory | `runtime_memory`, `runtime_memory_graph`, `memory_lineage`, `memory_replay`, `query_memory` |
| replay | `replay_runtime/graph/memory/dom/fingerprint/equivalence` |
| reconstruction | `reconstruct_runtime/graph/memory/replay/browser` |
| browser | `extract_web`, `render_page`, `runtime_session`, `authenticated_runtime`, … |
| families | `causality`, `semantic`, `synchronization`, `evolution`, `workflows`, `execution`, `query`, `connectors`, `persistence`, `distributed`, `orchestration` |

---

## Installation

```bash
dart pub add webweavex
```

or add to `pubspec.yaml`:

```yaml
dependencies:
  webweavex: ^2.0.1
  kaalka: ^5.0.0
```

Requires Dart SDK `>=3.3.0 <4.0.0`.

---

## Quick Start

```dart
import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  final hash = computeDeterministicHash({'status': 'ok'});
  final pipeline = await runCanonicalPipeline({
    'url': 'https://example.com',
    'sourceType': 'web',
  });
  print('$hash ${pipeline['bounded']}');
}
```

---

## Extraction systems

WebWeaveX models extraction as a **bounded, deterministic** operation over provided or fetched
input — never an unbounded crawl. The browser layer (`extractWeb`, `renderPage`,
`captureRuntime`) operates over a bounded HTTP surface; live-browser-only capabilities
(infinite scroll, DevTools frames) are documented as platform-deferred in
[`API_PARITY_VALIDATION_REPORT.md`](API_PARITY_VALIDATION_REPORT.md).

```dart
final result = await extractWeb('https://example.com');
print(result['kind']);          // extraction kind
print(result['deterministic_hash']);
```

---

## Runtime systems

```dart
final graph = buildRuntimeGraph({'session': {'authenticated': true}});
final runtime = {'unified_runtime_graph': graph.toJson()};
```

Runtime-cognition families each expose `run_*`, `save_*`, `load_*`, and `replay_*` entry points
with proven cross-language hash parity (causality, semantic, synchronization, evolution,
workflows, execution).

---

## Memory systems

```dart
final graph = buildRuntimeGraph({'session': {'authenticated': true}});
final memory = buildRuntimeMemory(graph);
final slice = queryRuntimeMemory(memory, 'graph');
final lineage = buildMemoryLineage(memory);
```

---

## Replay systems

```dart
final report = validateReplayEquivalence(envelope, envelopeClone);
print(report['equivalent']); // true when checks pass
```

Checks: graph hash, global fingerprint, browser identity, DOM hash (when present),
memory stable hash (when present).

---

## Reconstruction systems

```dart
final rebuilt = reconstructRuntime(extraction: envelope);
print(rebuilt['runtime_id']);
```

---

## Workflows

```dart
final plan = buildWorkflowPlan({'objective': 'extract-and-verify'});
final run = runAutonomousWorkflow(plan);
final replay = replayWorkflowRuntime(run);
```

---

## Graph intelligence

Runtime graphs are deterministically sorted and fingerprinted so identical operational state
yields identical identity:

```dart
final graph = buildRuntimeGraph({'agent_step': 'observe'});
final fp = graphFingerprint(graph);
final replayed = replayRuntimeGraph(graph.toJson());
```

---

## Deterministic systems

```
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka._proc → base64
```

| Layer | Mechanism |
|-------|-----------|
| Unicode | NFKC (Node when available, matching V8 `String.normalize('NFKC')`) + CRLF→LF |
| Objects | Sorted keys, volatile field strip |
| Crypto | `kaalka@5.0.0` byte `_proc` + base64 |
| Graph | Sorted nodes/edges, `graphFingerprint` |

**11/11** core vectors match the JavaScript reference:

```bash
dart run validation/validate_parity.dart   # crossLangMatch: true
```

---

## API Reference

The public barrel (`package:webweavex/webweavex.dart`) re-exports **53 family modules**
(~372 public functions, 7 classes). Grouped by family:

| Family | Representative public APIs |
|--------|----------------------------|
| crypto | `computeDeterministicHash`, `encryptValue`, `decryptValue`, `encryptSessionState`, `saveEncryptedSession`, `loadEncryptedSession` |
| determinism | `normalizeRuntimeValue`, `stableSerialize`, `computeGlobalRuntimeFingerprint`, `stabilizeDomHtml` |
| graph | `buildRuntimeGraph`, `graphFingerprint`, `queryRuntimeGraph`, `replayRuntimeGraph` |
| kernel | `runCanonicalPipeline`, `getRuntimeKernel`, `compileUnifiedRuntimeIr`, `RuntimeKernel`, `UniversalInput` |
| memory | `buildRuntimeMemory`, `queryRuntimeMemory`, `searchRuntimeMemory`, `buildMemoryLineage`, `buildRuntimeMemoryGraph` |
| replay | `validateReplayEquivalence`, `replayRuntimeState`, `validateFullRuntimeReplay`, `replayRuntimeMemory` |
| reconstruction | `reconstructRuntime`, `fabricateRuntimeReality`, `cloneRuntimeEnvironment`, `validateReconstructedRuntime` |
| browser | `extractWeb`, `renderPage`, `captureRuntime`, `buildBrowserIdentity`, `continueAuthenticatedRuntime` |
| adaptive | `healSelector`, `buildSemanticAnchor` (native Dart selector healing) |
| causality | `runCausalityRuntime`, `replayCausalRuntime`, `saveCausalMemory`, `loadCausalMemory` |
| semantic | `runSemanticRuntime`, `replaySemanticRuntime`, `buildSemanticMemory` |
| synchronization | `runSynchronizedRuntime`, `buildRuntimeDelta`, `replaySynchronizedRuntime` |
| evolution | `runEvolutionRuntime`, `buildRuntimeEvolution`, `evolveSelectorRuntime` |
| workflows | `runAutonomousWorkflow`, `buildWorkflowPlan`, `replayWorkflowRuntime` |
| execution | `runExecutionRuntime`, `executeRuntimeAction`, `simulateRuntimeExecution`, `replayRuntimeExecution` |
| connectors | `extractDatabaseRuntime`, `extractApiRuntime`, `extractRuntimeStreams`, `extractTelemetryRuntime` |
| query | `queryGraph`, `queryKnowledge`, `queryRepository`, `queryDocuments`, `querySemantics` |
| persistence | `saveRuntimeMemory`, `loadRuntimeMemory`, `saveDistributedCheckpoint`, `loadDistributedCheckpoint` |

Full per-API parity classification (Complete / Partial / Deferred):
[`PUBLIC_API_MATRIX.md`](PUBLIC_API_MATRIX.md) · [`API_PARITY_VALIDATION_REPORT.md`](API_PARITY_VALIDATION_REPORT.md).

---

## Examples

Runnable programs live in [`example/`](example/). AI-agent continuity pattern:

```dart
final graph = buildRuntimeGraph({'agent_step': 'observe'});
final memory = buildRuntimeMemory(graph);
final agentView = queryRuntimeMemory(memory, 'graph');
final continuity = encryptValue({'checkpoint': agentView}, 'agent-session-key');
```

Authenticated continuation (you supply authorized credentials — no bypass tooling):

```dart
saveAuthenticatedRuntime('./session.json', {'cookies': []}, 'your-key');
final result = await extractWeb('https://example.com',
    authenticated: true, sessionPath: './session.json', encryptionKey: 'your-key');
```

---

## Performance

WebWeaveX is CPU-bound deterministic serialization + hashing; there is no network in the core
path. Typical operations (graph build, fingerprint, hash, replay-equivalence) complete in
sub-millisecond to low-millisecond time on commodity hardware. The full 779-test suite runs in
~54 s including coverage instrumentation. No allocation-heavy hot loops; `List.sort` uses
index-tiebreak comparators to match Python's stable `sorted` without extra passes.

---

## Testing

```bash
dart test
```

**793 tests** across crypto, determinism, graph, replay, memory, reconstruction, kernel,
browser, connectors, selector-healing, and the 12 ported runtime families
(`test/parity/`, `test/engines/`).
See [`TEST_INVENTORY.md`](TEST_INVENTORY.md) and [`TEST_VALIDATION_REPORT.md`](TEST_VALIDATION_REPORT.md).

---

## Coverage

```bash
dart test --coverage=coverage
dart pub global run coverage:format_coverage --lcov --in=coverage \
  --out=coverage/lcov.info --report-on=lib --packages=.dart_tool/package_config.json
```

**97.25%** line coverage (6374/6554). One file (`normalization.dart`, 85.71%) carries a single
unreachable Node-fallback line. Details: [`COVERAGE_VALIDATION_REPORT.md`](COVERAGE_VALIDATION_REPORT.md).

---

## CI/CD

GitHub Actions (`.github/workflows/dart.yml`, `.github/workflows/ci.yml`) gate every push:

| Gate | Command |
|------|---------|
| Format | `dart format --set-exit-if-changed .` |
| Analyze | `dart analyze` |
| Test | `dart test` |
| Coverage ≥ 90% | LCOV gate |
| Parity | `dart run validation/validate_parity.dart` |
| Publish | `dart pub publish --dry-run` |

See [`CI_VALIDATION_REPORT.md`](CI_VALIDATION_REPORT.md).

---

## Pub.dev Release

| Field | Value |
|-------|-------|
| Package | `webweavex` |
| Version | **2.0.1** (aligned with Python & JavaScript) |
| License | Apache-2.0 |
| Dry-run | `dart pub publish --dry-run` → 0 warnings (1 benign version hint) |

Release readiness: [`RELEASE_READINESS_REPORT.md`](RELEASE_READINESS_REPORT.md).

---

## Contributing

Contributions are welcome. Before opening a PR, run the full gate sequence:

```bash
dart format --set-exit-if-changed .
dart analyze
dart test
dart run validation/validate_parity.dart
dart pub publish --dry-run
```

Any new public API must ship with a cross-language hash-parity vector and test — parity is
**proven**, never assumed. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## OSS Governance

| Document | Purpose |
|----------|---------|
| [LICENSE](LICENSE) | Apache-2.0 |
| [GOVERNANCE.md](GOVERNANCE.md) | Decision-making model |
| [MAINTAINERS.md](MAINTAINERS.md) | Current maintainers |
| [CODEOWNERS](CODEOWNERS) | Review ownership |
| [RELEASE.md](RELEASE.md) | Release process |
| [SUPPORT.md](SUPPORT.md) | Getting help |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [ROADMAP.md](ROADMAP.md) | Direction |

---

## Security

Authorized session material only — no credential cracking, no CAPTCHA/auth bypass. Report
vulnerabilities per [SECURITY.md](SECURITY.md).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term: widen bounded extraction parity, expand examples and
benchmarks, deepen the semantic/query sub-path coverage toward Complete.

---

## Vision

WebWeaveX aims to make **operational runtime cognition** a portable, deterministic, cross-language
substrate — so that any human or AI agent, in Python, JavaScript, or Dart, can capture, replay,
reconstruct, and reason about authenticated software systems with identical, verifiable results.
Determinism is the contract; parity across languages is the proof.

---

## License

Apache 2.0 — [LICENSE](LICENSE)

<p align="center"><strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper.</strong></p>
