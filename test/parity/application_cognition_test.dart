import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/application/application_cognition.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;

/// Application-cognition closure — run_application_cognition and its 12
/// engines over the certified bs4-parity soup. Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 667/667 fixtures, hash + deep equality).
void main() {
  final registry = <String, Function>{
    'run_application_cognition': runApplicationCognition,
    'extract_ui_semantics': extractUiSemantics,
    'build_form_runtime': buildFormRuntime,
    'build_dashboard_runtime': buildDashboardRuntime,
    'build_navigation_semantics': buildNavigationSemantics,
    'build_application_state': buildApplicationState,
    'build_application_transitions': buildApplicationTransitions,
    'build_action_graph': buildActionGraph,
    'build_workflow_graph': buildWorkflowGraph,
    'resolve_application_intent': resolveApplicationIntent,
    'recover_application_runtime': recoverApplicationRuntime,
    'build_application_context': buildApplicationContext,
    'remember_application_runtime': rememberApplicationRuntime,
  };

  group('application cognition closure (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/application_cognition_vectors.json')
          .readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 13 application functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(13));
      expect(registry.keys.toSet(), equals(fns));
    });

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        final actual =
            Function.apply(registry[fn]!, v['args'] as List<dynamic>);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('application cognition spot-checks', () {
    test('orchestrator carries prior state into transitions and memory', () {
      final out = runApplicationCognition(
          'https://x.test/now',
          '<html><body><nav><a href="/h">H</a></nav></body></html>',
          <dynamic>[],
          <String, dynamic>{
            'application_state': <String, dynamic>{'route': '/before'},
          });
      final transitions = (out['workflow'] as Map)['edges'] as List;
      expect(
          transitions.any((e) =>
              (e as Map)['from'] == '/before' && e['to'] == 'https://x.test/now'),
          isTrue);
      expect(((out['memory'] as Map)['objectives'] as List).single,
          equals('extract_dashboard'));
    });

    test('form recovery injects fallback inputs for empty forms', () {
      final out = recoverApplicationRuntime(
          '<form action="/empty"></form>',
          <String, dynamic>{'route': '/r', 'modals': <dynamic>[]});
      final recovered = (out['forms_recovered'] as List).single as Map;
      expect(recovered['recovered'], isTrue);
      expect((recovered['inputs'] as List).single,
          equals(<String, dynamic>{
            'name': 'fallback',
            'type': 'text',
            'required': false
          }));
    });
  });
}
