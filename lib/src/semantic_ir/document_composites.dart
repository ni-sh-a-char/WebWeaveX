/// Phase B document-layer composites of the Category-A semantic-IR port —
/// core.documents engines whose only in-closure dependencies are the proven
/// A.1 parser leaves. Proven Python ≡ JavaScript ≡ Dart by execution
/// (validation/semantic_ir/).
library;

import 'document_parser.dart'
    show
        assignSemanticRoles,
        extractHeadings,
        extractRhetoricalStructure,
        reconstructArgumentDependencies;
import 'py_compat.dart';

/// Python str.splitlines() over the common \n/\r/\r\n cases (mirrors
/// document_parser.dart's private helper).
List<String> _splitlines(String s) {
  if (s.isEmpty) return <String>[];
  return s.split(RegExp(r'\r\n|\r|\n'));
}

/// Port of core.documents.argument_dependency_engine.build_argument_dependencies.
Map<String, dynamic> buildArgumentDependencies(String text) {
  final lines = <String>[
    for (final ln in _splitlines(text))
      if (ln.trim().isNotEmpty) ln.trim()
  ];
  final claims = <Map<String, dynamic>>[
    for (var i = 0; i < lines.length; i++)
      <String, dynamic>{'id': 'c$i', 'order': i, 'content': lines[i]}
  ];
  final r = reconstructArgumentDependencies(claims);
  final nodes = <Map<String, dynamic>>[
    for (final c in claims)
      <String, dynamic>{'id': c['id'], 'content': c['content']}
  ];
  return <String, dynamic>{
    'dependencies': pyGet(r, 'edges', const <dynamic>[]),
    'nodes': nodes,
    'evidence': <String>['discourse:argument_order'],
    'deterministic': true,
  };
}

/// Port of core.documents.argument_graph_engine.build_argument_graph.
Map<String, dynamic> buildArgumentGraph(String text) {
  final rhet = extractRhetoricalStructure(text);
  final headings = <Map<dynamic, dynamic>>[
    for (final u in rhet['units'] as List)
      if (pyGet(u as Map, 'type', null) == 'heading') u
  ];
  final nodes = <Map<String, dynamic>>[
    for (var i = 0; i < headings.length; i++)
      <String, dynamic>{
        'id': 'h$i',
        'role': i == 0 ? 'claim' : 'support',
        'title': pyGet(headings[i], 'title', ''),
      }
  ];
  final edges = <Map<String, dynamic>>[
    for (var i = 0; i < nodes.length - 1; i++)
      <String, dynamic>{'from': nodes[i]['id'], 'to': nodes[i + 1]['id']}
  ];
  return <String, dynamic>{
    'nodes': nodes,
    'edges': edges,
    'deterministic_inputs': <String>['nodes=${nodes.length}'],
  };
}

/// Port of core.documents.instructional_flow_engine.extract_instructional_flow.
Map<String, dynamic> extractInstructionalFlow(String text) {
  final rhet = extractRhetoricalStructure(text);
  final steps = <Map<String, dynamic>>[];
  const keywords = <String>[
    'step',
    'tutorial',
    'install',
    'setup',
    'prerequisite'
  ];
  for (final uRaw in rhet['units'] as List) {
    final u = uRaw as Map;
    if (pyGet(u, 'type', null) == 'heading') {
      final title = pyToStr(pyGet(u, 'title', '')).toLowerCase();
      if (keywords.any(title.contains)) {
        steps.add(<String, dynamic>{
          'title': pyGet(u, 'title', null),
          'line': pyGet(u, 'line', null),
        });
      } else if ((pyGet(u, 'level', 9) as num) <= 2) {
        steps.add(<String, dynamic>{
          'title': pyGet(u, 'title', null),
          'line': pyGet(u, 'line', null),
          'implicit': true,
        });
      }
    }
  }
  final prerequisites = <dynamic>[
    for (var i = 0; i < steps.length - 1; i++) steps[i]['title']
  ];
  return <String, dynamic>{
    'steps': steps,
    'prerequisites': prerequisites,
    'deterministic_inputs': <String>['steps=${steps.length}'],
  };
}

/// Port of core.documents.rhetorical_parser_engine.parse_rhetorical_structure.
Map<String, dynamic> parseRhetoricalStructure(String text) {
  final structure = extractRhetoricalStructure(text);
  final roles = assignSemanticRoles(text);
  final units = pyGet(structure, 'units', const <dynamic>[]) as List;
  final roleMap = <dynamic, dynamic>{
    for (final r in pyGet(roles, 'roles', const <dynamic>[]) as List)
      if ((r as Map).containsKey('line')) r['line']: r['role']
  };
  final enriched = <Map<dynamic, dynamic>>[];
  for (final uRaw in units) {
    final u = uRaw as Map;
    final line = pyGet(u, 'line', null);
    enriched.add(<dynamic, dynamic>{
      ...u,
      'role': roleMap.containsKey(line)
          ? roleMap[line]
          : (pyGet(u, 'type', null) == 'heading' ? 'nucleus' : 'span'),
    });
  }
  final rhetoricalRoles = <String>{
    for (final r in enriched)
      if (pyTruthy(pyGet(r, 'role', ''))) pyGet(r, 'role', '') as String
  }.toList()
    ..sort();
  return <String, dynamic>{
    'units': enriched,
    'unit_count': enriched.length,
    'roles': pyGet(roles, 'roles', const <dynamic>[]),
    'rhetorical_roles': rhetoricalRoles,
    'deterministic_inputs': <dynamic>[
      ...pyGet(structure, 'deterministic_inputs', const <dynamic>[]) as List,
      'roles=${(pyGet(roles, 'roles', const <dynamic>[]) as List).length}',
    ],
  };
}

/// Port of core.documents.section_engine.extract_sections.
Map<String, dynamic> extractSections(String text) {
  final heads =
      pyGet(extractHeadings(text), 'headings', const <dynamic>[]) as List;
  final sections = <String>[
    for (final h in heads) pyGet(h as Map, 'title', '') as String
  ];
  final hierarchy = <Map<String, dynamic>>[
    for (final h in heads)
      <String, dynamic>{
        'title': pyGet(h as Map, 'title', ''),
        'level': pyGet(h, 'level', 1),
      }
  ];
  return <String, dynamic>{
    'sections': sections.toSet().toList()..sort(),
    'hierarchy': hierarchy,
  };
}
