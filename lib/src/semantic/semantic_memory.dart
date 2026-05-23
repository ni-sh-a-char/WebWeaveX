import '../crypto/kaalka_runtime.dart';

class SemanticMemory {
  SemanticMemory({this.maxEntries = 256});
  final int maxEntries;
  final _store = <String, dynamic>{};

  void put(String key, dynamic value) {
    if (_store.length >= maxEntries) _store.remove(_store.keys.first);
    _store[key] = value;
  }

  dynamic get(String key) => _store[key];
}

Map<String, dynamic> buildSemanticMemory([Map<String, dynamic>? semantic]) {
  return {
    'semantic_id': computeDeterministicHash(semantic ?? {}),
    'bounded': true,
  };
}
