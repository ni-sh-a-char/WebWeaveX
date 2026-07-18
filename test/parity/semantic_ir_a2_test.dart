import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/ast_engines.dart';
import 'package:webweavex/src/semantic_ir/graph_engines.dart';
import 'package:webweavex/src/semantic_ir/ir_base.dart';
import 'package:webweavex/src/semantic_ir/pressure_engines.dart';
import 'package:webweavex/src/semantic_ir/py_compat.dart';
import 'package:webweavex/src/semantic_ir/repository_engines.dart';

/// Phase A.2 of the Category-A semantic-IR port — 24 leaf functions across
/// core.semantic (pressure), core.ir._base, core.graph, core.repository and
/// core.ast. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/, 66/66 fixtures, hash + deep equality); here the
/// Dart output hash-equals the executed Python reference vectors.
void main() {
  dynamic call(String fn, List<dynamic> args) {
    switch (fn) {
      case 'compute_ambiguity_pressure':
        return computeAmbiguityPressure(args[0] as List<dynamic>);
      case 'compute_contradiction_pressure':
        return computeContradictionPressure(args[0]);
      case 'compute_evidence_boundary_pressure':
        return args.length > 1
            ? computeEvidenceBoundaryPressure(args[0] as int, args[1] as int)
            : computeEvidenceBoundaryPressure(args[0] as int);
      case 'compute_evidence_decay_pressure':
        return args.length > 1
            ? computeEvidenceDecayPressure(args[0] as int, args[1] as int)
            : computeEvidenceDecayPressure(args[0] as int);
      case 'compute_recursive_boundary_pressure':
        return computeRecursiveBoundaryPressure(args[0] as num, args[1] as int);
      case 'compute_recursive_convergence_pressure':
        return computeRecursiveConvergencePressure(
            args[0] as int, args[1] as num);
      case 'compute_recursive_dependency_pressure':
        return computeRecursiveDependencyPressure(
            args[0] as int, args[1] as int);
      case 'compute_semantic_boundary_pressure':
        return computeSemanticBoundaryPressure(args[0] as num, args[1] as num);
      case 'compute_truth_boundary_pressure':
        return computeTruthBoundaryPressure(args[0] as bool, args[1] as num);
      case 'compute_uncertainty_pressure':
        return computeUncertaintyPressure(
            args[0] as List<dynamic>, args[1] as List<dynamic>);
      case 'empty_confidence':
        return emptyConfidence();
      case 'empty_lineage':
        return args.isNotEmpty
            ? emptyLineage(args[0] as String)
            : emptyLineage();
      case 'merge_evidence':
        return mergeEvidence(args);
      case 'model_graph_entropy':
        return modelGraphEntropy(args[0] as Map);
      case 'detect_cycles':
        return detectCycles(args[0] as Map);
      case 'prove_topology':
        return proveTopology(args[0] as Map);
      case 'reason_api_surface':
        return reasonApiSurface(args[0]);
      case 'reconstruct_execution_flow':
        return reconstructExecutionFlow(args[0]);
      case 'detect_infra_signals':
        return detectInfraSignals(args[0] as List<dynamic>?);
      case 'resolve_runtime_dependencies':
        return args.length > 1
            ? resolveRuntimeDependencies(args[0], args[1] as String)
            : resolveRuntimeDependencies(args[0]);
      case 'infer_service_interactions':
        return inferServiceInteractions(args[0], args[1] as List<dynamic>);
      case 'build_control_flow_graph':
        return buildControlFlowGraph(args[0] as Map);
      case 'reconstruct_execution_paths':
        return reconstructExecutionPaths(args[0] as Map);
      case 'resolve_symbols':
        return resolveSymbols(args[0] as Map);
      default:
        throw StateError('unknown $fn');
    }
  }

  group('semantic-IR Phase A.2 — leaf engines (Python ≡ JS ≡ Dart)', () {
    final vectors = (jsonDecode(
      File('validation/parity/semantic_ir_a2_vectors.json').readAsStringSync(),
    ) as List<dynamic>)
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();

    test('vector set covers all 24 A.2 leaf functions', () {
      final fns = vectors.map((v) => v['fn'] as String).toSet();
      expect(fns, hasLength(24));
    });

    for (final v in vectors) {
      final id = v['id'] as String;
      final fn = v['fn'] as String;
      test('[$id] $fn Dart output hash-equals executed Python output', () {
        final actual = call(fn, v['args'] as List<dynamic>);
        expect(
          computeDeterministicHash(actual),
          equals(computeDeterministicHash(v['expected'])),
          reason: 'parity mismatch for $id',
        );
      });
    }
  });

  group('pythonRound — CPython round-half-to-even on binary doubles', () {
    test('ties go to even on the decimal expansion of the double', () {
      expect(pythonRound(0.5, 0), equals(0.0));
      expect(pythonRound(1.5, 0), equals(2.0));
      expect(pythonRound(2.5, 0), equals(2.0));
      // 2.675 is stored as 2.67499999999999982… so CPython rounds DOWN.
      expect(pythonRound(2.675, 2), equals(2.67));
      // 0.125 and 0.375 are exact binary ties — round to even.
      expect(pythonRound(0.125, 2), equals(0.12));
      expect(pythonRound(0.375, 2), equals(0.38));
    });

    test('accumulated float error collapses like CPython round', () {
      expect(pythonRound(0.4 + 5 * 0.06, 3), equals(0.7));
      expect(pythonRound(3 * 0.15, 3), equals(0.45));
      expect(pythonRound(0.1 + 2 * 0.06, 3), equals(0.22));
    });
  });

  group('A.2 contract spot-checks', () {
    test('resolve_symbols sort is stable for equal symbol names', () {
      final r = resolveSymbols(<String, dynamic>{
        'functions': [
          {'name': 'alpha'}
        ],
        'classes': [
          {'name': 'alpha'}
        ],
      });
      final syms = r['symbols'] as List<dynamic>;
      // Python sorted() is stable: the function entry precedes the class.
      expect((syms[0] as Map)['kind'], equals('function'));
      expect((syms[1] as Map)['kind'], equals('class'));
    });

    test('detect_cycles records bounded DFS cycles in insertion order', () {
      final r = detectCycles(<String, dynamic>{
        'edges': [
          {'from': 'a', 'to': 'b'},
          {'from': 'b', 'to': 'a'},
        ],
      });
      expect(r['cycle_count'], equals(1));
      expect((r['cycles'] as List).first, equals(['a', 'b', 'a']));
    });

    test('reconstruct_execution_flow keeps non-contiguous step indices', () {
      final r = reconstructExecutionFlow(<String, dynamic>{
        'symbols': {
          'functions': ['main']
        },
        'calls': {
          'calls': [
            {'caller': 'a'},
            'junk',
            {'caller': 'b'},
          ]
        },
      });
      final flow = r['flow'] as List<dynamic>;
      expect((flow[0] as Map)['step'], equals(0));
      expect((flow[1] as Map)['step'], equals(2));
    });
  });
}
