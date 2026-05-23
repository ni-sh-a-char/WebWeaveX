# Final Public npm Release Report — WebWeaveX v2.0.0

**Generated:** 2026-05-23  
**Branch:** `javascript` (commit `d39dd16`)  
**Maintainer:** piyush-mishra-00 \<piyushmishra.professional@gmail.com\>

---

## npm package

| Field | Value |
|-------|--------|
| **URL** | https://www.npmjs.com/package/webweavex |
| **Target version** | `2.0.0` |
| **Previous on registry** | `0.1.0` (legacy crawler positioning) |
| **Package size** | ~38.4 kB (packed) / ~181.7 kB (unpacked) |
| **Shipped files** | 9 (`dist/*`, `README.md`, `LICENSE`, `package.json`) |

---

## Publish status

| Step | Status |
|------|--------|
| Validation gates | **COMPLETE** |
| `npm pack` + local ESM/CJS install | **COMPLETE** |
| Git commit + push (`javascript`) | **COMPLETE** — `d39dd16` |
| `npm publish --access public` | **BLOCKED** — npm auth |

**Auth diagnostics:**

- `npm whoami` → `401 Unauthorized`
- `npm publish` → `404` (npm returns 404 when the token cannot publish to `webweavex`; package maintainer is `piyush-mishra-00`)

**To complete publish (maintainer action):**

```bash
git checkout javascript
npm login
# authenticate as npm user: piyush-mishra-00
npm whoami
npm publish --access public
npm view webweavex version
```

Optional: use a granular **Automation** token with publish scope:

```bash
npm config set //registry.npmjs.org/:_authToken=YOUR_TOKEN
npm publish --access public
```

---

## Validation gates (all passed pre-publish)

| Command | Result |
|---------|--------|
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm run test` | PASS — 35 files, 45 tests |
| `npm run coverage` | PASS — 92.96% lines, 83.85% branches |
| `npm run validate:parity` | PASS — 11/11 vectors |
| `npm run validate:production` | PASS |
| `npm run build` | PASS |
| `npm pack --dry-run` | PASS — clean tarball |

---

## Local install proof

```bash
npm pack
mkdir ../wwx-test-install && cd ../wwx-test-install
npm init -y
npm install ../WebWeaveX/webweavex-2.0.0.tgz
node -e "import('webweavex').then(m => console.log(typeof m.extractWeb))"
```

Result: `function` (ESM and CJS verified).

---

## Positioning (humans + AI agents)

WebWeaveX v2.0.0 is **deterministic runtime cognition infrastructure** — replay-safe, authenticated-runtime-aware, reconstruction-capable, cross-language deterministic — **not** a disposable scraper, AGI product, or bypass tool.

---

## Architecture summary

| Pillar | npm implementation |
|--------|-------------------|
| Runtime cognition | Browser capture + IR + graphs |
| Determinism | NFKC + stable serialization + fingerprints |
| Replay | `validateReplayEquivalence` |
| Reconstruction | IR-driven rebuild |
| Memory | Runtime memory fabric |
| Auth continuation | Encrypted sessions (user-supplied credentials) |
| Parity | `kaalka@5.0.0` + shared formula with Python |

---

## Ecosystem branches

| Branch | Package |
|--------|---------|
| `main` | Portal — https://github.com/ni-sh-a-char/WebWeaveX |
| `python` | PyPI `webweavex` |
| `javascript` | npm `webweavex` (this release) |

---

## GitHub release

Use [`docs/archive/GITHUB_RELEASE_NPM_v2.0.0.md`](./GITHUB_RELEASE_NPM_v2.0.0.md) as release notes when creating tag **`v2.0.0-javascript`** or updating the existing **`v2.0.0`** release on the `javascript` branch.

---

## Post-publish checklist (after `npm login`)

```bash
npm view webweavex version          # expect 2.0.0
mkdir ../wwx-live-test && cd ../wwx-live-test
npm init -y
npm install webweavex@2.0.0
node -e "import('webweavex').then(m => console.log(typeof m.extractWeb))"
```

---

## Roadmap

- npm `2.0.x` patch cadence for parity vectors and Playwright compatibility
- Published docs site aligned with runtime cognition positioning
- Continued cross-language parity with Python PyPI releases
