# RELEASE ENGINEERING REPORT

**Measured:** 2026-06-08T14:17:13.114923+00:00

**Status:** PASS

| Check | Result |
|------|--------|
| Tarball | webweavex-2.0.1.tgz (10 files) |
| Fresh-dir `npm install` | EXIT 0 |
| ESM `import('webweavex')` | OK, VERSION 2.0.1, 229 exports |
| CJS `require('webweavex')` | OK, VERSION 2.0.1 |
| Runtime execution (buildRuntimeGraph/fingerprint/encryptValue) | OK |
| Node compatibility | >=18 (engines) |
| ESM + CJS dual export | dist/index.js + dist/index.cjs + .d.ts/.d.cts |
| Python runtime dependency | none (0 in bundle) |

Installed in a clean directory outside the repo; imports + runtime calls verified.
