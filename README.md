<p align="center">
  <strong>Deterministic runtime cognition infrastructure<br/>for humans and AI agents · Dart native</strong>
</p>

<p align="center">
  <a href="https://pub.dev/packages/webweavex"><img src="https://img.shields.io/pub/v/webweavex?style=flat-square" alt="pub version"/></a>
  <img src="https://img.shields.io/badge/Dart-3.3%2B-0175C2?style=flat-square&logo=dart&logoColor=white" alt="Dart"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/parity-11%2F11-22c55e?style=flat-square" alt="Parity"/>
  <img src="https://img.shields.io/badge/deterministic-runtime-0f172a?style=flat-square" alt="Deterministic"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

---

## Hero

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** to understand, continue, reconstruct, replay, and reason about **authenticated operational software systems**.

This **`dart`** branch is the **native pub.dev implementation** — not a scraper, not an LLM wrapper, not AGI hype.

| Branch | Role |
|--------|------|
| [`main`](https://github.com/ni-sh-a-char/WebWeaveX) | Ecosystem portal |
| [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | PyPI runtime |
| [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | npm runtime |
| **`dart`** (this) | pub.dev runtime |

---

## What WebWeaveX is

- Runtime cognition infrastructure for operational systems
- Deterministic extraction, hashing, encryption, replay
- Authenticated runtime continuation (authorized credentials only)
- Cross-language parity with JavaScript and Python (`kaalka@5.0.0`)
- Replay-safe runtime memory and reconstruction

## What WebWeaveX is NOT

| Not | Reality |
|-----|---------|
| Scraper / crawler toy | Operational runtime substrate |
| AGI product | Bounded deterministic pipelines |
| Auth / CAPTCHA bypass | No credential cracking |
| LLM wrapper | Native Dart runtime library |

---

## Humans and AI agents

| Audience | Use |
|----------|-----|
| **Engineers** | Deterministic hashes, session continuation, runtime graphs |
| **Dart / Flutter agents** | Replay-safe memory, stable serialization, parity proofs |

---

## Cross-language parity

```
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka._proc → base64
```

**Verified:** 11/11 vectors against JavaScript reference (`validation/validate_parity.dart`).

**Honest requirement:** NFKC normalization uses Node.js when available (matches `String.normalize('NFKC')` in JavaScript). CRLF normalization always applies in pure Dart.

```bash
dart run validation/validate_parity.dart
```

Spec: [`docs/architecture/CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md)

---

## Quick start

```yaml
dependencies:
  webweavex: ^2.0.0
  kaalka: ^5.0.0
```

```dart
import 'package:webweavex/webweavex.dart';

void main() {
  final hash = computeDeterministicHash({'status': 'ok'});
  final enc = encryptValue({'session': true}, 'my-key');
  final dec = decryptValue(enc, 'my-key');
  print('$hash $dec');
}
```

---

## Validation

```bash
dart format --set-exit-if-changed .
dart analyze
dart test
dart run validation/validate_parity.dart
dart pub publish --dry-run
```

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

<p align="center">
  <strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper.</strong>
</p>
