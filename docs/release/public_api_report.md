# PUBLIC API REPORT

**Measured:** 2026-06-08T15:15:49.456865+00:00

- 229 runtime exports inventoried (`docs/specs/api_inventory.json`).
- 128-name specification public API contract (`specification/apis/README.md`) — 128/128 mapped to JS (`api_parity_report.json`).
- Functional equivalence: 5/5 (4 byte-identical cross-language + build_runtime_graph structural).
- Every public name importable + callable (87 Python / 196 JS executed; rest need domain inputs, covered by suites).
