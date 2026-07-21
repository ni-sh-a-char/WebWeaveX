# Changelog

All notable changes to the WebWeaveX Kotlin SDK will be documented in this file.

## [3.0.0] - 2026-07-12

### Added
- RuntimeKernel with universal extraction
- ExtractionPipeline (HTML, Markdown, JSON extraction)
- QueryEngine with indexed search and fallback
- QuerySession with prepared index reuse
- SearchIndex (token, type, field inverted index)
- NodeLookup for O(1) ID-based node resolution
- QueryPlanner with strategy selection
- WorkflowEngine with DAG scheduling
- MemoryEngine with deterministic memory
- ReplayEngine with snapshot validation
- Fingerprint (SHA-256 deterministic hashing)
- CanonicalSerialization (deterministic JSON)
- DeterministicClock (LogicalClock, ReplayClock, TestClock)
- KnowledgeGraph with entity relationships
- RepositoryAnalyzerEngine with language detection
- 8 typed exception classes
- HTTP transport and Crawler
- 133 automated tests
- Cross-language parity verified (1012 serialization vectors, 1012 fingerprint vectors)

### Architecture
- Executable specification → IR → Generator → Generated SDK → Kernel → Thin Runtime
- Deterministic execution with no wall-clock dependency
- Prepared index reuse for query sessions
- DAG-based workflow scheduling with topological ordering
