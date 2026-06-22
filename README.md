<p align="center">
  <strong>WebWeaveX — Java</strong><br/>
  <strong>Deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Java-17%2B-007396?style=flat-square&logo=openjdk&logoColor=white" alt="Java 17+"/>
  <img src="https://img.shields.io/badge/build-Maven-C71A36?style=flat-square&logo=apachemaven&logoColor=white" alt="Maven"/>
  <img src="https://img.shields.io/badge/Maven%20Central-io.webweavex%3Awebweavex-blue?style=flat-square" alt="Maven Central"/>
  <img src="https://img.shields.io/badge/parity-PASS-22c55e?style=flat-square" alt="Parity"/>
  <img src="https://img.shields.io/badge/tests-732%20passing-22c55e?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/coverage-96.42%25%20instruction-22c55e?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/API%20parity-69%20%2F%20128%20proven-3b82f6?style=flat-square" alt="API parity"/>
  <img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="License"/>
</p>

---

## Contents

- [Overview](#overview) · [Why WebWeaveX](#why-webweavex) · [What it is NOT](#what-webweavex-is-not)
- [Architecture](#architecture) · [Package structure](#package-structure) · [Installation](#installation)
- [Quick start](#quick-start) · [Maven usage](#maven-usage) · [Gradle usage](#gradle-usage)
- [API examples](#api-examples) · [Cross-language parity](#cross-language-parity) · [Implementation matrix](#implementation-matrix)
- [Build & test](#build--test) · [Coverage](#coverage) · [CI/CD](#cicd)
- [Governance](#governance) · [Branch policy](#branch-policy) · [Certification status](#certification-status)
- [Roadmap](#roadmap) · [Security](#security) · [License](#license)

---

## Overview

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI
agents** to understand, continue, reconstruct, replay, and reason about **authenticated
operational software systems**.

This **`java`** branch is the native **JVM / Maven Central** implementation. It targets
**byte-exact cross-language parity** with the canonical Python runtime (and, transitively,
the JavaScript and Dart runtimes):

```
Python  =  Java  =  JavaScript  =  Dart
```

| Branch | Ecosystem | Role |
|--------|-----------|------|
| `python` | PyPI | **Canonical** reference runtime (2.1.0) |
| **`java`** (this) | **Maven Central** | **JVM runtime (`io.webweavex:webweavex:2.1.0`)** |
| `javascript` | npm | JavaScript runtime (2.1.0) |
| `dart` | pub.dev | Dart runtime (2.1.0) |

> **Status: foundation-first build, in progress.** The deterministic + cryptographic
> bedrock — through which every other subsystem hashes and serializes — is implemented and
> verified **byte-exact** against canonical Python 2.1.0, together with the kernel, graph,
> IR, query, memory, and reconstruction slices. Higher layers (extraction, semantic,
> workflows, vision, OCR) are tracked in [`java/JAVA_PARITY_MATRIX.md`](java/JAVA_PARITY_MATRIX.md)
> and built session by session. **No stubs, placeholders, or TODO implementations are
> shipped** — only implemented, parity-proven code (see [Branch policy](#branch-policy)).

### Humans and AI agents

| Audience | Use |
|----------|-----|
| **Engineers** | Deterministic extraction, session continuation, replay audits on the JVM |
| **AI agents** | Replay-safe memory, graph identity, operational continuity — every output is a hashable, diffable IR |

---

## Why WebWeaveX

Traditional tools capture HTML, not **operational runtime state**. WebWeaveX provides
canonical serialization, Kaalka-sealed sessions, replay equivalence, and reconstruction
identities so that **how software runs** — not just what HTML was returned — becomes a
first-class, reproducible artifact, byte-identical across four languages.

| Problem | With WebWeaveX |
|---------|----------------|
| Ephemeral runtime state | Stabilized runtime graphs + fingerprints |
| Auth drift | Encrypted session continuation (authorized credentials only) |
| Nondeterministic replays | `validateReplayEquivalence` |
| Lost operational context | Runtime graphs + memory fabric |
| Cross-language drift | Byte-identical Kaalka hashes across Python · Java · JS · Dart |

## What WebWeaveX is NOT

| Not | Reality |
|-----|---------|
| Scraper / crawler | Operational runtime substrate |
| AGI product | Bounded, deterministic pipelines |
| Auth / CAPTCHA bypass | No credential cracking — authorized session material only |
| LLM wrapper | Native Java library, JDK-only deterministic core |

---

## Architecture

```text
Input → Canonical pipeline → Graph + Memory → Replay check → Reconstruction
              ↓
     Normalization + Kaalka v5 cipher (deterministic core)
```

The deterministic core is the contract everything else hashes through:

```
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → Kaalka v5 proc → base64
```

| Layer | Mechanism |
|-------|-----------|
| Unicode | NFKC (`java.text.Normalizer`, matching CPython `unicodedata`) + CRLF→LF + trailing-whitespace strip |
| Objects | Code-point-sorted keys, volatile-field strip, numeric canonicalization |
| Floats | Python `repr(float)` (shortest round-trip; positional/scientific thresholds) |
| Crypto | Kaalka v5 byte cipher + SHA-256 + base64 (`MessageDigest`, `Base64` — JDK only) |
| Graph | Deterministically sorted nodes/edges, `graphFingerprint` |

The deterministic core depends on the **JDK alone** — no third-party library can perturb
canonical bytes. Jackson is a **test-only** dependency used to load golden vectors.

---

## Package structure

```
io.webweavex
├── crypto          Hashing, Kaalka, KaalkaV5Proc, TimeKey          [implemented]
├── determinism     Normalization, PyFloat, CanonicalJson, PyJson,  [implemented]
│                   Py, PyRepr, PyRound, StableSerialize, GlobalRuntimeFingerprint
├── kernel          UniversalInput                                  [implemented]
├── graph           RuntimeGraph, GraphEntropy, GraphInvariants,    [implemented]
│                   GraphReconstruction, TopologyProof, SemanticGraphValidator …
├── ir              UnifiedRuntimeIr, MultimodalIr, SemanticGraphIr,[implemented]
│                   KnowledgeIr, IrBase
├── knowledge       OntologyReconciliation, ContradictionLattice,   [implemented]
│                   SemanticIdentity, OntologyConflict
├── query           GraphQuery, OntologyQuery, TopologyReasoning     [implemented]
├── memory          RuntimeMemory, MemoryQuery, MemorySearch         [implemented]
├── persistence     FingerprintHex                                  [implemented]
├── reconstruction  RuntimeReconstruction, RuntimeValidation,        [implemented]
│                   MemoryReconstruction, BrowserReconstruction
├── replay          ReplayEquivalence                               [implemented]
├── connectors      Database/Api/Stream/Telemetry/Container/Ide/    [implemented]
│                   Kubernetes runtime extraction (snapshot→envelope)
├── documents       DocumentRuntime (extract_document_runtime)      [implemented]
├── interaction     Pagination, InteractionGraph, PageView          [implemented]
├── session         EncryptedSessionStore (save/load session)       [implemented]
├── execution       ExecutionRuntime (sandbox/action/replay/        [implemented]
│                   simulate/run + ~20 engines)
├── synchronization SyncRuntime (delta/replay/run/save/load +       [implemented]
│                   ~18 engines)
├── workflow        WorkflowRuntime (objective/plan/run/replay/     [implemented]
│                   save/load + ~15 engines)
├── evolution       EvolutionRuntime (evolution/selector/run/save/  [implemented]
│                   load + ~17 engines)
├── causality       CausalityRuntime (run/replay/run-for-extract/   [implemented]
│                   save/load + ~18 engines)
├── streaming       StreamingRuntime (stream timeline/replay +      [implemented]
│                   live runtime run/save/load, connector reuse)
└── … extraction(HTML) · semantic · vision · ocr · …               [planned]
```

Full target layout (mirrors Python `core/`, JS `src/`, Dart `lib/src/`) and per-API status:
[`java/JAVA_PARITY_MATRIX.md`](java/JAVA_PARITY_MATRIX.md).

---

## Installation

WebWeaveX is published to **Maven Central** under coordinates `io.webweavex:webweavex`.
Requires **Java 17+** (built and tested on JDK 17 and 21).

### Maven usage

```xml
<dependency>
  <groupId>io.webweavex</groupId>
  <artifactId>webweavex</artifactId>
  <version>2.1.0</version>
</dependency>
```

### Gradle usage

```kotlin
// build.gradle.kts
dependencies {
    implementation("io.webweavex:webweavex:2.1.0")
}
```

```groovy
// build.gradle
dependencies {
    implementation 'io.webweavex:webweavex:2.1.0'
}
```

---

## Quick start

```java
import io.webweavex.crypto.Kaalka;
import io.webweavex.graph.RuntimeGraph;
import io.webweavex.determinism.GlobalRuntimeFingerprint;

import java.util.Map;

public class QuickStart {
    public static void main(String[] args) {
        // Deterministic content hash — byte-identical to Python/JS/Dart.
        String hash = Kaalka.computeKaalkaHash(Map.of("status", "ok"));

        // Build a deterministically sorted, fingerprinted runtime graph.
        var graph = RuntimeGraph.buildParityRuntimeGraph(
                Map.of("session", Map.of("authenticated", true)));
        String fp = RuntimeGraph.graphFingerprint(graph);

        System.out.println(hash);
        System.out.println(fp);
    }
}
```

---

## API examples

### Deterministic hashing & encryption (Kaalka)

```java
String hash = Kaalka.computeKaalkaHash(Map.of("k", "v"));     // compute_kaalka_hash
String enc  = Kaalka.encryptValue(Map.of("secret", 1), "key"); // encrypt_value
Object dec  = Kaalka.decryptValue(enc, "key");                 // decrypt_value
```

### Runtime graph, unified IR & global fingerprint

```java
var graph = RuntimeGraph.buildParityRuntimeGraph(payload);     // build_runtime_graph
var ir    = UnifiedRuntimeIr.compile(envelope);                // compile_unified_runtime_ir
String f  = GlobalRuntimeFingerprint.compute(envelope);        // compute_global_runtime_fingerprint
```

### Runtime memory fabric

```java
var memory = RuntimeMemory.build(runtimeHistory, lineage, semanticRelations); // build_runtime_memory
var hit    = MemoryQuery.queryRuntimeMemory(memory, "semantic", "a");         // query_runtime_memory
var found  = MemorySearch.searchRuntimeMemory(memory, "term");                // search_runtime_memory
```

### Query engines

```java
var g = GraphQuery.queryGraph(graph, "node-id");               // query_graph
var k = OntologyQuery.queryKnowledge(entities, edges);         // query_knowledge
var r = GraphQuery.queryRuntimeGraph(runtimeGraph, "node-id"); // query_runtime_graph
```

### Replay equivalence & reconstruction

```java
var report  = ReplayEquivalence.validate(envelope, clone);             // validate_replay_equivalence
var rebuilt = RuntimeReconstruction.reconstructRuntime(envelope);      // reconstruct_runtime
var ok      = RuntimeValidation.validateReconstructedRuntime(rebuilt); // validate_reconstructed_runtime
```

---

## Cross-language parity

`io.webweavex.parity.CrossLanguageParity*Test` loads golden vectors generated from a
materialized **canonical Python branch** (`tools/gen_java_parity_vectors*.py`) and asserts
Java is **byte-identical** to Python for canonical serialization, SHA-256/Kaalka hashes,
NFKC/CRLF normalization, code-point key ordering, `repr(float)`, and the kernel / graph /
IR / query / memory / reconstruction slices.

Because **Python ≡ JavaScript ≡ Dart** is already certified (70k+ byte-identical
comparisons), proving **Java ≡ Python** proves **Java ≡ JS ≡ Dart** for those APIs.

```bash
cd java
mvn -B -ntp test -Dtest='CrossLanguageParity*Test'
python ../tools/validate_java_manifest.py   # manifest governance gate
```

Single source of truth for the 128-API surface: [`PARITY_MANIFEST.json`](PARITY_MANIFEST.json).

---

## Implementation matrix

| Metric | Value |
| --- | --- |
| Total tracked public APIs (Python/JS/Dart) | **128** |
| Java implemented (parity-proven) | **69** |
| Java planned | 59 |
| Parity tests | **732 passing**, 0 failures, 0 errors |
| Instruction coverage (JaCoCo) | **96.42 %** |

Proven APIs today (69) span the determinism + crypto foundation, kernel/graph/IR,
query/memory/reconstruction, the connector-runtime extraction family
(`extract_database/api/runtime_streams/telemetry/container/ide/kubernetes_runtime`),
the document/interaction layer (`extract_document_runtime`, `extract_paginated_content`,
`build_interaction_graph`), and the session-crypto cluster (`encrypt_session_state`,
`decrypt_session_state`, `save_encrypted_session`, `load_encrypted_session`).

Per-API classification (Complete / Partial / Deferred · Java status):
[`java/JAVA_PARITY_MATRIX.md`](java/JAVA_PARITY_MATRIX.md).

---

## Build & test

```bash
cd java
mvn clean verify         # compile, test, JaCoCo coverage, jar + sources + javadoc
mvn -Prelease verify     # additionally GPG-signs artifacts for Maven Central
```

- **Java 17+** (CI matrix: JDK 17 and 21).
- Deterministic core uses the **JDK alone** (`java.text.Normalizer`, `MessageDigest`,
  `Base64`). Jackson is a **test-only** dependency (loads golden vectors).

### Regenerating golden vectors

```bash
# from a materialized canonical Python-branch checkout (so `core` is importable)
python tools/gen_java_parity_vectors.py java/src/test/resources/parity/golden_vectors.json
```

---

## Coverage

JaCoCo: **95.68 % instruction**. The uncovered remainder is unreachable defensive code
faithfully mirrored from the canonical runtimes (JDK-guaranteed `NoSuchAlgorithmException`
catches, the modular-cipher time-key fallback that always round-trips, float-format safety
branches). These are retained as 1:1 parity mirrors rather than removed to inflate the
metric — see [`java/COVERAGE_EXCEPTION_REPORT.md`](java/COVERAGE_EXCEPTION_REPORT.md).

---

## CI/CD

GitHub Actions gate every push and PR touching `java/**`, `tools/**`, or
`PARITY_MANIFEST.json`:

| Workflow | Gate |
|----------|------|
| [`java-build.yml`](.github/workflows/java-build.yml) | `mvn clean verify` on JDK 17 + 21, coverage artifact upload |
| [`java-parity.yml`](.github/workflows/java-parity.yml) | `CrossLanguageParity*Test` + `validate_java_manifest.py` |
| [`parity-regression.yml`](.github/workflows/parity-regression.yml) | Coverage floor (94 %) + proven-API floor (69) + manifest drift |

---

## Governance

| Document | Purpose |
|----------|---------|
| [LICENSE](LICENSE) | Apache-2.0 |
| [GOVERNANCE.md](GOVERNANCE.md) | Decision-making model |
| [MAINTAINERS.md](MAINTAINERS.md) | Current maintainers |
| [CODEOWNERS](CODEOWNERS) | Review ownership |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution workflow |
| [RELEASE.md](RELEASE.md) | Release process |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [ROADMAP.md](ROADMAP.md) | Direction |
| [JAVA_BRANCH_POLICY.md](JAVA_BRANCH_POLICY.md) | Maven-first branch rules |

Branch governance validator: `python tools/validate_java_manifest.py` (fails on manifest
drift, missing/extra source vs. matrix, undocumented or untested proven APIs, or any
foreign-ecosystem reference in this README).

---

## Branch policy

This branch is **Maven-first**. Python remains the canonical implementation. The full rules
are in [`JAVA_BRANCH_POLICY.md`](JAVA_BRANCH_POLICY.md); in short:

- No feature lands in Java without **Python parity vectors**.
- No API is marked complete without **parity proof**.
- **No stubs. No placeholders. No TODO implementations.**

See also the cleanup record: [`JAVA_BRANCH_AUDIT.md`](JAVA_BRANCH_AUDIT.md) ·
[`JAVA_CLEANUP_REPORT.md`](JAVA_CLEANUP_REPORT.md).

---

## Certification status

Each session ships a certification artifact with evidence:
[`java/SESSION_3_CERTIFICATION.md`](java/SESSION_3_CERTIFICATION.md) /
[`.json`](java/SESSION_3_CERTIFICATION.json),
[`java/foundation_certification.json`](java/foundation_certification.json), and the
branch-level [`JAVA_BRANCH_CERTIFICATION.md`](JAVA_BRANCH_CERTIFICATION.md). Every claim is
regenerated by execution (`mvn verify` + the manifest validator); nothing passes on the
strength of a report alone.

---

## Roadmap

Dependency-driven session order (see [`java/JAVA_PARITY_MATRIX.md`](java/JAVA_PARITY_MATRIX.md)
and [ROADMAP.md](ROADMAP.md)):

1. Extraction (HTML / document / repository) + `universal_extract`
2. Repository extraction
3. Document extraction
4. Semantic extraction (evidence layers, parsers)
5. Workflow layer
6. Vision
7. OCR

Each new API ships implemented-from-Python-canon, with golden vectors, parity tests, a
matrix entry, and a governance-validator update — never as a placeholder.

---

## Security

Authorized session material only — no credential cracking, no CAPTCHA/auth bypass. Report
vulnerabilities per [SECURITY.md](SECURITY.md).

---

## License

Apache 2.0 — [LICENSE](LICENSE)

<p align="center"><strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper.</strong></p>
