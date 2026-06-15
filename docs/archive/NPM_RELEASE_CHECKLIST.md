# npm Release Checklist — WebWeaveX 2.1.0 (JavaScript)

> Prepared, not published. Publication is a maintainer-gated step.

**Branch:** `javascript` · **Package:** `webweavex` · **Version:** `2.1.0`
**Certified commit:** `c8dec710522f82bb34b76d81a10cff156f69fcb1`

## Pre-flight (already verified this release)

- [x] `package.json` version = `2.1.0`; `package-lock.json` in sync
- [x] `src/index.ts` `VERSION` = `2.1.0`; `src/publicApi.ts` `version` = `2.1.0`
- [x] `npm ci` clean install (257 packages)
- [x] `npm run build` → ESM (`dist/index.js`) + CJS (`dist/index.cjs`) + types (`dist/index.d.ts`, `dist/index.d.cts`)
- [x] `npm pack` → `webweavex-2.1.0.tgz`
- [x] ESM + CJS both load `VERSION === "2.1.0"` (229 exports)
- [x] `npm test` (vitest) → 399 passed across 238 files
- [x] `CHANGELOG.md` has a `[2.1.0]` entry

## Build

```bash
git clone --branch javascript --single-branch https://github.com/ni-sh-a-char/WebWeaveX.git wwx-js
cd wwx-js
npm ci
npm run build
```

## Verify

```bash
npm test
npm pack
node -e "const w=require('./dist/index.cjs'); if(w.VERSION!=='2.1.0') throw new Error('bad version'); console.log('CJS OK', w.VERSION)"
node --input-type=module -e "import('./dist/index.js').then(w=>{if(w.VERSION!=='2.1.0')throw new Error('bad');console.log('ESM OK', w.VERSION)})"
```

## Publish (maintainer only)

```bash
npm login                       # or set NPM_TOKEN / .npmrc //registry.npmjs.org/:_authToken
npm publish --dry-run           # final audit
npm publish --access public
```

## Post-publish

- [ ] `npm view webweavex version` → `2.1.0`
- [ ] `npm install webweavex@2.1.0` in a clean dir; verify ESM + CJS import
- [ ] Tag the release: `git tag v2.1.0 && git push origin v2.1.0`
- [ ] Create GitHub Release notes from the `[2.1.0]` CHANGELOG section
