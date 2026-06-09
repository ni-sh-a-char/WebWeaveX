import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/connectors_runtime/connectors_runtime.dart';

List<Map<String, dynamic>> _maps(dynamic v) =>
    (v as List<dynamic>? ?? <dynamic>[])
        .map<Map<String, dynamic>>(
            (dynamic e) => (e as Map).cast<String, dynamic>())
        .toList();

/// Reconstructs the Dart result for a given vector `api` + `input`, mirroring
/// the exact calls in the Python vector generator.
dynamic _runVector(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'extract_api_runtime':
      return extractApiRuntime(
        apiType: input['api_type'] as String? ?? 'rest',
        snapshot: (input['snapshot'] as Map?)?.cast<String, dynamic>(),
      );

    case 'extract_runtime_streams':
      return extractRuntimeStreams(
        streamTypes: (input['stream_types'] as List<dynamic>?)?.cast<String>(),
        snapshot: (input['snapshot'] as Map?)?.cast<String, dynamic>(),
      );

    case 'extract_telemetry_runtime':
      return extractTelemetryRuntime(
        backends: (input['backends'] as List<dynamic>?)?.cast<String>(),
        snapshot: (input['snapshot'] as Map?)?.cast<String, dynamic>(),
      );

    case 'replay_stream_events':
      return replayStreamEvents(null, _maps(input['stream_log']));

    case 'build_stream_timeline':
      return buildStreamTimeline(_maps(input['events']));

    case 'build_interaction_graph':
      return buildInteractionGraph(_maps(input['interactions']));

    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  final File vectorsFile =
      File('validation/parity/connectors_runtime_api_vectors.json');
  final List<dynamic> vectors =
      jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;

  group('connectors/streaming/interaction runtime cross-language parity', () {
    for (final dynamic vDyn in vectors) {
      final Map<String, dynamic> v = (vDyn as Map).cast<String, dynamic>();
      final String api = v['api'] as String;
      final String expected = v['det_hash'] as String;
      final Map<String, dynamic> input =
          (v['input'] as Map).cast<String, dynamic>();

      test('$api :: ${jsonEncode(input)}', () {
        final dynamic result = _runVector(api, input);
        final String dartHash = computeDeterministicHash(result);
        expect(dartHash, equals(expected),
            reason: 'Dart hash must equal Python det_hash for $api');
      });
    }
  });

  group('branch coverage', () {
    test('api_type rest has no graphql/grpc keys', () {
      final Map<String, dynamic> r = extractApiRuntime();
      expect(r['api_type'], equals('rest'));
      expect(r.containsKey('graphql'), isFalse);
      expect(r.containsKey('grpc'), isFalse);
    });

    test('api_type graphql attaches graphql sub-runtime with sorted types', () {
      final Map<String, dynamic> r =
          extractApiRuntime(apiType: 'GraphQL', snapshot: <String, dynamic>{
        'graphql': <String, dynamic>{
          'types': <String>['Z', 'A']
        }
      });
      final Map<String, dynamic> g = r['graphql'] as Map<String, dynamic>;
      expect(g['protocol'], equals('graphql'));
      expect(g['types'], equals(<String>['A', 'Z']));
      expect(g['endpoints'], equals(<String>['/graphql']));
    });

    test('api_type grpc attaches grpc sub-runtime', () {
      final Map<String, dynamic> r =
          extractApiRuntime(apiType: 'grpc', snapshot: <String, dynamic>{
        'grpc': <String, dynamic>{
          'services': <String>['s2', 's1'],
          'methods': <String>['m2', 'm1'],
        }
      });
      final Map<String, dynamic> g = r['grpc'] as Map<String, dynamic>;
      expect(g['services'], equals(<String>['s1', 's2']));
      expect(g['methods'], equals(<String>['m1', 'm2']));
    });

    test('endpoints sorted by string', () {
      final Map<String, dynamic> r =
          extractApiRuntime(snapshot: <String, dynamic>{
        'endpoints': <String>['/z', '/a', '/m']
      });
      expect(r['endpoints'], equals(<String>['/a', '/m', '/z']));
    });

    test('default stream types kafka/redis/websocket sorted', () {
      final Map<String, dynamic> r = extractRuntimeStreams();
      final List<dynamic> streams = r['streams'] as List<dynamic>;
      expect(r['count'], equals(3));
      expect((streams[0] as Map)['stream_type'], equals('kafka'));
      expect((streams[1] as Map)['stream_type'], equals('redis_streams'));
      expect((streams[2] as Map)['stream_type'], equals('websocket'));
    });

    test('redis branch maps streams to topics', () {
      final Map<String, dynamic> r =
          extractRuntimeStreams(streamTypes: <String>[
        'redis'
      ], snapshot: <String, dynamic>{
        'redis': <String, dynamic>{
          'streams': <String>['x']
        }
      });
      final Map<String, dynamic> s =
          (r['streams'] as List<dynamic>).first as Map<String, dynamic>;
      expect(s['stream_type'], equals('redis_streams'));
      expect(s['topics'], equals(<String>['x']));
    });

    test('websocket branch maps connections to topics', () {
      final Map<String, dynamic> r =
          extractRuntimeStreams(streamTypes: <String>[
        'websocket'
      ], snapshot: <String, dynamic>{
        'websocket': <String, dynamic>{
          'connections': <String>['ws://a']
        }
      });
      final Map<String, dynamic> s =
          (r['streams'] as List<dynamic>).first as Map<String, dynamic>;
      expect(s['stream_type'], equals('websocket'));
      expect(s['topics'], equals(<String>['ws://a']));
    });

    test('sse/queue branch reads topics section', () {
      final Map<String, dynamic> r =
          extractRuntimeStreams(streamTypes: <String>[
        'sse'
      ], snapshot: <String, dynamic>{
        'sse': <String, dynamic>{
          'topics': <String>['e1']
        }
      });
      final Map<String, dynamic> s =
          (r['streams'] as List<dynamic>).first as Map<String, dynamic>;
      expect(s['stream_type'], equals('sse'));
      expect(s['topics'], equals(<String>['e1']));
    });

    test('unknown stream type is skipped (no entry)', () {
      final Map<String, dynamic> r =
          extractRuntimeStreams(streamTypes: <String>['unknown']);
      expect(r['count'], equals(0));
    });

    test('telemetry default backends sorted', () {
      final Map<String, dynamic> r = extractTelemetryRuntime();
      expect(r['backends'],
          equals(<String>['jaeger', 'opentelemetry', 'prometheus']));
      expect(r['degraded'], isFalse);
    });

    test('telemetry caps spans and logs at 10000', () {
      final List<Map<String, dynamic>> big =
          List<Map<String, dynamic>>.generate(
              10005, (int i) => <String, dynamic>{'i': i});
      final Map<String, dynamic> r = extractTelemetryRuntime(
          snapshot: <String, dynamic>{'spans': big, 'logs': big});
      expect((r['spans'] as List).length, equals(10000));
      expect((r['logs'] as List).length, equals(10000));
    });

    test('replay produces stepped events', () {
      final Map<String, dynamic> r =
          replayStreamEvents(null, <Map<String, dynamic>>[
        <String, dynamic>{'id': 'a'},
        <String, dynamic>{'id': 'b'}
      ]);
      final List<dynamic> replay = r['replay'] as List<dynamic>;
      expect(replay.length, equals(2));
      expect((replay[0] as Map)['step'], equals(0));
      expect((replay[1] as Map)['replayed'], isTrue);
    });

    test('timeline orders by (timestamp,id,source) and links edges', () {
      final Map<String, dynamic> r = buildStreamTimeline(<Map<String, dynamic>>[
        <String, dynamic>{'id': 'b', 'timestamp': 2},
        <String, dynamic>{'id': 'a', 'timestamp': 1},
      ]);
      final List<dynamic> events = r['events'] as List<dynamic>;
      expect((events[0] as Map)['id'], equals('a'));
      expect((events[1] as Map)['id'], equals('b'));
      final List<dynamic> edges = r['edges'] as List<dynamic>;
      expect(edges.length, equals(1));
      expect((edges[0] as Map)['relation'], equals('stream_next'));
    });

    test('interaction graph classifies node types and relations', () {
      final Map<String, dynamic> g =
          buildInteractionGraph(<Map<String, dynamic>>[
        <String, dynamic>{'action': 'click', 'selector': '#x'},
        <String, dynamic>{'action': 'fill', 'selector': '#f'},
        <String, dynamic>{'action': 'select', 'selector': '.tab1'},
        <String, dynamic>{'action': 'wait', 'selector': '.modal'},
        <String, dynamic>{'action': 'hover', 'selector': '#h'},
      ]);
      final List<dynamic> nodes = g['nodes'] as List<dynamic>;
      // node[0] is the synthetic root
      expect((nodes[0] as Map)['type'], equals('state'));
      expect((nodes[1] as Map)['type'], equals('page')); // click
      expect((nodes[2] as Map)['type'], equals('form')); // fill
      expect((nodes[3] as Map)['type'], equals('tab')); // select on .tab1
      expect((nodes[4] as Map)['type'], equals('modal')); // wait on .modal
      final List<dynamic> edges = g['edges'] as List<dynamic>;
      expect((edges[0] as Map)['relation'], equals('click'));
      expect((edges[1] as Map)['relation'], equals('submission'));
      expect((edges[2] as Map)['relation'], equals('submission'));
      expect((edges[3] as Map)['relation'], equals('navigation'));
      expect((edges[4] as Map)['relation'], equals('hover'));
      expect(g['graph_hash'], isA<String>());
    });

    test('empty interaction graph has only root node', () {
      final Map<String, dynamic> g =
          buildInteractionGraph(<Map<String, dynamic>>[]);
      expect((g['nodes'] as List).length, equals(1));
      expect((g['edges'] as List).length, equals(0));
    });
  });
}
