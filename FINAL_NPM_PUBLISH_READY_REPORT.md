# FINAL NPM PUBLISH READY REPORT

| Check | Status |
|-------|--------|
| `npm pack` | OK (~27 kB) |
| `npm publish --dry-run` | OK |
| ESM + CJS + types | OK |
| `kaalka` dependency | `file:packages/kaalka` (bundle or publish `kaalka@2` separately) |

```bash
npm publish --access public
```

Ensure `packages/kaalka` is published first or inlined per release policy.
