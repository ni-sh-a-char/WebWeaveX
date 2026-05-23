<p align="center">
  <img src="https://img.shields.io/badge/WebWeaveX-2.0.0-0f172a?style=for-the-badge&labelColor=1e293b" alt="WebWeaveX"/>
</p>

<p align="center">
  <strong>Deterministic runtime cognition infrastructure<br/>for humans and AI agents · browser &amp; Playwright native</strong>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/webweavex"><img src="https://img.shields.io/npm/v/webweavex?style=flat-square&logo=npm&label=version" alt="npm version"/></a>
  <a href="https://www.npmjs.com/package/webweavex"><img src="https://img.shields.io/npm/dm/webweavex?style=flat-square&logo=npm&label=downloads" alt="npm downloads"/></a>
  <img src="https://img.shields.io/badge/Node-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node.js"/>
  <img src="https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/coverage-90%25%2B-22c55e?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/CI-javascript-22c55e?style=flat-square&logo=githubactions&logoColor=white" alt="CI"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="License"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

<p align="center">
  <a href="#installation">Install</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#cross-language-determinism">Determinism</a> ·
  <a href="#validation">Validation</a> ·
  <a href="docs/architecture/CROSS_LANGUAGE_PARITY.md">Parity spec</a>
</p>

---

## What is WebWeaveX?

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** on the operational web. It captures browser runtime behavior—DOM, graphs, memory, workflows—and produces **replay-safe** artifacts you can audit, hash, and continue across authenticated sessions.

This npm package is **not** a crawler toolkit or LLM wrapper. It is **browser-native operational runtime infrastructure** with Playwright integration.

