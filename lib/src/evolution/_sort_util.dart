/// Stable sort matching Python's `sorted` (Timsort is stable; Dart's
/// List.sort is not). Used wherever the Python reference relies on stable
/// ordering for tie-break determinism.
List<T> stableSorted<T>(Iterable<T> items, int Function(T a, T b) compare) {
  final indexed = items.toList(growable: false);
  final order = List<int>.generate(indexed.length, (i) => i);
  order.sort((ai, bi) {
    final c = compare(indexed[ai], indexed[bi]);
    if (c != 0) return c;
    return ai.compareTo(bi);
  });
  return <T>[for (final i in order) indexed[i]];
}

/// Compares two strings by Unicode code point, matching Python `str` ordering.
int pyStrCompare(String a, String b) {
  final ar = a.runes.toList(growable: false);
  final br = b.runes.toList(growable: false);
  final n = ar.length < br.length ? ar.length : br.length;
  for (var i = 0; i < n; i++) {
    if (ar[i] != br[i]) return ar[i] < br[i] ? -1 : 1;
  }
  if (ar.length == br.length) return 0;
  return ar.length < br.length ? -1 : 1;
}
