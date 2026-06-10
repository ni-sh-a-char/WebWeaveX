import '../crypto/kaalka_runtime.dart';
import '../determinism/dom_stabilization.dart';
import '../determinism/fingerprint.dart';
import '../graph/runtime_graph.dart';
import 'authenticated_runtime.dart';
import 'capture_runtime.dart';

Future<Map<String, dynamic>> extractWeb(
  String url, {
  bool authenticated = false,
  String? sessionPath,
  String? encryptionKey,
  bool semanticRuntime = false,
}) async {
  final captured = await captureRuntime(url);
  var sessionMeta = <String, dynamic>{};
  if (authenticated && sessionPath != null && encryptionKey != null) {
    final session = loadAuthenticatedRuntime(sessionPath, encryptionKey);
    sessionMeta = {
      'session_loaded': true,
      'cookie_count': (session['cookies'] as List?)?.length ?? 0,
    };
  }

  final graph = buildRuntimeGraph({
    'browser': {'url': captured['url'], 'dom_hash': captured['dom_hash']},
    'network': (captured['network'] as List).take(50).toList(),
  });

  final envelope = <String, dynamic>{
    'bounded': true,
    'runtime': {
      'available': captured['available'],
      'dom_stabilization': {'stabilized_hash': captured['dom_hash']},
      'spa_stabilization': {
        'stable_dom_hash': computeStableDomHash(url),
      },
      'session': sessionMeta,
    },
    'browser_ir': {
      'runtime_identity': computeDeterministicHash({
        'url': captured['url'],
        'routes': captured['routes'],
      }),
      'storage': captured['storage'],
    },
    'unified_runtime_graph': graph.toJson(),
    'graph': graph.toJson(),
    'pipeline_hash': computeDeterministicHash({'url': url, 'kind': 'web'}),
  };

  envelope['global_runtime_fingerprint'] =
      computeRuntimePipelineFingerprint(envelope, graph);
  if (semanticRuntime) {
    envelope['semantic'] = {'entities': <dynamic>[], 'bounded': true};
  }
  return envelope;
}
