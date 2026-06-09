import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/kernel_runtime/kernel_runtime.dart';
import 'package:webweavex/webweavex.dart' show computeDeterministicHash;

Map<String, dynamic> _asMap(dynamic v) =>
    Map<String, dynamic>.from(v as Map<dynamic, dynamic>);

List<Map<String, dynamic>> _asMapList(dynamic v) =>
    (v as List<dynamic>).map((e) => _asMap(e)).toList();

UniversalInput _universalInputFrom(Map<String, dynamic> input) =>
    UniversalInput(
      source: (input['source'] as String?) ?? '',
      sourceType: (input['source_type'] as String?) ?? 'auto',
      url: (input['url'] as String?) ?? '',
      path: (input['path'] as String?) ?? '',
      session: input['session'] == null ? null : _asMap(input['session']),
      options: input['options'] == null ? null : _asMap(input['options']),
      tick: (input['tick'] as int?) ?? 0,
    );

Map<String, Map<String, dynamic>> _phaseResultsFrom(dynamic v) {
  if (v == null) return <String, Map<String, dynamic>>{};
  final src = _asMap(v);
  final out = <String, Map<String, dynamic>>{};
  src.forEach((k, value) => out[k] = _asMap(value));
  return out;
}

dynamic _callApi(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'compile_unified_runtime_ir':
      return compileUnifiedRuntimeIr(
        registry: input['registry'] == null ? null : _asMap(input['registry']),
        graph: input['graph'] == null ? null : _asMap(input['graph']),
        bus: input['bus'] == null ? null : _asMapList(input['bus']),
        phaseResults: input['phase_results'] == null
            ? null
            : _asMapList(input['phase_results']),
        sources: input['sources'] == null ? null : _asMap(input['sources']),
      );
    case 'UniversalInput.to_dict':
      return _universalInputFrom(input).toDict();
    case 'schedule_kernel_phases':
      return scheduleKernelPhases(
        (input['phases'] as List<dynamic>).map((e) => '$e').toList(),
        tick: (input['tick'] as int?) ?? 0,
      );
    case 'register_runtime_phase':
      var registry = <String, dynamic>{'phases': <String, dynamic>{}};
      for (final raw in (input['sequence'] as List<dynamic>)) {
        final pair = raw as List<dynamic>;
        registry =
            registerRuntimePhase(registry, pair[0] as String, _asMap(pair[1]));
      }
      return registry;
    case 'list_runtime_phases':
      return listRuntimePhases();
    case 'publish_runtime_event':
      var bus = <Map<String, dynamic>>[];
      for (final raw in (input['sequence'] as List<dynamic>)) {
        final triple = raw as List<dynamic>;
        final published = publishRuntimeEvent(
            bus, triple[0] as String, _asMap(triple[1]),
            tick: triple[2] as int);
        bus = _asMapList(published['bus']);
      }
      return bus;
    case 'build_kernel_topology':
      return buildKernelTopology(_asMap(input['graph']));
    case 'coordinate_kernel_phases':
      return coordinateKernelPhases(_asMapList(input['phase_results']),
          tick: (input['tick'] as int?) ?? 0);
    case 'replay_kernel_state':
      return replayKernelState(_asMapList(input['events']));
    case 'build_kernel_policy':
      return buildKernelPolicy();
    case 'enforce_kernel_policy':
      return enforceKernelPolicy(buildKernelPolicy(),
          input['phase_count'] as int, input['node_count'] as int);
    case 'enforce_runtime_boundary':
      return enforceRuntimeBoundary(input);
    case 'RuntimeKernel.compileIr':
      final kernel =
          RuntimeKernel(runtimeKind: input['runtime_type'] as String);
      return kernel.compileIr(
        phaseResults: _phaseResultsFrom(input['phase_results']),
        tick: (input['tick'] as int?) ?? 0,
      );
    default:
      throw StateError('unknown api $api');
  }
}

