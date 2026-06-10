import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  test('replay equivalence for identical envelopes', () {
    final graph = buildRuntimeGraph({'a': 1});
    final envelope = {
      'bounded': true,
      'pipeline_hash': 'abc',
      'unified_runtime_graph': graph.toJson(),
      'graph': graph.toJson(),
      'browser_ir': {'runtime_identity': 'id1'},
      'global_runtime_fingerprint': computeRuntimePipelineFingerprint(
        {'bounded': true, 'pipeline_hash': 'abc'},
        graph,
      ),
    };
    final result = validateReplayEquivalenceExtended(
        envelope, Map<String, dynamic>.from(envelope));
    expect(result['equivalent'], isTrue);
  });
}
