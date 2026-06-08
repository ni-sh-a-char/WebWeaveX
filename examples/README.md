# WebWeaveX Examples

Runnable examples. After `npm install webweavex`:

```bash
npx tsx examples/runtime-graphs.ts
```

| Example | Demonstrates |
|---------|--------------|
| `basic-extraction.ts` | Canonical extraction pipeline over an input source |
| `runtime-graphs.ts` | Merging runtime IRs into one deterministic graph + fingerprint |
| `replay-equivalence.ts` | Proving a replayed runtime equals the original |
| `deterministic-hashing.ts` | Kaalka hashing, fingerprints, authenticated encryption |
| `browser.ts` | Browser / Playwright-native extraction |

Every example imports the public `webweavex` API and is verified against the published package.
