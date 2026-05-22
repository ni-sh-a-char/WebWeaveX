# FINAL IMPORT STABILITY REPORT

- `import webweavex` time: **0.0 ms**
- Version: **2.0.0**

## Module checks

| Module | OK | ms |
|--------|-----|-----|
| `webweavex` | True | 4408.01 |
| `core.kernel.runtime_pipeline` | True | 0.73 |
| `core.determinism` | True | 0.55 |
| `core.replay` | True | 0.55 |

## Rules

- No import-time browser launch
- No import-time network I/O
- Lazy IR package exports