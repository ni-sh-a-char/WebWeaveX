<p align="center">
  <br/>
  <img src="https://img.shields.io/badge/WebWeaveX-v3.0.0-0f172a?style=for-the-badge&logo=kotlin&logoColor=white" alt="WebWeaveX v3.0.0"/>
  <br/><br/>
  <strong>Production-grade deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
  <br/>
  <em>Operational runtime substrate · Maven Central · replay-safe · Kaalka v5 parity</em>
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Kotlin-1.9+-7F52FF?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin 1.9+"/>
  <img src="https://img.shields.io/badge/JVM-17+-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="JVM 17+"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/></a>
  <img src="https://img.shields.io/badge/tests-183%20passing-22c55e?style=flat-square" alt="Tests passing"/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?style=flat-square" alt="Build passing"/>
  <img src="https://img.shields.io/badge/deterministic%20runtime-0ea5e9?style=flat-square" alt="Deterministic runtime"/>
  <img src="https://img.shields.io/badge/replay--safe-14b8a6?style=flat-square" alt="Replay-safe"/>
  <img src="https://img.shields.io/badge/Kaalka-verified-7c3aed?style=flat-square" alt="Kaalka verified"/>
  <img src="https://img.shields.io/badge/production%20ready-15803d?style=flat-square" alt="Production ready"/>
  <img src="https://img.shields.io/badge/OSS-infrastructure-64748b?style=flat-square" alt="Open Source"/>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20WebWeaveX-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

---

## Table of Contents

