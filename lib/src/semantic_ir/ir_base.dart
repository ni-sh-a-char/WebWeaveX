/// Phase A.2 (core.ir._base leaves) of the Category-A semantic-IR port.
/// Proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
library;

import 'py_compat.dart';

/// Port of core.ir._base.empty_confidence.
Map<String, dynamic> emptyConfidence() => <String, dynamic>{
      'score': 0.0,
      'basis': <dynamic>[],
      'deterministic': true,
    };

/// Port of core.ir._base.empty_lineage.
Map<String, dynamic> emptyLineage([String stage = 'ir']) => <String, dynamic>{
      'stages': <Map<String, dynamic>>[
        <String, dynamic>{'stage': stage}
      ],
      'depth': 1,
    };

/// Port of core.ir._base.merge_evidence (`*parts` varargs taken as a list).
/// Python: `sorted({str(e) for part in parts for e in (part or []) if e})`.
Map<String, dynamic> mergeEvidence(List<dynamic> parts) {
  final seen = <String>{};
  for (final part in parts) {
    final items = pyTruthy(part) ? part as List<dynamic> : const <dynamic>[];
    for (final e in items) {
      if (pyTruthy(e)) seen.add(pyToStr(e));
    }
  }
  final sortedItems = seen.toList()..sort();
  return <String, dynamic>{
    'items': sortedItems,
    'count': sortedItems.length,
  };
}
