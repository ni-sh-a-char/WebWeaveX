import '../crypto/kaalka_runtime.dart';
import 'capture_runtime.dart';

Future<Map<String, dynamic>> captureRuntimeSnapshot(
  String url, {
  int tick = 0,
  Map<String, dynamic>? session,
}) async {
  final captured = await captureRuntime(url);
  final snapshotId = computeDeterministicHash({
    'url': captured['url'],
    'dom_hash': captured['dom_hash'],
    'tick': tick,
    'session_id': session?['session_id'] ?? '',
  });
  return {
    ...captured,
    'snapshot_id': snapshotId,
    'captured_at_tick': tick,
    'bounded': true,
  };
}

Map<String, dynamic> compareRuntimeSnapshots(
  Map<String, dynamic> a,
  Map<String, dynamic> b,
) {
  final domMatch = a['dom_hash'] == b['dom_hash'];
  final routeMatch = a['routes'].toString() == b['routes'].toString();
  return {
    'equivalent': domMatch && routeMatch,
    'dom_match': domMatch,
    'route_match': routeMatch,
    'bounded': true,
  };
}
