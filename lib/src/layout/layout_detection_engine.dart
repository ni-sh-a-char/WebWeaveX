/// Port of core/layout/layout_detection_engine.py: detect_layout_blocks.
library;

const int maxBlocks = 10000;

/// Port of core/layout/layout_detection_engine.detect_layout_blocks.
Map<String, dynamic> detectLayoutBlocks(
  List<Map<String, dynamic>> ocrRegions,
) {
  final List<Map<String, dynamic>> blocks = <Map<String, dynamic>>[];

  final int limit =
      ocrRegions.length > maxBlocks ? maxBlocks : ocrRegions.length;

  for (int idx = 0; idx < limit; idx++) {
    final Map<String, dynamic> region = ocrRegions[idx];
    blocks.add(<String, dynamic>{
      'id': 'block_$idx',
      'bbox': region['bbox'],
      'text': region.containsKey('text') ? region['text'] : '',
      'type': 'text_block',
    });
  }

  return <String, dynamic>{
    'blocks': blocks,
    'bounded': true,
  };
}
