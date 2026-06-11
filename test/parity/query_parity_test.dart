import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/query/graph_ir.dart';
import 'package:webweavex/src/query/knowledge_ir.dart';
import 'package:webweavex/src/query/python_repr.dart';
import 'package:webweavex/src/query/query.dart';
import 'package:webweavex/src/query/topology_reasoning.dart';

/// Reconstructs the Dart result for a vector `api` + `input`, mirroring the
/// exact Python call shapes used to generate validation/parity/
/// query_api_vectors.json.
dynamic _runVector(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'query_graph':
      if (input.containsKey('graph')) {
        return queryGraph(
          graph: (input['graph'] as Map).cast<String, dynamic>(),
          node: input['node'] as String? ?? '',
        );
      }
      if (input.containsKey('result')) {
        return queryGraph(
          result: (input['result'] as Map).cast<String, dynamic>(),
          node: input['node'] as String? ?? '',
        );
      }
      return queryGraph(node: input['node'] as String? ?? '');

    case 'query_knowledge':
      if (input.containsKey('result')) {
        return queryKnowledge(
            result: (input['result'] as Map).cast<String, dynamic>());
      }
      return queryKnowledge(
        entities: input['entities'] as List<dynamic>?,
        edges: input['edges'] as List<dynamic>?,
      );

    case 'query_repo':
      return queryRepo((input['result'] as Map).cast<String, dynamic>());

    case 'query_repository':
      return queryRepository(
          result: (input['result'] as Map).cast<String, dynamic>());

    case 'query_documents':
      return queryDocuments(
          result: (input['result'] as Map).cast<String, dynamic>());

    case 'query_semantics':
      return querySemantics(
        input['query_type'] as String,
        (input['payload'] as Map).cast<String, dynamic>(),
      );

    case 'reason_semantically':
      return reasonSemantically(
        input['domain'] as String,
        (input['payload'] as Map).cast<String, dynamic>(),
      );

    case 'analyze':
      return analyze(
        input['nodes'] as List<dynamic>,
        input['edges'] as List<dynamic>,
      );

    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  group('query/reasoning/IR cross-language hash parity', () {
    final file = File('validation/parity/query_api_vectors.json');
    final vectors = (jsonDecode(file.readAsStringSync()) as List<dynamic>)
        .cast<Map<String, dynamic>>();

    test('vector file is non-empty', () {
      expect(vectors, isNotEmpty);
    });

    for (final v in vectors) {
      final api = v['api'] as String;
      final input = (v['input'] as Map).cast<String, dynamic>();
      final expected = v['det_hash'] as String;
      test(
          '$api :: ${jsonEncode(input).substring(0, input.toString().length.clamp(0, 60))}',
          () {
        final output = _runVector(api, input);
        expect(computeDeterministicHash(output), equals(expected));
      });
    }
  });

  group('branch coverage — query_engines', () {
    test('queryGraph graph path with node filter', () {
      final out = queryGraph(graph: <String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'abc'},
          <String, dynamic>{'id': 'xyz'},
        ],
        'edges': <dynamic>[
          <String, dynamic>{
            'from': 'abc',
            'to': 'xyz',
            'evidence': <dynamic>['e']
          }
        ],
      }, node: 'ab');
      expect((out['nodes'] as List<dynamic>).length, 1);
      expect((out['edges'] as List<dynamic>).length, 1);
    });

    test('queryGraph result path without relationships uses raw graph', () {
      final out = queryGraph(result: <String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'a'}
        ],
        'edges': <dynamic>[],
      });
      expect(out['bounded'], isTrue);
    });

    test('queryKnowledge dict-extraction path', () {
      final out = queryKnowledge(result: <String, dynamic>{
        'content': <String, dynamic>{
          'knowledge_v2': <String, dynamic>{'a': 1},
          'knowledge_reconstruction_v18': <String, dynamic>{'b': 2},
        }
      });
      expect(out['knowledge_v2'], <String, dynamic>{'a': 1});
      expect(out['knowledge_v18'], <String, dynamic>{'b': 2});
    });

    test('queryKnowledge dict-extraction path with empty result', () {
      final out = queryKnowledge();
      expect(out['knowledge_v2'], <String, dynamic>{});
    });

    test('querySemantics unknown type returns unknown_query_type', () {
      final out = querySemantics('???', <String, dynamic>{});
      expect((out['result'] as Map)['error'], 'unknown_query_type');
      expect(out['target'], '');
    });

    test('reasonSemantically unknown domain', () {
      final out = reasonSemantically('???', <String, dynamic>{});
      expect(out['error'], 'unknown_domain');
    });

    test('analyze with n<=1 keeps density 0', () {
      final out = analyze(<dynamic>[
        <String, dynamic>{'id': 'a'}
      ], <dynamic>[]);
      expect(out['density'], 0.0);
    });

    test('compileDocument routes to the proven document IR', () {
      final ir = compileDocument('# T\nbody\n');
      expect((ir['confidence'] as Map)['score'], equals(0.7));
      expect(ir.containsKey('_raw'), isTrue);
    });

    test('compileRepository routes to the proven repository IR', () {
      final ir = compileRepository('');
      expect((ir['confidence'] as Map)['score'], equals(0.4));
      expect(ir.containsKey('semantic_ast'), isTrue);
    });

    test('queryRepository source path routes to the repository IR', () {
      final out =
          queryRepository(source: 'function a() { b(); }', path: 'svc.js');
      expect(out['explainable'], isTrue);
      expect((out['ir'] as Map).containsKey('semantic_evidence'), isTrue);
    });

    test('queryDocuments text path routes to the document IR', () {
      final out = queryDocuments(text: '# H\nline\n');
      expect(out['explainable'], isTrue);
      expect((out['ir'] as Map).containsKey('rhetorical_units'), isTrue);
    });

    test('queryDocuments empty path returns the empty-text document IR', () {
      final out = queryDocuments();
      expect(out['explainable'], isTrue);
      expect(((out['ir'] as Map)['confidence'] as Map)['score'], equals(0.3));
    });
  });

  group('branch coverage — IR engines', () {
    test('validateSemanticEdge forbidden type field', () {
      final r = validateSemanticEdge(<String, dynamic>{'type': 'x'});
      expect(r['reason'], 'forbidden_type_field');
    });

    test('validateSemanticEdge missing endpoints', () {
      final r = validateSemanticEdge(<String, dynamic>{'from': 'a'});
      expect(r['reason'], 'missing_endpoints');
    });

    test('validateSemanticEdge string evidence is wrapped', () {
      final r = validateSemanticEdge(
          <String, dynamic>{'from': 'a', 'to': 'b', 'evidence': 'e'});
      expect(r['valid'], isTrue);
      expect(r['evidence_count'], 1);
    });

    test('checkGraphInvariants dangling + type violations', () {
      final inv = checkGraphInvariants(<String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'a'}
        ],
        'edges': <dynamic>[
          <String, dynamic>{'from': 'a', 'to': 'z', 'type': 'bad'}
        ],
      });
      expect(inv['valid'], isFalse);
      expect((inv['violations'] as List<dynamic>).length, 2);
    });

    test('mergeWithEvidence rejects silent merge', () {
      final m = mergeWithEvidence(<Map<String, dynamic>>[
        <String, dynamic>{'evidence': <dynamic>[]}
      ]);
      expect(m['merged'], isFalse);
    });

    test('reconcileOntologyEdges rejects edges missing evidence', () {
      final r = reconcileOntologyEdges(<dynamic>[
        <String, dynamic>{'from': 'a', 'to': 'b'}
      ]);
      expect((r['rejected'] as List<dynamic>).length, 1);
      expect((r['reconciled'] as List<dynamic>).length, 0);
    });

    test('buildContradictionLattice sorts and scores pressure', () {
      final l = buildContradictionLattice(<dynamic>[
        <dynamic>['z', 'a'],
        <dynamic>['a', 'b'],
      ]);
      expect((l['pairs'] as List<dynamic>).first, <String>['a', 'b']);
      expect(l['count'], 2);
      expect(l['pressure'], 0.5);
    });

    test('identityHash is deterministic 16-hex', () {
      final h = identityHash('Alpha');
      expect((h['id'] as String).length, 16);
    });

    test('topology proveTopology hubs and max_degree', () {
      final p = proveTopology(<String, dynamic>{
        'edges': <dynamic>[
          <String, dynamic>{'from': 'a', 'to': 'b'},
          <String, dynamic>{'from': 'a', 'to': 'c'},
          <String, dynamic>{'from': 'a', 'to': 'd'},
        ],
      });
      expect(p['hubs'], <String>['a']);
      expect(p['max_degree'], 3);
    });

    test('detectCycles finds a cycle', () {
      final c = detectCycles(<String, dynamic>{
        'edges': <dynamic>[
          <String, dynamic>{'from': 'a', 'to': 'b'},
          <String, dynamic>{'from': 'b', 'to': 'a'},
        ],
      });
      expect(c['cycle_count'], greaterThan(0));
    });
  });

  group('python_repr', () {
    test('dict repr uses single quotes and python separators', () {
      expect(pythonStr(<String, dynamic>{'k': 'v'}), "{'k': 'v'}");
    });

    test('list / bool / none / double repr', () {
      expect(pythonStr(<dynamic>[1, true, null, 2.0]), '[1, True, None, 2.0]');
    });

    test('string with single quote switches to double quotes', () {
      expect(pythonStr("it's"), '"it\'s"');
    });

    test('string with both quotes stays single-quoted and escapes', () {
      expect(pythonStr('a\'b"c'), "'a\\'b\"c'");
    });

    test('escapes backslash, newline, carriage return and tab', () {
      expect(pythonStr('a\\b\nc\rd\te'), "'a\\\\b\\nc\\rd\\te'");
    });

    test('int and non-integer double repr', () {
      expect(pythonStr(7), '7');
      expect(pythonStr(1.5), '1.5');
    });

    test('nested map/list repr matches CPython', () {
      expect(
          pythonStr(<String, dynamic>{
            'g': <dynamic>[
              <String, dynamic>{'id': 'a'}
            ]
          }),
          "{'g': [{'id': 'a'}]}");
    });
  });
}
