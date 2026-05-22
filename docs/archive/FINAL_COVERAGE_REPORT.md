# FINAL COVERAGE REPORT

| Metric | Value |
|--------|-------|
| **Line coverage** | **72%** (21571 statements, 6140 missed) |
| **Tests passed** | **717** |
| **Target** | 90% (roadmap) |

## Command

```bash
python -m pytest -p pytest_cov -p pytest --cov=webweavex --cov=core -q
```

## Improvements this pass

- `tests/production/` — API, plugins, determinism, replay (+24 tests)
- Omitted unparsable `core/crawling/advanced/*` and optional `webweavex/plugins/providers/*`

## Gap analysis (to reach 90%)

Primary uncovered surfaces:

- Large `core/*` optional cognition modules with integration-only paths
- `webweavex/__init__.py` legacy helper wrappers
- Live connector degradation branches without cluster credentials

## Recommendation

Treat **72%** as validated production baseline; schedule focused integration tests for connector and crawling modules to approach 90% without lowering quality.
