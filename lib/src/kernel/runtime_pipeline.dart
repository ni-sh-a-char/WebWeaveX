import '../browser/extract_web.dart';
import '../crypto/kaalka_runtime.dart';
import '../determinism/fingerprint.dart';
import '../graph/runtime_graph.dart';

String _detectKind(Map<String, dynamic> input) {
  final explicit = input['sourceType'] as String?;
  if (explicit != null && explicit != 'auto') return explicit;
  final src = (input['url'] ?? input['path'] ?? input['source']) as String;
  if (src.startsWith('http://') || src.startsWith('https://')) return 'web';
  if (RegExp(r'\.(pdf|docx|md|html|txt)$', caseSensitive: false)
      .hasMatch(src)) {
    return 'document';
  }
  return 'text';
}

Future<Map<String, dynamic>> runCanonicalPipeline(
  Map<String, dynamic> input, {
  bool authenticated = false,
  String? sessionPath,
  String? encryptionKey,
  bool semanticRuntime = false,
}) async {
  final kind = _detectKind(input);
  final target = (input['url'] ?? input['path'] ?? input['source']) as String;

  late Map<String, dynamic> extraction;
  if (kind == 'web') {
    extraction = await extractWeb(
      target,
      authenticated: authenticated,
      sessionPath: sessionPath,
      encryptionKey: encryptionKey,
      semanticRuntime: semanticRuntime,
    );
  } else {
    final graph = buildRuntimeGraph({
      'text': {'source': target}
    });
    extraction = {
      'bounded': true,
      'unified_runtime_graph': graph.toJson(),
      'graph': graph.toJson(),
      'runtime': {'available': false, 'kind': kind},
      'pipeline_hash':
          computeDeterministicHash({'target': target, 'kind': kind}),
    };
    extraction['global_runtime_fingerprint'] =
        computeGlobalRuntimeFingerprint(extraction, graph);
  }

  return {
    ...extraction,
    'ingestion': {'kind': kind, 'target': target, 'bounded': true},
  };
}
