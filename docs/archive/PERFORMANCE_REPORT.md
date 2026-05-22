# PERFORMANCE REPORT

**Generated:** 2026-05-22T17:37:21Z

| Benchmark | ms |
|-----------|-----|
| extract_web | 10457.93 |
| extract_repository | 18.42 |
| reconstruct_runtime | 0.07 |
| memory_merge | 0.1 |

## Observations

- Web extraction dominated by Playwright network idle wait.
- Repository extraction scales with file count (bounded ingestion).
- Reconstruction and memory merge are sub-millisecond on fixed inputs.