# JAVA_SESSION_9_STATE

**Machine-derived project state (Phase 0).** Regenerated from repository state — validator,
matrix, and the relative-aware dependency ranking (`tools/rank_remaining_apis.py`). Prior
generated files not trusted.

| Metric | Value | Source |
| --- | ---: | --- |
| Total manifest APIs | 128 | `PARITY_MANIFEST.json` |
| **Java parity-proven** | **37** | validator (`PASS 37/128`) |
| Remaining | 91 | 128 − 37 |
| — clean-portable (0 forbidden) | ~46 | mass trace (59 clean baseline − 13 implemented S7/S8/S9) |
| — forbidden-blocked | 42 | mass trace (re-proved) |
| — special (RuntimeKernel, `__version__`, `version`) | 3 | manifest |
| Tests | 454 | `mvn verify` |
| Instruction coverage | 95.88% | JaCoCo (floor 94 %) |
| `PROVEN_FLOOR` | 37 | parity-regression.yml |

## Blocker classes (of the 42 blocked)

| Class | APIs | Root cause |
| --- | ---: | --- |
| bs4 import barrier (semantic/evidence eager `__init__`) | ~26 | BeautifulSoup imported (not executed) via `core.semantic`/`core.evidence` |
| full extraction stack (bs4+lxml+net+OCR+PDF+DOCX+browser) | ~10 | real HTML/web extraction |
| network only | 1 | `crawl` |
| OCR/filesystem | 2 | `extract_multimodal`, `ingest_input` |
| platform (`sys.platform`) | included above | `extract_native`, `run_native_cognition` |

## Substrate classes (built, reusable)

| Substrate | Java | Status |
| --- | --- | --- |
| canonical determinism | `Normalization`, `StableSerialize`, `CanonicalJson`, `PyFloat`, `PyRepr`, `PyRound`, `PyText` | proven |
| `json.dumps` / `json.loads` | `PyJson` / **`PyJsonParse`** | proven (S8) |
| Kaalka crypto | `Kaalka`, `KaalkaV5Proc`, `TimeKey`, `KaalkaSession` | proven |
| runtime graph / IR merge | `RuntimeGraph`, `ExecutionRuntime.buildUnifiedRuntimeGraph` | proven |
| connector envelope helpers | `connectors.Connectors` | proven |

## Proven subsystems (Java packages)

determinism · crypto · kernel · graph · ir · knowledge · query · memory · persistence ·
reconstruction · replay · connectors (7) · documents · interaction · session · **execution (6)**.
