import 'dart:convert';

import '../graph/runtime_graph.dart';
import 'normalization.dart';

String stableSerialize(dynamic value) {
  if (value is String) {
    return normalizeRuntimeValue(value);
  }
  if (value is RuntimeGraph) {
    return jsonEncode(
        stableSortKeys(Map<String, dynamic>.from(value.toJson())));
  }
  if (value is Map) {
    return jsonEncode(stableSortKeys(Map<String, dynamic>.from(value)));
  }
  if (value is List) {
    final asMap = <String, dynamic>{};
    for (var i = 0; i < value.length; i++) {
      final item = value[i];
      if (item is Map) {
        asMap['$i'] = stableSortKeys(Map<String, dynamic>.from(item));
      } else {
        asMap['$i'] = item;
      }
    }
    return jsonEncode(stableSortKeys(asMap));
  }
  return jsonEncode(value);
}
