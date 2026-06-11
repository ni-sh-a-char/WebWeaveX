/// Port of core/tables/table_extraction_engine.py: extract_tables.
library;

import 'package:webweavex/src/soup/soup.dart' show pyStrip;

const int maxRows = 1000;

/// Port of core/tables/table_extraction_engine.extract_tables.
Map<String, dynamic> extractTables(
  Map<String, dynamic> layoutBlocks,
) {
  final List<Map<String, dynamic>> tables = <Map<String, dynamic>>[];

  final List<List<String>> currentRows = <List<String>>[];

  final List<dynamic> blocks = layoutBlocks.containsKey('blocks')
      ? layoutBlocks['blocks'] as List<dynamic>
      : <dynamic>[];

  for (final dynamic blockRaw in blocks) {
    final Map<String, dynamic> block = blockRaw as Map<String, dynamic>;
    final String text =
        (block.containsKey('text') ? block['text'] : '') as String;

    if (text.contains('|')) {
      currentRows.add(<String>[
        for (final String x in text.split('|')) pyStrip(x),
      ]);
    }
  }

  if (currentRows.isNotEmpty) {
    tables.add(<String, dynamic>{
      'rows': currentRows.length > maxRows
          ? currentRows.sublist(0, maxRows)
          : currentRows,
    });
  }

  return <String, dynamic>{
    'tables': tables,
    'bounded': true,
  };
}