- [What is WebWeaveX?](#what-is-webweavex)
- [Why AI agents need this](#why-ai-agents-need-this)
- [What makes it different](#what-makes-it-different)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Code Examples](#code-examples)
- [Determinism](#determinism)
- [Cross-Language Parity](#cross-language-parity)
- [Performance](#performance)
- [API Reference](#api-reference)
- [Comparison](#comparison)
- [Security](#security-model)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Roadmap](#roadmap)
- [License](#license)

---

## What is WebWeaveX?

> **WebWeaveX is to runtime state what Git is to source code: deterministic, replayable, reconstructable, and auditable.**

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** operating on authenticated software. It captures how systems actually run—browser DOM, sessions, Electron, native UI, workflows, connectors—and compiles **replay-safe runtime graphs** with **Kaalka-encrypted persistence** (`webweavex-formula+kaalka@5.0.0`).

This is **not** a scraping library or LLM wrapper. It is an **operational runtime substrate** for extraction, memory, execution, reconstruction, and replay equivalence.

---

## Why AI agents need this

| Agent Failure Mode | Operational Impact | WebWeaveX Capability |
|--------------------|--------------------|----------------------|
| Lost browser state | Re-authentication | Runtime continuation |
| Lost workflow context | Restart execution | Runtime memory fabric |
| DOM instability | Broken selectors | DOM stabilization |
| Replay drift | Non-repeatable behavior | Replay equivalence |
| Session expiration | Lost progress | Encrypted persistence |

WebWeaveX provides a deterministic runtime layer beneath agents so operational state becomes persistent, replayable, and auditable.

---

## What makes it different

| Tool | Primary Focus |
|------|---------------|
| Playwright | Browser automation |
| Selenium | Browser automation |
| BeautifulSoup | HTML parsing |
| **WebWeaveX** | **Deterministic runtime cognition infrastructure** |

WebWeaveX does not replace these tools. It provides deterministic runtime infrastructure that can sit beneath them.

---

## Architecture

```text
Input -> Canonical Pipeline -> Graph + Memory -> Replay Check -> Reconstruction
                 |
        Normalization + Kaalka v5
```

Layered source layout (`src/main/kotlin/io/webweavex/`):

| Layer | Packages |
|-------|----------|
| crypto | KaalkaV5 (encryption, time-key derivation) |
| determinism | Normalization, StableSerialize, CanonicalJson |
| fingerprint | SHA-256 hashing, Kaalka graph fingerprinting |
| runtime | RuntimeKernel, DeterministicClock, data model |
| extract | ExtractionPipeline, HTML/JSON/Markdown extractors |
| repository | QueryEngine, QuerySession, SearchIndex, NodeLookup |
| graph | RuntimeGraph with fingerprinting |
| memory | MemoryStore, MemoryEntry, MemoryEngine |
| replay | ReplayEngine, ReplaySnapshot |
| workflow | WorkflowEngine (DAG scheduling) |
| fetch | HttpTransport, Crawler |
| exceptions | 8 typed exception classes |

---

## Installation

### Gradle (Kotlin DSL)

```kotlin
repositories {
    mavenCentral()
}

dependencies {
    implementation("io.webweavex:webweavex-kotlin:3.0.0")
}
```

### Gradle (Groovy)

```groovy
repositories {
    mavenCentral()
}

dependencies {
    implementation 'io.webweavex:webweavex-kotlin:3.0.0'
}
```

### Maven

```xml
<dependency>
    <groupId>io.webweavex</groupId>
    <artifactId>webweavex-kotlin</artifactId>
    <version>3.0.0</version>
</dependency>
```

### Requirements

- Kotlin 1.9+
- JVM 17+
- Gradle 7.6+ or Maven 3.6+

---

## Quick Start

```kotlin
import io.webweavex.runtime.*
import io.webweavex.repository.*
import io.webweavex.fingerprint.Fingerprint

fun main() {
    // 1. Create the runtime kernel
    val kernel = RuntimeKernel.create()

    // 2. Extract content
    val input = UniversalInput(source = "<html><h1>Hello WebWeaveX</h1></html>")
    val output = kernel.extract(input)
    println("Fingerprint: ${output.fingerprint}")

    // 3. Build a knowledge graph
    val graph = KnowledgeGraph(
        nodes = listOf(
            KnowledgeNode("file1", "file", mapOf("name" to "Main.kt")),
            KnowledgeNode("mod1", "module", mapOf("name" to "core")),
        ),
        edges = listOf(KnowledgeEdge("file1", "mod1", "imports"))
    )

    // 4. Create a query session with prepared index
    val session = QuerySession(graph)
    val results = session.search("Main")
    println("Found ${results.totalMatches} matches")

    // 5. Deterministic fingerprinting
    val fingerprint = Fingerprint.compute(mapOf("version" to "3.0.0"))
    println("Fingerprint: $fingerprint")
}
```

---

## Code Examples

<details>
<summary><strong>Query engine, workflow, memory, replay, repository analysis</strong></summary>

### Query engine with prepared index

```kotlin
import io.webweavex.repository.*

val graph = KnowledgeGraph(nodes, edges)
val session = QuerySession(graph)

// Indexed search
val results = session.search("kotlin")
println("Found ${results.totalMatches} results in ${results.indexed}")

// Type filtering
val files = session.filterByType("file")

// Boolean queries
val specific = QueryEngine.booleanQuery(
    graph,
    must = listOf("kotlin"),
    mustNot = listOf("java")
)
```

### Workflow execution

```kotlin
import io.webweavex.workflow.*

val steps = listOf(
    WorkflowStep("fetch", { mapOf("url" to "https://example.com") }),
    WorkflowStep("parse", { mapOf("parsed" to true) }, dependsOn = listOf("fetch")),
    WorkflowStep("store", { mapOf("stored" to true) }, dependsOn = listOf("parse"))
)

val result = WorkflowEngine.execute(steps, emptyMap())
println("Success: ${result.success}, Steps: ${result.executionOrder.size}")
```

### Memory engine

```kotlin
import io.webweavex.memory.*

var store = MemoryEngine.create()
store = store.put("context", mapOf("user" to "agent", "task" to "analysis"))
val context = store.get("context")
println("Context: $context")
```

### Replay engine

```kotlin
import io.webweavex.replay.*

val state = mapOf("step" to 1, "data" to "processing")
val snapshot = ReplayEngine.createSnapshot(state, stepIndex = 0)
println("Fingerprint: ${snapshot.fingerprint}")
```

### Repository analysis

```kotlin
import io.webweavex.repository.*

val summary = RepositoryAnalyzerEngine.analyze(java.io.File("."))
println("Files: ${summary.totalFiles}")
println("Languages: ${summary.languages}")
```

### Deterministic fingerprinting

```kotlin
import io.webweavex.fingerprint.*

val data = mapOf("key" to "value", "version" to "3.0.0")
val fp = Fingerprint.compute(data)
println("Fingerprint: $fp")  // Always identical for same input
```

### Kaalka encryption

```kotlin
import io.webweavex.crypto.KaalkaV5

val encrypted = KaalkaV5.encryptValue(mapOf("secret" to "data"), "my-key")
val decrypted = KaalkaV5.decryptValue(encrypted["encrypted"] as String, "my-key")
println("Decrypted: ${decrypted["decrypted"]}")
```

</details>

---

## Determinism

| Mechanism | Purpose |
|-----------|---------|
| `DeterministicClock` | No wall-clock drift - LogicalClock, ReplayClock, TestClock |
| `StableSerialize` | Deterministic JSON with sorted keys |
| `Fingerprint.compute()` | SHA-256 deterministic hash |
| `SearchIndex.build()` | Deterministic index construction |
| `QuerySession` | Prepared index reuse - identical queries yield identical results |
| `WorkflowEngine` | Topological sort with stable ordering |
| `ReplayEngine` | Snapshot validation and equivalence checking |
| `KaalkaV5` | Deterministic encryption for identity |

---

## Cross-Language Parity

| Feature | Python | JavaScript | Dart | Kotlin | Java |
|---------|:------:|:----------:|:----:|:------:|:----:|
| Serialization | Yes | Yes | Yes | Yes | Yes |
| Normalization | Yes | Yes | Yes | Yes | Yes |
| Fingerprinting | Yes | Yes | Yes | Yes | Yes |
| Replay | Yes | Yes | Yes | Yes | Yes |
| Determinism | Yes | Yes | Yes | Yes | Yes |
| Kaalka v5 | Yes | Yes | Yes | Yes | N/A |

| Metric | Result |
|--------|--------|
| Serialization vectors | 1012 byte-identical |
| Fingerprinting vectors | 1012 byte-identical |
| Total SDK tests | 1886+ |

---

## Performance

| Workload | Result |
|----------|:------:|
| Stable serialize (100k ops) | <10s |
| Fingerprint (100k ops) | <10s |
| Kaalka encrypt (100k ops) | <15s |
| Graph fingerprint (100k ops) | <15s |
| Replay snapshot (100k ops) | <10s |
| Query session (1000 queries) | <5s |
| Large workflow (500 steps) | <1s |

Benchmark methodology: Kotlin 1.9.22, JVM 17, Gradle 7.6.5, Windows/Linux.

---

## API Reference

### Core types

| Type | Description |
|------|-------------|
| `RuntimeKernel` | Central orchestrator for extraction |
| `UniversalInput` / `UniversalOutput` | Standardized I/O |
| `KnowledgeGraph` | Entity-relationship graph |
| `QueryEngine` | Search with indexed and fallback paths |
| `QuerySession` | Reusable query session with prepared index |
| `SearchIndex` | Token/type/field inverted index |
| `NodeLookup` | O(1) ID-based node resolution |
| `QueryPlanner` | Deterministic strategy selection |
| `WorkflowEngine` | DAG workflow execution |
| `MemoryEngine` | Deterministic key-value memory |
| `ReplayEngine` | Snapshot creation and validation |
| `Fingerprint` | SHA-256 deterministic hashing |
| `StableSerialize` | Deterministic JSON serialization |
| `KaalkaV5` | Deterministic encryption |
| `ExtractionPipeline` | HTML/Markdown/JSON extraction |

---

## Comparison

| Tool | Primary Focus |
|------|---------------|
| Playwright | Browser automation |
| Selenium | Browser automation |
| BeautifulSoup | HTML parsing |
| LangChain | LLM orchestration |
| CrewAI | Agent orchestration |
| **WebWeaveX Kotlin** | **Deterministic runtime cognition infrastructure** |

---

## Security Model

| Control | Implementation |
|---------|----------------|
| No arbitrary eval | Deterministic execution paths |
| Bounded extraction | Configurable limits |
| Deterministic persistence | Kaalka-compatible checkpoints |
| Deterministic clock | No wall-clock in core path |

See [SECURITY.md](SECURITY.md). Report issues responsibly.

---

## Contributing

Before opening a PR, run the full gate sequence:

```bash
./gradlew clean test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## FAQ

**What is Kaalka?**
Kaalka is a deterministic cryptographic persistence substrate. `kaalka@5.0.0` provides byte-identical encrypted values across Python, JavaScript, Dart, and Kotlin.

**Why deterministic?**
Determinism enables audit, replay proofs, cross-run diffing, and agent continuity. Without it, operational systems cannot be trusted as engineering substrates.

**Does this replace Playwright?**
No. WebWeaveX provides deterministic runtime infrastructure. Playwright provides browser automation. They serve different purposes and can work together.

**Can AI agents use this?**
Yes. Every output is a bounded, deterministic, evidence-carrying IR that agents can hash, diff, replay, and reason over.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

---

## License

Apache License 2.0 — [LICENSE](LICENSE)

---

<p align="center">
  <strong>WebWeaveX is deterministic runtime cognition infrastructure — not a disposable scraper, not AGI hype, not an LLM wrapper.</strong>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-piyushmishra00-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>
