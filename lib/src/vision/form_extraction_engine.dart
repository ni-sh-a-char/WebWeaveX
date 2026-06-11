/// Port of core/vision/form_extraction_engine.py: extract_forms.
library;

const Set<String> inputKeywords = <String>{
  'email',
  'password',
  'username',
  'search',
};

/// Port of core/vision/form_extraction_engine.extract_forms.
Map<String, dynamic> extractForms(
  Map<String, dynamic> blocks,
) {
  final List<Map<String, dynamic>> forms = <Map<String, dynamic>>[];

  final List<dynamic> blockList = blocks.containsKey('blocks')
      ? blocks['blocks'] as List<dynamic>
      : <dynamic>[];

  for (final dynamic blockRaw in blockList) {
    final Map<String, dynamic> block = blockRaw as Map<String, dynamic>;
    final String text =
        ((block.containsKey('text') ? block['text'] : '') as String)
            .toLowerCase();

    if (inputKeywords.contains(text)) {
      forms.add(<String, dynamic>{
        'field': text,
        'bbox': block['bbox'],
      });
    }
  }

  return <String, dynamic>{
    'forms': forms,
    'bounded': true,
  };
}
