# WebWeaveX Agent Usage Guide

## Overview

WebWeaveX provides AI-agent friendly capabilities for integrating web intelligence into agent systems.

## Basic Usage

### Python

```python
from webweavex import WebWeaveX

wx = WebWeaveX()

# Standard extraction
result = wx.extract("Contact test@example.com or call 555-1234")
print(result.to_dict())

# Agent-friendly extraction
agent_result = wx.extract_agent("Contact test@example.com")
print(agent_result)
```

### Node.js

```javascript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();

// Standard extraction
const result = wx.extract("Contact test@example.com");

// Agent-friendly extraction
const agentResult = wx.extractAgent("Contact test@example.com");
```

## Agent Mode Output

The `extract_agent()` method returns structured output:

```python
{
    "task": "web_analysis",
    "input": "Contact test@example.com",
    "output": { /* WXP result */ },
    "summary": "Extracted 2 entities from text.",
    "actions": ["contact", "analyze"],
    "confidence": 0.5
}
```

### Fields

- **task**: Always "web_analysis"
- **input**: Input text (truncated to 500 chars)
- **output**: Full WXP result
- **summary**: Deterministic text summary
- **actions**: Suggested actions based on entities
- **confidence**: Score 0.0-1.0 based on entity density

## Memory Export

Export for memory systems (e.g., Mem0, OpenMemory):

```python
result = wx.extract(text)
memory = wx.to_memory_block(result)
# {
#   "type": "webweavex_memory",
#   "entities": [...],
#   "relations": [...],
#   "graph": {...},
#   "timestamp": "2024-01-01T00:00:00.000Z",
#   "source": "webweavex"
# }
```

## RAG Integration

Convert to RAG-ready chunks:

```python
result = wx.extract(document)
chunks = wx.to_rag_chunks(result)
# [
#   {
#     "text": "chunk text...",
#     "metadata": {
#       "entities": [...],
#       "relations": [...],
#       "source": "webweavex"
#     }
#   }
# ]
```

## Streaming

Progressive extraction for long documents:

```python
for stage in wx.extract_stream(text):
    print(f"Stage: {stage}")
# Output:
# Stage: cleaning
# Stage: chunking
# Stage: entities
# Stage: relations
# Stage: graph
# Stage: insights
```

## Tool Schema

OpenAI-compatible tool definitions:

```python
schema = WebWeaveX.get_tool_schema()
# {
#   "name": "webweavex_extract",
#   "description": "Extract structured intelligence from text",
#   "parameters": {
#     "type": "object",
#     "properties": {"input": {"type": "string"}},
#     "required": ["input"]
#   }
# }
```

## Capabilities Registry

Check available features:

```python
caps = WebWeaveX.get_capabilities()
# ["extract", "entities", "graph", "rag", "agent_mode", "memory_export", "streaming"]
```

## Pretty Print

Human-readable output:

```python
result = wx.extract(text)
print(wx.pretty_print(result))
# ==================================================
# WebWeaveX Analysis
# ==================================================
#
# ENTITY SUMMARY:
# ------------------------------
#   email:test@example.com: 1
#
# STATISTICS:
# ------------------------------
#   Total Entities: 1
#   Unique Entities: 1
# ...
```

## Error Handling

All methods are error-safe:

```python
result = wx.extract("")  # Returns valid empty result
# {
#   "meta": {"title": "", "url": ""},
#   "content": {"text": ""},
#   ...
# }

agent_result = wx.extract_agent(None)  # Returns error-safe result
# {
#   "task": "web_analysis",
#   "confidence": 0.0,
#   ...
# }
```

## Integration Examples

### OpenAI Function Calling

```python
import openai
from webweavex import WebWeaveX

wx = WebWeaveX()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Extract info from: Contact test@example.com"}],
    functions=[WebWeaveX.get_tool_schema()]
)
```

### Custom Agent

```python
class WebAgent:
    def __init__(self):
        self.wx = WebWeaveX()
    
    def process(self, text):
        agent_result = self.wx.extract_agent(text)
        
        if agent_result["confidence"] > 0.7:
            return self.wx.to_rag_chunks(agent_result["output"])
        
        return {"action": "analyze", "data": agent_result}
```
