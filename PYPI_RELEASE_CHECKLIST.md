# PyPI Release Checklist — WebWeaveX 2.1.0 (Python)

> Prepared, not published. Publication is a maintainer-gated step.

**Branch:** `python` · **Package:** `webweavex` · **Version:** `2.1.0`
**Certified commit:** `9625f4ad3126c14b56314ff9b55eac15ab71cda6`

## Pre-flight (already verified this release)

- [x] `pyproject.toml` version = `2.1.0`; `webweavex.__version__` = `2.1.0`
- [x] `python -m build` produces `webweavex-2.1.0-py3-none-any.whl` + `webweavex-2.1.0.tar.gz`
- [x] `python -m twine check dist/*` → PASSED (wheel + sdist)
- [x] Fresh-venv install from wheel imports cleanly; `__version__ == "2.1.0"`
- [x] `pytest -q` → 772 passed, 1 skipped, coverage 90.32% (≥ 90%)
- [x] `CHANGELOG.md` has a `[2.1.0]` entry

## Build

```bash
git clone --branch python --single-branch https://github.com/ni-sh-a-char/WebWeaveX.git wwx-py
cd wwx-py
python -m pip install --upgrade build twine
rm -rf dist build
python -m build
```

## Verify

```bash
python -m twine check dist/*
python -m venv .venv && . .venv/Scripts/activate   # (Linux/mac: source .venv/bin/activate)
pip install dist/webweavex-2.1.0-py3-none-any.whl
python -c "import webweavex; assert webweavex.__version__ == '2.1.0'; print('OK', webweavex.__version__)"
```

## Publish (maintainer only)

```bash
# TestPyPI first (recommended)
python -m twine upload --repository testpypi dist/*
# Production PyPI
python -m twine upload dist/*
```

Requires a PyPI API token (`~/.pypirc` or `TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-...`).

## Post-publish

- [ ] `pip install webweavex==2.1.0` from PyPI in a clean env; verify import + version
- [ ] Tag the release: `git tag v2.1.0 && git push origin v2.1.0`
- [ ] Create GitHub Release notes from the `[2.1.0]` CHANGELOG section
