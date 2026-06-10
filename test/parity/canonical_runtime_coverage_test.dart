import 'package:test/test.dart';
import 'package:webweavex/src/parity/canonical_runtime.dart';

/// Branch coverage for the canonical-runtime JSON/graph helpers. Format
/// correctness is proven against Python in canonical_runtime_parity_test.dart;
/// here we exercise the escape/number/edge branches.
void main() {
  group('compact/default sorted JSON', () {
    test('escapes control chars, quotes, backslashes; spaces in default', () {
      final v = <String, dynamic>{
        'z': 'tab\tnl\ncr\rquote"back\\end',
        'a': <dynamic>[1, 2.5, true, false, null, 'x'],
        'u': 'cafe \u{1F680}',
      };
      final compact = compactSortedJson(v);
      final pretty = defaultSortedJson(v);
      expect(compact.startsWith('{"a":['), isTrue);
      expect(compact.contains(r'\t'), isTrue);
      expect(compact.contains(r'\n'), isTrue);
      expect(compact.contains(r'\r'), isTrue);
      expect(compact.contains(r'\"'), isTrue);
      expect(compact.contains(r'\\'), isTrue);
      expect(pretty.contains('": '), isTrue);
      expect(pretty.contains(', '), isTrue);
    });

    test('integral and large floats both serialize', () {
      expect(compactSortedJson(<String, dynamic>{'n': 3.0}), contains('3.0'));
      expect(compactSortedJson(<String, dynamic>{'n': 1e20}), isNotEmpty);
    });
  });

  group('normalizeGraphContract', () {
    test('sorts nodes/edges and honors from/to edge keys', () {
      final n = normalizeGraphContract(<String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'b'},
          <String, dynamic>{'id': 'a'},
          'not-a-map',
        ],
        'edges': <dynamic>[
          <String, dynamic>{'from': 'b', 'to': 'a', 'type': 'e'},
          <String, dynamic>{'source': 'a', 'target': 'b', 'type': 'e'},
        ],
      });
      expect((n['nodes'] as List).length, equals(3));
      expect((n['edges'] as List).length, equals(2));
      expect(n['bounded'], isTrue);
    });

    test('null graph yields empty normalized form', () {
      final n = normalizeGraphContract(null);
      expect(n['nodes'], equals(<dynamic>[]));
      expect(n['edges'], equals(<dynamic>[]));
    });
  });

  group('graphHashCanonical + fingerprint edges', () {
    test('graph hash is deterministic', () {
      final g = <String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'a', 'type': 't', 'name': 'n'}
        ],
        'edges': <dynamic>[],
      };
      expect(graphHashCanonical(g), equals(graphHashCanonical(g)));
    });

    test('fingerprint covers dom_stabilization and from/to edges', () {
      final fp = computeGlobalRuntimeFingerprint(
        extraction: <String, dynamic>{
          'unified_runtime_graph': <String, dynamic>{
            'nodes': <dynamic>[
              <String, dynamic>{'id': 1}
            ],
            'edges': <dynamic>[
              <String, dynamic>{'from': 'a', 'to': 'b', 'type': 'x'}
            ],
          },
          'runtime': <String, dynamic>{
            'dom_stabilization': <String, dynamic>{'stabilized_hash': 'h'}
          },
          'browser_ir': <String, dynamic>{'runtime_identity': 'id'},
        },
        memory: <String, dynamic>{
          'memory': <String, dynamic>{
            'stable_hash': 'sh',
            'runtime_history': <dynamic>[1, 2, 3]
          }
        },
      );
      expect(fp, isNotEmpty);
    });
  });
}
