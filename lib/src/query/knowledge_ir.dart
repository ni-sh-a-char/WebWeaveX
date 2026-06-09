/// Native Dart port of the deterministic knowledge / ontology IR pipeline
/// (Python `core/knowledge/*`, `core/evidence/*`, `core/ir/knowledge_ir.py`).
///
/// Parity proven against `compute_deterministic_hash`.
library;

import 'dart:convert';

import 'package:crypto/crypto.dart';

List<dynamic> _asList(dynamic v) =>
    v is List ? List<dynamic>.from(v) : <dynamic>[];

Map<String, dynamic> _asMap(dynamic v) =>
    v is Map ? Map<String, dynamic>.from(v) : <String, dynamic>{};

/// Port of `core.knowledge.semantic_identity_calculus.identity_hash`.
Map<String, dynamic> identityHash(String name, [String namespace = '']) {
  final raw = utf8.encode('$namespace:$name');
  final digest = sha256.convert(raw).toString().substring(0, 16);
  return <String, dynamic>{
    'name': name,
    'namespace': namespace,
    'id': digest,
    'deterministic_inputs': <String>['name=$name', 'namespace=$namespace'],
  };
}

/// Port of `core.knowledge.semantic_identity_resolver.resolve_semantic_identities`.
Map<String, dynamic> resolveSemanticIdentities(List<dynamic> entities,
    [String namespace = '']) {
  final resolved = <Map<String, dynamic>>[];
  for (final e in entities) {
    if (e != null && '$e'.isNotEmpty && e != false) {
      resolved.add(identityHash('$e', namespace));
    }
  }
  final byId = <String, dynamic>{};
  for (final r in resolved) {
    byId['${r['id']}'] = r['name'];
  }
  return <String, dynamic>{
    'entities': resolved,
    'index': byId,
    'count': resolved.length,
  };
}

/// Port of `core.knowledge.ontology_lineage_engine.stamp_ontology_lineage`.
Map<String, dynamic> stampOntologyLineage(Map<String, dynamic> edge,
    {String stage = 'ontology'}) {
  final lineage = _asMap(edge['lineage']);
  final stages = lineage['stages'] is List
      ? List<dynamic>.from(lineage['stages'] as List)
      : <dynamic>[];
  stages.add(<String, dynamic>{
    'stage': stage,
    'from': edge['from'],
    'to': edge['to'],
  });
  return <String, dynamic>{
    ...edge,
    'lineage': <String, dynamic>{
      ...lineage,
      'stages': stages,
      'depth': stages.length,
    },
  };
}

/// Port of `core.knowledge.semantic_merge_rigor_engine.merge_with_evidence`.
Map<String, dynamic> mergeWithEvidence(List<Map<String, dynamic>> sources) {
  final mergedEvidence = <String>[];
  for (final s in sources) {
    var ev = s['evidence'] ?? <dynamic>[];
    if (ev is String) ev = <dynamic>[ev];
    final evList = _asList(ev);
    if (evList.isEmpty) {
      return <String, dynamic>{
        'merged': false,
        'reason': 'silent_merge_forbidden',
        'sources': sources.length,
      };
    }
    for (final e in evList) {
      mergedEvidence.add('$e');
    }
  }
  final unique = mergedEvidence.toSet().toList()..sort();
  return <String, dynamic>{
    'merged': true,
    'evidence': unique,
    'source_count': sources.length,
    'deterministic_inputs': <String>['sources=${sources.length}'],
  };
}

/// Port of `core.knowledge.ontology_reconciliation_engine.reconcile_ontology_edges`.
Map<String, dynamic> reconcileOntologyEdges(List<dynamic> edges) {
  final reconciled = <Map<String, dynamic>>[];
  final rejected = <Map<String, dynamic>>[];
  for (final e in edges) {
    final em = _asMap(e);
    final ev = _asList(em['evidence']);
    if (ev.isEmpty) {
      rejected.add(<String, dynamic>{'edge': e, 'reason': 'missing_evidence'});
      continue;
    }
    reconciled.add(stampOntologyLineage(em, stage: 'reconcile'));
  }
  final mergeInput = reconciled
      .map((e) => <String, dynamic>{'evidence': e['evidence'] ?? <dynamic>[]})
      .toList();
  final merge = mergeWithEvidence(mergeInput);
  return <String, dynamic>{
    'reconciled': reconciled,
    'rejected': rejected,
    'merge': merge,
    'lineage': <String, dynamic>{
      'stage': 'ontology_reconciliation',
      'count': reconciled.length,
    },
  };
}

