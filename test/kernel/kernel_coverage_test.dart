import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  Map<String, dynamic> populatedExtraction() {
    final graph = buildRuntimeGraph(<String, dynamic>{
      'browser': <String, dynamic>{'url': 'x', 'dom_hash': 'h'},
      'network': <dynamic>[
        <String, dynamic>{'url': 'x', 'method': 'GET'},
      ],
    });
    return <String, dynamic>{
      'bounded': true,
      'unified_runtime_graph': graph.toJson(),
      'graph': graph.toJson(),
      'runtime': <String, dynamic>{
        'available': true,
        'session': <String, dynamic>{'token': 'abc'},
      },
      'browser_ir': <String, dynamic>{
        'runtime_identity': 'ident-123',
        'storage': <String, dynamic>{'k': 'v'},
      },
      'runtime_memory': <String, dynamic>{
        'runtime_history': <dynamic>[
          <String, dynamic>{'step': 0},
        ],
      },
    };
  }

  group('runCanonicalPipeline kind detection', () {
    test('text kind (plain source) builds offline runtime envelope', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'source': 'just some plain text content',
      });
      final ingestion = out['ingestion'] as Map<String, dynamic>;
      expect(ingestion['kind'], 'text');
      expect(ingestion['target'], 'just some plain text content');
      final runtime = out['runtime'] as Map<String, dynamic>;
      expect(runtime['available'], isFalse);
      expect(out['unified_runtime_graph'], isA<Map<String, dynamic>>());
      expect(out['global_runtime_fingerprint'], isNotEmpty);
    });

    test('document kind via .pdf path extension', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'path': '/docs/report.PDF',
      });
      final ingestion = out['ingestion'] as Map<String, dynamic>;
      expect(ingestion['kind'], 'document');
      expect((out['runtime'] as Map<String, dynamic>)['kind'], 'document');
    });

    test('document kind via .md path extension', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'path': 'notes.md',
      });
      expect((out['ingestion'] as Map<String, dynamic>)['kind'], 'document');
    });

    test('explicit sourceType overrides detection', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'sourceType': 'custom',
        'source': 'http://example.com/should-be-ignored',
      });
      expect((out['ingestion'] as Map<String, dynamic>)['kind'], 'custom');
      // Non-web branch => no real network hit.
      expect((out['runtime'] as Map<String, dynamic>)['available'], isFalse);
    });

    test('sourceType=auto falls through to URL/extension detection', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'sourceType': 'auto',
        'source': 'plain.txt',
      });
      expect((out['ingestion'] as Map<String, dynamic>)['kind'], 'document');
    });

    test('web kind hits extractWeb branch; unroutable host => unavailable',
        () async {
      // Connection refused on port 1 returns fast from renderPage catch block,
      // exercising the entire web branch without real external network access.
      final out = await runCanonicalPipeline(<String, dynamic>{
        'url': 'http://127.0.0.1:1/page',
      });
      final ingestion = out['ingestion'] as Map<String, dynamic>;
      expect(ingestion['kind'], 'web');
      expect(ingestion['target'], 'http://127.0.0.1:1/page');
      final runtime = out['runtime'] as Map<String, dynamic>;
      expect(runtime['available'], isFalse);
      expect(out['browser_ir'], isA<Map<String, dynamic>>());
    });

    test('web kind with authenticated + semanticRuntime flags', () async {
      final out = await runCanonicalPipeline(
        <String, dynamic>{'url': 'http://127.0.0.1:1/auth'},
        authenticated: true,
        sessionPath: null,
        encryptionKey: null,
        semanticRuntime: true,
      );
      expect((out['ingestion'] as Map<String, dynamic>)['kind'], 'web');
      // semanticRuntime adds a semantic section.
      expect(out['semantic'], isA<Map<String, dynamic>>());
    });

    test('https URL is detected as web', () async {
      final out = await runCanonicalPipeline(<String, dynamic>{
        'source': 'https://127.0.0.1:1/secure',
      });
      expect((out['ingestion'] as Map<String, dynamic>)['kind'], 'web');
    });
  });

  group('runReplayPipeline', () {
    test('replays a populated extraction and reports equivalence', () {
      final out = runReplayPipeline(populatedExtraction());
      expect(out['replayed'], isA<Map<String, dynamic>>());
      expect(out['validation'], isA<Map<String, dynamic>>());
      expect(out['equivalent'], isTrue);
      expect(out['bounded'], isTrue);
    });

    test('handles an empty extraction', () {
      final out = runReplayPipeline(<String, dynamic>{});
      expect(out['bounded'], isTrue);
      expect(out['validation'], isA<Map<String, dynamic>>());
    });
  });

  group('runReconstructionPipeline', () {
    test('reconstructs and replays a populated extraction', () {
      final out = runReconstructionPipeline(populatedExtraction());
      final reconstructed = out['reconstructed'] as Map<String, dynamic>;
      expect((reconstructed['runtime_id'] as String).length, 32);
      expect(reconstructed['reconstructed'], isTrue);
      final replay = out['replay'] as Map<String, dynamic>;
      expect(replay['replayed'], isA<Map<String, dynamic>>());
      expect(replay['validation'], isA<Map<String, dynamic>>());
      expect(out['bounded'], isTrue);
    });

    test('handles an empty extraction', () {
      final out = runReconstructionPipeline(<String, dynamic>{});
      expect(out['reconstructed'], isA<Map<String, dynamic>>());
      expect(out['replay'], isA<Map<String, dynamic>>());
      expect(out['bounded'], isTrue);
    });
  });
}
