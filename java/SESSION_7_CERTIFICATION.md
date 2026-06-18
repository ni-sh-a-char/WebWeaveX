# SESSION 7 CERTIFICATION

**Autonomous-continuation slice: remaining dependency-clean connector-runtime cluster.**
Branch `java`. Python canon `origin/python` @ `9625f4a` (2.1.0).

## Substrate / infrastructure produced (per the PRIMARY RULE)

- `tools/rank_remaining_apis.py` + `.result.json` — machine-derived ranking of **all 101
  remaining APIs** by dependency cleanliness (56 clean / 42 forbidden), which also **re-proves
  every blocker** in one pass.
- `java/JAVA_REAL_STATUS.md`, `java/JAVA_GOVERNANCE_AUDIT.md`, `java/JAVA_NEXT_TARGET_RANKING.md`
  — machine-derived status, governance, and target queue.

## Implemented APIs (3) — `core.connectors` cluster

| Manifest API | Java class | Python canon | Closure |
| --- | --- | --- | --- |
| `extract_container_runtime` | `io.webweavex.connectors.ContainerConnector` | `container_connector_engine` (+ `docker_connector_engine`) | 2 m / 0 forbidden |
| `extract_ide_runtime` | `io.webweavex.connectors.IdeConnector` | `ide_connector_engine` | 1 m / 0 forbidden |
| `extract_kubernetes_runtime` | `io.webweavex.connectors.KubernetesConnector` | `kubernetes_connector_engine` | 1 m / 0 forbidden |

All three are manifest `Complete` **and** in `executable_proven_apis`. Pure snapshot→envelope
transforms reusing the proven Session-4 `Connectors` helpers + `PyRepr.str` (for the k8s
`str(item.get("name", item))` sort, incl. nameless-pod `str(dict)`). **No new substrate, no
filesystem, no parser.** No stubs/TODOs/placeholders.

## Parity proof

- Generator: `tools/gen_java_parity_vectors_s7.py` (imports canonical `core`).
- Vectors: `golden_vectors_s7.json` — **18** (7 container, 5 ide, 6 kubernetes) covering
  empty/default, full, ordering (image/namespace/pod-by-name + Unicode), nested (topology/pod
  dicts), malformed (missing keys, non-bool `degraded` passthrough), mutation (nameless pod →
  `str(dict)` sort key), boundary (events cap, alias `podman`/`oci`/upper-case), edge (empty
  dict), regression (unknown runtime → degraded).
- Test: `CrossLanguageParityS7Test` — `stable_serialize` + `compute_kaalka_hash` byte-equal to
  Python. **18/18 PASS**.

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 24 | **27** |
| Remaining (of 128) | 104 | **101** |
| Total tests | 269 | **287** |
| Instruction coverage | 95.45% | **95.57%** (Container 97.7%, Ide/Kubernetes 100%) |
| `PROVEN_FLOOR` | 24 | **27** |

## Governance & quality gates

Validator **PASS 27/128** (MAPPING +3); matrix regenerated (27); manifest unchanged. Coverage
increased; all new tests parity-backed (no synthetic/self-consistency). `mvn verify` BUILD
SUCCESS (287/0/0).

## Next target

`core.workflows` (7 clean APIs) — largest clean cluster; then a JDK-only `json.loads` substrate
to unlock the `decrypt_*`/`load_*` roundtrip families. See
[`JAVA_NEXT_TARGET_RANKING.md`](JAVA_NEXT_TARGET_RANKING.md).
