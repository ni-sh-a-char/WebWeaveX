// Execute Dart semantic-IR ported functions; emit output + hash.
//   dart run validation/semantic_ir/run_dart.dart validation/semantic_ir/fixtures.json
import 'dart:convert';
import 'dart:io';

import 'package:webweavex/src/crypto/hashing.dart'
    show computeDeterministicHash;
import 'package:webweavex/src/semantic_ir/ast_engines.dart';
import 'package:webweavex/src/semantic_ir/document_parser.dart';
import 'package:webweavex/src/semantic_ir/graph_engines.dart';
import 'package:webweavex/src/semantic_ir/ir_base.dart';
import 'package:webweavex/src/semantic_ir/pressure_engines.dart';
import 'package:webweavex/src/semantic_ir/repository_engines.dart';

List<Map<String, dynamic>> _claims(dynamic v) => <Map<String, dynamic>>[
      for (final e in v as List) Map<String, dynamic>.from(e as Map)
    ];

dynamic _call(String fn, List<dynamic> args) {
  switch (fn) {
    // A.1 — document parser leaves
    case 'extract_rhetorical_structure':
      return extractRhetoricalStructure(args[0] as String?);
    case 'assign_semantic_roles':
      return assignSemanticRoles(args[0] as String?);
    case 'extract_headings':
      return extractHeadings(args[0] as String?);
    case 'reconstruct_argument_dependencies':
      return reconstructArgumentDependencies(_claims(args[0]));
    case 'resolve_coreferences':
      return resolveCoreferences(args[0] as String?);
    // A.2 — semantic pressure leaves
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
      return computeRecursiveDependencyPressure(args[0] as int, args[1] as int);
    case 'compute_semantic_boundary_pressure':
      return computeSemanticBoundaryPressure(args[0] as num, args[1] as num);
    case 'compute_truth_boundary_pressure':
      return computeTruthBoundaryPressure(args[0] as bool, args[1] as num);
    case 'compute_uncertainty_pressure':
      return computeUncertaintyPressure(
          args[0] as List<dynamic>, args[1] as List<dynamic>);
    // A.2 — ir/_base leaves
    case 'empty_confidence':
      return emptyConfidence();
    case 'empty_lineage':
      return args.isNotEmpty ? emptyLineage(args[0] as String) : emptyLineage();
    case 'merge_evidence':
      return mergeEvidence(args);
    // A.2 — graph leaves
    case 'model_graph_entropy':
      return modelGraphEntropy(args[0] as Map);
    case 'detect_cycles':
      return detectCycles(args[0] as Map);
    case 'prove_topology':
      return proveTopology(args[0] as Map);
    // A.2 — repository leaves
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
    // A.2 — ast leaves
    case 'build_control_flow_graph':
      return buildControlFlowGraph(args[0] as Map);
    case 'reconstruct_execution_paths':
      return reconstructExecutionPaths(args[0] as Map);
    case 'resolve_symbols':
      return resolveSymbols(args[0] as Map);
    default:
      throw StateError('unknown fn $fn');
  }
}

void main(List<String> argv) {
  final fixtures =
      jsonDecode(File(argv[0]).readAsStringSync()) as List<dynamic>;
  final out = <Map<String, dynamic>>[];
  for (final f in fixtures) {
    final fx = Map<String, dynamic>.from(f as Map);
    final fn = fx['fn'] as String;
    try {
      final result = _call(fn, fx['args'] as List<dynamic>);
      out.add(<String, dynamic>{
        'id': fx['id'],
        'fn': fn,
        'output': result,
        'hash': computeDeterministicHash(result),
      });
    } catch (e) {
      out.add(
          <String, dynamic>{'id': fx['id'], 'fn': fn, 'error': e.toString()});
    }
  }
  stdout.write(jsonEncode(out));
}
