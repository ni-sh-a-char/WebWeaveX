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
  <img src="https://img.shields.io/badge/JVM-11+-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="JVM 11+"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/></a>
  <img src="https://img.shields.io/badge/tests-133%20passing-22c55e?style=flat-square" alt="Tests passing"/>
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

<p align="center">
  <br/>
</p>

---

## Contents

- [What is WebWeaveX?](#what-is-webweavex)
- [Humans and AI agents](#humans-and-ai-agents)
- [Core capabilities](#core-capabilities)
- [Architecture](#architecture)
- [Quick start](#quick-start)
- [Code examples](#code-examples)
- [Determinism](#determinism)
- [Cross-language parity](#cross-language-parity)
- [Performance](#performance)
- [API reference](#api-reference)
- [Comparison](#comparison)
- [Installation](#installation)
- [Contributing](#contributing)
- [Security](#security-model)
- [License](#license)

---

## What is WebWeaveX?

> **WebWeaveX is to runtime state what Git is to source code: deterministic, replayable, reconstructable, and auditable.**

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** operating on authenticated software. It captures how systems actually run—browser DOM, sessions, Electron, native UI, workflows, connectors—and compiles **replay-safe runtime graphs** with **Kaalka-encrypted persistence** (`webweavex-formula+kaalka@5.0.0`).

This is **not** a scraping library or LLM wrapper. It is an **operational runtime substrate** for extraction, memory, execution, reconstruction, and replay equivalence.

---

## Humans and AI agents

**WebWeaveX is designed for both humans and AI agents.**

| Audience | Use |
|----------|-----|
| **Engineers** | Inspect authenticated systems, preserve workflows, audit runtime behavior |
| **AI agents** | Maintain continuity, deterministic state, replay-safe memory, environment reconstruction |

Same APIs, same determinism contract, same honesty about authorization.

---

## Core capabilities

| Capability | Description |
|------------|-------------|
| **Extraction** | Bounded HTML/Markdown/JSON extraction with deterministic output |
| **Query engine** | Typed queries, metadata filters, graph traversal, deterministic ranking |
| **Workflow execution** | DAG scheduling, topological ordering, deterministic replay |
| **Memory fabric** | Deterministic memory store with stable fingerprints |
| **Replay** | Snapshot creation, equivalence validation, deterministic verification |
| **Repository analysis** | Language detection (27 extensions, 12 manifest types), dependency extraction |
| **Knowledge graph** | Entity relationships, semantic search, graph validation |
| **Fingerprinting** | SHA-256 deterministic fingerprints, byte-identical cross-language |
| **Canonical serialization** | Deterministic JSON with stable key ordering |
| **Deterministic clock** | LogicalClock, ReplayClock, TestClock—no wall-clock drift |
| **Search indexing** | Token/type/field inverted index with O(1) NodeLookup |
| **Query sessions** | Prepared index reuse across multiple queries |

---

## Architecture

```text
┌──────────────────┐
│    UniversalInput│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ RuntimeKernel    │
│ extract()        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ExtractionPipeline│
│ HTML/JSON/MD     │
└────────┬─────────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌────────┐┌──────────┐┌──────────┐
│Knowledge││QueryEngine││SearchIdx │
│ Graph  ││Session    ││NodeLookup│
└───┬────┘└────┬─────┘└────┬─────┘
    │          │            │
    └──────────┼────────────┘
               ▼
      ┌─────────────────┐
      │CanonicalSerializ│
      │  Fingerprint    │
      └────────┬────────┘
               ▼
      ┌─────────────────┐
      │   ReplayEngine  │
      │   MemoryEngine  │
      └─────────────────┘
```

### Source layout

```
kotlin/src/main/kotlin/io/webweavex/
├── runtime/          # RuntimeKernel, DeterministicClock, configs
├── extract/          # ExtractionPipeline, HTML/JSON/Markdown extractors
├── repository/       # QueryEngine, QuerySession, SearchIndex, NodeLookup
├── graph/            # KnowledgeGraph
├── workflow/         # WorkflowEngine, DAG scheduler
├── memory/           # MemoryEngine, deterministic memory
├── replay/           # ReplayEngine, snapshot validation
├── fingerprint/      # SHA-256 fingerprinting
├── serialization/    # Canonical JSON serialization
├── determinism/      # Clock abstractions
├── fetch/            # HTTP transport, crawler
└── exceptions/       # Typed exception hierarchy
```

---

## Quick start

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

### Five-minute tutorial

```kotlin
import io.webweavex.runtime.*
import io.webweavex.repository.*
import io.webweavex.extract.ExtractionPipeline
import io.webweavex.extract.ExtractionRequest

// 1. Create the runtime kernel
val kernel = RuntimeKernel.create()

// 2. Extract content
val input = UniversalInput(source = "<html><h1>Hello WebWeaveX</h1></html>")
val output = kernel.extract(input)
println("Fingerprint: ${output.fingerprint}")
println("Version: ${output.version}")

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

// 5. Query metrics
val metrics = session.metrics()
println("Queries: ${metrics.totalQueries}, Indexed: ${metrics.indexedQueries}")

// 6. Deterministic fingerprinting
val fingerprint = Fingerprint.compute(mapOf("version" to "3.0.0"))
println("Fingerprint: $fingerprint")
```

---

## Code examples

<details>
<summary><strong>Query engine, workflow, memory, replay, repository analysis</strong></summary>

### Query engine with prepared index

```kotlin
import io.webweavex.repository.*

val graph = KnowledgeGraph(nodes, edges)
val session = QuerySession(graph)

// Indexed search (uses prepared SearchIndex)
val results = session.search("kotlin")
println("Found ${results.totalMatches} results in ${results.indexed}")

// Type filtering
val files = session.filterByType("file")

// Relationship queries
val imports = session.findByRelationship("imports")

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
println("Success: ${result.success}, Steps: ${result.executedSteps.size}")
```

### Memory engine

```kotlin
import io.webweavex.memory.*

var store = MemoryEngine.create()
store = store.put("context", mapOf("user" to "agent", "task" to "analysis"))
store = store.put("results", listOf("item1", "item2"))

val context = store.get("context")
println("Context: $context")
```

### Replay engine

```kotlin
import io.webweavex.replay.*

val state = mapOf("step" to 1, "data" to "processing")
val snapshot = ReplayEngine.createSnapshot(state, stepIndex = 0)

println("Fingerprint: ${snapshot.fingerprint}")
println("State: ${snapshot.state}")
```

### Repository analysis

```kotlin
import io.webweavex.repository.*

val summary = RepositoryAnalyzerEngine.analyze(File("./my-project"))
println("Files: ${summary.totalFiles}")
println("Languages: ${summary.languages}")
println("Dependencies: ${summary.dependencies}")
```

### Deterministic fingerprinting

```kotlin
import io.webweavex.fingerprint.*

val data = mapOf("key" to "value", "version" to "3.0.0")
val fp = Fingerprint.compute(data)
println("Fingerprint: $fp")  // Always identical for same input
```

</details>

---

## Determinism

WebWeaveX guarantees deterministic behavior across runs:

| Mechanism | Purpose |
|-----------|---------|
| `DeterministicClock` | No wall-clock drift—LogicalClock, ReplayClock, TestClock |
| `CanonicalSerialization` | Stable JSON with sorted keys |
| `Fingerprint.compute()` | SHA-256 deterministic hash |
| `SearchIndex.build()` | Deterministic index construction |
| `QuerySession` | Prepared index reuse—identical queries yield identical results |
| `WorkflowEngine` | Topological sort with stable ordering |
| `ReplayEngine` | Snapshot validation and equivalence checking |

**Cross-language parity:** Serialization and fingerprinting vectors are byte-identical with Python, JavaScript, Dart, and Java SDKs (1012 vectors verified).

---

## Cross-language parity

WebWeaveX ships across five language implementations with verified parity:

| Feature | Python | JavaScript | Dart | Java | Kotlin |
|---------|--------|------------|------|------|--------|
| Extraction | Yes | Yes | Yes | Yes | Yes |
| Query Engine | Yes | Yes | Yes | Yes | Yes |
| Workflow | Yes | Yes | Yes | Yes | Yes |
| Memory | Yes | Yes | Yes | Yes | Yes |
| Replay | Yes | Yes | Yes | Yes | Yes |
| Fingerprinting | Yes | Yes | Yes | Yes | Yes |
| Serialization | Yes | Yes | Yes | Yes | Yes |
| Determinism | Yes | Yes | Yes | Yes | Yes |
| Knowledge Graph | Yes | Yes | Yes | Yes | Yes |
| Repository Analysis | Yes | Yes | Yes | Yes | Yes |

| Metric | Result |
|--------|--------|
| Serialization vectors | 1012 byte-identical |
| Fingerprinting vectors | 1012 byte-identical |
| Total SDK tests | 1084+ |

---

## Performance

| Workload | Result |
|----------|--------|
| Index build (1000 nodes) | <100ms |
| Query session (100 queries) | <5s total |
| Indexed query latency | O(log n) token lookup |
| NodeLookup resolution | O(1) hash map |
| Memory footprint | Minimal—immutable structures |

Benchmark methodology: Kotlin 1.9.22, Gradle 7.6.5, JVM 11+, Windows/Linux.

---

## API reference

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
| `CanonicalSerialization` | Deterministic JSON serialization |
| `ExtractionPipeline` | HTML/Markdown/JSON extraction |
| `RepositoryAnalyzerEngine` | Repository analysis and language detection |
| `DeterministicClock` | Clock abstractions (Logical/Replay/Test) |

### QueryEngine

```kotlin
// Search with automatic index building
QueryEngine.search(graph, "query")

// Search with prepared index (no rebuild)
QueryEngine.searchWithIndex("query", searchIndex)

// Type filtering
QueryEngine.filterByType(graph, "file")

// Relationship queries
QueryEngine.findByRelationship(graph, "imports")

// Boolean queries
QueryEngine.booleanQuery(graph, must = listOf("a"), mustNot = listOf("b"))
```

### QuerySession

```kotlin
// Create session (builds index once)
val session = QuerySession(graph)

// Reuse across many queries
val r1 = session.search("query1")
val r2 = session.search("query2")

// Check metrics
val m = session.metrics()
println("Queries: ${m.totalQueries}, Indexed: ${m.indexedQueries}")

// Index statistics
val stats = session.indexStatistics()
```

---

## Comparison

| Tool | Primary Focus |
|------|---------------|
| Playwright | Browser automation |
| Scrapy | Crawling |
| BeautifulSoup | HTML parsing |
| LangChain | LLM orchestration |
| CrewAI | Agent orchestration |
| **WebWeaveX Kotlin** | **Deterministic runtime cognition infrastructure** |

---

## Installation

### Requirements

- Kotlin 1.9+
- JVM 11+
- Gradle 7.6+ or Maven 3.6+

### Gradle

```kotlin
dependencies {
    implementation("io.webweavex:webweavex-kotlin:3.0.0")
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

### Verify installation

```kotlin
import io.webweavex.runtime.RuntimeKernel

val kernel = RuntimeKernel.create()
println(kernel.version) // 3.0.0
```

---

## Validation

| Check | Result |
|-------|--------|
| Tests | 133 passing |
| Build | Gradle clean build successful |
| Determinism | All clock/serialization/fingerprint paths deterministic |
| Cross-language parity | Serialization + fingerprinting byte-identical |
| API review | All public APIs frozen and documented |

```bash
cd kotlin
gradle clean test
```

---

## Security model

| Control | Implementation |
|---------|----------------|
| No arbitrary eval | Deterministic execution paths |
| Bounded extraction | Configurable limits |
| Deterministic persistence | Kaalka-compatible checkpoints |
| Encrypted memory | Deterministic fingerprinting |
| Replay-safe recovery | Snapshot validation |

See [SECURITY.md](SECURITY.md). Report issues responsibly.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

| Rule | Requirement |
|------|-------------|
| Determinism | No `System.currentTimeMillis()`, `Math.random()`, or `UUID.randomUUID()` in runtime paths |
| Replay safety | Preserve graph normalization semantics |
| Canonical pipeline | Single execution path |
| Tests | `gradle test` must pass |
| Kotlin style | Kotlin idioms, immutable data classes, no unnecessary mutation |

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

- Deeper native JVM integrations
- Expanded connector ecosystems
- Stronger replay guarantees
- Larger runtime memory fabrics
- Distributed operational cognition

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

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
