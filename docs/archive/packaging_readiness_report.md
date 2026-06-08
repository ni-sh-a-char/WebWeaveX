# PACKAGING READINESS REPORT

**Measured:** 2026-06-08T12:50:01.779247+00:00

## npm (JavaScript)

| Item | Value | Result |
|------|-------|--------|
| name | webweavex | OK |
| version | 2.0.0 | **ALREADY PUBLISHED on npm** |
| files | dist, README.md, LICENSE | OK |
| main/module/types | dist/index.{cjs,js,d.ts} | OK |
| exports | `.` | OK |
| license | Apache-2.0 | OK |
| `npm pack` | 9 files, 0 non-product | OK |
| clean install (ESM+CJS) | 229 exports | OK |

## PyPI (Python)

| Item | Value | Result |
|------|-------|--------|
| name | webweavex | OK |
| version | 2.0.0 | **ALREADY PUBLISHED on PyPI** (2.0.0,1.0.3,1.0.2,1.0.1,0.1.0) |
| pyproject build-system | setuptools | OK |
| requires-python | >=3.10 | OK |
| license | Apache-2.0 | OK |
| wheel + sdist build | both built | OK |
| `twine check` | **both PASSED** | OK |
| clean-venv install outside repo | import + API OK | OK |

## Blocking issue for publication

Both registries already host `webweavex==2.0.0` (published from the *previous* code). The current certified build is labelled 2.0.0 but differs substantially (full convergence + Python determinism import fix). **Republishing 2.0.0 is impossible** — `npm publish` returns 403 (cannot overwrite) and `twine upload` returns 400 (file already exists).

**Required before publish:** bump the version in `package.json` and `pyproject.toml` (the public API surface is preserved and the changes are internal-convergence/bugfix → suggest `2.0.1`), then `npm publish` and `twine upload`.
