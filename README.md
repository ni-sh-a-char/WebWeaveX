# WebWeaveX — Universal Intelligence Interface Layer (UIL)

**A deterministic, cross-language web intelligence library for AI-native infrastructure.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/PIYUSH-MISHRA-00/WebWeaveX)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-yellow)](implementations/python)
[![Node.js](https://img.shields.io/badge/node-18+-yellow)](implementations/node)
[![Java](https://img.shields.io/badge/java-11+-yellow)](implementations/java)
[![Kotlin](https://img.shields.io/badge/kotlin-1.9+-yellow)](implementations/kotlin)
[![Dart](https://img.shields.io/badge/dart-3.0+-yellow)](implementations/dart)

---

## Vision

WebWeaveX establishes a **global standard** for web intelligence extraction — a universal interface layer (UIL) that provides deterministic, AI-agent compatible extraction across all major programming languages.

---

## What is WebWeaveX?

WebWeaveX is a **production-grade library** (like `requests`, `numpy`, `axios`) for extracting structured intelligence from text and web content. It runs inside your applications, installs via package managers, and exposes clean APIs.

**WebWeaveX is NOT:**
- A backend server
- A framework
- A wrapper around external APIs
- A service with hidden processes

**WebWeaveX IS:**
- A standalone library (installable via pip, npm, Maven, Gradle, pub)
- Deterministic — same input always produces identical output
- Cross-language consistent — Python, Node.js, Java, Kotlin, Dart produce matching results
- AI-agent ready — built for LLM integration, RAG pipelines, and autonomous agents
- Production-ready — fully validated with 35+ automated tests

---

## Features

| Feature | Description |
|---------|-------------|
| **Extract** | Full pipeline: fetch → parse → clean → chunk → extract |
| **Entities** | Regex-based extraction: email, URL, phone, number, capitalized |
| **Graph** | Entity co-occurrence graph with nodes and edges |
| **Insights** | Statistics: entity counts, types, word count, text length |
| **Agent Mode** | AI-friendly output with confidence scores and action suggestions |
| **Memory Blocks** | Export format for memory systems (Mem0, OpenMemory) |
| **RAG Chunks** | RAG-ready text chunks with entity metadata |
| **Streaming** | Progressive extraction for long documents |
| **Tool Schema** | OpenAI-compatible function definitions |

---

## Installation

### Python

```bash
pip install webweavex
```

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
result = wx.extract("Contact test@example.com or call 555-1234")
print(result.to_dict())
```

### Node.js

```bash
npm install webweavex
```

```javascript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();
const result = wx.extract("Contact test@example.com or call 555-1234");
console.log(result);
```

### Java

```xml
<dependency>
    <groupId>com.webweavex</groupId>
    <artifactId>webweavex</artifactId>
    <version>1.0.0</version>
</dependency>
```

```java
import com.webweavex.WebWeaveX;

WebWeaveX wx = new WebWeaveX();
Map<String, Object> result = wx.extract("Contact test@example.com");
```

### Kotlin

```kotlin
// Gradle
implementation("com.webweavex:webweavex:1.0.0")
```

```kotlin
import com.webweavex.WebWeaveX

val wx = WebWeaveX()
val result = wx.extract("Contact test@example.com")
```

### Dart

```bash
dart pub add webweavex
```

```dart
import 'package:webweavex/webweavex.dart';

final wx = WebWeaveX();
final result = wx.extract('Contact test@example.com');
```

---

## Quick Usage

### Standard Extraction

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
result = wx.extract("""
    Contact us at support@example.com or visit https://example.com.
    Call +1-555-123-4567 for immediate assistance.
""")

# Access results
print(result.meta)      # {"title": "", "url": ""}
print(result.content)   # {"text": "..."}
print(result.entities)  # [{"type": "email", "value": "..."}, ...]
print(result.graph)     # {"nodes": [...], "edges": [...]}
```

### Agent Mode (AI-Friendly)

```python
agent_result = wx.extract_agent("Contact test@example.com")
# Returns:
# {
#   "task": "web_analysis",
#   "input": "...",
#   "output": {...},
#   "summary": "Extracted 2 entities from text.",
#   "actions": ["contact", "analyze"],
#   "confidence": 0.45
# }
```

### Memory Blocks (for RAG Systems)

```python
memory = wx.to_memory_block(result)
# {
#   "type": "webweavex_memory",
#   "entities": [...],
#   "relations": [...],
#   "graph": {...},
#   "timestamp": "2026-01-01T00:00:00Z",
#   "source": "webweavex"
# }
```

### RAG Chunks

```python
chunks = wx.to_rag_chunks(result)
# [
#   {
#     "text": "...",
#     "metadata": {
#       "entities": [...],
#       "relations": [...],
#       "source": "webweavex"
#     }
#   }
# ]
```

### Streaming

```python
for stage in wx.extract_stream(text):
    print(f"Stage: {stage}")
# cleaning → chunking → entities → relations → graph → insights
```

### Tool Schema (OpenAI Integration)

```python
schema = WebWeaveX.get_tool_schema()
# {
#   "name": "webweavex_extract",
#   "description": "Extract structured intelligence from text",
#   "parameters": {...}
# }
```

---

## Validation

Run the full validation suite:

```bash
python core/test_runner/validate_full_system.py
```

**Validation covers:**
- Schema correctness
- Determinism (10 identical runs)
- Cross-language parity (Python ↔ Node ↔ Java ↔ Kotlin ↔ Dart)
- Agent mode output
- RAG chunk format
- Memory block format
- Tool schema validity
- Error handling safety
- Streaming correctness
- Performance (<5s for 100 runs)

**Current Status:** 35/35 tests passing (100%)

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/architecture.md](docs/architecture.md) | System design and pipeline overview |
| [docs/schema.md](docs/schema.md) | WXP v1 output schema specification |
| [docs/agent_usage.md](docs/agent_usage.md) | AI agent integration guide |
| [docs/installation.md](docs/installation.md) | Detailed installation per language |
| [docs/examples.md](docs/examples.md) | Usage examples per language |
| [docs/contributing.md](docs/contributing.md) | Contribution guidelines |
| [docs/security.md](docs/security.md) | Security policy |

---

## Architecture

```
Input → Clean → Chunk → Entities → Relations → Graph → Insights → Output
```

Each stage processes the previous stage's output, ensuring consistent data flow.

---

## Determinism Guarantees

WebWeaveX guarantees **byte-identical output** across:
- Multiple runs (same input → same output)
- All implementations (Python = Node = Java = Kotlin = Dart)
- Sorted ordering (entities by type/value, relations by source/target)

---

## License

Apache License 2.0 — See [LICENSE](LICENSE) file for details.

---

## Vision Statement

WebWeaveX aims to become the **universal interface layer** for web intelligence — a zero-dependency, deterministic engine that any AI system can use to understand web content.

**Mission:** Make structured web intelligence accessible, consistent, and reliable across every programming language.

---

## Support

- **Issues:** https://github.com/PIYUSH-MISHRA-00/WebWeaveX/issues
- **Discussions:** https://github.com/PIYUSH-MISHRA-00/WebWeaveX/discussions

---

**WebWeaveX** — *Universal Intelligence Interface Layer*
