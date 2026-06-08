# Release Process (Python / PyPI)

WebWeaveX (Python) is released to PyPI as the `webweavex` package.

## Pre-release gates

```bash
python -m pip install -e ".[dev]"
python -W error -c "import webweavex"     # must import cleanly, no warnings
pytest                                     # full suite must pass
python -m build                            # build sdist + wheel
python -m twine check dist/*               # metadata must pass
```

All gates must pass before release.

## Versioning

- Single source intent: `pyproject.toml` `version` and `webweavex.__version__` must match.
- Never republish an existing PyPI version. Bump the version for any new release.

## Publish (maintainer, authenticated)

```bash
python -m build
python -m twine check dist/*
python -m twine upload --repository pypi dist/*
```

## Post-publish verification

```bash
pip install webweavex
python -c "import webweavex; print(webweavex.__version__)"
pip show webweavex
```

The JavaScript (npm) product has its own release process on the `javascript` branch.
