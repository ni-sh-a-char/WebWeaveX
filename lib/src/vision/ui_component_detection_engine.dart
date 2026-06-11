/// Port of core/vision/ui_component_detection_engine.py: detect_ui_components.
library;

const Set<String> buttonKeywords = <String>{
  'submit',
  'login',
  'sign in',
  'continue',
};

/// Port of core/vision/ui_component_detection_engine.detect_ui_components.
Map<String, dynamic> detectUiComponents(
  Map<String, dynamic> blocks,
) {
  final List<Map<String, dynamic>> components = <Map<String, dynamic>>[];

  final List<dynamic> blockList = blocks.containsKey('blocks')
      ? blocks['blocks'] as List<dynamic>
      : <dynamic>[];

  for (final dynamic blockRaw in blockList) {
    final Map<String, dynamic> block = blockRaw as Map<String, dynamic>;
    final String text =
        ((block.containsKey('text') ? block['text'] : '') as String)
            .toLowerCase();

    if (buttonKeywords.contains(text)) {
      components.add(<String, dynamic>{
        'type': 'button',
        'text': text,
        'bbox': block['bbox'],
      });
    }
  }

  return <String, dynamic>{
    'components': components,
    'bounded': true,
  };
}