| Capability | Description |
|------------|-------------|
| **Authenticated runtime continuation** | Resume sessions when *you* supply valid cookies/tokens |
| **Replay-safe extraction** | Stable fingerprints, not one-off HTML dumps |
| **Runtime graphs** | Canonical node/edge ordering for operational topology |
| **Reconstruction** | Bounded rebuild from unified IR |
| **DOM / SPA stabilization** | Framework noise stripped before hashing |
| **Kaalka crypto fabric** | Registry [`kaalka@5.0.0`](https://www.npmjs.com/package/kaalka) + WebWeaveX normalization |

**Branch:** [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) (this package) · [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) · [`main`](https://github.com/ni-sh-a-char/WebWeaveX) portal

### Why this exists

Modern operational systems fail when:

- tools are **stateless** after login  
- SPAs change DOM on every render  
- replay cannot prove **equivalence** across runs  
- teams lack a **single canonical pipeline** for runtime IR  

WebWeaveX addresses extraction, stabilization, hashing, encryption, and replay in one native TypeScript runtime.

---

## What WebWeaveX is NOT

| Not | Reality |
|-----|---------|
| AGI / autonomous hacking | Deterministic, bounded pipelines |
| CAPTCHA bypass | No bot-defense circumvention |
| Auth bypass | No credential cracking or MFA defeat |
| Malware / spyware | OSS infrastructure for authorized engineering |
| Browser exploitation | Playwright-based extraction you control |
| “Magic” universal extraction | Requires legitimate session material |

---

## Humans and AI agents

**WebWeaveX is designed for both humans and AI agents.**

| Audience | Use |
|----------|-----|
| **Engineers** | Debug SPAs, stabilize DOM, audit authenticated flows |
| **Browser AI agents** | Deterministic Playwright continuity, replay-safe memory, operational graphs |

Same APIs, same determinism contract, same honesty about authorization.

---

## Runtime cognition

**Runtime cognition** means treating the live operational environment (DOM, session, graph, memory) as a **bounded, hashable, replayable** artifact—not a one-off screenshot. WebWeaveX compiles that artifact through a single canonical pipeline so humans and agents can **continue**, **audit**, and **prove equivalence** across ticks.

---

## Why AI agents need deterministic runtime infrastructure

| Problem | Without substrate | With WebWeaveX |
|---------|-------------------|----------------|
| Auth loss | Re-login every step | `saveAuthenticatedRuntime` / `loadAuthenticatedRuntime` |
| State drift | Cookies/storage diverge | Kaalka-sealed session blobs |
| DOM instability | Framework IDs break diffs | `stabilizeDomHtml` + `computeStableDomHash` |
| Replay inconsistency | Same prompt, different hash | `validateReplayEquivalence` (graph + fingerprint + DOM + memory) |
| Ephemeral memory | No operational graph | `buildRuntimeMemory` / `queryRuntimeMemory` |

### AI agent memory

```ts
import { buildRuntimeGraph, buildRuntimeMemory, queryRuntimeMemory } from "webweavex";

const graph = buildRuntimeGraph({ step: "login", next: "dashboard" });
const runtime = buildRuntimeMemory(graph, [{ step: "login" }]);
const memory = queryRuntimeMemory(runtime, "graph");
```

### Replay equivalence

```ts
import { validateReplayEquivalence } from "webweavex";

const a = await runCanonicalPipeline({ source: "https://example.com", sourceType: "web" });
const b = structuredClone(a);
const replay = validateReplayEquivalence(a, b);
console.log(replay.equivalent, replay.checks);
```

### Runtime reconstruction

```ts
import { reconstructRuntime, rebuildExecutionGraph } from "webweavex";

const rebuilt = reconstructRuntime({ extraction: pipeline });
const graph = rebuildExecutionGraph(pipeline);
console.log(rebuilt.runtime, graph.nodes.length);
```

### Human workflows

```ts
import { extractWeb, validateReplayEquivalence, buildRuntimeGraph } from "webweavex";

const extraction = await extractWeb("https://app.example.com");
const graph = buildRuntimeGraph(extraction);
console.log(validateReplayEquivalence(extraction, structuredClone(extraction)).equivalent);
```

---

## Runtime memory

Runtime memory is a **bounded graph + history fabric** with deterministic `stable_hash` for replay continuity.

| API | Role |
|-----|------|
| `buildRuntimeMemory` | Compile graph + history into memory envelope |
| `stableMemoryHash` | Deterministic memory fingerprint |
| `mergeRuntimeMemories` | Federate bounded histories |
| `queryRuntimeMemory` | Keyed lookup for agents (`graph`, `runtime_history`, …) |

---

## Replay equivalence

Replay is not string diff. WebWeaveX checks **graph fingerprint**, **global runtime fingerprint**, **stabilized DOM hash**, **semantic fingerprint**, and **memory stable hash** when present.

```ts
validateReplayEquivalence(original, candidate);
```

---

## Runtime reconstruction

Reconstruction rebuilds **runtime identity**, **normalized graph**, and **bounded** flags from unified extraction IR—deterministic across identical inputs.

```ts
reconstructRuntime({ extraction });
replayRuntime(extraction);
rebuildExecutionGraph(extraction);
```

---

## Why browser AI agents fail today

| Failure | Symptom |
|---------|---------|
| Auth loss | Agent re-authenticates unpredictably |
| State drift | Cookies/storage diverge across steps |
| DOM instability | Framework IDs break comparisons |
| Replay inconsistency | Same prompt, different runtime hash |
| Ephemeral memory | No federated runtime graph |

**WebWeaveX introduces:**

- stabilized runtime identity (`computeStableDomHash`, `stabilizeDomHtml`)  
- deterministic DOM normalization  
- replay equivalence (`validateReplayEquivalence`)  
- authenticated runtime continuation (authorized credentials only)  
- runtime memory fabric (`buildRuntimeMemory`, `stableMemoryHash`)  

---

## Why existing systems fail

| Problem | Raw automation / agents | WebWeaveX |
|---------|---------------------|-----------|
| Auth continuity | ❌ Lost after login | ✅ Encrypted session continuation |
| Replay determinism | ❌ Brittle snapshots | ✅ Graph + fingerprint equivalence |
| SPA stabilization | ❌ Volatile DOM IDs | ✅ Stabilized DOM hashing |
| Runtime reconstruction | ❌ None | ✅ IR-driven rebuild |
| Memory / workflow graphs | ❌ Ad hoc | ✅ Federated runtime memory |
| Replay equivalence proofs | ❌ String diff only | ✅ Semantic + DOM + graph checks |

---

## Core capabilities

- `extractWeb()` — bounded browser extraction  
- `runCanonicalPipeline()` — single orchestration path  
- `validateReplayEquivalence()` — graph, fingerprint, DOM hash  
- `saveAuthenticatedRuntime()` / `loadAuthenticatedRuntime()` — Kaalka-encrypted sessions  
- `buildRuntimeGraph()` / `graphFingerprint()` — operational graphs  
- `buildRuntimeMemory()` / `mergeRuntimeMemories()` — memory fabric  
- `reconstructRuntime()` / `replayRuntime()` — reconstruction layer  
- `runExecutionRuntime()` — allowlisted execution sandbox  
- `computeDeterministicHash()` — SHA-256 over canonical serialization  

---

## Authenticated runtime continuation

WebWeaveX can **continue authenticated sessions only when valid user-authorized credentials, cookies, tokens, or session state are supplied.**

```ts
import { saveAuthenticatedRuntime, extractWeb } from "webweavex";

await saveAuthenticatedRuntime(
  "./session.kaalka",
  { cookies: [], headers: { authorization: "Bearer <your-token>" } },
  "your-encryption-key",
);

const result = await extractWeb("https://app.example.com", {
  authenticated: true,
  sessionPath: "./session.kaalka",
  encryptionKey: "your-encryption-key",
});
```

**No auth bypass · no CAPTCHA bypass · no credential cracking.**

---

## Cross-language determinism

WebWeaveX owns **normalization, serialization, UTF-8 encoding, and replay stabilization**. [Kaalka](https://www.npmjs.com/package/kaalka) is the **crypto substrate only** (`kaalka@5.0.0`, exact pin).

```text
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka._proc → base64
```

**Truthful parity statement**

> Cross-language **runtime normalization and replay parity** are implemented and documented.  
> **Full ciphertext parity** depends on matching crypto substrates across runtime implementations.  
> The Python branch must adopt [`docs/architecture/CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md) for byte-identical encrypt output.

```bash
npm run validate:parity
```

---

## Architecture

```text
                    ┌─────────────────────────────────────────┐
                    │           Universal Input               │
                    └────────────────────┬────────────────────┘
                                         ▼
┌──────────────┐   ┌──────────────────────────────────────────────────┐
│   Browser    │──▶│ Canonical Pipeline · DOM stabilization · Graph IR  │
│ (Playwright) │   └───────────────┬──────────────────────────────────┘
└──────────────┘                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
  ┌─────────────┐          ┌─────────────┐           ┌─────────────┐
  │   Replay    │          │   Memory    │           │ Reconstruct │
  │ equivalence │          │   fabric    │           │  + execute  │
  └──────┬──────┘          └──────┬──────┘           └──────┬──────┘
         │                        │                         │
         └────────────────────────┼─────────────────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │ Normalization · Kaalka seal │
                    │   Runtime graph fingerprint │
                    └─────────────────────────────┘
```

---

## Installation

```bash
npm install webweavex
```

Optional browser runtime:

```bash
npx playwright install chromium
```

From source (`javascript` branch):

```bash
git clone https://github.com/ni-sh-a-char/WebWeaveX.git
cd WebWeaveX
git checkout javascript
npm ci
npm run build
```

---

## Quick start

```ts
import {
  extractWeb,
  computeDeterministicHash,
  validateReplayEquivalence,
  runCanonicalPipeline,
} from "webweavex";

const extraction = await extractWeb("https://example.com");
console.log(extraction.bounded, extraction.global_runtime_fingerprint);

const pipeline = await runCanonicalPipeline({
  source: "https://example.com",
  sourceType: "web",
});

console.log(
  validateReplayEquivalence(pipeline, structuredClone(pipeline)).equivalent,
);

console.log(computeDeterministicHash({ status: "ok" }));
```

---

## Real-world examples

<details>
<summary><strong>Playwright auth + encrypted session</strong></summary>

```ts
import { saveAuthenticatedRuntime, loadAuthenticatedRuntime } from "webweavex";

const key = process.env.WWX_SESSION_KEY!;
saveAuthenticatedRuntime("./session.kaalka", loadAuthenticatedRuntime("./session.kaalka", key), key);
```

</details>

<details>
<summary><strong>DOM stabilization fingerprint</strong></summary>

```ts
import { computeStableDomHash, stabilizeDomHtml } from "webweavex";

const html = await page.content();
const stable = stabilizeDomHtml(html);
console.log(computeStableDomHash(stable));
```

</details>

<details>
<summary><strong>Runtime graph + memory</strong></summary>

```ts
import { buildRuntimeGraph, buildRuntimeMemory, graphFingerprint } from "webweavex";

const graph = buildRuntimeGraph({ step: "login", next: "dashboard" });
console.log(graphFingerprint(graph));
console.log(buildRuntimeMemory(graph).stable_hash);
```

</details>

<details>
<summary><strong>Reconstruction</strong></summary>

```ts
import { reconstructRuntime } from "webweavex";

const rebuilt = reconstructRuntime({ extraction: pipeline });
console.log(rebuilt.runtime);
```

</details>

---

## Determinism model

| Layer | Mechanism |
|-------|-----------|
| Unicode | NFKC + CRLF → LF |
| Objects | Sorted keys; volatile fields stripped |
| Graphs | Deterministic node/edge ordering |
| DOM | UUID/timestamp/framework attr stabilization |
| Crypto | UTF-8 → Kaalka `_proc` → base64 |
| Replay | Graph hash + global fingerprint + stabilized DOM |

Full specification: [`docs/architecture/CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md)

---

## Validation

| Command | Purpose |
|---------|---------|
| `npm test` | Vitest (40+ cases) |
| `npm run coverage` | ≥90% lines, ≥80% branches on `src/` |
| `npm run validate:parity` | Cross-language vector harness |
| `npm run validate:production` | Production smoke checks |
| `npm run validate:ecosystem` | Replay · graph · memory · reconstruction gates |
| `npm run validate:replay` | Replay equivalence vectors |
| `npm pack --dry-run` | Publish tarball audit |

CI runs on every push to `javascript` (lint, typecheck, coverage, parity, build, pack).

---

## Security model

- **No arbitrary `eval`** in production paths  
- **Allowlisted** `runExecutionRuntime` actions  
- **Deterministic, bounded** pipelines with graceful degradation  
- **Kaalka-encrypted** persistence when enabled  
- See [SECURITY.md](SECURITY.md) for disclosure policy  

---

## Repository structure

```text
WebWeaveX/                    # javascript branch
├── README.md
├── LICENSE · SECURITY.md · CONTRIBUTING.md · CHANGELOG.md · ROADMAP.md
├── package.json · tsconfig.json · tsup.config.ts · vitest.config.ts
├── src/                      # Production runtime
├── tests/                    # Vitest suites
├── docs/
│   ├── architecture/         # Parity spec, architecture
│   └── archive/              # Engineering reports (not shipped on npm)
├── examples/                 # Runnable samples
├── validation/
│   ├── parity/               # Cross-language vectors
│   ├── replay/               # Replay equivalence gates
│   ├── runtime_graph/        # Graph + fingerprint gates
│   ├── runtime_memory/       # Memory fabric gates
│   ├── reconstruction/       # Reconstruction gates
│   ├── validateParity.ts
│   ├── validateProduction.ts
│   └── validateEcosystem.ts
└── .github/                  # CI, templates, funding
```

---

## Contributing

We welcome focused PRs that preserve **determinism and replay safety**. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

```bash
npm run lint && npm run typecheck && npm run coverage && npm run validate:parity
```

---

## Roadmap

See [ROADMAP.md](ROADMAP.md). Highlights:

- Python branch alignment with parity spec  
- Additional language ports (Rust, Go) on separate branches  
- Deeper connector ecosystem  
- Published npm cadence for `webweavex@2.x`  

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

---

<p align="center">
  <strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable web scraper.</strong>
  <br/><br/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20WebWeaveX-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>
