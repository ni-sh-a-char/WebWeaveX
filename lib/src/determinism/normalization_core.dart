const volatileRuntimeKeys = {
  'timestamp',
  'created_at',
  'updated_at',
  'nonce',
  'request_id',
  'csrf',
  'generated_at',
  'runtime_id',
  'random',
  'uuid',
};

String normalizeRuntimeValueCore(String value) {
  var s = value.replaceAll('\r\n', '\n').replaceAll('\r', '\n');
  s = s.replaceAll(RegExp(r'\s+$'), '');
  return s;
}

Map<String, dynamic> stableSortKeys(Map<String, dynamic> obj) {
  final sorted = <String, dynamic>{};
  final keys = obj.keys.toList()..sort();
  for (final k in keys) {
    if (volatileRuntimeKeys.contains(k)) continue;
    final v = obj[k];
    if (v is Map) {
      sorted[k] = stableSortKeys(Map<String, dynamic>.from(v));
    } else if (v is List) {
      sorted[k] = v.map((item) {
        if (item is Map) {
          return stableSortKeys(Map<String, dynamic>.from(item));
        }
        return item;
      }).toList();
    } else {
      sorted[k] = v;
    }
  }
  return sorted;
}

dynamic normalizeRuntimeState(Map<String, dynamic> state) =>
    stableSortKeys(state);
