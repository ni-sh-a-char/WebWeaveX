<p align="center">
  <br/>
  <img src="https://img.shields.io/badge/WebWeaveX-v2.0.0-0f172a?style=for-the-badge&logo=javascript&logoColor=white" alt="WebWeaveX"/>
  <br/><br/>
  <strong>Deterministic runtime extraction and replay infrastructure for authenticated operational systems</strong>
  <br/>
  <em>Native TypeScript · Node.js 18+ · <a href="https://www.npmjs.com/package/kaalka">kaalka@5.0.0</a></em>
  <br/><br/>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/webweavex"><img src="https://img.shields.io/npm/v/webweavex?style=flat-square&logo=npm" alt="npm version"/></a>
  <a href="https://www.npmjs.com/package/webweavex"><img src="https://img.shields.io/npm/dm/webweavex?style=flat-square&logo=npm" alt="npm downloads"/></a>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/>
  <img src="https://img.shields.io/badge/coverage-90%25%2B-22c55e?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/Node-18+-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+"/>
  <img src="https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/CI-passing-22c55e?style=flat-square" alt="CI"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

---

## 1. What is WebWeaveX?

**WebWeaveX** is **deterministic runtime extraction and replay infrastructure** for authenticated operational systems. It captures how web applications actually run—DOM, graphs, memory, workflows—and produces **replay-safe, auditable runtime artifacts** with cryptographic continuity via **[Kaalka](https://www.npmjs.com/package/kaalka)**.

| Branch | Role |
|--------|------|
| [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | Native npm package (this branch) |
| [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | PyPI implementation |
| [`main`](https://github.com/ni-sh-a-char/WebWeaveX) | Language-neutral portal |

---

## 2. What WebWeaveX is NOT

| Not | Why |
|-----|-----|
| AGI or autonomous hacking | Bounded, deterministic pipelines only |
| CAPTCHA bypass | No bot-defense circumvention |
| Credential cracking | No password/MFA attacks |
| Auth bypass tooling | No login-wall breaking |
| Malware / botnets | Engineering infrastructure for authorized use |
| “Magic” universal extraction | Requires legitimate session material you supply |

---

## 3. Why existing systems fail

| Approach | Failure mode |
|----------|----------------|
| HTML-only parsers | No live runtime state |
| Stateless crawlers | Auth discontinuity after login |
| Raw Playwright/Puppeteer | No unified IR, replay proofs, or crypto fabric |
| Probabilistic AI agents | Non-reproducible runs |
| Unstabilized SPAs | DOM/hash drift breaks replay |

---

## 4. Core features

- **Authenticated runtime continuation** — encrypt and reload session state you authorize  
- **Deterministic replay** — graph + fingerprint + stabilized DOM equivalence  
- **DOM stabilization** — strip framework noise, nonces, volatile scripts  
- **Runtime graphs** — canonical node/edge ordering  
- **Reconstruction** — bounded topology rebuild from IR  
- **Runtime memory fabric** — merge and hash federated memories  
- **Execution runtime** — allowlisted action sandbox  
- **Cross-language formula** — documented in [`docs/architecture/CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md)

---

## 5. Authenticated runtime continuation

WebWeaveX can **continue authenticated sessions only when valid user-authorized credentials, cookies, tokens, or session state are supplied** by you.

```ts
import { saveAuthenticatedRuntime, loadAuthenticatedRuntime, extractWeb } from "webweavex";

saveAuthenticatedRuntime("./session.kaalka", { cookies: [], headers: {} }, "your-encryption-key");

const result = await extractWeb("https://app.example.com", {
  authenticated: true,
  sessionPath: "./session.kaalka",
  encryptionKey: "your-encryption-key",
});
```

**Explicit:** no auth bypass · no credential cracking · no CAPTCHA solving claims.

---

## 6. Cross-language determinism

WebWeaveX **owns normalization**. [Kaalka `5.0.0`](https://www.npmjs.com/package/kaalka) is **only** the crypto substrate from npm.

```text
normalizeRuntimeValue
  → stableSerialize
  → UTF-8 (Buffer.from(..., "utf8"))
  → deriveKaalkaTimeKey(key)   # pure SHA-256, no system clock
  → kaalka@5._proc(bytes)
  → base64
```

**Honest parity statement:** identical ciphertext across Python and JavaScript requires **the same formula** on both branches. Legacy Python `kaalka_runtime_engine` (v2 byte-XOR + hex) does **not** match until migrated to this spec. See `npm run validate:parity`.

---

## 7. Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Browser   │────▶│ Canonical Pipeline│────▶│  Runtime Graph  │
│ (Playwright)│     │  + DOM stabilize  │     │  + Fingerprints │
└─────────────┘     └────────┬─────────┘     └────────┬────────┘
                             │                        │
                    ┌────────▼────────┐        ┌───────▼────────┐
                    │ Memory / Replay │        │ Reconstruction │
                    │ + Execution IR  │        │ + Kaalka crypto│
                    └─────────────────┘        └────────────────┘
```

---

## 8. Quick start

```bash
git clone https://github.com/ni-sh-a-char/WebWeaveX.git
git checkout javascript
npm ci
npx playwright install chromium
npm run build
npm test
```

```bash
npm install webweavex
```

```ts
import { extractWeb, computeDeterministicHash } from "webweavex";

const out = await extractWeb("https://example.com");
console.log(out.bounded, out.global_runtime_fingerprint);
console.log(computeDeterministicHash({ ok: true }));
```

---

## 9. Real examples

<details>
<summary>Replay validation</summary>

```ts
import { runCanonicalPipeline, validateReplayEquivalence } from "webweavex";

const pipe = await runCanonicalPipeline({ source: "https://example.com", sourceType: "web" });
console.log(validateReplayEquivalence(pipe, structuredClone(pipe)).equivalent);
```

</details>

<details>
<summary>Deterministic hashing & Kaalka encrypt</summary>

```ts
import { encryptValue, decryptValue, deriveKaalkaTimeKey } from "webweavex";

const enc = encryptValue({ probe: 1 }, "my-key");
console.log(deriveKaalkaTimeKey("my-key")); // H:MM:SS — deterministic
console.log(decryptValue(enc.encrypted, "my-key").decrypted);
```

</details>

<details>
<summary>Runtime memory</summary>

```ts
import { buildRuntimeMemory, stableMemoryHash } from "webweavex";

const mem = buildRuntimeMemory({ events: [{ type: "navigate" }] });
console.log(stableMemoryHash(mem));
```

</details>

---

## 10. Validation

| Command | Purpose |
|---------|---------|
| `npm test` | Vitest unit + integration suites |
| `npm run coverage` | ≥90% lines, ≥80% branches on `src/` |
| `npm run validate:parity` | Cross-language vector harness |
| `npm run validate` | Real-world smoke validation |
| `npm pack --dry-run` | npm publish readiness |

Reports: `validation/parity/parity_report.md`, `FINAL_*_REPORT.md` (generated via `npm run reports:final`).

---

## 11. Security model

- **No arbitrary `eval`** in production paths  
- **Allowlisted** execution actions (`runExecutionRuntime`)  
- **Kaalka-encrypted** session files when persistence is enabled  
- **Deterministic, bounded** pipelines — failures degrade safely  

See [SECURITY.md](SECURITY.md).

---

## 12. OSS & governance

| Document | Link |
|----------|------|
| License | [Apache 2.0](LICENSE) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Code of conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Security | [SECURITY.md](SECURITY.md) |
| Roadmap | [ROADMAP.md](ROADMAP.md) |
| Funding | [Buy Me a Coffee](https://buymeacoffee.com/piyushmishra00) |

---

## 13. Repository structure

```
src/                 # Production runtime (kernel, browser, crypto, replay, …)
docs/architecture/   # Cross-language parity spec
validation/parity/   # JS/Python vector harness
tests/               # Vitest (scoped coverage on src/)
examples/            # Runnable samples
.github/             # CI, issue/PR templates, FUNDING.yml
```

**Not included:** local `packages/kaalka` clones — only registry `kaalka@5.0.0`.

---

## 14. Final positioning

**WebWeaveX is deterministic runtime cognition infrastructure — not a disposable web scraper.**

It gives engineering teams **replay-safe operational continuity** across authenticated systems, with cryptographic persistence and honest cross-language contracts.

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-piyushmishra00-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/piyushmishra00)
