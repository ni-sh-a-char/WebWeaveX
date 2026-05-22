# COVERAGE REPORT

**WebWeaveX v2.0.0** — `pytest --cov=webweavex --cov=core`

| Metric | Value |
|--------|-------|
| **Total coverage** | **68%** |
| **Tests passed** | **675** |
| **Target** | 90%+ (roadmap) |

## Notes

- Core runtime paths (browser, kernel, Kaalka, memory, execution, reconstruction) have strong coverage.
- Lower coverage areas: `webweavex/plugins/`, `webweavex/api/`, optional connector queues, and legacy extract facades.
- Reaching 90% requires dedicated tests for plugin/API surfaces without expanding scope in this pass.

## Command

```bash
python -m pytest -p pytest_cov -p pytest --cov=webweavex --cov=core --cov-report=term:skip-covered -q
```
