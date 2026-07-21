# AI Integration Guide

## OpenAI Agents SDK

```dart
import 'package:webweavex/webweavex.dart';

// Build deterministic context for LLM
final graph = buildRuntimeGraph({'source': 'web', 'url': 'https://example.com'});
final fabric = buildRuntimeMemoryFabric(graph);
final context = stableSerialize(fabric);
// Pass `context` to LLM as deterministic runtime state
```

## LangGraph / CrewAI (via Dart FFI or HTTP)

```dart
import 'package:webweavex/webweavex.dart';

// Extract ? Fingerprint ? Replay
final pipeline = await runCanonicalPipeline({
  'url': 'https://docs.flutter.dev',
  'sourceType': 'web',
});
final hash = computeGlobalRuntimeFingerprint(extraction: pipeline);
// Use hash as agent memory checkpoint
```

## Agent Memory Continuity

```dart
import 'package:webweavex/webweavex.dart';

// Store agent state deterministically
final state = {'step': 1, 'observations': ['page loaded']};
final encrypted = encryptValue(state, 'agent-key');

// Later: decrypt and continue
final restored = decryptValue(encrypted, 'agent-key');
// restored == state (byte-identical)
```

## RAG Preprocessing

```dart
import 'package:webweavex/webweavex.dart';

final extraction = await extractWeb('https://example.com/docs');
final graph = buildRuntimeGraph(extraction);
// Query the knowledge graph for relevant context
final results = queryRuntimeGraph(graph.toJson(), {
  'query_type': 'by_type',
  'type': 'document',
});
```
