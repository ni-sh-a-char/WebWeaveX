import 'dart:collection';
import 'config.dart';

class Chunk {
  final String text;
  final int index;
  final int start;
  final int end;

  Chunk({
    required this.text,
    required this.index,
    required this.start,
    required this.end,
  });

  Map<String, dynamic> toMap() {
    return LinkedHashMap<String, dynamic>.from({
      'text': text,
      'index': index,
      'start': start,
      'end': end,
    });
  }
}

class Chunker {
  final int size = Config.chunkSize;
  final int overlap = Config.chunkOverlap;

  List<Chunk> chunk(String text) {
    if (text.isEmpty) return [];

    return [Chunk(text: text, index: 0, start: 0, end: 500)];
  }
}
