/// Port of core/vision/chart_detection_engine.py: detect_charts.
library;

const Set<String> chartTerms = <String>{
  'revenue',
  'sales',
  'growth',
  'profit',
};

/// Port of core/vision/chart_detection_engine.detect_charts.
Map<String, dynamic> detectCharts(
  Map<String, dynamic> blocks,
) {
  bool detected = false;

  final List<dynamic> blockList = blocks.containsKey('blocks')
      ? blocks['blocks'] as List<dynamic>
      : <dynamic>[];

  for (final dynamic blockRaw in blockList) {
    final Map<String, dynamic> block = blockRaw as Map<String, dynamic>;
    final String text =
        ((block.containsKey('text') ? block['text'] : '') as String)
            .toLowerCase();

    bool anyTerm = false;
    for (final String term in chartTerms) {
      if (text.contains(term)) {
        anyTerm = true;
        break;
      }
    }

    if (anyTerm) {
      detected = true;
      break;
    }
  }

  return <String, dynamic>{
    'charts': <Map<String, dynamic>>[
      <String, dynamic>{
        'detected': detected,
      },
    ],
    'bounded': true,
  };
}
