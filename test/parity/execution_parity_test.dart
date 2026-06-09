import 'dart:convert';
import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/src/crypto/hashing.dart';
import 'package:webweavex/src/execution/execution.dart';
import 'package:webweavex/src/execution/runtime_permissions_engine.dart';

/// Reconstructs the Dart result for a given vector `api` + `input` shape,
/// mirroring the exact calls in WebWeaveX/_gen_exec_vectors.py.
dynamic _runVector(String api, Map<String, dynamic> input) {
  switch (api) {
    case 'build_runtime_sandbox':
      return buildRuntimeSandbox(
        runtime: input['runtime'] as String? ?? 'browser',
        allowedActions:
            (input['allowed_actions'] as List<dynamic>?)?.cast<String>(),
        maxActions: input['max_actions'] as int? ?? 1000,
        timeoutTicks: input['timeout_ticks'] as int? ?? 10000,
        replayPolicy: input['replay_policy'] as String? ?? 'strict',
        rollbackEnabled: input['rollback_enabled'] as bool? ?? true,
      );

    case 'execute_runtime_action':
      final Map<String, dynamic> sandbox =
          buildRuntimeSandbox(runtime: input['sandbox'] as String);
      Map<String, dynamic>? perms;
      if (input.containsKey('permissions')) {
        perms = buildRuntimePermissions(
            scopes: (input['permissions'] as List<dynamic>).cast<String>());
      }
      return executeRuntimeAction(
        (input['raw_action'] as Map).cast<String, dynamic>(),
        sandbox: sandbox,
        permissions: perms,
        tick: input['tick'] as int? ?? 0,
      );

    case 'simulate_runtime_execution':
      final Map<String, dynamic>? sandbox = input.containsKey('sandbox')
          ? buildRuntimeSandbox(runtime: input['sandbox'] as String)
          : null;
      return simulateRuntimeExecution(
        (input['actions'] as List<dynamic>).cast<Map<String, dynamic>>(),
        sandbox: sandbox,
        tick: input['tick'] as int? ?? 0,
      );

    case 'replay_runtime_execution':
      return replayRuntimeExecution(
        (input['actions'] as List<dynamic>).cast<Map<String, dynamic>>(),
        transactions: (input['transactions'] as List<dynamic>?)
            ?.cast<Map<String, dynamic>>(),
        mutations: (input['mutations'] as List<dynamic>?)
            ?.cast<Map<String, dynamic>>(),
        tick: input['tick'] as int? ?? 0,
      );

    case 'run_execution_runtime':
      return runExecutionRuntime(
        sources: (input['sources'] as Map?)?.cast<String, dynamic>(),
        runtime: input['runtime'] as String? ?? 'browser',
        tick: input['tick'] as int? ?? 0,
        simulate: input['simulate'] as bool? ?? false,
        rollbackEnabled: input['rollback_enabled'] as bool? ?? true,
      );

    case 'run_execution_for_extraction':
      return runExecutionForExtraction(
        executionRuntime: input['execution_runtime'] as bool? ?? true,
        sources: (input['sources'] as Map?)?.cast<String, dynamic>(),
        runtime: input['runtime'] as String? ?? 'browser',
        tick: input['tick'] as int? ?? 0,
        simulateExecution: input['simulate_execution'] as bool? ?? false,
        mergeGraph: input['merge_graph'] as bool? ?? true,
      );

    default:
      throw StateError('unknown api: $api');
  }
}

void main() {
  final File vectorsFile = File('validation/parity/execution_api_vectors.json');
  final List<dynamic> vectors =
      jsonDecode(vectorsFile.readAsStringSync()) as List<dynamic>;

  group('execution family cross-language parity', () {
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

  group('branch coverage smoke', () {
    test('sandbox runtimes produce distinct allowed_actions', () {
      expect(buildRuntimeSandbox(runtime: 'terminal')['allowed_actions'],
          equals(<String>['terminal_command']));
      expect(buildRuntimeSandbox(runtime: 'vm')['allowed_actions'],
          equals(<String>['vm_execute']));
    });

    test('executed browser click yields action payload', () {
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'browser');
      final Map<String, dynamic> r = executeRuntimeAction(
        <String, dynamic>{'type': 'browser_click', 'selector': '#ok'},
        sandbox: sb,
      );
      expect(r['executed'], isTrue);
      expect((r['action'] as Map)['action_type'], equals('browser_click'));
    });

    test('disabled extraction short-circuits', () {
      final Map<String, dynamic> r =
          runExecutionForExtraction(executionRuntime: false);
      expect(r['enabled'], isFalse);
    });
  });
}
