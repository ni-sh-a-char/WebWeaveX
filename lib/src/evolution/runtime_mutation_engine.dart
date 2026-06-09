import '_sort_util.dart';

const int maxMutations = 10000;

/// Port of core/evolution_runtime/runtime_mutation_engine.py
List<Map<String, dynamic>> buildRuntimeMutations(
  Map<String, dynamic> selector,
  Map<String, dynamic> workflow,
  Map<String, dynamic> semantic,
  Map<String, dynamic> sync,
) {
  final mutations = <Map<String, dynamic>>[];

  final selectors = (selector['selectors'] as List?) ?? <dynamic>[];
  for (final raw in selectors.take(maxMutations)) {
    final item = raw as Map;
    mutations.add(<String, dynamic>{
      'kind': 'selector',
      'target': '${item['original'] ?? ''}',
      'evolved': '${item['evolved'] ?? ''}',
    });
  }

  final executionOrdering = workflow['execution_ordering'];
  if (_truthy(executionOrdering)) {
    mutations.add(<String, dynamic>{
      'kind': 'workflow',
      'target': 'execution_ordering',
      'evolved': executionOrdering,
    });
  }

  final domain = semantic['domain'];
  if (_truthy(domain)) {
    mutations.add(<String, dynamic>{
      'kind': 'semantic',
      'target': 'domain',
      'evolved': domain,
    });
  }

  final convergence = sync['convergence'];
  if (_truthy(convergence)) {
    mutations.add(<String, dynamic>{
      'kind': 'sync',
      'target': 'convergence',
      'evolved': true,
    });
  }

  return stableSorted<Map<String, dynamic>>(mutations, (a, b) {
    final c = pyStrCompare('${a['kind']}', '${b['kind']}');
    if (c != 0) return c;
    return pyStrCompare('${a['target']}', '${b['target']}');
  });
}

bool _truthy(dynamic v) {
  if (v == null) return false;
  if (v is bool) return v;
  if (v is String) return v.isNotEmpty;
  if (v is num) return v != 0;
  if (v is Iterable) return v.isNotEmpty;
  if (v is Map) return v.isNotEmpty;
  return true;
}
