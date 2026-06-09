/// Faithful Dart port of the Python `core.semantic.*` engines.
///
/// Each function mirrors the exact Map/List structure the corresponding
/// Python engine builds, so that `computeDeterministicHash` over the Dart
/// output equals Python's `compute_deterministic_hash` over the same output.
///
/// HTML-bearing engines (UI / tables) are ported for the empty-HTML path
/// only — no BeautifulSoup equivalent is bundled. Non-empty HTML is out of
/// scope and documented as such.
library;

/// Lexicographic comparison of two string tuples (mirrors Python tuple sort).
int _compareKeys(List<String> a, List<String> b) {
  for (var i = 0; i < a.length && i < b.length; i++) {
    final c = a[i].compareTo(b[i]);
    if (c != 0) return c;
  }
  return a.length.compareTo(b.length);
}

// ---------------------------------------------------------------------------
// entity_extraction_engine
// ---------------------------------------------------------------------------

final Map<String, RegExp> _entityPatterns = <String, RegExp>{
  'organization':
      RegExp(r'\b(inc|corp|llc|ltd|company)\b', caseSensitive: false),
  'api': RegExp(r'\b(api|endpoint|rest|graphql)\b', caseSensitive: false),
  'metric': RegExp(r'\b(kpi|metric|latency|throughput|error rate)\b',
      caseSensitive: false),
  'user': RegExp(r'\b(user|account|profile|login)\b', caseSensitive: false),
  'service':
      RegExp(r'\b(service|microservice|worker|queue)\b', caseSensitive: false),
  'workflow': RegExp(r'\b(workflow|pipeline|job|task)\b', caseSensitive: false),
  'infrastructure': RegExp(r'\b(kubernetes|docker|vm|cluster|deploy)\b',
      caseSensitive: false),
};

