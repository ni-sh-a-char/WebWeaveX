# WebWeaveX Examples

This document provides usage examples for each supported language.

---

## Python Examples

### Basic Extraction

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
result = wx.extract("Contact test@example.com or call 555-1234")

# Access all fields
print(f"Title: {result.meta.title}")
print(f"URL: {result.meta.url}")
print(f"Text: {result.content.text}")
print(f"Entities: {result.entities}")
print(f"Graph: {result.graph}")
```

### Entity Extraction Only

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
entities = wx.entities("Email test@example.com or visit https://example.com")

for e in entities:
    print(f"Type: {e.type}, Value: {e.value}")
```

### Graph Building

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
graph = wx.graph("Contact test@example.com for support")

print(f"Nodes: {graph.nodes}")
print(f"Edges: {graph.edges}")
```

---

## Node.js Examples

### Basic Extraction

```javascript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();
const result = wx.extract("Contact test@example.com");

console.log(result.meta);
console.log(result.content);
console.log(result.entities);
```

### Async Usage

```javascript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();

// Using async/await (if supported by implementation)
const process = async () => {
    const result = wx.extract("Contact test@example.com");
    return result;
};
```

---

## Java Examples

### Basic Extraction

```java
import com.webweavex.WebWeaveX;
import java.util.Map;

public class Example {
    public static void main(String[] args) {
        WebWeaveX wx = new WebWeaveX();
        Map<String, Object> result = wx.extract("Contact test@example.com");
        
        Map<String, Object> meta = (Map<String, Object>) result.get("meta");
        Map<String, Object> content = (Map<String, Object>) result.get("content");
        System.out.println(content.get("text"));
    }
}
```

---

## Kotlin Examples

### Basic Extraction

```kotlin
import com.webweavex.WebWeaveX

fun main() {
    val wx = WebWeaveX()
    val result = wx.extract("Contact test@example.com")
    
    val content = result["content"] as? Map<*, *>
    println(content?.get("text"))
}
```

### Agent Mode

```kotlin
import com.webweavex.WebWeaveX

fun main() {
    val wx = WebWeaveX()
    val agentResult = wx.extractAgent("Contact test@example.com")
    
    println(agentResult["summary"])
    println(agentResult["confidence"])
}
```

---

## Dart Examples

### Basic Extraction

```dart
import 'package:webweavex/webweavex.dart';

void main() {
  final wx = WebWeaveX();
  final result = wx.extract('Contact test@example.com');
  
  print(result['content']);
}
```

### RAG Chunks

```dart
import 'package:webweavex/webweavex.dart';

void main() {
  final wx = WebWeaveX();
  final result = wx.extract('Contact test@example.com');
  final chunks = wx.toRagChunks(result);
  
  for (final chunk in chunks) {
    print(chunk['text']);
  }
}
```

---

## Advanced Examples

### Cross-Language Consistency

All implementations produce identical output:

```python
# Python
result = wx.extract("Contact test@example.com")
print(result.to_json())
```

```javascript
// JavaScript
const result = wx.extract("Contact test@example.com");
console.log(JSON.stringify(result));
```

Both produce the same JSON structure with identical entity ordering.

### RAG Pipeline Integration

```python
from webweavex import WebWeaveX
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

wx = WebWeaveX()
result = wx.extract(document_text)

# Get RAG-ready chunks
chunks = wx.to_rag_chunks(result)

# Embed for vector search
embeddings = OpenAIEmbeddings()
texts = [c['text'] for c in chunks]
vectors = embeddings.embed_documents(texts)
```

### Memory System Export

```python
from webweavex import WebWeaveX
import json

wx = WebWeaveX()
result = wx.extract(text)

# Export to memory system format
memory = wx.to_memory_block(result)

# For Mem0, OpenMemory, etc.
print(json.dumps(memory))
```

---

## Performance Examples

### Batch Processing

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
documents = ["doc1 text...", "doc2 text...", "doc3 text..."]

for doc in documents:
    result = wx.extract(doc)
    # Process result
```

### Streaming Large Documents

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
large_document = "..." * 10000

for stage in wx.extract_stream(large_document):
    print(f"Processing: {stage}")
    # Update progress UI
```

---

## Error Handling

All methods are error-safe:

```python
from webweavex import WebWeaveX

wx = WebWeaveX()

# Empty input
result = wx.extract("")
# Returns valid empty structure

# Invalid input  
result = wx.extract(None)
# Returns valid empty structure

# Agent mode with bad input
agent_result = wx.extract_agent("")
# Returns: {"confidence": 0.0, "summary": "...", ...}
```
