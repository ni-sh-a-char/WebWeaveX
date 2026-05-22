# Contributing to WebWeaveX

Thank you for helping improve deterministic runtime extraction infrastructure.

## Setup

```bash
git clone https://github.com/PIYUSH-MISHRA-00/webweavex.git
cd webweavex
pip install -e ".[dev,browser]"
playwright install chromium   # optional, for browser tests
```

## Before you open a PR

```bash
pytest -q
python -m build
python -c "import webweavex; assert webweavex.__version__ == '2.0.0'"
```

Scoped production coverage must remain **≥ 90%** (see `pyproject.toml`).

## Design rules

1. **Canonical pipeline only** — new runtime behavior integrates with `run_canonical_pipeline()` or an existing phase orchestrator; no parallel mega-orchestrators.
2. **Determinism** — no `random`, no `uuid4`, no time-based IDs in persisted or hashed structures.
3. **Kaalka persistence** — operational checkpoints use `encrypt_value` / session wrappers with `algorithm: kaalka`; no pickle or plaintext runtime stores.
4. **Replay-safe** — graph normalization and fingerprints must remain stable for equivalent inputs.
5. **Bounded output** — public functions return dicts with `bounded: True` where applicable.
6. **No import-time side effects** — `import webweavex` must not launch browsers or network jobs.

## Code style

- Match surrounding modules (types, `from __future__ import annotations`, minimal comments).
- Prefer extending existing engines over new top-level shim files.
- Tests should assert real behavior, not implementation trivia.

## Pull requests

Use the PR template in `.github/PULL_REQUEST_TEMPLATE.md`.

## Questions

Open a [GitHub issue](https://github.com/PIYUSH-MISHRA-00/webweavex/issues) or see [docs/](docs/README.md).
