<p align="center">
  <br/>
  <img src="https://img.shields.io/badge/WebWeaveX-v3.0.0-0f172a?style=for-the-badge&logo=dart&logoColor=white" alt="WebWeaveX v3.0.0"/>
  <br/><br/>
  <strong>Production-grade deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
  <br/>
  <em>Operational runtime substrate · pub.dev · replay-safe · Kaalka v5 parity</em>
  <br/><br/>
</p>

<p align="center">
  <a href="https://pub.dev/packages/webweavex"><img src="https://img.shields.io/pub/v/webweavex?style=flat-square&logo=dart&logoColor=white" alt="pub.dev version"/></a>
  <img src="https://img.shields.io/badge/Dart-3.3%2B-0175C6?style=flat-square&logo=dart&logoColor=white" alt="Dart 3.3+"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/></a>
  <img src="https://img.shields.io/badge/tests-543%20passing-22c55e?style=flat-square" alt="Tests passing"/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?style=flat-square" alt="Build passing"/>
  <img src="https://img.shields.io/badge/deterministic%20runtime-0ea5e9?style=flat-square" alt="Deterministic runtime"/>
  <img src="https://img.shields.io/badge/replay--safe-14b8a6?style=flat-square" alt="Replay-safe"/>
  <img src="https://img.shields.io/badge/Kaalka-verified-7c3aed?style=flat-square" alt="Kaalka verified"/>
  <img src="https://img.shields.io/badge/production%20ready-15803d?style=flat-square" alt="Production ready"/>
  <img src="https://img.shields.io/badge/OSS-infrastructure-64748b?style=flat-square" alt="Open Source"/>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20WebWeaveX-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

---

## Table of Contents

