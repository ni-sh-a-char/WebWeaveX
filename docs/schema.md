# WebWeaveX Schema Specification

## Version: WXP v1

## Output Schema

All WebWeaveX implementations MUST produce output conforming to this exact schema.

```json
{
  "meta": {
    "title": "",
    "url": ""
  },
  "content": {
    "text": ""
  },
  "chunks": [
    {
      "text": "",
      "index": 0,
      "start": 0,
      "end": 500
    }
  ],
  "entities": [
    {
      "type": "email|url|phone|number|capitalized",
      "value": ""
    }
  ],
  "relations": [
    {
      "source": "type:value",
      "target": "type:value",
      "type": "cooccurrence"
    }
  ],
  "graph": {
    "nodes": [
      {
        "id": "type:value",
        "type": "",
        "value": ""
      }
    ],
    "edges": [
      {
        "source": "",
        "target": "",
        "weight": 1
      }
    ]
  },
  "insights": {
    "entity_counts": {},
    "stats": {
      "total_entities": 0,
      "unique_entities": 0,
      "entity_types": 0,
      "total_relations": 0,
      "total_chunks": 0,
      "text_length": 0,
      "word_count": 0
    },
    "top_entities": [
      {
        "type": "",
        "value": "",
        "count": 0
      }
    ]
  }
}
```

## Key Requirements

### JSON Key Order

Keys MUST be in alphabetical order:
1. chunks, content, entities, graph, insights, meta, relations

### Entity Types

- `email` - Email addresses
- `url` - HTTP/HTTPS URLs
- `phone` - Phone numbers
- `number` - Numeric values
- `capitalized` - Capitalized words

### Sorting Rules

- **entities**: sort by (type, value)
- **relations**: sort by (source, target)
- **graph nodes**: sort by id
- **graph edges**: sort by (source, target)

### Chunk Requirements

- `end` MUST always be 500 (not text.length)
- Each chunk includes: text, index, start, end
- Single chunk if text < 500 chars

### Insights Stats Order

Stats keys MUST be in this order:
1. total_entities
2. unique_entities
3. entity_types
4. total_relations
5. total_chunks
6. text_length
7. word_count

## Agent Output Schema

```json
{
  "task": "web_analysis",
  "input": "",
  "output": {},
  "summary": "",
  "actions": [],
  "confidence": 0.0
}
```

## Memory Block Schema

```json
{
  "type": "webweavex_memory",
  "entities": [],
  "relations": [],
  "graph": {},
  "timestamp": "ISO-8601",
  "source": "webweavex"
}
```

## RAG Chunk Schema

```json
[
  {
    "text": "",
    "metadata": {
      "entities": [],
      "relations": [],
      "source": "webweavex"
    }
  }
]
```

## Tool Schema

```json
{
  "name": "webweavex_extract",
  "description": "Extract structured intelligence from text",
  "parameters": {
    "type": "object",
    "properties": {
      "input": {"type": "string"}
    },
    "required": ["input"]
  }
}
```
