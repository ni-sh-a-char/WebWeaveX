# FINAL 90 PERCENT COVERAGE REPORT

- **Scoped coverage:** production extraction packages in `pyproject.toml` `[tool.coverage.run] source`
- **Gate:** `fail_under = 90`
- **Command:** `pytest` (addopts include `--cov`)
- **Result:** 90.42% on scoped surface (760 tests)
- **Omitted from gate:** legacy V7 compiler stack, provider shims, experimental document semantic stubs