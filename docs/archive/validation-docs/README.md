# Validation

## CI gates

```bash
pytest -q                 # 760+ tests, scoped coverage ≥ 90%
python -m build           # webweavex-2.0.0-py3-none-any.whl
python -c "import webweavex; print(webweavex.__version__)"
```

## Production master

```bash
python validation/final_production_master.py
```

Runs import stability, Kaalka cross-language checks, real-world matrix (when network/tools available), connector and reconstruction validators.

## Coverage scope

Coverage is measured on **production extraction packages** listed in `pyproject.toml` `[tool.coverage.run] source`, with explicit `omit` for legacy V7 compiler stack and experimental stubs.

## Reports

- Final release summary: [WEBWEAVEX_v2_FINAL_RELEASE_REPORT.md](WEBWEAVEX_v2_FINAL_RELEASE_REPORT.md)
- Historical reports: [../archive/](../archive/)
