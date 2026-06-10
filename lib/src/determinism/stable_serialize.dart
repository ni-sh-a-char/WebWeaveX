import '../graph/runtime_graph.dart';
import 'canonical_json_encode.dart';
import 'normalization.dart';

String stableSerialize(dynamic value) {
  if (value is String) {
    return normalizeRuntimeValue(value);
  }
  if (value is RuntimeGraph) {
    return canonicalJsonEncode(
        stableSortKeys(Map<String, dynamic>.from(value.toJson())));
  }
  if (value is Map) {
    return canonicalJsonEncode(
        stableSortKeys(Map<String, dynamic>.from(value)));
  }
  if (value is List) {
    final asMap = <String, dynamic>{};
    for (var i = 0; i < value.length; i++) {
      final item = value[i];
      if (item is Map) {
        asMap['$i'] = stableSortKeys(Map<String, dynamic>.from(item));
      } else {
        asMap['$i'] = canonicalizeNumber(item);
      }
    }
    // No outer stableSortKeys here: volatile-key stripping applies only to
    // dict items directly inside the list (Python/JS keyed-object semantics);
    // the encoder sorts keys itself.
    return canonicalJsonEncode(asMap);
  }
  return canonicalJsonEncode(value);
}
