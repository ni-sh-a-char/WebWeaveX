# JAVA_SESSION_18_CERTIFICATION

**`core.identity` — 3 APIs + ~11 fingerprint engines, byte-exact.** Branch `java`. Canon
`origin/python` @ `9625f4a` (2.1.0). Phase 0 verified `HEAD == origin/java` (`08d7dca`);
matrix/validator rebuilt live (started 77/128).

## Dependency proof + runtime import audit (Phases 1–2)

| API | def module | closure | forbidden | runtime import |
| --- | --- | ---: | ---: | --- |
| `build_browser_identity` | `identity.browser_identity_orchestrator` | 28 m / 1092 L | 0 | **import OK** |
| `save_browser_identity` | `identity.fingerprint_persistence_engine` | 28 m / 1092 L | 0 | **import OK** |
| `load_browser_identity` | `identity.fingerprint_persistence_engine` | 28 m / 1092 L | 0 | **import OK** |

Per the S17 lesson, each module was **actually imported in Python** (not trusted from the tracer
alone) — all clean, no eager-`__init__` bs4, no Playwright/platform coupling. The fingerprints are
deterministic table+hash transforms (canvas/webgl/font/navigator/etc.), not live browser probes.

## Implemented APIs (3)

`io.webweavex.identity.IdentityRuntime` — `build_browser_identity` (orchestrator over 11 engines:
profile, user_agent, platform, language, timezone, webgl, canvas, font, media_device, navigator,
entropy, fingerprint) + `save/load_browser_identity` (session envelope).

Reuses `Kaalka` (`compute_kaalka_hash` and `compute_kaalka_hash_payload` are both the
sha256-of-stable_serialize hash) + `KaalkaSession` envelope. Serializable output (no
self-reference). **Zero new substrate. No stubs.**

## Proofs (machine-derived)

| Gate | Result |
| --- | --- |
| Parity | `CrossLanguageParityS18Test` **57/57** byte-exact (orchestrator + 11 engines × 4 profiles + entropy/normalize/fingerprint + save/load) |
| Coverage | **96.426 % → 96.511 %** (IdentityRuntime 98.9 %) |
| Governance | validator **PASS 80/128**; matrix 80; MAPPING +3; `PROVEN_FLOOR` 77→80; manifest unchanged |
| Full suite | `mvn clean verify` **817/0/0** BUILD SUCCESS |

## Counts

| Metric | Before | After |
| --- | --- | --- |
| Parity-proven APIs | 77 | **80** |
| Remaining (of 128) | 51 | **48** |
| Total tests | 760 | **817** |
| Instruction coverage | 96.426 % | **96.511 %** |
| `PROVEN_FLOOR` | 77 | **80** |

Next: connectors remainder + the deferred memory orchestrator
([`JAVA_SESSION_19_PLAN.md`](JAVA_SESSION_19_PLAN.md)). Mission active — 80/128.
