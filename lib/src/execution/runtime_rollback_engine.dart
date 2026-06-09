/// Port of core/execution/runtime_rollback_engine.
Map<String, dynamic> _subMap(Map<String, dynamic> src, String key) {
  final dynamic v = src[key];
  if (v is Map) return <String, dynamic>{...v.cast<String, dynamic>()};
  return <String, dynamic>{};
}

Map<String, dynamic> restoreRuntimeCheckpoint(Map<String, dynamic> checkpoint) {
  return <String, dynamic>{
    'browser': _subMap(checkpoint, 'browser'),
    'interaction': _subMap(checkpoint, 'interaction'),
    'native': _subMap(checkpoint, 'native'),
    'workflow': _subMap(checkpoint, 'workflow'),
    'synchronization': _subMap(checkpoint, 'synchronization'),
    'memory': _subMap(checkpoint, 'memory'),
    'restored': true,
    'bounded': true,
  };
}

Map<String, dynamic> rollbackRuntimeState(
  Map<String, dynamic> prior, [
  Map<String, dynamic>? current,
]) {
  final Map<String, dynamic> restored = restoreRuntimeCheckpoint(prior);
  return <String, dynamic>{
    'prior': prior,
    'current': current ?? <String, dynamic>{},
    'restored_state': restored,
    'rolled_back': true,
    'replay_safe': true,
    'bounded': true,
  };
}
