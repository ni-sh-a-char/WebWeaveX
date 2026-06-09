/// Port of core/execution/runtime_mutation_engine.track_runtime_mutations.
Map<String, dynamic> trackRuntimeMutations({
  List<Map<String, dynamic>>? prior,
  Map<String, dynamic>? mutation,
}) {
  final List<Map<String, dynamic>> mutations = <Map<String, dynamic>>[
    ...(prior ?? <Map<String, dynamic>>[])
  ];
  if (mutation != null) {
    mutations.add(<String, dynamic>{
      'kind': '${mutation['kind'] ?? 'unknown'}',
      'target': '${mutation['target'] ?? ''}',
      'tick': _asInt(mutation['tick'], 0),
      'ordered_index': mutations.length,
    });
  }

  final List<Map<String, dynamic>> sortedMutations = <Map<String, dynamic>>[
    ...mutations
  ]..sort((Map<String, dynamic> a, Map<String, dynamic> b) {
      final int t = _asInt(a['tick'], 0).compareTo(_asInt(b['tick'], 0));
      if (t != 0) return t;
      final int oi = _asInt(a['ordered_index'], 0)
          .compareTo(_asInt(b['ordered_index'], 0));
      if (oi != 0) return oi;
      return '${a['kind'] ?? ''}'.compareTo('${b['kind'] ?? ''}');
    });

  Map<String, dynamic> byKind = <String, dynamic>{
    'dom': sortedMutations
        .where((Map<String, dynamic> m) => m['kind'] == 'dom')
        .toList(),
    'native': sortedMutations
        .where((Map<String, dynamic> m) => m['kind'] == 'native')
        .toList(),
    'workflow': sortedMutations
        .where((Map<String, dynamic> m) => m['kind'] == 'workflow')
        .toList(),
    'synchronization': sortedMutations
        .where((Map<String, dynamic> m) => m['kind'] == 'sync')
        .toList(),
    'memory': sortedMutations
        .where((Map<String, dynamic> m) => m['kind'] == 'memory')
        .toList(),
  };

  return <String, dynamic>{
    'mutations': sortedMutations,
    'by_kind': byKind,
    'count': sortedMutations.length,
    'deterministic_order': true,
    'bounded': true,
  };
}

int _asInt(dynamic v, int fallback) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? fallback;
  return fallback;
}
