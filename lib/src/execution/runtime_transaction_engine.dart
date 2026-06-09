import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Port of core/execution/runtime_transaction_engine.
Map<String, dynamic> beginRuntimeTransaction({
  int tick = 0,
  String checkpointId = '',
}) {
  // Python json.dumps({"tick":tick,"checkpoint":checkpoint_id}, sort_keys=True)
  // default separators (", ", ": "). Keys sorted: checkpoint, tick.
  final String payload =
      '{"checkpoint": ${jsonEncode(checkpointId)}, "tick": $tick}';
  final String transactionId =
      sha256.convert(utf8.encode(payload)).toString().substring(0, 32);

  return <String, dynamic>{
    'transaction_id': transactionId,
    'actions': <dynamic>[],
    'mutations': <dynamic>[],
    'transitions': <dynamic>[],
    'checkpoints':
        checkpointId.isNotEmpty ? <String>[checkpointId] : <String>[],
    'committed': false,
    'rolled_back': false,
    'bounded': true,
  };
}

Map<String, dynamic> commitRuntimeTransaction(
    Map<String, dynamic> transaction) {
  final Map<String, dynamic> updated = <String, dynamic>{...transaction};
  updated['committed'] = true;
  updated['rolled_back'] = false;
  return updated;
}

Map<String, dynamic> rollbackRuntimeTransaction(
    Map<String, dynamic> transaction) {
  final Map<String, dynamic> updated = <String, dynamic>{...transaction};
  updated['committed'] = false;
  updated['rolled_back'] = true;
  updated['actions'] = <dynamic>[];
  updated['mutations'] = <dynamic>[];
  return updated;
}
