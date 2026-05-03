# 🚀 WebWeaveX

> **AI-powered web intelligence extraction engine**

Transform web content into structured, AI-ready data with a deterministic pipeline.

---

## ✨ What WebWeaveX Does

WebWeaveX extracts structured data from web sources:

- **Clean text** from HTML
- **Code blocks** from repositories  
- **Knowledge** from documentation
- **Results** from search engines

---

## ⚡ Features

- **8-Stage Pipeline** — intent → extraction → ranking → output
- **Schema-Locked Output** — always 7 predictable keys
- **Multi-Source** — GitHub, StackOverflow, web search
- **Adaptive Extraction** — recovers from weak pages
- **Deterministic** — same input → same output
- **Agent-Friendly** — structured_data and ui_schema for AI

---

## 📦 Installation

```bash
pip install webweavex
```

---

## 🚀 Quick Start

```python
from webweavex import run

# Basic usage
result = run({"input": "calculator app python"})

print(result["human_readable"])
print(result["structured_data"])
print(result["confidence"])
```

**Output:**
```json
{
  "human_readable": "Repository search results - GitHub...",
  "structured_data": {"query_source": "github", "has_content": true},
  "ui_schema": {"type": "ui_render", "components": [...]},
  "confidence": 0.9,
  "source": "github",
  "reconstructed_project": [],
  "version": "v1_phase_14"
}
```

---

## 📋 Output Schema (Always 7 Keys)

| Key | Type | Description |
|-----|------|-------------|
| `human_readable` | str | Human-friendly summary |
| `structured_data` | dict | Machine-usable data |
| `ui_schema` | dict | UI-ready components |
| `confidence` | float | 0.0-1.0 confidence |
| `source` | str | Data source (github, web, etc.) |
| `reconstructed_project` | list | Code files if extracted |
| `version` | str | Engine version |

---

## 🎯 Use Cases

```python
# Calculator app
result = run({"input": "calculator app python"})

# Weather dashboard
result = run({"input": "weather dashboard India"})

# ML pipeline
result = run({"input": "machine learning pipeline"})

# Todo app
result = run({"input": "todo app with login"})
```

---

## 🔧 For Developers

```python
# Import the API
from webweavex import run, validate_request, validate_response, ENGINE_VERSION

# Validate input
validated = validate_request({"input": "my query"})
print(validated)  # {"input": "my query", "mode": "normal"}

# Run with strict mode
result = run({"input": "calculator app", "mode": "strict"})
```

---

## 🏗️ Architecture

```
User Input → Intent Resolution → Source Planning → Query Building
    → Fetch Engine → Adaptive Extraction → Ranking → Execution
    → Output Engine → Structured Result (7 keys)
```

---

## ⚠️ Limitations

- **Web Dependent** — requires internet connection
- **Rate Limits** — may be affected by source websites
- **Not Deterministic** — web content changes; outputs may vary over time

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions welcome! Open an issue or PR on GitHub.

---

## 🔗 Links

- GitHub: https://github.com/webweavex/webweavex
- PyPI: https://pypi.org/project/webweavex/

---

⭐ Star us if you find this useful!