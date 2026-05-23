<p align="center">
  <strong>Deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
</p>

<p align="center">
  <a href="https://pub.dev/packages/webweavex"><img src="https://img.shields.io/pub/v/webweavex?style=flat-square" alt="pub"/></a>
  <img src="https://img.shields.io/badge/Dart-3.3%2B-0175C6?style=flat-square&logo=dart&logoColor=white" alt="Dart"/>
  <img src="https://img.shields.io/badge/parity-11%2F11-22c55e?style=flat-square" alt="Parity"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="License"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Coffee"/></a>
</p>

---

## What is WebWeaveX?

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** to understand, continue, reconstruct, replay, and reason about **authenticated operational software systems**.

This **`dart`** branch is the native **pub.dev** implementation — not a scraper, not an LLM wrapper, not AGI hype.

| Branch | Role |
|--------|------|
| [`main`](https://github.com/ni-sh-a-char/WebWeaveX) | Ecosystem portal |
| [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | **Canonical** PyPI runtime |
| [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | npm runtime |
| **`dart`** (this) | pub.dev runtime |

Spec: [CANONICAL_RUNTIME_SPEC.md](docs/architecture/CANONICAL_RUNTIME_SPEC.md) · Matrix: [ECOSYSTEM_MATRIX.md](docs/architecture/ECOSYSTEM_MATRIX.md)

---

## Humans and AI agents

**WebWeaveX is designed for both humans and AI agents.**

| Audience | Use |
|----------|-----|
| **Engineers** | Deterministic extraction, session continuation, replay audits |
| **AI agents** | Replay-safe memory, graph identity, operational continuity |

---

## Why AI agents need deterministic runtime infrastructure

| Problem | With WebWeaveX |
|---------|----------------|
| Ephemeral browser state | Stabilized DOM + runtime fingerprints |
| Auth drift | Encrypted session continuation (authorized credentials) |
| Nondeterministic replays | `validateReplayEquivalence` |
| Lost operational context | Runtime graphs + memory fabric |

---

## What WebWeaveX is NOT

| Not | Reality |
|-----|---------|
| Scraper / crawler | Operational runtime substrate |
| AGI product | Bounded deterministic pipelines |
| Auth / CAPTCHA bypass | No credential cracking |
| LLM wrapper | Native Dart library |

---

## Why existing systems fail

Traditional tools capture HTML, not **operational runtime state**. WebWeaveX provides canonical serialization, Kaalka-sealed sessions, replay equivalence, and reconstruction IDs.

---

## Runtime cognition

Replay-safe graphs, fingerprints, and memory hashes let humans and agents reason about **how software runs**, not only what HTML was returned.

---

## Runtime memory

```dart
final graph = buildRuntimeGraph({'session': {'authenticated': true}});
final runtime = {'unified_runtime_graph': graph.toJson()};
final memory = buildRuntimeMemory(graph);
final slice = queryRuntimeMemory(memory, 'graph');
```

---

## Replay equivalence

```dart
final report = validateReplayEquivalence(envelope, envelopeClone);
print(report['equivalent']); // true when checks pass
```

Checks: graph hash, global fingerprint, browser identity, DOM hash (when present), memory stable hash (when present).

---

## Runtime reconstruction

```dart
final rebuilt = reconstructRuntime(extraction: envelope);
print(rebuilt['runtime_id']);
```

---

## Authenticated runtime continuation

```dart
saveAuthenticatedRuntime('./session.json', {'cookies': []}, 'your-key');
final result = await extractWeb('https://example.com',
    authenticated: true, sessionPath: './session.json', encryptionKey: 'your-key');
```

**You** supply authorized credentials. No bypass tooling.

---

## Cross-language parity

```
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka._proc → base64
```

**11/11** vectors match JavaScript reference. **Honest:** NFKC uses Node.js when on PATH (matches V8 `String.normalize('NFKC')`).

```bash
dart run validation/validate_parity.dart
```

---

## Architecture

```text
Input → Canonical pipeline → Graph + Memory → Replay check → Reconstruction
              ↓
     Normalization + Kaalka v5 (pub.dev kaalka)
```

---

## Quick start (humans)

```yaml
dependencies:
  webweavex: ^2.0.0
  kaalka: ^5.0.0
```

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

## AI agent usage

```dart
final graph = buildRuntimeGraph({'agent_step': 'observe'});
final memory = buildRuntimeMemory(graph);
final agentView = queryRuntimeMemory(memory, 'graph');
final continuity = encryptValue({'checkpoint': agentView}, 'agent-session-key');
```

Agents use the **same deterministic substrate** as engineering teams.

---

## Determinism

| Layer | Mechanism |
|-------|-----------|
| Unicode | NFKC (Node when available) + CRLF→LF |
| Objects | Sorted keys, volatile field strip |
| Crypto | `kaalka@5.0.0` byte `_proc` + base64 |
| Graph | Sorted nodes/edges, `graphFingerprint` |

---

## Validation

```bash
dart format --set-exit-if-changed .
dart analyze
dart test
dart run validation/validate_parity.dart
dart run validation/validate_production.dart
dart pub publish --dry-run
```

| Gate | Path |
|------|------|
| Parity | `validation/parity/` |
| Replay | `validation/replay/` |
| Graph | `validation/runtime_graph/` |
| Memory | `validation/runtime_memory/` |
| Reconstruction | `validation/reconstruction/` |

---

## Security

Authorized session material only. See [SECURITY.md](SECURITY.md).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

---

## License

Apache 2.0 — [LICENSE](LICENSE)

<p align="center"><strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper.</strong></p>
