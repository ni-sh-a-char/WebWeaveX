/// Port of core/multimodal/universal_multimodal_extraction_engine.py:
/// extract_multimodal.
library;

import 'package:webweavex/src/ir/multimodal_ir.dart';
import 'package:webweavex/src/layout/layout_detection_engine.dart';
import 'package:webweavex/src/ocr/ocr_engine.dart';
import 'package:webweavex/src/tables/table_extraction_engine.dart';
import 'package:webweavex/src/vision/chart_detection_engine.dart';
import 'package:webweavex/src/vision/form_extraction_engine.dart';
import 'package:webweavex/src/vision/ui_component_detection_engine.dart';

/// Port of universal_multimodal_extraction_engine.extract_multimodal.
Map<String, dynamic> extractMultimodal(
  String path,
) {
  final Map<String, dynamic> ocr = extractOcr(path);

  final List<dynamic> regionsRaw = ocr.containsKey('regions')
      ? ocr['regions'] as List<dynamic>
      : <dynamic>[];
  final List<Map<String, dynamic>> regions = <Map<String, dynamic>>[
    for (final dynamic region in regionsRaw) region as Map<String, dynamic>,
  ];

  final Map<String, dynamic> layout = detectLayoutBlocks(regions);

  final Map<String, dynamic> tables = extractTables(layout);

  final Map<String, dynamic> forms = extractForms(layout);

  final Map<String, dynamic> charts = detectCharts(layout);

  final Map<String, dynamic> ui = detectUiComponents(layout);

  final Map<String, dynamic> multimodalIr = compileMultimodalIr(
    layout: layout,
    tables: tables,
    forms: forms,
    charts: charts,
    ui: ui,
  );

  return <String, dynamic>{
    'ocr': ocr,
    'layout': layout,
    'tables': tables,
    'forms': forms,
    'charts': charts,
    'ui': ui,
    'multimodal_ir': multimodalIr,
    'bounded': true,
  };
}
