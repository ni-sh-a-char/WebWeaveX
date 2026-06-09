import '_sort_util.dart';

/// Port of core/evolution_runtime/selector_evolution_engine.py
Map<String, dynamic> evolveSelectorRuntime([
  Map<String, dynamic>? selectors,
  Map<String, dynamic>? healed,
]) {
  final s = selectors ?? <String, dynamic>{};
  final h = healed ?? <String, dynamic>{};
  final evolved = <Map<String, dynamic>>[];

  final healedKeys = h.keys.toList()..sort(pyStrCompare);
  for (final original in healedKeys) {
    final replacement = h[original];
    evolved.add(<String, dynamic>{
      'original': original,
      'evolved': replacement,
      'strategy': 'healed_promotion',
      'fallback': "[data-evolved='$replacement']",
    });
  }

  final selectorKeys = s.keys.toList()..sort(pyStrCompare);
  for (final selector in selectorKeys) {
    if (h.containsKey(selector)) {
      continue;
    }
    evolved.add(<String, dynamic>{
      'original': selector,
      'evolved': s[selector],
      'strategy': 'structural_upgrade',
      'fallback': s[selector],
    });
  }

  return <String, dynamic>{
    'selectors': evolved,
    'count': evolved.length,
    'bounded': true,
  };
}