void main() {
  final vectorsFile = File('validation/parity/kernel_api_vectors.json');

  group('kernel-runtime family — Python parity', () {
    late List<dynamic> vectors;

    setUpAll(() {
      vectors = jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;
    });

    test('vector file loads', () {
      expect(vectors, isNotEmpty);
    });

    test('hash parity for every vector', () {
      for (final raw in vectors) {
        final v = raw as Map<String, dynamic>;
        final api = v['api'] as String;
        final input = _asMap(v['input']);
        final expected = v['det_hash'] as String;
        final result = _callApi(api, input);
        final actual = computeDeterministicHash(result);
        expect(actual, equals(expected),
            reason:
                'NO-MATCH for $api\n  expected=$expected\n  actual=$actual');
      }
    });
  });

  group('UniversalInput — structural + hash parity', () {
    test('toDict shape: defaults, sorted options, session default, bounded',
        () {
      final ui = UniversalInput(
        source: 'https://x',
        options: <String, dynamic>{'z': 1, 'a': 2, 'm': 3},
      );
      final d = ui.toDict();
      expect(d['source'], equals('https://x'));
      expect(d['source_type'], equals('auto'));
      expect(d['url'], equals(''));
      expect(d['path'], equals(''));
      expect(d['session'], equals(<String, dynamic>{}));
      expect((d['options'] as Map<String, dynamic>).keys.toList(),
          equals(<String>['a', 'm', 'z']));
      expect(d['tick'], equals(0));
      expect(d['bounded'], isTrue);
    });

    test('session passthrough overrides empty default', () {
      final ui =
          UniversalInput(source: 's', session: <String, dynamic>{'token': 't'});
      expect(ui.toDict()['session'], equals(<String, dynamic>{'token': 't'}));
    });

    test('computeDeterministicHash(toDict) stable across instances', () {
      final a = UniversalInput(source: 's', tick: 5).toDict();
      final b = UniversalInput(source: 's', tick: 5).toDict();
      expect(computeDeterministicHash(a), equals(computeDeterministicHash(b)));
    });
  });

  group('branch coverage', () {
    test('detectKind: explicit source_type wins', () {
      expect(detectKind(UniversalInput(source: 'x', sourceType: 'repository')),
          equals('repository'));
    });
    test('detectKind: http(s) → web', () {
      expect(detectKind(UniversalInput(source: 'http://a')), equals('web'));
      expect(detectKind(UniversalInput(source: 'https://a')), equals('web'));
    });
    test('detectKind: document extensions', () {
      for (final ext in <String>['pdf', 'docx', 'md', 'html', 'txt']) {
        expect(
            detectKind(UniversalInput(source: 'f.$ext')), equals('document'));
      }
    });
    test('detectKind: falls back to text; uses url then path', () {
      expect(detectKind(UniversalInput(source: 'plain')), equals('text'));
      expect(detectKind(UniversalInput(source: '', url: 'https://u')),
          equals('web'));
      expect(detectKind(UniversalInput(source: '', path: 'p.md')),
          equals('document'));
    });

    test('getRuntimeKernel returns singleton; new instance on type change', () {
      final a = getRuntimeKernel();
      final b = getRuntimeKernel();
      expect(identical(a, b), isTrue);
      final c = getRuntimeKernel(runtimeType: 'native');
      expect(identical(a, c), isFalse);
      expect(c.runtimeKind, equals('native'));
    });

    test('compileIr empty vs populated phases differ; deterministic', () {
      final kernel = RuntimeKernel(runtimeKind: 'browser');
      final empty = kernel.compileIr();
      final empty2 = kernel.compileIr();
      expect(computeDeterministicHash(empty),
          equals(computeDeterministicHash(empty2)));
      // No phases registered → registry keeps its initial shape (no
      // 'registered' key), matching Python (register_runtime_phase unused).
      expect((empty['registry'] as Map)['phases'], equals(<String, dynamic>{}));

      final populated = kernel.compileIr(
        phaseResults: <String, Map<String, dynamic>>{
          'semantic': <String, dynamic>{'enabled': true, 'bounded': true},
        },
      );
      expect((populated['registry'] as Map)['registered'],
          equals(<String>['semantic']));
      expect(computeDeterministicHash(empty),
          isNot(equals(computeDeterministicHash(populated))));
    });

    test('compileIr harvests IR + still yields canonical empty graph', () {
      final kernel = RuntimeKernel(runtimeKind: 'browser');
      final out = kernel.compileIr(
        phaseResults: <String, Map<String, dynamic>>{
          'memory': <String, dynamic>{
            'bounded': true,
            'memory_ir': <String, dynamic>{'ir': 'runtime_memory'},
          },
        },
      );
      expect((out['graph'] as Map)['ir'], equals('unified_runtime_graph'));
      expect((out['graph'] as Map)['nodes'], equals(<dynamic>[]));
      expect((out['boundary'] as Map)['ir_count'], equals(1));
    });

    test('shutdown reflects initialized tick (0)', () {
      final out = RuntimeKernel(runtimeKind: 'browser').shutdown();
      expect(out['shutdown'], isTrue);
      expect(out['final_tick'], equals(0));
    });

    test('runCanonicalPipeline bounded path: input dict + kind + not proven',
        () {
      final out = runCanonicalPipeline(
          UniversalInput(source: 'https://app.example.com', tick: 2));
      expect(out['kind'], equals('web'));
      expect(out['hash_proven'], isFalse);
      expect((out['input'] as Map)['bounded'], isTrue);
      expect(out['bounded'], isTrue);
    });

    test('mergeKernelState concatenates irs', () {
      final merged = mergeKernelState(
        <String, dynamic>{
          'irs': <dynamic>[
            <String, dynamic>{'a': 1}
          ]
        },
        <String, dynamic>{
          'irs': <dynamic>[
            <String, dynamic>{'b': 2}
          ],
          'graph': <String, dynamic>{'g': 1},
        },
      );
      expect((merged['irs'] as List).length, equals(2));
      expect(merged['graph'], equals(<String, dynamic>{'g': 1}));
    });

    test('initializeRuntime + buildKernelState wiring', () {
      final init = initializeRuntime(runtimeType: 'native', tick: 3);
      expect(init['initialized'], isTrue);
      final state = init['state'] as Map<String, dynamic>;
      expect(state['tick'], equals(3));
      expect((state['context'] as Map)['runtime_type'], equals('native'));
    });
  });
}
