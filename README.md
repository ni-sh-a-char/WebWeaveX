<p align="center">
  <strong>WebWeaveX — Native TypeScript Runtime Infrastructure</strong><br/>
  <em>Deterministic extraction · replay-safe graphs · Kaalka persistence</em>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/webweavex"><img src="https://img.shields.io/npm/v/webweavex?style=flat-square" alt="npm"/></a>
  <img src="https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Node-18+-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node 18+"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/>
  <img src="https://img.shields.io/badge/coverage-88%25%2B-6366f1?style=flat-square" alt="Coverage"/>
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?style=flat-square&logo=buy-me-a-coffee" alt="Buy Me a Coffee"/></a>
</p>

> **Branch:** `javascript` — native implementation only. Architecture portal: [`main`](https://github.com/ni-sh-a-char/WebWeaveX). Python: [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python).

## What is WebWeaveX?

Native **deterministic runtime extraction** and **replay-safe operational cognition** for authenticated SPAs, Electron surfaces, and synchronized runtimes. **Zero Python dependency.**

## What it is NOT

Not auth bypass, malware, CAPTCHA defeat, AGI agents, or subprocess bridges to other languages.

## Quick start

```bash
npm install webweavex
npm install playwright   # browser extraction
```

```typescript
import { extractWeb, runCanonicalPipeline, validateReplayEquivalence } from "webweavex";

const out = await extractWeb("https://example.com");
console.log(out.bounded, out.global_runtime_fingerprint);

const pipe = await runCanonicalPipeline({ source: "https://example.com", sourceType: "web" });
console.log(pipe.pipeline_hash);
```

## Canonical pipeline

`UniversalInput` → `runCanonicalPipeline()` → unified runtime graph (single path).

## Authenticated runtime continuation

Users authenticate themselves; WebWeaveX captures and **encrypts** session state with **Kaalka** (`saveAuthenticatedRuntime` / `loadAuthenticatedRuntime`). No MFA bypass.

## Architecture

```
Input → Canonical Pipeline → Runtime Cognition → Semantic / Causality / Workflow
  → Synchronization → Federated Memory → Execution Fabric → Reconstruction → Universal Runtime Graph
```

## Validation

```bash
npm run test
npm run coverage
npm run build
npm run validate
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
