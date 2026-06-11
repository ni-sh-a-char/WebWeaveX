/// Port of core/ir/multimodal_ir.py: compile_multimodal_ir.
library;

/// Port of core/ir/multimodal_ir.compile_multimodal_ir.
Map<String, dynamic> compileMultimodalIr({
  required Map<String, dynamic> layout,
  required Map<String, dynamic> tables,
  required Map<String, dynamic> forms,
  required Map<String, dynamic> charts,
  required Map<String, dynamic> ui,
}) {
  final dynamic blocks = layout.containsKey('blocks')
      ? layout['blocks']
      : <Map<String, dynamic>>[];
  return <String, dynamic>{
    'ir': 'multimodal',
    'semantic_blocks': blocks,
    'layout_tree': layout,
    'tables': tables,
    'charts': charts,
    'forms': forms,
    'navigation': <dynamic>[],
    'ui_components': ui,
    'layout': layout,
    'bounded': true,
  };
}