Map<String, dynamic> extractSemanticEntities(
  String text, [
  Map<String, dynamic>? structure,
]) {
  final struct = structure ?? <String, dynamic>{};
  final entities = <Map<String, dynamic>>[];
  final relations = <Map<String, dynamic>>[];
  var entityIndex = 0;

  for (final entry in _entityPatterns.entries) {
    final label = entry.key;
    if (entry.value.hasMatch(text)) {
      entities.add(<String, dynamic>{
        'id': 'entity:$label:$entityIndex',
        'type': label,
        'label': label,
        'source': 'pattern',
      });
      entityIndex++;
    }
  }

  final actions = (struct['actions'] as List<dynamic>? ?? const <dynamic>[]);
  for (final action in actions.take(5000)) {
    final a = action as Map<dynamic, dynamic>;
    final label = a['label'] ?? a['type'] ?? '';
    entities.add(<String, dynamic>{
      'id': 'entity:ui_action:$entityIndex',
      'type': 'ui_action',
      'label': '$label',
      'source': 'structure',
    });
    entityIndex++;
  }

  final artifacts =
      (struct['artifacts'] as List<dynamic>? ?? const <dynamic>[]);
  for (final artifact in artifacts.take(5000)) {
    entities.add(<String, dynamic>{
      'id': 'entity:runtime:$entityIndex',
      'type': 'runtime_artifact',
      'label': '$artifact',
      'source': 'runtime',
    });
    entityIndex++;
  }

  entities.sort((a, b) => (a['id'] as String).compareTo(b['id'] as String));

  for (var index = 1; index < entities.length; index++) {
    relations.add(<String, dynamic>{
      'from': entities[index - 1]['id'],
      'to': entities[index]['id'],
      'relation': 'related_to',
    });
  }

  return <String, dynamic>{
    'entities': entities,
    'relations': relations,
    'ontology': <String, dynamic>{},
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// entity_resolution_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> resolveSemanticEntities(List<dynamic> entities) {
  final canonical = <String, String>{};
  final resolved = <Map<String, dynamic>>[];

  final sorted = entities
      .map((e) => Map<String, dynamic>.from(e as Map<dynamic, dynamic>))
      .toList()
    ..sort((a, b) => '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));

  for (final entity in sorted) {
    final label =
        '${entity['label'] ?? entity['type'] ?? ''}'.toLowerCase().trim();
    var canonicalId = canonical[label];
    if (canonicalId == null || canonicalId.isEmpty) {
      canonicalId = '${entity['id'] ?? ''}';
      canonical[label] = canonicalId;
    }
    resolved.add(<String, dynamic>{
      ...entity,
      'canonical_id': canonicalId,
      'resolved': true,
    });
  }

  return <String, dynamic>{
    'entities': resolved,
    'canonical_map': canonical,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// domain_classification_engine
// ---------------------------------------------------------------------------

final List<List<dynamic>> _domainRules = <List<dynamic>>[
  <dynamic>[
    'saas',
    RegExp(r'\b(saas|subscription|tenant|workspace)\b', caseSensitive: false)
  ],
  <dynamic>[
    'finance',
    RegExp(r'\b(invoice|ledger|payment|billing|revenue)\b',
        caseSensitive: false)
  ],
  <dynamic>[
    'analytics',
    RegExp(r'\b(analytics|dashboard|kpi|metrics|report)\b',
        caseSensitive: false)
  ],
  <dynamic>[
    'infrastructure',
    RegExp(r'\b(kubernetes|terraform|infra|cluster|deploy)\b',
        caseSensitive: false)
  ],
  <dynamic>[
    'devops',
    RegExp(r'\b(ci/cd|pipeline|build|release|deploy)\b', caseSensitive: false)
  ],
  <dynamic>[
    'crm',
    RegExp(r'\b(crm|customer|lead|opportunity|contact)\b', caseSensitive: false)
  ],
  <dynamic>[
    'ecommerce',
    RegExp(r'\b(cart|checkout|product|order|sku)\b', caseSensitive: false)
  ],
  <dynamic>[
    'support',
    RegExp(r'\b(ticket|support|helpdesk|incident)\b', caseSensitive: false)
  ],
  <dynamic>[
    'security',
    RegExp(r'\b(security|auth|oauth|permission|role)\b', caseSensitive: false)
  ],
  <dynamic>[
    'developer_tooling',
    RegExp(r'\b(ide|repository|api|sdk|debug)\b', caseSensitive: false)
  ],
];

Map<String, dynamic> classifySemanticDomain(
  String text, [
  List<String>? signals,
]) {
  final sig = signals ?? const <String>[];
  final combined = '$text ${sig.join(' ')}';
  final scores = <String, int>{};

  for (final rule in _domainRules) {
    final domain = rule[0] as String;
    final pattern = rule[1] as RegExp;
    final matches = pattern.allMatches(combined).length;
    if (matches > 0) {
      scores[domain] = matches;
    }
  }

  String primary;
  if (scores.isEmpty) {
    primary = 'saas';
  } else {
    final entries = scores.entries.toList()
      ..sort((a, b) {
        final byScore = b.value.compareTo(a.value); // -score => descending
        if (byScore != 0) return byScore;
        return a.key.compareTo(b.key);
      });
    primary = entries.first.key;
  }

  return <String, dynamic>{
    'domain': primary,
    'scores': scores,
    'signals': sig,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// ontology_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> buildSemanticOntology(
  List<dynamic> entities,
  String domain,
) {
  final entityTypes = <String>{
    for (final e in entities) '${(e as Map<dynamic, dynamic>)['type'] ?? ''}'
  }.toList()
    ..sort();

  final taxonomy = <String, dynamic>{
    'entity': entityTypes,
    'runtime': <String>['browser', 'native', 'distributed', 'application'],
    'workflow': <String>['transition', 'submit', 'navigate', 'objective'],
    'ui': <String>['form', 'dashboard', 'navigation', 'authentication'],
    'infrastructure': <String>['service', 'api', 'deployment', 'monitoring'],
  };

  return <String, dynamic>{
    'entity_taxonomy': taxonomy['entity'],
    'runtime_ontology': taxonomy['runtime'],
    'workflow_ontology': taxonomy['workflow'],
    'ui_ontology': taxonomy['ui'],
    'infrastructure_ontology': taxonomy['infrastructure'],
    'primary_domain': domain,
    'taxonomy': taxonomy,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// ui_semantics_engine (empty-HTML path only)
// ---------------------------------------------------------------------------

Map<String, dynamic> extractUiSemantics(
  String html, [
  List<dynamic>? actions,
]) {
  if (html.trim().isNotEmpty) {
    throw UnsupportedError(
      'extractUiSemantics: non-empty HTML requires a BeautifulSoup-equivalent '
      'parser which is not bundled. Empty-HTML parity only.',
    );
  }
  final acts = actions ?? const <dynamic>[];
  return <String, dynamic>{
    'destructive_actions': <dynamic>[],
    'primary_workflows': <dynamic>[],
    'navigation_intent': false,
    'dashboards': false,
    'forms': 0,
    'admin_panels': false,
    'settings': false,
    'authentication': false,
    'billing': false,
    'monitoring': false,
    'actions': acts.take(1000).toList(),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// table_semantics_engine (empty-HTML path only)
// ---------------------------------------------------------------------------

Map<String, dynamic> extractTableSemantics(String html) {
  if (html.trim().isNotEmpty) {
    throw UnsupportedError(
      'extractTableSemantics: non-empty HTML requires a BeautifulSoup-equivalent '
      'parser which is not bundled. Empty-HTML parity only.',
    );
  }
  return <String, dynamic>{
    'tables': <dynamic>[],
    'primary_kind': 'none',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// document_semantics_engine
// ---------------------------------------------------------------------------

final List<List<dynamic>> _docKindRules = <List<dynamic>>[
  <dynamic>[
    'contract',
    RegExp(r'agreement|terms|party|signature', caseSensitive: false)
  ],
  <dynamic>[
    'technical_doc',
    RegExp(r'architecture|module|implementation', caseSensitive: false)
  ],
  <dynamic>[
    'api_reference',
    RegExp(r'endpoint|request|response|openapi', caseSensitive: false)
  ],
  <dynamic>['invoice', RegExp(r'invoice|amount due|tax', caseSensitive: false)],
  <dynamic>[
    'report',
    RegExp(r'summary|findings|quarter|annual', caseSensitive: false)
  ],
  <dynamic>[
    'resume',
    RegExp(r'experience|education|skills', caseSensitive: false)
  ],
  <dynamic>[
    'legal',
    RegExp(r'whereas|jurisdiction|liability', caseSensitive: false)
  ],
  <dynamic>[
    'specification',
    RegExp(r'requirements|shall|must|specification', caseSensitive: false)
  ],
];

Map<String, dynamic> extractDocumentSemantics(String text) {
  var kinds = <String>[
    for (final rule in _docKindRules)
      if ((rule[1] as RegExp).hasMatch(text)) rule[0] as String
  ];
  if (kinds.isEmpty) {
    kinds = <String>['document'];
  }
  final sortedKinds = <String>[...kinds]..sort();
  return <String, dynamic>{
    'kinds': sortedKinds,
    'primary_kind': sortedKinds.first,
    'length': text.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// repository_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractRepositorySemantics(
  List<String>? files,
  String text,
) {
  final f = files ?? const <String>[];
  final combined = '$text ${f.join(' ')}';

  final roles = <String>[];
  if (RegExp(r'api|routes|controller', caseSensitive: false)
      .hasMatch(combined)) {
    roles.add('api_surface');
  }
  if (RegExp(r'docker|k8s|helm|terraform', caseSensitive: false)
      .hasMatch(combined)) {
    roles.add('deployment_topology');
  }
  if (RegExp(r'service|worker|queue', caseSensitive: false)
      .hasMatch(combined)) {
    roles.add('service_boundary');
  }
  if (RegExp(r'react|vue|angular|next', caseSensitive: false)
      .hasMatch(combined)) {
    roles.add('frontend_framework');
  }
  if (RegExp(r'django|flask|fastapi|express', caseSensitive: false)
      .hasMatch(combined)) {
    roles.add('backend_framework');
  }

  var purpose = 'application';
  final lower = combined.toLowerCase();
  if (lower.contains('docs')) {
    purpose = 'documentation';
  } else if (lower.contains('infra')) {
    purpose = 'infrastructure';
  }

  final archRoles = roles.toSet().toList()..sort();

  return <String, dynamic>{
    'architecture_roles': archRoles,
    'service_boundaries': <String>[
      for (final r in roles)
        if (r == 'service_boundary') r
    ],
    'api_ownership': roles.contains('api_surface'),
    'deployment_topology': roles.contains('deployment_topology'),
    'framework_semantics': <String>[
      for (final r in roles)
        if (r.contains('framework')) r
    ],
    'repository_purpose': purpose,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// application_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractApplicationSemantics(
  Map<String, dynamic>? applicationResult,
) {
  final app = applicationResult ?? <String, dynamic>{};
  final workflow =
      (app['workflow'] as Map<dynamic, dynamic>? ?? const <dynamic, dynamic>{});
  final execution = (app['execution'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});
  final forms =
      (app['forms'] as Map<dynamic, dynamic>? ?? const <dynamic, dynamic>{});
  final intent =
      (app['intent'] as Map<dynamic, dynamic>? ?? const <dynamic, dynamic>{});
  final executed =
      (execution['executed'] as List<dynamic>? ?? const <dynamic>[]);
  final uiSemantics = (app['ui_semantics'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});
  final edges = (workflow['edges'] as List<dynamic>? ?? const <dynamic>[]);
  final formList = (forms['forms'] as List<dynamic>? ?? const <dynamic>[]);

  return <String, dynamic>{
    'workflow_purpose': '${intent['intent'] ?? 'operate'}',
    'runtime_intent': '${execution['objective'] ?? ''}',
    'business_operations': <String>[
      for (final step in executed)
        '${(step as Map<dynamic, dynamic>)['action'] ?? ''}'
    ],
    'ui_functionality': uiSemantics.keys.map((k) => '$k').toList(),
    'operational_actions': edges.length,
    'form_operations': formList.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// causality_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractCausalitySemantics(
  Map<String, dynamic>? causalityResult,
) {
  final causality = causalityResult ?? <String, dynamic>{};
  final inner = (causality['causality'] as Map<dynamic, dynamic>?) ?? causality;
  final propagation = (inner['propagation'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});
  final alignment = (inner['alignment'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});

  final handoffs =
      (propagation['handoffs'] as List<dynamic>? ?? const <dynamic>[]);
  final criticalChains = <Map<String, dynamic>>[
    for (final handoff in handoffs.take(1000))
      <String, dynamic>{
        'from': '${(handoff as Map<dynamic, dynamic>)['from'] ?? ''}',
        'to': '${handoff['to'] ?? ''}',
        'impact': 'cross_runtime_propagation',
      }
  ];

  return <String, dynamic>{
    'workflow_propagation_meaning': 'sequential_runtime_handoff',
    'operational_impact': criticalChains.length,
    'runtime_significance': alignment['runtime_count'] ?? 0,
    'critical_event_chains': criticalChains,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// workflow_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractWorkflowSemantics(
  Map<String, dynamic>? workflow,
  String objective,
) {
  final wf = workflow ?? <String, dynamic>{};
  final nodes = (wf['nodes'] as List<dynamic>? ?? const <dynamic>[]);
  final edges = (wf['edges'] as List<dynamic>? ?? const <dynamic>[]);

  return <String, dynamic>{
    'objective': objective,
    'workflow_steps': nodes.length,
    'transitions': edges.length,
    'semantic_intent': objective.isNotEmpty ? objective : 'operational_flow',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// browser_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractBrowserSemantics(
  String url,
  String html, [
  Map<String, dynamic>? extraction,
]) {
  final ext = extraction ?? <String, dynamic>{};
  final requests = (ext['requests'] as List<dynamic>? ?? const <dynamic>[]);
  return <String, dynamic>{
    'origin': url,
    'page_role': 'web_application',
    'network_artifacts': requests.length,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// runtime_semantics_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> extractRuntimeSemantics(
  Map<String, dynamic>? runtimeGraph,
  Map<String, dynamic>? sources,
) {
  final rg = runtimeGraph ?? <String, dynamic>{};
  final src = sources ?? <String, dynamic>{};
  final nodes = (rg['nodes'] as List<dynamic>? ?? const <dynamic>[]);
  final edges = (rg['edges'] as List<dynamic>? ?? const <dynamic>[]);
  final layers = src.keys.toList()..sort();
  return <String, dynamic>{
    'node_count': nodes.length,
    'edge_count': edges.length,
    'runtime_layers': layers,
    'meaning': 'unified_runtime_cognition',
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_alignment_engine
// ---------------------------------------------------------------------------

Map<String, dynamic> alignSemanticRuntimes({
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? repository,
  Map<String, dynamic>? document,
  Map<String, dynamic>? multimodal,
  Map<String, dynamic>? runtime,
}) {
  final layers = <String, dynamic>{
    'browser': browser ?? <String, dynamic>{},
    'native': native ?? <String, dynamic>{},
    'repository': repository ?? <String, dynamic>{},
    'document': document ?? <String, dynamic>{},
    'multimodal': multimodal ?? <String, dynamic>{},
    'runtime': runtime ?? <String, dynamic>{},
  };

  final alignedDomains = <Map<String, dynamic>>[];
  for (final entry in layers.entries) {
    final payload = entry.value as Map<dynamic, dynamic>;
    if (payload.isNotEmpty) {
      alignedDomains.add(<String, dynamic>{
        'layer': entry.key,
        'domain': '${payload['domain'] ?? payload['primary_kind'] ?? ''}',
      });
    }
  }

  return <String, dynamic>{
    'layers': layers,
    'aligned_domains': alignedDomains,
    'aligned': true,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_diff_engine
// ---------------------------------------------------------------------------

bool _deepEquals(dynamic a, dynamic b) {
  if (a is Map && b is Map) {
    if (a.length != b.length) return false;
    for (final k in a.keys) {
      if (!b.containsKey(k)) return false;
      if (!_deepEquals(a[k], b[k])) return false;
    }
    return true;
  }
  if (a is List && b is List) {
    if (a.length != b.length) return false;
    for (var i = 0; i < a.length; i++) {
      if (!_deepEquals(a[i], b[i])) return false;
    }
    return true;
  }
  return a == b;
}

Map<String, dynamic> diffSemanticRuntime(
  Map<String, dynamic> previous,
  Map<String, dynamic> current,
) {
  final prevEntities = <String>{
    for (final item in ((previous['entities'] as Map<dynamic, dynamic>? ??
            const <dynamic, dynamic>{})['entities'] as List<dynamic>? ??
        const <dynamic>[]))
      '${(item as Map<dynamic, dynamic>)['id'] ?? ''}'
  };
  final currEntities = <String>{
    for (final item in ((current['entities'] as Map<dynamic, dynamic>? ??
            const <dynamic, dynamic>{})['entities'] as List<dynamic>? ??
        const <dynamic>[]))
      '${(item as Map<dynamic, dynamic>)['id'] ?? ''}'
  };

  final prevDomain =
      '${(previous['domain'] as Map<dynamic, dynamic>? ?? const <dynamic, dynamic>{})['domain'] ?? ''}';
  final currDomain =
      '${(current['domain'] as Map<dynamic, dynamic>? ?? const <dynamic, dynamic>{})['domain'] ?? ''}';

  final added = currEntities.difference(prevEntities).toList()..sort();
  final removed = prevEntities.difference(currEntities).toList()..sort();

  return <String, dynamic>{
    'entities_added': added,
    'entities_removed': removed,
    'domain_changed': prevDomain != currDomain,
    'ontology_evolved': !_deepEquals(previous['ontology'], current['ontology']),
    'workflow_mutated': !_deepEquals(previous['workflow'], current['workflow']),
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// semantic_graph_engine
// ---------------------------------------------------------------------------

const Map<String, String> _relationMap = <String, String>{
  'organization': 'owns',
  'service': 'deploys',
  'api': 'exposes',
  'metric': 'monitors',
  'user': 'authenticates',
  'workflow': 'triggers',
  'infrastructure': 'depends_on',
  'ui_action': 'mutates',
};

Map<String, dynamic> buildSemanticGraph(
  List<dynamic> entities,
  List<dynamic> relations,
) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];

  for (final e in entities.take(10000)) {
    final entity = e as Map<dynamic, dynamic>;
    final entityType = '${entity['type'] ?? 'entity'}';
    nodes.add(<String, dynamic>{
      'id': '${entity['id'] ?? ''}',
      'type': entityType,
      'label': '${entity['label'] ?? ''}',
    });
  }

  for (final r in relations.take(10000)) {
    final relation = r as Map<dynamic, dynamic>;
    edges.add(<String, dynamic>{
      'from': '${relation['from'] ?? ''}',
      'to': '${relation['to'] ?? ''}',
      'relation': '${relation['relation'] ?? 'related_to'}',
    });
  }

  for (final e in entities.take(10000)) {
    final entity = e as Map<dynamic, dynamic>;
    final entityType = '${entity['type'] ?? ''}';
    final mapped = _relationMap[entityType];
    if (mapped != null && nodes.length > 1) {
      edges.add(<String, dynamic>{
        'from': '${entity['id'] ?? ''}',
        'to': nodes[0]['id'],
        'relation': mapped,
      });
    }
  }

  if (nodes.isEmpty) {
    nodes.add(<String, dynamic>{'id': 'semantic:root', 'type': 'semantic'});
  }

  final sortedNodes = <Map<String, dynamic>>[...nodes]
    ..sort((a, b) => (a['id'] as String).compareTo(b['id'] as String));
  final sortedEdges = <Map<String, dynamic>>[...edges]
    ..sort((a, b) => _compareKeys(
          <String>[
            '${a['from'] ?? ''}',
            '${a['to'] ?? ''}',
            '${a['relation'] ?? ''}'
          ],
          <String>[
            '${b['from'] ?? ''}',
            '${b['to'] ?? ''}',
            '${b['relation'] ?? ''}'
          ],
        ));

  return <String, dynamic>{
    'nodes': sortedNodes,
    'edges': sortedEdges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core.ir.semantic_runtime_ir
// ---------------------------------------------------------------------------

Map<String, dynamic> compileSemanticRuntimeIr(Map<String, dynamic> cognition) {
  return <String, dynamic>{
    'ir': 'semantic_runtime',
    'ontology': cognition['ontology'] ?? <String, dynamic>{},
    'entities': cognition['entities'] ?? <String, dynamic>{},
    'semantic_graph': cognition['semantic_graph'] ?? <String, dynamic>{},
    'domain': cognition['domain'] ?? <String, dynamic>{},
    'ui_semantics': cognition['ui'] ?? <String, dynamic>{},
    'table_semantics': cognition['tables'] ?? <String, dynamic>{},
    'document_semantics': cognition['document'] ?? <String, dynamic>{},
    'repository_semantics': cognition['repository'] ?? <String, dynamic>{},
    'application_semantics': cognition['application'] ?? <String, dynamic>{},
    'causality_semantics': cognition['causality'] ?? <String, dynamic>{},
    'workflow_semantics': cognition['workflow'] ?? <String, dynamic>{},
    'alignment': cognition['alignment'] ?? <String, dynamic>{},
    'bounded': true,
  };
}

Map<String, dynamic> semanticRuntimeIrToGraph(Map<String, dynamic> semanticIr) {
  final graph = (semanticIr['semantic_graph'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});
  var nodes = (graph['nodes'] as List<dynamic>? ?? const <dynamic>[])
      .map((n) => Map<String, dynamic>.from(n as Map<dynamic, dynamic>))
      .toList();
  final edges =
      (graph['edges'] as List<dynamic>? ?? const <dynamic>[]).toList();

  final ontology = (semanticIr['ontology'] as Map<dynamic, dynamic>? ??
      const <dynamic, dynamic>{});
  final primaryDomain = ontology['primary_domain'];
  if (primaryDomain != null && '$primaryDomain'.isNotEmpty) {
    nodes.add(<String, dynamic>{
      'id': 'domain:$primaryDomain',
      'type': 'domain',
    });
  }

  if (nodes.isEmpty) {
    nodes = <Map<String, dynamic>>[
      <String, dynamic>{'id': 'semantic:root', 'type': 'semantic'}
    ];
  }

  final sortedNodes = <Map<String, dynamic>>[...nodes]
    ..sort((a, b) => '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));

  return <String, dynamic>{
    'ir': 'semantic_runtime_graph',
    'nodes': sortedNodes,
    'edges': edges,
    'bounded': true,
  };
}

// ---------------------------------------------------------------------------
// core.runtime_graph.runtime_graph_engine — build_runtime_graph
// (list-of-IRs merge; distinct from the RuntimeGraph-class buildRuntimeGraph)
// ---------------------------------------------------------------------------

const int _maxGraphNodes = 1000000;
const int _maxGraphEdges = 5000000;

Map<String, dynamic> mergeRuntimeIrsToGraph(List<dynamic> runtimeIrs) {
  final nodes = <Map<String, dynamic>>[];
  final edges = <Map<String, dynamic>>[];
  final seenNodes = <String>{};
  final seenEdges = <String>{};

  for (final r in runtimeIrs.take(10000)) {
    final runtime = r as Map<dynamic, dynamic>;
    final runtimeType = '${runtime['ir'] ?? 'unknown'}';

    final runtimeNodes =
        (runtime['nodes'] as List<dynamic>? ?? const <dynamic>[]);
    final runtimeEdges =
        (runtime['edges'] as List<dynamic>? ?? const <dynamic>[]);

    for (final n in runtimeNodes) {
      final node = n as Map<dynamic, dynamic>;
      final nodeId = '${node['id'] ?? ''}'.trim();
      if (nodeId.isEmpty) continue;
      if (seenNodes.contains(nodeId)) continue;
      seenNodes.add(nodeId);
      final enriched = Map<String, dynamic>.from(node)
        ..['runtime_type'] = runtimeType;
      nodes.add(enriched);
      if (nodes.length >= _maxGraphNodes) break;
    }

    for (final e in runtimeEdges) {
      final edge = e as Map<dynamic, dynamic>;
      final src = '${edge['from'] ?? ''}'.trim();
      final dst = '${edge['to'] ?? ''}'.trim();
      final relation = '${edge['relation'] ?? 'related_to'}'.trim();
      if (src.isEmpty || dst.isEmpty) continue;
      final edgeKey = '$src $dst $relation';
      if (seenEdges.contains(edgeKey)) continue;
      seenEdges.add(edgeKey);
      final enriched = Map<String, dynamic>.from(edge)
        ..['runtime_type'] = runtimeType;
      edges.add(enriched);
      if (edges.length >= _maxGraphEdges) break;
    }
  }

  final sortedNodes = <Map<String, dynamic>>[...nodes]
    ..sort((a, b) => '${a['id'] ?? ''}'.compareTo('${b['id'] ?? ''}'));
  final sortedEdges = <Map<String, dynamic>>[...edges]
    ..sort((a, b) => _compareKeys(
          <String>[
            '${a['from'] ?? ''}',
            '${a['to'] ?? ''}',
            '${a['relation'] ?? ''}'
          ],
          <String>[
            '${b['from'] ?? ''}',
            '${b['to'] ?? ''}',
            '${b['relation'] ?? ''}'
          ],
        ));

  return <String, dynamic>{
    'ir': 'unified_runtime_graph',
    'nodes': sortedNodes,
    'edges': sortedEdges,
    'bounded': true,
  };
}
