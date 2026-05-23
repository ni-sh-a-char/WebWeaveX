# WebWeaveX v2.0.0 — npm (JavaScript) Public Release

**Release date:** 2026-05-23  
**Branch:** [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript)  
**npm:** [`webweavex@2.0.0`](https://www.npmjs.com/package/webweavex)

---

## Summary

WebWeaveX **v2.0.0** on npm is **deterministic runtime cognition infrastructure** for **humans and AI agents** — browser-native extraction, replay-safe operational cognition, authenticated runtime continuation, and cross-language parity with the Python implementation via **`kaalka@5.0.0`**.

This is a **major** release over `0.1.0`: new architecture, new crypto pipeline, new positioning. It is **not** a scraper SDK or LLM wrapper.

---

## What it is

- Deterministic runtime substrate for operational web systems
- Playwright-integrated browser capture and DOM stabilization
- Replay equivalence, reconstruction, runtime memory, and execution fabric
- Encrypted session continuation when **you** supply authorized credentials

## What it is NOT

- AGI, auth bypass, CAPTCHA defeat, credential theft, or malware tooling

---

## Install

```bash
npm install webweavex@2.0.0
```

```js
import { extractWeb } from "webweavex";
```

Dual publish: **ESM** + **CJS** + TypeScript declarations (`sideEffects: false`).

---

## Validation (release gates)

| Gate | Result |
|------|--------|
| Tests | 45/45 pass |
| Coverage | 92.96% lines / 83.85% branches |
| Cross-language parity | 11/11 vectors (`kaalka@5.0.0`) |
| Production validation | PASS |
| Tarball | 9 files — `dist/`, `README.md`, `LICENSE` only |

---

## Crypto / parity

```
normalizeRuntimeValue → stableSerialize → deriveKaalkaTimeKey → UTF-8 → kaalka._proc → base64
```

Registry dependency: **`kaalka@5.0.0`** only (no local crypto fork).

---

## Ecosystem

| Branch | Role |
|--------|------|
| `main` | Language-neutral portal |
| `python` | PyPI implementation |
| `javascript` | npm implementation (this release) |

---

## Links

- [README (javascript)](https://github.com/ni-sh-a-char/WebWeaveX/blob/javascript/README.md)
- [Parity spec](https://github.com/ni-sh-a-char/WebWeaveX/blob/javascript/docs/architecture/CROSS_LANGUAGE_PARITY.md)
- [SECURITY.md](https://github.com/ni-sh-a-char/WebWeaveX/blob/javascript/SECURITY.md)
- [Buy Me a Coffee](https://buymeacoffee.com/piyushmishra00)

**License:** Apache 2.0
