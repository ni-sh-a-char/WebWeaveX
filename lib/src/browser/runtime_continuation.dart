import '../crypto/kaalka_runtime.dart';
import '../determinism/fingerprint.dart';
import '../graph/runtime_graph.dart';
import 'browser_identity.dart';
import 'capture_runtime.dart';
import 'render_page.dart';
import 'runtime_session.dart';
import 'spa_stabilizer.dart';

/// HTTP-bounded authenticated continuation (Playwright not available in Dart package).
Future<Map<String, dynamic>> continueAuthenticatedRuntime(
  String url, {
  required String sessionPath,
  required String encryptionKey,
  int tick = 0,
}) async {
  final session = restoreRuntimeSession(sessionPath, encryptionKey);
  return extractWithSession(url, session, tick: tick);
}

Future<Map<String, dynamic>> extractWithSession(
  String url,
  Map<String, dynamic> session, {
  int tick = 0,
}) async {
  final rendered = await renderPage(url);
  final html = rendered['html'] as String? ?? '';
  final spa = stabilizeSpaDom(html, route: url);
  final captured = await captureRuntime(url);
  final identity = buildBrowserIdentityFromCapture(captured);
  final graph = buildRuntimeGraph({
    'browser': {'url': url, 'identity': identity['runtime_identity']},
    'session': {'session_id': session['session_id'], 'continued': true},
  });
  final envelope = <String, dynamic>{
    'bounded': true,
    'runtime': {
      'available': rendered['available'] ?? false,
      'dom_stabilization': {'stabilized_hash': captured['dom_hash']},
      'spa_stabilization': spa,
      'session': {'session_id': session['session_id'], 'continuation': true},
    },
    'browser_ir': {
      'runtime_identity': identity['runtime_identity'],
      'storage': captured['storage'],
    },
    'unified_runtime_graph': graph.toJson(),
    'pipeline_hash': computeDeterministicHash(
        {'url': url, 'kind': 'continuation', 'tick': tick}),
  };
  envelope['global_runtime_fingerprint'] =
      computeRuntimePipelineFingerprint(envelope, graph);
  return envelope;
}
