# NPM PUBLISH REPORT

**Attempted:** 2026-06-08T15:28:44.189439+00:00

**Result:** NOT PUBLISHED — registry rejected unauthenticated write.

| Step | Result |
|------|--------|
| `npm publish --dry-run` | SUCCESS — `+ webweavex@2.0.1`, 10 files, integrity sha512 computed |
| `prepublishOnly` hook (build+test+differential+equivalence) | ALL PASS (399 tests, 25/25 equivalence probes) |
| Package assembly | 10 files, 1.2 MB |
| Registry PUT | **E404 Not Found — PUT https://registry.npmjs.org/webweavex** (unauthenticated write rejected) |
| `npm whoami` | E401 (no credentials; `~/.npmrc` has no valid token; `NPM_TOKEN` absent) |
| Post-attempt registry state | `webweavex` versions = [0.1.0, 2.0.0] — 2.0.1 NOT published |

**Conclusion:** the v2.0.1 package is valid and publish-ready (dry-run + prepublishOnly gates pass), but this environment is not authenticated to npm, so publication could not complete. Nothing was uploaded; 2.0.1 remains available.

### To publish (maintainer, authenticated account)
```bash
npm login    # or configure a valid authToken in ~/.npmrc
npm publish --access public   # from the javascript tree; prepublishOnly re-runs gates automatically
npm view webweavex version    # expect 2.0.1
```
