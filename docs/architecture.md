# WebWeaveX Architecture

## Overview

WebWeaveX is a **cross-language universal web intelligence library** with deterministic output parity across Python, Node.js, Java, Kotlin, and Dart.

## Core Design Principles

1. **Python is Source of Truth** - Never modify other languages to fix issues; fix implementations to match Python
2. **Deterministic Output** - All outputs must be byte-for-byte identical across runs
3. **Cross-Language Parity** - All languages MUST produce identical JSON output
4. **Backward Compatible** - New features must be optional and non-breaking

## Pipeline Architecture

```
Input → Clean → Chunk → Entities → Relations → Graph → Insights → Output
```

### Stage Details

1. **Clean**: Normalize whitespace, trim, standardize text
2. **Chunk**: Split text into 500-char chunks with overlap
3. **Entities**: Extract using regex (email, URL, phone, number, capitalized)
4. **Relations**: Generate pairwise co-occurrence relations
5. **Graph**: Build node/edge structure from entities
6. **Insights**: Compute statistics and entity counts

## Schema (WXP v1)

```json
{
  "meta": {"title": "", "url": ""},
  "content": {"text": ""},
  "chunks": [],
  "entities": [],
  "relations": [],
  "graph": {"nodes": [], "edges": []},
  "insights": {
    "entity_counts": {},
    "stats": {},
    "top_entities": []
  }
}
```

## Language Implementations

### Python (Canonical)
- Location: `implementations/python/webweavex/`
- Package: `webweavex`

### Node.js
- Location: `implementations/node/`
- Package: `@webweavex/node`

### Java
- Location: `implementations/java/`
- Package: `com.webweavex`

### Kotlin
- Location: `implementations/kotlin/`
- Package: `com.webweavex`

### Dart
- Location: `implementations/dart/`
- Package: `webweavex`

## Validation System

The validation system runs comprehensive tests:
- Schema validation
- Determinism verification
- Cross-language parity
- Agent mode correctness
- Memory block format
- RAG chunk format
- Tool schema validity
- Error handling
- Streaming correctness
- Performance benchmarking

Run validation:
```bash
python core/test_runner/validate_full_system.py
```

## AI Agent Integration

WebWeaveX includes agent capabilities:
- `extract_agent()` - AI-friendly output with confidence scores
- `to_memory_block()` - Memory format for RAG systems
- `to_rag_chunks()` - RAG-ready text chunks
- `extract_stream()` - Progressive extraction
- Tool schemas for OpenAI compatibility
