# FINAL NPM AUDIT REPORT

- Package name: `webweavex`
- Version: `2.0.0`
- Crypto dependency: `kaalka@5.0.0` (exact pin)
- No `file:packages/kaalka` or local crypto forks
- `sideEffects: false`, dual ESM/CJS via tsup
- `prepublishOnly`: build + test + parity validation

## Publish checklist

1. `npm publish --access public` (when approved)
2. Tag `v2.0.0` on `javascript` branch
3. Ensure Python branch documents parity spec migration