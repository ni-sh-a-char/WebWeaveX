/// Phase A (document-parser leaves) of the Category-A semantic-IR port.
/// Canonical ports of core.documents.* leaf functions (no in-closure deps),
/// proven Python ≡ Dart by execution (validation/semantic_ir/). Pure regex/line
/// heuristics — bit-faithful to the Python source.
library;

const int maxArgumentEdges = 300;

final RegExp _headingLine = RegExp(r'^(#{1,6})\s+(.+)$');
final RegExp _listItem = RegExp(r'^[-*]\s+');
final RegExp _mdHeading = RegExp(r'^(#{1,6})\s+(.+)$', multiLine: true);
final RegExp _htmlHeading =
    RegExp(r'<h([1-6])[^>]*>(.*?)</h\1>', caseSensitive: false, dotAll: true);
final RegExp _headingTextOnly = RegExp(r'^#{1,6}\s+(.+)$', multiLine: true);
final RegExp _pronoun =
    RegExp(r'\b(it|this|that|they|these|those)\b', caseSensitive: false);

const List<List<String>> _rolePatternSpecs = <List<String>>[
  <String>[r'\b(example|for instance)\b', 'example'],
  <String>[r'\b(therefore|thus|hence)\b', 'conclusion'],
  <String>[r'\b(because|since|due to)\b', 'reason'],
  <String>[r'\b(note|warning|caution)\b', 'notice'],
];
final List<List<Object>> _rolePatterns = <List<Object>>[
  for (final s in _rolePatternSpecs)
    <Object>[RegExp(s[0], caseSensitive: false), s[1]],
];

/// Python str.splitlines() — splits on \n, \r, \r\n (and a few unicode breaks);
/// no trailing empty element. We cover the common \n/\r/\r\n cases.
List<String> _splitlines(String s) {
  if (s.isEmpty) return <String>[];
  return s.split(RegExp(r'\r\n|\r|\n'));
}

/// Port of core.documents.rhetorical_structure_engine.extract_rhetorical_structure.
Map<String, dynamic> extractRhetoricalStructure(String? text) {
  final lines = _splitlines(text ?? '');
  final units = <Map<String, dynamic>>[];
  for (var i = 0; i < lines.length; i++) {
    final stripped = lines[i].trim();
    final m = _headingLine.firstMatch(stripped);
    if (m != null) {
      units.add(<String, dynamic>{
        'type': 'heading',
        'level': m.group(1)!.length,
        'title': m.group(2),
        'line': i,
      });
    } else if (_listItem.hasMatch(stripped)) {
      units.add(<String, dynamic>{'type': 'list_item', 'line': i});
    } else if (stripped.startsWith('```')) {
      units.add(<String, dynamic>{'type': 'code_fence', 'line': i});
    }
  }
  return <String, dynamic>{
    'units': units,
    'unit_count': units.length,
    'deterministic_inputs': <String>['units=${units.length}'],
  };
}

/// Port of core.documents.semantic_role_engine.assign_semantic_roles.
Map<String, dynamic> assignSemanticRoles(String? text) {
  final roles = <Map<String, dynamic>>[];
  final lines = _splitlines(text ?? '');
  for (var i = 0; i < lines.length; i++) {
    final ln = lines[i];
    for (final spec in _rolePatterns) {
      if ((spec[0] as RegExp).hasMatch(ln)) {
        roles.add(<String, dynamic>{
          'line': i,
          'role': spec[1],
          'text': ln.length > 120 ? ln.substring(0, 120) : ln,
        });
        break;
      }
    }
  }
  return <String, dynamic>{'roles': roles, 'count': roles.length};
}

/// Port of core.documents.heading_engine.extract_headings.
Map<String, dynamic> extractHeadings(String? text) {
  final src = text ?? '';
  final items = <Map<String, dynamic>>[];
  for (final m in _mdHeading.allMatches(src)) {
    items.add(<String, dynamic>{
      'level': m.group(1)!.length,
      'title': m.group(2)!.trim(),
    });
  }
  for (final m in _htmlHeading.allMatches(src)) {
    items.add(<String, dynamic>{
      'level': int.parse(m.group(1)!),
      'title': m.group(2)!.trim(),
    });
  }
  // sorted(md + html, key=lambda x: (x["level"], x["title"])) — stable.
  final indexed = <List<dynamic>>[
    for (var i = 0; i < items.length; i++) <dynamic>[items[i], i]
  ]..sort((a, b) {
      final am = a[0] as Map<String, dynamic>;
      final bm = b[0] as Map<String, dynamic>;
      final c = (am['level'] as int).compareTo(bm['level'] as int);
      if (c != 0) return c;
      final t = (am['title'] as String).compareTo(bm['title'] as String);
      return t != 0 ? t : (a[1] as int).compareTo(b[1] as int);
    });
  return <String, dynamic>{
    'headings': <dynamic>[for (final p in indexed) p[0]],
  };
}

/// Port of core.documents.argument_dependency_engine.reconstruct_argument_dependencies.
Map<String, dynamic> reconstructArgumentDependencies(
    List<Map<String, dynamic>> claims) {
  int orderOf(Map<String, dynamic> c) {
    final o = c['order'];
    if (o is int) return o;
    if (o is num) return o.toInt();
    if (o is String) return int.tryParse(o) ?? 0;
    return 0;
  }

  final indexed = <List<dynamic>>[
    for (var i = 0; i < claims.length; i++) <dynamic>[claims[i], i]
  ]..sort((a, b) {
      final c = orderOf(a[0] as Map<String, dynamic>)
          .compareTo(orderOf(b[0] as Map<String, dynamic>));
      return c != 0 ? c : (a[1] as int).compareTo(b[1] as int);
    });
  final ordered = <Map<String, dynamic>>[
    for (final p in indexed) p[0] as Map<String, dynamic>
  ];

  final edges = <Map<String, dynamic>>[];
  for (var idx = 1; idx < ordered.length; idx++) {
    final prevC = ordered[idx - 1];
    final curC = ordered[idx];
    if (curC['depends_on'] != null &&
        curC['depends_on'].toString().isNotEmpty) {
      edges.add(<String, dynamic>{
        'from': curC['depends_on'],
        'to': curC['id'],
        'metadata': <String, dynamic>{
          'kind': 'argument_support',
          'basis': 'explicit_dependency',
        },
      });
    } else {
      edges.add(<String, dynamic>{
        'from': prevC['id'],
        'to': curC['id'],
        'metadata': <String, dynamic>{
          'kind': 'argument_sequence',
          'basis': 'document_order',
        },
      });
    }
  }
  final bounded = edges.length > maxArgumentEdges
      ? edges.sublist(0, maxArgumentEdges)
      : edges;
  return <String, dynamic>{
    'edges': bounded,
    'count': edges.length > maxArgumentEdges ? maxArgumentEdges : edges.length,
    'deterministic': true,
  };
}

/// Port of core.documents.coreference_resolution_engine.resolve_coreferences.
Map<String, dynamic> resolveCoreferences(String? text) {
  final src = text ?? '';
  final headings =
      _headingTextOnly.allMatches(src).map((m) => m.group(1)!).toList();
  final pronouns = _pronoun.allMatches(src).map((m) => m.group(1)!).toList();
  final antecedent = headings.isNotEmpty ? headings.last : '';
  final limited = pronouns.length > 50 ? pronouns.sublist(0, 50) : pronouns;
  final chains = <Map<String, dynamic>>[
    for (final p in limited)
      <String, dynamic>{'pronoun': p, 'antecedent': antecedent}
  ];
  return <String, dynamic>{'chains': chains, 'count': chains.length};
}
