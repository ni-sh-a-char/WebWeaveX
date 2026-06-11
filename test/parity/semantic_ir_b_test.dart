import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/composites_b.dart';
import 'package:webweavex/src/semantic_ir/document_composites.dart';
import 'package:webweavex/src/semantic_ir/evidence_layer_b.dart';
import 'package:webweavex/src/semantic_ir/python_ast_parser.dart';

/// Phase B of the Category-A semantic-IR port — the first non-leaf layer
/// (32 functions whose only in-closure dependencies are proven Phase-A
/// leaves; private record helpers prove inside their parents). Proven
/// Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/,
/// 493/493 fixtures, hash + deep equality). The 4 parse_source-gated
/// engines (model_execution_dependencies, analyze_runtime_semantics,
/// build_service_runtime_graph, build_repository_semantic_ir) are deferred
/// to the parser-subsystem phase.
void main() {
  final registry = <String, Function>{
    'parse_python_ast': parsePythonAst,
    'build_argument_dependencies': buildArgumentDependencies,
    'build_argument_graph': buildArgumentGraph,
    'extract_instructional_flow': extractInstructionalFlow,
    'parse_rhetorical_structure': parseRhetoricalStructure,
    'extract_sections': extractSections,
    'apply_confidence_degradation': applyConfidenceDegradation,
    'reason_deterministically': reasonDeterministically,
    'score_epistemic_confidence': scoreEpistemicConfidence,
    'preserve_incompleteness': preserveIncompleteness,
    'model_inference_limits': modelInferenceLimits,
    'validate_inference': validateInference,
    'apply_reality_constraints': applyRealityConstraints,
    'detect_recursive_dependency': detectRecursiveDependency,
    'detect_recursive_semantic_closure': detectRecursiveSemanticClosure,
    'detect_semantic_attractor': detectSemanticAttractor,
    '_ground_parser': groundParser,
    'detect_semantic_monoculture': detectSemanticMonoculture,
    'detect_semantic_monopoly': detectSemanticMonopoly,
    'score_reliability': scoreReliability,
    'apply_epistemic_restraint': applyEpistemicRestraint,
    'propagate_uncertainty': propagateUncertainty,
    'suppress_speculative_inference': suppressSpeculativeInference,
    'propagate_uncertainty_math': propagateUncertaintyMath,
    'suppress_unsupported_continuity': suppressUnsupportedContinuity,
    'detect_unsupported_stabilization': detectUnsupportedStabilization,
    'reason_topology': reasonTopology,
    'empty_document_ir': emptyDocumentIr,
    'empty_repository_ir': emptyRepositoryIr,
    'reason_api_contract': reasonApiContract,
    'model_infra_relationships': modelInfraRelationships,
    'apply_contradiction_restraint': applyContradictionRestraint,
  };

  // Python kw-only params, flattened to trailing positionals in py2ts order
  // (mirrors validation/semantic_ir/run_dart.dart).
  const kwOrder = <String, List<List<dynamic>>>{
    'apply_confidence_degradation': <List<dynamic>>[
      <dynamic>['contradiction_count', 0],
      <dynamic>['ambiguity_count', 0],
      <dynamic>['uncertainty_count', 0],
      <dynamic>['unsupported_expansion_count', 0],
      <dynamic>['speculation_count', 0],
      <dynamic>['parser_weakness', false],
    ],
    'suppress_speculative_inference': <List<dynamic>>[
      <dynamic>['inferred', false],
      <dynamic>['min_evidence', 2],
      <dynamic>['fragility_level', 'medium'],
    ],
    'suppress_unsupported_continuity': <List<dynamic>>[
      <dynamic>['min_evidence', 2],
    ],
    'detect_unsupported_stabilization': <List<dynamic>>[
      <dynamic>['min_evidence', 2],
    ],
  };

  group('semantic-IR Phase B — first non-leaf layer (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_b_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 32 Phase B functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(32));
      expect(registry.keys.toSet(), equals(fns));
    });

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        var args = List<dynamic>.from(v['args'] as List);
        final kwargs = v['kwargs'] as Map<String, dynamic>?;
        if (kwargs != null && kwargs.isNotEmpty) {
          final order = kwOrder[fn]!;
          args = <dynamic>[
            ...args,
            for (final spec in order)
              kwargs.containsKey(spec[0]) ? kwargs[spec[0]] : spec[1],
          ];
        }
        final actual = Function.apply(registry[fn]!, args);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('Phase B contract spot-checks', () {
    test(
        'async def is NOT a FunctionDef (CPython AsyncFunctionDef semantics; '
        'the JS-branch scanner diverges here — executed-Python vector)', () {
      const code = 'import json, re\n\n@decorator\nasync def fetch(url):\n'
          '    data = await get(url)\n    return data\n\n'
          "result = fetch('x')\n";
      // Executed canonical output: PYTHONPATH=<py2.0.1>
      //   core.ast.python_ast_engine.parse_python_ast(code)
      final expected = <String, dynamic>{
        'language': 'python',
        'imports': <dynamic>[
          <String, dynamic>{
            'modules': <String>['json', 're'],
            'node': <String, dynamic>{
              'type': 'Import',
              'lineno': 1,
              'end_lineno': 1
            },
          }
        ],
        'functions': <dynamic>[],
        'classes': <dynamic>[],
        'assignments': <dynamic>[
          <String, dynamic>{
            'targets': <String>['result'],
            'node': <String, dynamic>{
              'type': 'Assign',
              'lineno': 8,
              'end_lineno': 8
            },
          },
          <String, dynamic>{
            'targets': <String>['data'],
            'node': <String, dynamic>{
              'type': 'Assign',
              'lineno': 5,
              'end_lineno': 5
            },
          },
        ],
        'ast_grounded': true,
        'bounded': true,
      };
      expect(parsePythonAst(code), equals(expected));
    });

    test('epistemic restraint mutates the bundle with fragility pressure', () {
      final bundle = <String, dynamic>{
        'evidence': <String>['e1'],
        'fragility': <String, dynamic>{'level': 'high'},
        'contradicted': <String, dynamic>{
          'pairs': <dynamic>[
            <String>['x', 'y']
          ]
        },
      };
      final out = applyEpistemicRestraint(bundle);
      expect(identical(out, bundle), isTrue);
      expect((out['fragility_pressure'] as Map)['level'], equals('high'));
      expect((out['restraint'] as Map)['conservative_default'], isTrue);
    });

    test('uncertainty math combines parent multiplicatively', () {
      final r = propagateUncertaintyMath(0, 2, 1, 0.4);
      // local U = min(1, 0.2 + 0.3 + 0.2) + 0.3 (evidence<2) = 1.0
      // combined = 1 - 0.6*(1-1.0) = 1.0; confidence = 0.0
      expect(r['uncertainty_score'], equals(1.0));
      expect(r['confidence_score'], equals(0.0));
      expect(r['parent_uncertainty'], equals(0.4));
    });

    test('document sections dedupe and sort', () {
      final r = extractSections('# Z\n## A\n# Z\n');
      expect(r['sections'], equals(<String>['A', 'Z']));
      expect((r['hierarchy'] as List), hasLength(3));
    });
  });
}
