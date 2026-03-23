# WebWeaveX

**Universal installable library for web intelligence**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/webweavex/webweavex)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

WebWeaveX is a **pure library** (like `requests`, `axios`, `numpy`) for web intelligence. It runs inside your projects, installs via package managers, and exposes functions/classes directly.

**WebWeaveX is NOT:**
- A backend server
- A framework
- A wrapper around other services
- A service with hidden processes

**WebWeaveX IS:**
- A standalone library
- Installable via pip, npm, Maven, Gradle, pub
- Deterministic and reproducible
- Cross-language consistent

---

## Features

- **Fetch**: HTTP fetching with retries and timeout
- **Parse**: HTML parsing with BeautifulSoup/cheerio/jsoup
- **Clean**: Text normalization and cleaning
- **Chunk**: Sliding window text chunking
- **Entities**: Regex-based entity extraction (email, URL, phone, etc.)
- **Graph**: Entity co-occurrence graph building
- **AI Engine**: Optional AI integration (OpenAI, OpenRouter, Groq, Ollama)
- **Agent System**: Lightweight tool-based agent

---

## Installation

### Python

```bash
pip install webweavex
```

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
result = wx.crawl("https://example.com")
print(result.text)
```

### Node.js

```bash
npm install webweavex
```

```typescript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();
const result = await wx.crawl("https://example.com");
console.log(result.text);
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
CrawlResult result = wx.crawl("https://example.com");
System.out.println(result.getText());
```

### Kotlin

```kotlin
// Gradle
implementation("com.webweavex:webweavex-kotlin:1.0.0")
```

```kotlin
import com.webweavex.WebWeaveX

val wx = WebWeaveX()
val result = wx.crawl("https://example.com")
println(result.text)
```

### Dart

```bash
dart pub add webweavex
```

```dart
import 'package:webweavex/webweavex.dart';

final wx = WebWeaveX();
final result = await wx.crawl('https://example.com');
print(result.text);
```

---

## API Reference

### Python

```python
from webweavex import WebWeaveX

wx = WebWeaveX()

# Crawl a URL
result = wx.crawl("https://example.com")

# Extract entities
entities = wx.entities("Contact test@example.com")

# Build entity graph
graph = wx.graph("Visit https://example.com")

# Clean text
cleaned = wx.clean("  Hello    World  ")

# Chunk text
chunks = wx.chunk("Long text...")

# Compare URLs
comparison = wx.compare(["https://example.com", "https://example.org"])

# Diff URLs
diff = wx.diff("https://example.com", "https://example.org")
```

### Node.js

```typescript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();

// Crawl a URL
const result = await wx.crawl("https://example.com");

// Extract entities
const entities = wx.entities("Contact test@example.com");

// Build entity graph
const graph = wx.graph("Visit https://example.com");
```

---

## Architecture

```
Pipeline: fetch → parse → clean → chunk → entities → graph
```

Each stage processes output from the previous stage, ensuring consistent data flow.

---

## Determinism

WebWeaveX guarantees **deterministic output**:
- All outputs are sorted
- No randomness in processing
- Stable JSON across runs
- Identical outputs guaranteed

---

## Configuration

WebWeaveX follows the `core/specs/wxp_v1.yaml` specification for all configuration. Default values:

```yaml
fetch:
  timeout: 10
  retries: 3

chunking:
  size: 500
  overlap: 50

cleaning:
  normalize_whitespace: true
```

---

## AI Integration

WebWeaveX includes optional AI support for:

- **OpenAI**: Set `OPENAI_API_KEY`
- **OpenRouter**: Set `OPENROUTER_API_KEY`
- **Groq**: Set `GROQ_API_KEY`
- **Ollama**: Local installation

AI is disabled by default and only activates when API keys are set.

---

## Agent System

Lightweight tool-based agent for task execution:

```python
wx = WebWeaveX()

# Execute task
result = wx.agent_task("crawl https://example.com")

# List available tools
tools = wx.list_agent_tools()
# ['crawl', 'rag', 'graph', 'compare', 'weave', 'diff']
```

---

## Testing

```bash
# Run Python tests
cd implementations/python
pip install -e .
pytest tests/

# Run cross-language tests
cd core/test_runner
python cross_language_runner.py
```

---

## Directory Structure

```
WebWeaveX/
├── core/
│   ├── specs/           # Canonical specification (wxp_v1.yaml)
│   ├── test_cases/      # Test cases
│   └── test_runner/     # Cross-language test runner
├── implementations/
│   ├── python/          # Python canonical implementation
│   ├── node/            # Node.js implementation
│   ├── java/            # Java implementation
│   ├── kotlin/           # Kotlin implementation
│   └── dart/            # Dart implementation
└── README.md
```

---

## Contributing

1. Follow the canonical spec (`core/specs/wxp_v1.yaml`)
2. Implement in all target languages
3. Ensure deterministic output
4. Pass cross-language tests

---

## License

MIT License - See LICENSE file for details.
