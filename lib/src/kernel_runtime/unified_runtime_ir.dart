/// Port of core/ir/unified_runtime_ir.py — compileUnifiedRuntimeIr.
///
/// Parity contract: the returned map is byte-identical to the Python
/// `compile_unified_runtime_ir(...)` under `compute_deterministic_hash`.
library;

Map<String, dynamic> _phasePayload(
  Map<String, dynamic> phases,
  Map<String, dynamic> sources,
  String key,
) {
  if (phases.containsKey(key)) {
    final value = phases[key];
    if (value is Map) {
      return Map<String, dynamic>.from(value);
    }
    return <String, dynamic>{'payload': value};
  }
  final src = sources[key];
  if (src is Map) {
    return Map<String, dynamic>.from(src);
  }
  return <String, dynamic>{};
}

dynamic _phaseOrSource(
  Map<String, dynamic> phases,
  String phaseKey,
  Map<String, dynamic> sources,
  String sourceKey,
) {
  if (phases.containsKey(phaseKey)) {
    return phases[phaseKey];
  }
  final src = sources[sourceKey];
  return src ?? <String, dynamic>{};
}

int _busSortKey(Map<String, dynamic> a, Map<String, dynamic> b) {
  final at = (a['tick'] as int?) ?? 0;
  final bt = (b['tick'] as int?) ?? 0;
  if (at != bt) return at.compareTo(bt);
  final ao = (a['order'] as int?) ?? 0;
  final bo = (b['order'] as int?) ?? 0;
  return ao.compareTo(bo);
}

/// Compile the unified runtime IR from registry/graph/bus/phase results.
Map<String, dynamic> compileUnifiedRuntimeIr({
  Map<String, dynamic>? registry,
  Map<String, dynamic>? graph,
  List<Map<String, dynamic>>? bus,
  List<Map<String, dynamic>>? phaseResults,
  Map<String, dynamic>? sources,
}) {
  final reg = registry ?? <String, dynamic>{};
  final g = graph ?? <String, dynamic>{};
  final busList =
      List<Map<String, dynamic>>.from(bus ?? <Map<String, dynamic>>[]);
  final prList =
      List<Map<String, dynamic>>.from(phaseResults ?? <Map<String, dynamic>>[]);
  final src = sources ?? <String, dynamic>{};

  final phasesRaw = reg['phases'];
  final phases = phasesRaw is Map
      ? Map<String, dynamic>.from(phasesRaw)
      : <String, dynamic>{};

  // Python sorted() is stable; index-tiebreak preserves original order on ties.
  final sortedBus = busList.asMap().entries.toList()
    ..sort((a, b) {
      final cmp = _busSortKey(a.value, b.value);
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });
  final sortedPr = prList.asMap().entries.toList()
    ..sort((a, b) {
      final cmp =
          '${a.value['phase'] ?? ''}'.compareTo('${b.value['phase'] ?? ''}');
      return cmp != 0 ? cmp : a.key.compareTo(b.key);
    });

  return <String, dynamic>{
    'ir': 'unified_runtime',
    'browser': _phasePayload(phases, src, 'browser'),
    'interaction': _phasePayload(phases, src, 'interaction'),
    'streaming': _phasePayload(phases, src, 'streaming'),
    'adaptive': _phasePayload(phases, src, 'adaptive'),
    'application': _phasePayload(phases, src, 'application'),
    'native': _phasePayload(phases, src, 'native'),
    'causality': _phasePayload(phases, src, 'causality'),
    'semantic': _phaseOrSource(phases, 'semantic', src, 'semantic'),
    'workflow': _phaseOrSource(phases, 'semantic', src, 'workflow'),
    'synchronization': _phaseOrSource(phases, 'synchronization', src, 'sync'),
    'evolution': _phasePayload(phases, src, 'evolution'),
    'connectors': _phasePayload(phases, src, 'connectors'),
    'memory': _phaseOrSource(phases, 'memory', src, 'memory'),
    'execution': _phaseOrSource(phases, 'execution', src, 'execution'),
    'reconstruction':
        _phaseOrSource(phases, 'reconstruction', src, 'reconstruction'),
    'runtime_graph': g,
    'event_bus': sortedBus.map((e) => e.value).toList(),
    'phase_results': sortedPr.map((e) => e.value).toList(),
    'bounded': true,
  };
}
