# Contributing

1. Fork and branch from `main`
2. Install: `pip install -e ".[dev,browser,parsers]"`
3. Run tests: `pytest -q`
4. Build: `python -m build`
5. Submit PR with deterministic, bounded changes only

## Rules

- No `eval` / `exec` in production paths
- No probabilistic runtime behavior
- Kaalka for any new persistence
- New features go under canonical `core/<phase>/` packages — no `*_v2` trees