- [Why WebWeaveX exists](#why-webweavex-exists)
- [What makes it different](#what-makes-it-different)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Five-Minute Tour](#five-minute-tour)
- [Examples](#examples)
- [Determinism](#determinism)
- [Cross-Language Parity](#cross-language-parity)
- [Performance](#performance)
- [Comparison](#comparison)
- [Use Cases](#use-cases)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Security](#security-model)
- [License](#license)

---

## Why WebWeaveX exists

Modern software is authenticated, stateful, SPA-based, and operationally dynamic. Traditional extraction captures HTML snapshots. WebWeaveX captures **how software actually runs** — browser DOM, sessions, workflows, and knowledge graphs — and compiles it into **deterministic, replayable, fingerprintable runtime graphs**.

> **WebWeaveX is to runtime state what Git is to source code: deterministic, replayable, reconstructable, and auditable.**

| Failure Mode | Traditional Approach | WebWeaveX |
|--------------|---------------------|-----------|
| Ephemeral browser state | Re-scrape | Stabilized DOM + fingerprints |
| Auth drift | Re-login | Encrypted session continuation |
| Nondeterministic replays | Hope for the best | `validateReplayEquivalence` |
| Lost operational context | Start over | Runtime graphs + memory fabric |
| Cross-run reasoning breaks | Ephemeral DOM | Stable hashes + parity-validated crypto |

---

## What makes it different

WebWeaveX is not a scraping library or LLM wrapper. It is a **deterministic runtime cognition substrate**.

| Category | Focus |
|----------|-------|
| Browser automation | Execute actions (Playwright, Puppeteer) |
| Web scraping | Extract content (Scrapy, BeautifulSoup) |
| Agent orchestration | Coordinate reasoning (LangChain, CrewAI) |
| **Runtime cognition infrastructure** | **Preserve operational runtime state** |

Key differentiators:

- **Deterministic output** — same input always produces byte-identical output
- **Kaalka v5 encryption** — cross-language verified cryptographic persistence
- **Replay equivalence** — prove two runtime states are operationally identical
- **Cross-language parity** — Python, JavaScript, Dart share identical contracts
- **12 runtime-cognition families** — causality, semantic, workflows, execution, and more

---

## Architecture

```text
Input → Canonical Pipeline → Graph + Memory → Replay Check → Reconstruction
                 ↓
        Normalization + Kaalka v5
```

Layered source layout (`lib/src/`):

| Layer | Packages |
|-------|----------|
| crypto | `kaalka_runtime`, `kaalka_v5_proc`, `time_key`, `hashing` |
| determinism | `normalization`, `dom_stabilization`, `fingerprint`, `stable_serialize` |
| graph | `runtime_graph`, `runtime_graph_replay`, `runtime_graph_reconstruction` |
| kernel | `runtime_pipeline`, `replay_pipeline`, `reconstruction_pipeline`, `kernel_runtime` |
| memory | `runtime_memory`, `runtime_memory_graph`, `memory_lineage`, `memory_replay`, `query_memory` |
| replay | `replay_runtime`, `replay_graph`, `replay_memory`, `replay_dom`, `replay_fingerprint`, `replay_equivalence` |
| reconstruction | `reconstruct_runtime`, `reconstruct_graph`, `reconstruct_memory`, `reconstruct_replay`, `reconstruct_browser` |
| browser | `extract_web`, `render_page`, `runtime_session`, `authenticated_runtime`, `spa_stabilizer` |
| families | `causality`, `semantic`, `synchronization`, `evolution`, `workflows`, `execution`, `query`, `connectors`, `persistence`, `distributed`, `orchestration` |

---

## Features

| Feature | Description |
|---------|-------------|
| **Deterministic core** | `normalizeRuntimeValue → stableSerialize → UTF-8 → Kaalka v5 → base64` — byte-identical to Python and JavaScript |
| **Runtime graphs** | Sorted, fingerprinted node/edge graphs (`buildRuntimeGraph`, `graphFingerprint`) |
| **Runtime memory** | Build, query, search, and lineage-track operational memory |
| **Replay equivalence** | Prove two runtime envelopes are operationally identical |
| **Reconstruction** | Rebuild deterministic runtime identities from extraction envelopes |
| **Authenticated continuation** | Kaalka-encrypted session save/load (you supply credentials) |
| **12 runtime-cognition families** | Causality, semantic, synchronization, evolution, workflows, execution, and more |
| **Cross-language parity** | 11/11 core + ~145 runtime-API hash vectors verified |
| **Graph intelligence** | Deterministic traversal, fingerprinting, and query |

---

## Installation

```bash
dart pub add webweavex
```

Or add to `pubspec.yaml`:

```yaml
dependencies:
  webweavex: ^3.0.0
  kaalka: ^5.0.0
```

Requires Dart SDK `>=3.3.0 <4.0.0`.

---

## Quick Start

```dart
import 'package:webweavex/webweavex.dart';

Future<void> main() async {
  // Deterministic hash
  final hash = computeDeterministicHash({'status': 'ok'});
  print('Hash: $hash');

  // Build a runtime graph
  final graph = buildRuntimeGraph({'session': {'authenticated': true}});
  final fp = graphFingerprint(graph);
  print('Fingerprint: $fp');

  // Validate replay equivalence
  final report = validateReplayEquivalence(
    {'unified_runtime_graph': graph.toJson()},
    {'unified_runtime_graph': graph.toJson()},
  );
  print('Equivalent: ${report['equivalent']}');
}
```

---

## Five-Minute Tour

### 1. Extract content

```dart
final result = await extractWeb('https://example.com');
print(result['kind']);              // extraction kind
print(result['deterministic_hash']);
```

### 2. Build a runtime graph

```dart
final graph = buildRuntimeGraph({'agent_step': 'observe'});
final fp = graphFingerprint(graph);
print('Graph fingerprint: $fp');
```

### 3. Store runtime memory

```dart
final memory = buildRuntimeMemory(
  runtimeHistory: [{'tick': 1, 'kind': 'workflow'}],
  lineage: [{'id': 'a'}],
  semanticRelations: [{'from': 'a', 'to': 'b'}],
);
final found = queryRuntimeMemory(memory, 'semantic', 'a');
```

### 4. Validate replay

```dart
final report = validateReplayEquivalence(envelope, envelopeClone);
print(report['equivalent']); // true when checks pass
```

### 5. Reconstruct runtime

```dart
final rebuilt = reconstructRuntime(extraction: envelope);
print(rebuilt['runtime_id']);
```

### 6. Execute a workflow

```dart
final plan = buildWorkflowPlan({'objective': 'extract-and-verify'});
final run = runAutonomousWorkflow(plan);
final replay = replayWorkflowRuntime(run);
```

---

## Examples

### AI Agent Runtime Continuity

```dart
final graph = buildRuntimeGraph({'agent_step': 'observe'});
final fabric = buildRuntimeMemoryFabric(graph);
final agentView = queryRuntimeMemoryFabric(fabric, 'graph');
final continuity = encryptValue({'checkpoint': agentView}, 'agent-session-key');
```

### Authenticated Session Continuation

```dart
saveAuthenticatedRuntime('./session.json', {'cookies': []}, 'your-key');
final result = await extractWeb(
  'https://example.com',
  authenticated: true,
  sessionPath: './session.json',
  encryptionKey: 'your-key',
);
```

### Repository Intelligence

```dart
final repo = queryRepository(source: 'my-project');
final graph = queryGraph(source: 'my-project');
final docs = queryDocuments(text: '...document text...');
```

### Application Cognition

```dart
final app = runApplicationCognition('https://app.example.com', '<html>...</html>');
```

Full runnable examples: [`example/`](example/)

---

## Determinism

Every WebWeaveX operation is deterministic:

```text
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka._proc → base64
```

| Layer | Mechanism |
|-------|-----------|
| Unicode | NFKC normalization + CRLF → LF |
| Objects | Sorted keys, volatile field strip |
| Crypto | Kaalka v5 byte `_proc` + base64 |
| Graph | Sorted nodes/edges, `graphFingerprint` |

**Verified across 1000 iterations** — bit-identical output for:

| Mechanism | Status |
|-----------|:------:|
| `stableSerialize` | Byte-identical |
| `normalizeRuntimeValue` | Byte-identical |
| `graphFingerprint` | Byte-identical |
| `computeRuntimePipelineFingerprint` | Byte-identical |
| `validateReplayEquivalence` | Byte-identical |
| `computeGlobalRuntimeFingerprint` | Byte-identical |

---

## Cross-Language Parity

Dart, Python, and JavaScript share byte-identical deterministic contracts:

| Proof | Scale | Result |
|-------|-------|--------|
| Core determinism | 10k vectors x 3 runs x 3 languages | 60,001/60,001 byte-identical |
| Extraction | 10k synthetic + 1,006 real pages + 14 torture | 3-way PASS |
| Semantic IR | 667 fixtures, ~300 engines | 3-way hash + deep equality |
| Million-vector battery | 1,000,000 vectors across 5 IR families | Single aggregate digest, identical in all 3 |

```bash
dart run validation/validate_parity.dart   # crossLangMatch: true
```

---

## Performance

WebWeaveX is CPU-bound deterministic serialization + hashing with no network in the core path.

| Operation | Typical Latency |
|-----------|:---------------:|
| Graph build | <1ms |
| Fingerprint | <1ms |
| Stable serialize | <1ms |
| Replay equivalence | <5ms |
| Full 543-test suite | ~10s |

No allocation-heavy hot loops. `List.sort` uses index-tiebreak comparators for stable ordering.

---

## Comparison

| Tool | Focus | Deterministic | Replay | Knowledge Graph | Memory | Cross-Language |
|------|-------|:------------:|:------:|:---------------:|:------:|:--------------:|
| Playwright | Browser automation | No | No | No | No | Multi |
| Puppeteer | Browser automation | No | No | No | No | JS only |
| BeautifulSoup | HTML parsing | No | No | No | No | Python |
| Cheerio | HTML parsing | No | No | No | No | JS |
| Selenium | Browser automation | No | No | No | No | Multi |
| Firecrawl | Web extraction | No | No | No | No | API |
| Crawl4AI | Web extraction | No | No | No | No | Python |
| Browserbase | Browser infrastructure | No | No | No | No | API |
| **WebWeaveX** | **Runtime cognition** | **Yes** | **Yes** | **Yes** | **Yes** | **3 languages** |

WebWeaveX does not replace these tools. It provides deterministic runtime infrastructure that can sit beneath them.

---

## Use Cases

| Use Case | How WebWeaveX Helps |
|----------|-------------------|
| **AI Agent Memory** | Replay-safe memory fabric with deterministic fingerprints |
| **Compliance Auditing** | Deterministic replay of operational states |
| **Documentation Indexing** | Repository analysis with knowledge graphs |
| **Browser Automation** | Stabilized DOM with SPA support |
| **Enterprise Search** | Query across runtime graphs and memory |
| **Knowledge Graphs** | Build entity-relationship graphs from any source |
| **Repository Understanding** | Dependency analysis, language detection, architecture extraction |
| **Research** | Deterministic extraction for reproducible research |
| **Data Preservation** | Encrypted, replayable operational state |
| **Offline Replay** | Continue operations from saved state |
| **LLM Preprocessing** | Structured IR for language model context |
| **Agent Continuity** | Maintain state across agent sessions |

---

## FAQ

**What is Kaalka?**

Kaalka is a deterministic cryptographic persistence substrate. `kaalka@5.0.0` provides byte-identical encrypted values across Python, JavaScript, and Dart implementations.

**Why deterministic?**

Determinism enables audit, replay proofs, cross-run diffing, and agent continuity. Without it, operational systems cannot be trusted as engineering substrates.

**Why replay?**

Replay proves two runtime states are operationally identical — not just visually similar, but cryptographically equivalent. This is essential for auditing, debugging, and agent memory.

**Does this replace Playwright?**

No. WebWeaveX provides deterministic runtime infrastructure. Playwright provides browser automation. They serve different purposes and can work together.

**Does this replace Selenium?**

Same answer. Selenium automates browsers. WebWeaveX captures and replays operational state.

**Can it crawl SPAs?**

The browser layer supports SPA stabilization via `spa_stabilizer.dart`. Live-browser capabilities (infinite scroll, DevTools frames) are platform-deferred.

**Can it extract repositories?**

Yes. `queryRepository`, `queryGraph`, and the `repository_engines` subsystem provide dependency analysis, language detection, and architecture extraction.

**How is this different from scraping?**

Scraping captures HTML. WebWeaveX captures operational runtime state — DOM, sessions, workflows, memory, and knowledge graphs — in a deterministic, replayable, fingerprintable format.

**Can AI agents use this?**

Yes. Every output is a bounded, deterministic, evidence-carrying IR that agents can hash, diff, replay, and reason over. See [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Near-term: widen bounded extraction parity, expand examples and benchmarks, deepen semantic/query sub-path coverage.

---

## Contributing

Before opening a PR, run the full gate sequence:

```bash
dart format --set-exit-if-changed .
dart analyze
dart test
dart run validation/validate_parity.dart
dart pub publish --dry-run
```

Any new public API must ship with a cross-language hash-parity vector and test — parity is **proven**, never assumed.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## Security Model

| Control | Implementation |
|---------|----------------|
| No arbitrary eval | Deterministic execution paths only |
| Bounded extraction | Configurable limits on all extraction |
| Encrypted persistence | Kaalka v5 only |
| No auth bypass | Authorized credentials required |

See [SECURITY.md](SECURITY.md). Report issues responsibly.

---

## License

Apache License 2.0 — [LICENSE](LICENSE)

---

<p align="center">
  <strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper, not AGI hype, not an LLM wrapper.</strong>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-piyushmishra00-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>
