# Contributing to WebWeaveX

Thank you for your interest in contributing to WebWeaveX!

This document outlines the guidelines and processes for contributing.

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

---

## How to Contribute

### 1. Fork the Repository

Start by forking the repository on GitHub:

```bash
git clone https://github.com/PIYUSH-MISHRA-00/WebWeaveX.git
cd WebWeaveX
```

### 2. Create a Feature Branch

Work on a feature branch:

```bash
git checkout -b feature/your-feature-name
```

### 3. Development Setup

#### Python

```bash
cd implementations/python/webweavex
pip install -e .
```

#### Node.js

```bash
cd implementations/node
npm install
```

#### Java

```bash
cd implementations/java
mvn compile
```

#### Kotlin

```bash
cd implementations/kotlin
gradle build
```

#### Dart

```bash
cd implementations/dart
dart pub get
```

### 4. Run Tests

Before submitting, run the full validation:

```bash
python core/test_runner/validate_full_system.py
```

All 35 tests must pass.

### 5. Make Your Changes

Follow these rules:

1. **Python is source of truth** — Never modify Python to match other languages
2. **All languages must match Python** — Fix implementations to match Python behavior
3. **Deterministic output** — No randomness allowed
4. **Alphabetical ordering** — Keys must be in alphabetical order
5. **snake_case only** — No camelCase in JSON keys

---

## Pull Request Process

### Before Submitting

1. Run validation: `python core/test_runner/validate_full_system.py`
2. Ensure all tests pass
3. Update documentation if needed
4. Add test cases for new features

### Submitting

1. Push your branch: `git push origin feature/your-feature-name`
2. Open a Pull Request
3. Describe your changes
4. Reference any related issues

### PR Requirements

- Clear description of changes
- Link to related issues
- Validation results showing all tests pass
- No breaking changes to existing APIs

---

## Implementation Guidelines

### Schema Compliance

All implementations must follow the WXP v1 schema:

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

### Entity Types

Supported entity types:
- `email` — Email addresses
- `url` — HTTP/HTTPS URLs
- `phone` — Phone numbers
- `number` — Numeric values
- `capitalized` — Capitalized words

### Sorting Rules

- **entities**: sort by (type, value)
- **relations**: sort by (source, target)
- **nodes**: sort by id
- **edges**: sort by (source, target)

### Chunk Requirements

- `end` MUST always be 500 (not text.length)
- Each chunk includes: text, index, start, end

---

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Validation output

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)

---

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

## Questions?

- **Issues:** https://github.com/PIYUSH-MISHRA-00/WebWeaveX/issues
- **Discussions:** https://github.com/PIYUSH-MISHRA-00/WebWeaveX/discussions

---

Thank you for contributing to WebWeaveX!
