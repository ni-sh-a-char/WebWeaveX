/// Deterministic interaction replay, ported from the canonical Python
/// `core.interaction.interaction_replay_engine.replay_interactions`
/// (+ `record_interaction`).
///
/// Parity scope: the RETURNED structure is a full-fidelity, pure function of
/// `interactionLog` — byte-for-byte equivalent to Python (proven by
/// deep-equality vectors). The live-page action dispatch in Python
/// (`_ACTION_DISPATCH[handler](page, action)`) drives a real browser and has
/// no effect on the returned value; that side-effecting dispatch is the
/// documented bounded/deferred edge, so this is classified Partial.
library;

const int _maxReplayActions = 1000;

/// Port of `record_interaction(action, selector, metadata=None, step=0)`.
Map<String, dynamic> recordInteraction(
  String action,
  String selector, {
  Map<String, dynamic>? metadata,
  int step = 0,
}) {
  return <String, dynamic>{
    'id': 'interaction_$step',
    'timestamp': step,
    'action': action.trim(),
    'selector': selector.trim(),
    'metadata': metadata == null
        ? <String, dynamic>{}
        : Map<String, dynamic>.from(metadata),
    'bounded': true,
  };
}

/// Port of `replay_interactions(page, interaction_log)`.
///
/// `page` is accepted for signature parity but intentionally unused: the live
/// browser dispatch is the bounded/deferred edge. The returned map is a pure
/// deterministic function of [interactionLog].
Map<String, dynamic> replayInteractions(
  List<Map<String, dynamic>> interactionLog, {
  Object? page,
}) {
  final replayLog = <Map<String, dynamic>>[];
  final limit = interactionLog.length > _maxReplayActions
      ? _maxReplayActions
      : interactionLog.length;
  for (var index = 0; index < limit; index++) {
    final action = interactionLog[index];
    final actionType =
        (action['action'] ?? action['type'] ?? '').toString().trim();
    final selector = (action['selector'] ?? '').toString();
    final md = action['metadata'];
    final metadata =
        md is Map ? Map<String, dynamic>.from(md) : <String, dynamic>{};
    replayLog.add(<String, dynamic>{
      'step': index,
      'action': recordInteraction(
        actionType,
        selector,
        metadata: metadata,
        step: index,
      ),
      'replayed': true,
    });
  }
  return <String, dynamic>{
    'replay': replayLog,
    'bounded': true,
  };
}
