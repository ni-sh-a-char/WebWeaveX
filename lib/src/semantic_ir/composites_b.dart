/// Phase B graph/IR/repository/semantic composites of the Category-A
/// semantic-IR port — engines whose only in-closure dependencies are proven
/// Phase-A leaves. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'graph_engines.dart' show modelGraphEntropy, proveTopology;
import 'ir_base.dart' show emptyConfidence, emptyLineage;
import 'pressure_engines.dart' show computeContradictionPressure;
import 'py_compat.dart';
import 'repository_engines.dart' show detectInfraSignals, reasonApiSurface;

/// Port of core.graph.topology_reasoning_engine.reason_topology.
Map<String, dynamic> reasonTopology(Map<dynamic, dynamic> graph) {
  final proof = proveTopology(graph);
  final entropy = modelGraphEntropy(graph);
  return <String, dynamic>{
    ...proof,
    'entropy': pyGet(entropy, 'entropy', 0),
    'evidence': <String>['graph:topology_proof'],
    'justification': <String, dynamic>{
      'hubs': pyGet(proof, 'hubs', const <dynamic>[]),
      'max_degree': pyGet(proof, 'max_degree', 0),
    },
    'uncertainty': <String, dynamic>{
      'visible': (pyGet(entropy, 'entropy', 0) as num) > 0
    },
    'deterministic_inputs':
        pyGet(proof, 'deterministic_inputs', const <dynamic>[]),
  };
}

/// Port of core.ir.document_ir.empty_document_ir.
Map<String, dynamic> emptyDocumentIr() => <String, dynamic>{
      'concepts': <dynamic>[],
      'claims': <dynamic>[],
      'arguments': <dynamic>[],
      'tutorial_steps': <dynamic>[],
      'dependencies': <dynamic>[],
      'references': <dynamic>[],
      'contradictions': <dynamic>[],
      'rhetorical_units': <dynamic>[],
      'semantic_roles': <dynamic>[],
      'explanation_chains': <dynamic>[],
      'concept_progressions': <dynamic>[],
      'instructional_flows': <dynamic>[],
      'semantic_graph': <dynamic, dynamic>{},
      'lineage': emptyLineage('document_ir'),
      'confidence': emptyConfidence(),
    };

/// Port of core.ir.repository_ir.empty_repository_ir.
Map<String, dynamic> emptyRepositoryIr() => <String, dynamic>{
      'services': <dynamic>[],
      'runtimes': <dynamic>[],
      'dependencies': <dynamic>[],
      'events': <dynamic>[],
      'queues': <dynamic>[],
      'apis': <dynamic>[],
      'deployments': <dynamic>[],
      'infra': <dynamic>[],
      'execution_flows': <dynamic>[],
      'topology': <dynamic>[],
      'runtime_constraints': <dynamic>[],
      'semantic_evidence': <dynamic, dynamic>{},
      'graph': <dynamic, dynamic>{},
      'lineage': emptyLineage('repository_ir'),
      'confidence': emptyConfidence(),
    };

/// Port of core.repository.api_contract_reasoning_engine.reason_api_contract.
Map<String, dynamic> reasonApiContract(Map<dynamic, dynamic> spec) {
  final surface = reasonApiSurface(spec);
  final contracts = <Map<String, dynamic>>[
    for (final p in pyGet(surface, 'paths', const <dynamic>[]) as List)
      <String, dynamic>{
        'path': (p as Map)['path'],
        'method': p['method'],
        'contract': 'http',
        'evidence': <String>['openapi:paths'],
      }
  ];
  return <String, dynamic>{
    ...surface,
    'contracts': contracts,
    'contract_count': contracts.length,
  };
}

/// Port of core.repository.infra_relationship_engine.model_infra_relationships.
Map<String, dynamic> modelInfraRelationships(List<dynamic> files) {
  final signals = detectInfraSignals(files);
  final names = <dynamic>[
    for (final s in pyGet(signals, 'signals', const <dynamic>[]) as List)
      (s as Map)['file']
  ];
  final edges = <Map<String, dynamic>>[
    for (var i = 0; i < names.length - 1; i++)
      <String, dynamic>{
        'from': names[i],
        'to': names[i + 1],
        'relation': 'co_deployed',
        'evidence': <String>['infra:signal'],
      }
  ];
  return <String, dynamic>{
    'signals': pyGet(signals, 'signals', const <dynamic>[]),
    'edges': edges,
    'evidence': pyGet(signals, 'evidence', const <dynamic>[]),
  };
}

/// Port of core.semantic.contradiction_restraint_engine
/// .apply_contradiction_restraint. Mutates and returns `bundle`.
Map<dynamic, dynamic> applyContradictionRestraint(
    Map<dynamic, dynamic> bundle) {
  dynamic orElse(dynamic v, dynamic fallback) => pyTruthy(v) ? v : fallback;
  final contradicted = orElse(
      pyGet(bundle, 'contradicted', <dynamic, dynamic>{}),
      orElse(pyGet(bundle, 'contradictions', <dynamic, dynamic>{}),
          <dynamic, dynamic>{}));
  final pressure = computeContradictionPressure(contradicted);
  bundle['contradiction_pressure'] = pressure;
  bundle['fragility_pressure'] = <dynamic, dynamic>{
    ...pyGet(bundle, 'fragility_pressure', <dynamic, dynamic>{}) as Map,
    'contradiction': pressure['pressure'],
  };
  return bundle;
}