/// Port of `core.evidence.contradiction_lattice_engine.build_contradiction_lattice`.
Map<String, dynamic> buildContradictionLattice(List<dynamic> pairs) {
  final normalized = <List<String>>[];
  for (final p in pairs) {
    if (p is List && p.length >= 2) {
      normalized.add(<String>['${p[0]}', '${p[1]}']);
    }
  }
  final count = normalized.length;
  final pressure = _round(_min(1.0, count * 0.25), 3);
  // sorted(normalized): tuples compared lexicographically (first then second).
  final sorted = List<List<String>>.from(normalized)
    ..sort((a, b) {
      final c = a[0].compareTo(b[0]);
      if (c != 0) return c;
      return a[1].compareTo(b[1]);
    });
  return <String, dynamic>{
    'pairs': sorted.map((t) => <String>[t[0], t[1]]).toList(),
    'count': count,
    'pressure': pressure,
    'rigor': 'lattice_enumeration',
    'deterministic_inputs': <String>['pair_count=$count', 'pressure=$pressure'],
  };
}

/// Port of `core.knowledge.ontology_conflict_engine.detect_ontology_conflicts`.
Map<String, dynamic> detectOntologyConflicts(List<dynamic> edges) {
  final pairs = <List<String>>[];
  for (final e in edges) {
    final em = _asMap(e);
    final c = _asMap(em['contradictions']);
    for (final p in _asList(c['pairs'])) {
      if (p is List && p.length >= 2) {
        pairs.add(<String>['${p[0]}', '${p[1]}']);
      }
    }
  }
  final lattice = buildContradictionLattice(pairs);
  return <String, dynamic>{
    'conflicts': lattice['pairs'],
    'pressure': lattice['pressure'],
    'contradiction_pressure': lattice['pressure'],
    'uncertainty': <String, dynamic>{'visible': (lattice['count'] as int) > 0},
  };
}

/// Port of `core.ir.knowledge_ir.compile_knowledge_ir`.
Map<String, dynamic> compileKnowledgeIr(
    List<dynamic> entities, List<dynamic> edges) {
  final recon = reconcileOntologyEdges(edges);
  final ids = resolveSemanticIdentities(entities);
  final conflicts = detectOntologyConflicts(edges);
  final conflictList = _asList(conflicts['conflicts']);
  final evidence = <dynamic>[];
  for (final e in edges) {
    if (e is Map) {
      evidence.add(e['evidence'] ?? <dynamic>[]);
    }
  }
  return <String, dynamic>{
    'entities': entities,
    'relations': recon['reconciled'] ?? <dynamic>[],
    'ontology': edges,
    'semantic_identity': ids['entities'] ?? <dynamic>[],
    'contradictions': conflicts['conflicts'] ?? <dynamic>[],
    'evidence': evidence,
    'lineage': <dynamic>[recon['lineage']],
    'reconciliation': recon,
    'confidence': <String, dynamic>{
      'score': conflictList.isEmpty ? 0.9 : 0.5,
      'basis': <dynamic>[],
      'deterministic': true,
    },
  };
}

num _min(num a, num b) => a < b ? a : b;

/// Mirrors Python `round(x, n)` (banker's rounding) for the small positive
/// values used here.
num _round(num value, int digits) {
  final factor = _pow10(digits);
  final scaled = value * factor;
  final floor = scaled.floorToDouble();
  final diff = scaled - floor;
  double rounded;
  if (diff > 0.5) {
    rounded = floor + 1;
  } else if (diff < 0.5) {
    rounded = floor;
  } else {
    // Banker's rounding: round half to even.
    rounded = (floor % 2 == 0) ? floor : floor + 1;
  }
  final result = rounded / factor;
  return result;
}

double _pow10(int n) {
  var r = 1.0;
  for (var i = 0; i < n; i++) {
    r *= 10;
  }
  return r;
}
