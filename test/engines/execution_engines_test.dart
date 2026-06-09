import 'package:test/test.dart';
import 'package:webweavex/src/execution/runtime_rollback_engine.dart';
import 'package:webweavex/src/execution/runtime_recovery_engine.dart';
import 'package:webweavex/src/execution/runtime_queue_engine.dart';
import 'package:webweavex/src/execution/runtime_coordination_engine.dart';
import 'package:webweavex/src/execution/runtime_scheduler_engine.dart';
import 'package:webweavex/src/execution/runtime_transaction_engine.dart';
import 'package:webweavex/src/execution/runtime_mutation_engine.dart';
import 'package:webweavex/src/execution/runtime_action_engine.dart';
import 'package:webweavex/src/execution/runtime_transition_engine.dart';
import 'package:webweavex/src/execution/runtime_replay_engine.dart';
import 'package:webweavex/src/execution/runtime_federation_engine.dart';
import 'package:webweavex/src/execution/runtime_simulation_engine.dart';
import 'package:webweavex/src/execution/runtime_execution_engine.dart';
import 'package:webweavex/src/execution/runtime_worker_engine.dart';
import 'package:webweavex/src/execution/runtime_sandbox_engine.dart';
import 'package:webweavex/src/execution/runtime_permissions_engine.dart';
import 'package:webweavex/src/execution/runtime_policy_engine.dart';
import 'package:webweavex/src/execution/runtime_state_engine.dart';
import 'package:webweavex/src/execution/execution_runtime_ir.dart';
import 'package:webweavex/src/execution/runtime_execution_orchestrator.dart';

void main() {
  group('runtime_rollback_engine', () {
    test('restoreRuntimeCheckpoint with Map sub-values copies them', () {
      final Map<String, dynamic> cp = <String, dynamic>{
        'browser': <String, dynamic>{'tab': 1},
        'interaction': <String, dynamic>{'click': 2},
        'native': <String, dynamic>{'win': 3},
        'workflow': <String, dynamic>{'step': 4},
        'synchronization': <String, dynamic>{'sync': 5},
        'memory': <String, dynamic>{'mem': 6},
      };
      final Map<String, dynamic> out = restoreRuntimeCheckpoint(cp);
      expect(out['restored'], isTrue);
      expect(out['bounded'], isTrue);
      expect((out['browser'] as Map<String, dynamic>)['tab'], 1);
      expect((out['memory'] as Map<String, dynamic>)['mem'], 6);
    });

    test('restoreRuntimeCheckpoint with non-Map / missing keys yields empty',
        () {
      final Map<String, dynamic> cp = <String, dynamic>{
        'browser': 'not-a-map',
        'native': <dynamic>[1, 2, 3],
      };
      final Map<String, dynamic> out = restoreRuntimeCheckpoint(cp);
      expect(out['browser'], <String, dynamic>{});
      expect(out['native'], <String, dynamic>{});
      expect(out['workflow'], <String, dynamic>{});
      expect(out['restored'], isTrue);
    });

    test('rollbackRuntimeState with current provided', () {
      final Map<String, dynamic> prior = <String, dynamic>{
        'browser': <String, dynamic>{'a': 1}
      };
      final Map<String, dynamic> current = <String, dynamic>{'live': true};
      final Map<String, dynamic> out = rollbackRuntimeState(prior, current);
      expect(out['prior'], prior);
      expect(out['current'], current);
      expect(out['rolled_back'], isTrue);
      expect(out['replay_safe'], isTrue);
      expect(
          (out['restored_state'] as Map<String, dynamic>)['restored'], isTrue);
    });

    test('rollbackRuntimeState without current defaults to empty map', () {
      final Map<String, dynamic> out =
          rollbackRuntimeState(<String, dynamic>{});
      expect(out['current'], <String, dynamic>{});
      expect(out['bounded'], isTrue);
    });
  });

  group('runtime_recovery_engine', () {
    test('recoverRuntimeExecution with no args (all defaults)', () {
      final Map<String, dynamic> out = recoverRuntimeExecution();
      expect(out['recovered_actions'], <dynamic>[]);
      expect(out['checkpoint_restored'], isFalse);
      expect(out['workflows_resumed'], 0);
      expect(out['replay_safe'], isTrue);
      expect(out['bounded'], isTrue);
    });

    test('recoverRuntimeExecution with failed actions, checkpoint, workflows',
        () {
      final Map<String, dynamic> out = recoverRuntimeExecution(
        failedActions: <Map<String, dynamic>>[
          <String, dynamic>{'id': 'b'},
          <String, dynamic>{'id': 'a'},
        ],
        checkpoint: <String, dynamic>{'state': <String, dynamic>{}},
        interruptedWorkflows: <dynamic>[
          <String, dynamic>{'wf': 1},
          <String, dynamic>{'wf': 2},
        ],
      );
      expect(out['checkpoint_restored'], isTrue);
      expect(out['workflows_resumed'], 2);
      final List<dynamic> recovered = out['recovered_actions'] as List<dynamic>;
      expect(recovered.length, 2);
      // sorted by id: 'a' first
      expect((recovered[0] as Map<String, dynamic>)['id'], 'a');
      expect((recovered[0] as Map<String, dynamic>)['recovered'], isTrue);
      expect((recovered[0] as Map<String, dynamic>)['replay_index'], 0);
      expect((recovered[1] as Map<String, dynamic>)['replay_index'], 1);
    });

    test('recoverRuntimeExecution action missing id sorts as empty string', () {
      final Map<String, dynamic> out = recoverRuntimeExecution(
        failedActions: <Map<String, dynamic>>[
          <String, dynamic>{'noid': true},
        ],
      );
      expect((out['recovered_actions'] as List<dynamic>).length, 1);
    });
  });

  group('runtime_queue_engine', () {
    test('enqueue sorts by priority then order', () {
      Map<String, dynamic> r = enqueueRuntimeAction(
          <Map<String, dynamic>>[], <String, dynamic>{'name': 'low'},
          priority: 1);
      List<Map<String, dynamic>> q =
          (r['queue'] as List<dynamic>).cast<Map<String, dynamic>>();
      r = enqueueRuntimeAction(q, <String, dynamic>{'name': 'high'},
          priority: 5);
      q = (r['queue'] as List<dynamic>).cast<Map<String, dynamic>>();
      expect(r['size'], 2);
      expect(r['bounded'], isTrue);
      // highest priority first
      expect((q.first['action'] as Map<String, dynamic>)['name'], 'high');
    });

    test('enqueue with string priority via _asInt String branch', () {
      // priority param is int; exercise _asInt String/num via order field not
      // possible directly, so build queue items with mixed priority types.
      final List<Map<String, dynamic>> seed = <Map<String, dynamic>>[
        <String, dynamic>{
          'action': <String, dynamic>{'n': 1},
          'priority': '7',
          'order': '0'
        },
        <String, dynamic>{
          'action': <String, dynamic>{'n': 2},
          'priority': 3.0,
          'order': 1
        },
      ];
      final Map<String, dynamic> r =
          enqueueRuntimeAction(seed, <String, dynamic>{'n': 3}, priority: 0);
      final List<Map<String, dynamic>> q =
          (r['queue'] as List<dynamic>).cast<Map<String, dynamic>>();
      // string '7' -> 7 highest priority, sorts first
      expect((q.first['action'] as Map<String, dynamic>)['n'], 1);
      expect(r['size'], 3);
    });

    test('enqueue _asInt fallback for unparsable string and other type', () {
      final List<Map<String, dynamic>> seed = <Map<String, dynamic>>[
        <String, dynamic>{
          'action': <String, dynamic>{'n': 1},
          'priority': 'notnum',
          'order': true
        },
      ];
      final Map<String, dynamic> r =
          enqueueRuntimeAction(seed, <String, dynamic>{'n': 2}, priority: 0);
      expect(r['size'], 2);
    });

    test('dequeue empty returns null action', () {
      final Map<String, dynamic> r =
          dequeueRuntimeAction(<Map<String, dynamic>>[]);
      expect(r['action'], isNull);
      expect(r['queue'], <Map<String, dynamic>>[]);
      expect(r['bounded'], isTrue);
    });

    test('dequeue populated returns highest-priority head', () {
      final List<Map<String, dynamic>> queue = <Map<String, dynamic>>[
        <String, dynamic>{
          'action': <String, dynamic>{'n': 'a'},
          'priority': 1,
          'order': 0
        },
        <String, dynamic>{
          'action': <String, dynamic>{'n': 'b'},
          'priority': 9,
          'order': 1
        },
      ];
      final Map<String, dynamic> r = dequeueRuntimeAction(queue);
      expect((r['action'] as Map<String, dynamic>)['n'], 'b');
      expect((r['queue'] as List<dynamic>).length, 1);
    });
  });

  group('runtime_coordination_engine', () {
    test('coordinate with empty queue and no federation routes', () {
      final Map<String, dynamic> out = coordinateRuntimeExecution(
        <Map<String, dynamic>>[],
        <String, dynamic>{},
      );
      expect(out['queue_size'], 0);
      expect(out['routes'], <dynamic>[]);
      expect(out['workflow_bound'], isFalse);
      expect(out['sync_bound'], isFalse);
      expect(out['rollback_order'], <dynamic>[]);
      expect(out['coordinated'], isTrue);
    });

    test('coordinate with routes, workflow, sync and priority/order sort', () {
      final Map<String, dynamic> federation = <String, dynamic>{
        'execution_routes': <dynamic>[
          <String, dynamic>{'worker_id': 'w1'},
          <String, dynamic>{'worker_id': 'w2'},
        ],
      };
      final List<Map<String, dynamic>> queue = <Map<String, dynamic>>[
        <String, dynamic>{'priority': '2', 'order': 1},
        <String, dynamic>{'priority': 5, 'order': 0},
        <String, dynamic>{'priority': 5, 'order': 1},
      ];
      final Map<String, dynamic> out = coordinateRuntimeExecution(
        queue,
        federation,
        workflow: <String, dynamic>{'wf': 1},
        syncState: <String, dynamic>{'s': 1},
      );
      expect(out['queue_size'], 3);
      expect(out['workflow_bound'], isTrue);
      expect(out['sync_bound'], isTrue);
      // rollback order is reversed routes
      expect(out['rollback_order'], <dynamic>['w2', 'w1']);
    });

    test('coordinate workflow empty map is not bound', () {
      final Map<String, dynamic> out = coordinateRuntimeExecution(
        <Map<String, dynamic>>[],
        <String, dynamic>{},
        workflow: <String, dynamic>{},
        syncState: <String, dynamic>{},
      );
      expect(out['workflow_bound'], isFalse);
      expect(out['sync_bound'], isFalse);
    });
  });

  group('runtime_scheduler_engine', () {
    test('schedule empty actions', () {
      final Map<String, dynamic> out =
          scheduleRuntimeExecution(<Map<String, dynamic>>[]);
      expect(out['scheduled'], <dynamic>[]);
      expect(out['worker_id'], 'worker:0');
      expect(out['deterministic'], isTrue);
    });

    test('schedule sorts by priority, tick, id with cooldown', () {
      final List<Map<String, dynamic>> actions = <Map<String, dynamic>>[
        <String, dynamic>{'id': 'z'},
        <String, dynamic>{'id': 'a'},
        <String, dynamic>{'id': 'm'},
      ];
      final Map<String, dynamic> out = scheduleRuntimeExecution(
        actions,
        priorities: <String, int>{'a': 5, 'z': 5},
        cooldownTicks: 2,
        tick: 10,
        workerId: 'worker:7',
      );
      final List<dynamic> sched = out['scheduled'] as List<dynamic>;
      expect(sched.length, 3);
      expect(out['worker_id'], 'worker:7');
      expect(out['cooldown_ticks'], 2);
      // priority 5 for a and z; tie broken by tick then id.
      // ticks: z idx0 ->10, a idx1 ->12, m idx2 ->14. a(p5,t12) vs z(p5,t10):
      // z has lower tick so z first.
      final Map<String, dynamic> first = sched.first as Map<String, dynamic>;
      expect((first['action'] as Map<String, dynamic>)['id'], 'z');
      expect(first['priority'], 5);
      expect(first['paced'], isTrue);
    });

    test('schedule id-tie path with equal priority and tick', () {
      final List<Map<String, dynamic>> actions = <Map<String, dynamic>>[
        <String, dynamic>{'id': 'b'},
        <String, dynamic>{'id': 'a'},
      ];
      // cooldown 0 -> all ticks equal -> sort falls to id comparison
      final Map<String, dynamic> out =
          scheduleRuntimeExecution(actions, tick: 0);
      final List<dynamic> sched = out['scheduled'] as List<dynamic>;
      expect(
          ((sched.first as Map<String, dynamic>)['action']
              as Map<String, dynamic>)['id'],
          'a');
    });
  });

  group('runtime_transaction_engine', () {
    test('begin with empty checkpoint id', () {
      final Map<String, dynamic> tx = beginRuntimeTransaction(tick: 3);
      expect((tx['transaction_id'] as String).length, 32);
      expect(tx['checkpoints'], <String>[]);
      expect(tx['committed'], isFalse);
      expect(tx['rolled_back'], isFalse);
    });

    test('begin with checkpoint id populates checkpoints', () {
      final Map<String, dynamic> tx =
          beginRuntimeTransaction(tick: 1, checkpointId: 'cp1');
      expect(tx['checkpoints'], <String>['cp1']);
    });

    test('commit sets committed true', () {
      final Map<String, dynamic> tx = beginRuntimeTransaction();
      final Map<String, dynamic> committed = commitRuntimeTransaction(tx);
      expect(committed['committed'], isTrue);
      expect(committed['rolled_back'], isFalse);
    });

    test('rollback clears actions/mutations and sets flags', () {
      final Map<String, dynamic> tx = <String, dynamic>{
        'committed': true,
        'rolled_back': false,
        'actions': <dynamic>[1, 2],
        'mutations': <dynamic>[3],
      };
      final Map<String, dynamic> rb = rollbackRuntimeTransaction(tx);
      expect(rb['committed'], isFalse);
      expect(rb['rolled_back'], isTrue);
      expect(rb['actions'], <dynamic>[]);
      expect(rb['mutations'], <dynamic>[]);
    });
  });

  group('runtime_mutation_engine', () {
    test('track with no prior and no mutation', () {
      final Map<String, dynamic> out = trackRuntimeMutations();
      expect(out['mutations'], <dynamic>[]);
      expect(out['count'], 0);
      expect(out['deterministic_order'], isTrue);
      final Map<String, dynamic> byKind =
          out['by_kind'] as Map<String, dynamic>;
      expect(byKind['dom'], <dynamic>[]);
    });

    test('track adds mutation and buckets by kind, sorting branches', () {
      final List<Map<String, dynamic>> prior = <Map<String, dynamic>>[
        <String, dynamic>{
          'kind': 'native',
          'target': 't1',
          'tick': 5,
          'ordered_index': 0
        },
        <String, dynamic>{
          'kind': 'dom',
          'target': 't2',
          'tick': 1,
          'ordered_index': 1
        },
        // same tick & index as next -> kind tiebreak
        <String, dynamic>{
          'kind': 'sync',
          'target': 't3',
          'tick': '1',
          'ordered_index': 1
        },
      ];
      final Map<String, dynamic> out = trackRuntimeMutations(
        prior: prior,
        mutation: <String, dynamic>{'kind': 'memory', 'target': 'm', 'tick': 2},
      );
      final List<dynamic> muts = out['mutations'] as List<dynamic>;
      expect(muts.length, 4);
      // tick 1 entries sort first; tie on tick(1)+index(1) -> kind dom < sync
      expect((muts[0] as Map<String, dynamic>)['kind'], 'dom');
      expect((muts[1] as Map<String, dynamic>)['kind'], 'sync');
      final Map<String, dynamic> byKind =
          out['by_kind'] as Map<String, dynamic>;
      expect((byKind['memory'] as List<dynamic>).length, 1);
      expect((byKind['synchronization'] as List<dynamic>).length, 1);
      expect((byKind['native'] as List<dynamic>).length, 1);
      expect(out['count'], 4);
    });

    test('track mutation with missing kind/target defaults', () {
      final Map<String, dynamic> out = trackRuntimeMutations(
        mutation: <String, dynamic>{'tick': 'bad'},
      );
      final List<dynamic> muts = out['mutations'] as List<dynamic>;
      expect((muts[0] as Map<String, dynamic>)['kind'], 'unknown');
      expect((muts[0] as Map<String, dynamic>)['tick'], 0);
    });
  });

  group('runtime_action_engine', () {
    test('build action with null payload', () {
      final Map<String, dynamic> a =
          buildRuntimeAction('browser_click', 'browser', null, tick: 1);
      expect((a['id'] as String).length, 32);
      expect(a['runtime'], 'browser');
      expect(a['action_type'], 'browser_click');
      expect(a['payload'], <String, dynamic>{});
      expect(a['timestamp'], 1);
    });

    test('build action with nested list/map payload (List branch)', () {
      final Map<String, dynamic> a = buildRuntimeAction(
        'custom',
        'native',
        <String, dynamic>{
          'items': <dynamic>[
            1,
            'two',
            <String, dynamic>{'k': 'v'}
          ],
          'flag': true,
        },
        tick: 9,
      );
      expect((a['id'] as String).length, 32);
      expect((a['payload'] as Map<String, dynamic>)['flag'], isTrue);
    });
  });

  group('runtime_transition_engine', () {
    test('enqueue/execute/commit/rollback/simulate happy paths', () {
      expect(applyRuntimeTransition('idle', 'enqueue')['to'], 'queued');
      expect(applyRuntimeTransition('queued', 'execute')['to'], 'executing');
      expect(applyRuntimeTransition('executing', 'commit')['to'], 'committed');
      expect(
          applyRuntimeTransition('executing', 'rollback')['to'], 'rolled_back');
      expect(applyRuntimeTransition('idle', 'simulate')['to'], 'simulating');
    });

    test('fail and recover events', () {
      final Map<String, dynamic> failed =
          applyRuntimeTransition('executing', 'fail');
      expect(failed['to'], 'failed');
      expect(failed['valid'], isTrue);
      final Map<String, dynamic> rec =
          applyRuntimeTransition('failed', 'recover');
      expect(rec['to'], 'recovering');
    });

    test('unknown state falls back to idle; unknown event uses first target',
        () {
      final Map<String, dynamic> out =
          applyRuntimeTransition('bogus_state', 'noop_event');
      expect(out['from'], 'idle');
      // idle targets are [queued, simulating] -> first = queued
      expect(out['to'], 'queued');
      expect(out['valid'], isTrue);
    });

    test('event not valid for current state uses first target', () {
      // committed only allows ->idle; 'execute' not applicable
      final Map<String, dynamic> out =
          applyRuntimeTransition('committed', 'execute');
      expect(out['from'], 'committed');
      expect(out['to'], 'idle');
    });
  });

  group('runtime_replay_engine', () {
    test('replay with empty inputs', () {
      final Map<String, dynamic> out =
          replayRuntimeExecution(<Map<String, dynamic>>[]);
      expect(out['actions'], <dynamic>[]);
      expect(out['transactions'], <dynamic>[]);
      expect(out['mutations'], <dynamic>[]);
      expect(out['replayed'], isTrue);
      expect(out['identical'], isTrue);
    });

    test('replay sorts actions, transactions, mutations (tick tie branch)', () {
      final Map<String, dynamic> out = replayRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'id': 'b'},
          <String, dynamic>{'id': 'a'},
        ],
        transactions: <Map<String, dynamic>>[
          <String, dynamic>{'transaction_id': 'y'},
          <String, dynamic>{'transaction_id': 'x'},
        ],
        mutations: <Map<String, dynamic>>[
          <String, dynamic>{'tick': '2', 'ordered_index': 0},
          <String, dynamic>{'tick': 1, 'ordered_index': 5},
          // tie on tick 1 -> ordered_index decides
          <String, dynamic>{'tick': 1, 'ordered_index': 1},
        ],
        tick: 4,
      );
      expect((out['actions'] as List<dynamic>)[0]['id'], 'a');
      expect((out['transactions'] as List<dynamic>)[0]['transaction_id'], 'x');
      final List<dynamic> muts = out['mutations'] as List<dynamic>;
      expect((muts[0] as Map<String, dynamic>)['ordered_index'], 1);
      expect((muts[1] as Map<String, dynamic>)['ordered_index'], 5);
      expect(out['tick'], 4);
    });
  });

  group('runtime_federation_engine', () {
    test('federate with workers and no actions (empty action pool)', () {
      final Map<String, dynamic> out = federateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'worker_id': 'w1', 'runtime': 'browser'},
        ],
      );
      final List<dynamic> routes = out['execution_routes'] as List<dynamic>;
      expect(routes.length, 1);
      expect((routes[0] as Map<String, dynamic>)['action_id'], 'route:0');
      expect(out['federated'], isTrue);
    });

    test('federate with actions mapped by modulo index', () {
      final Map<String, dynamic> out = federateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'worker_id': 'wa'},
          <String, dynamic>{'worker_id': 'wb'},
        ],
        <Map<String, dynamic>>[
          <String, dynamic>{'id': 'act0'},
        ],
      );
      final List<dynamic> routes = out['execution_routes'] as List<dynamic>;
      expect(routes.length, 2);
      // both workers map to the single action via modulo
      expect((routes[0] as Map<String, dynamic>)['action_id'], 'act0');
      expect((routes[1] as Map<String, dynamic>)['action_id'], 'act0');
    });

    test('federate empty actions list also hits empty pool path', () {
      final Map<String, dynamic> out = federateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'worker_id': 'w'},
        ],
        <Map<String, dynamic>>[],
      );
      expect(
          (((out['execution_routes'] as List<dynamic>)[0])
              as Map<String, dynamic>)['action_id'],
          'route:0');
    });
  });

  group('runtime_simulation_engine', () {
    test('simulate empty actions', () {
      final Map<String, dynamic> out =
          simulateRuntimeExecution(<Map<String, dynamic>>[]);
      expect(out['simulated'], isTrue);
      expect(out['predicted_mutations'], <dynamic>[]);
      expect(out['rollback_required'], isFalse);
      expect(out['runtime_mutated'], isFalse);
    });

    test('simulate executed action picks selector/window/command targets', () {
      final Map<String, dynamic> out = simulateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'type': 'browser_click', 'selector': '#a'},
          <String, dynamic>{'type': 'native_focus', 'window': 'win'},
        ],
        tick: 1,
      );
      final List<dynamic> predicted =
          out['predicted_mutations'] as List<dynamic>;
      expect(predicted.length, 2);
      expect((predicted[0] as Map<String, dynamic>)['target'], '#a');
      expect((predicted[1] as Map<String, dynamic>)['target'], 'win');
    });

    test('simulate forbidden action sets rollback_required', () {
      // empty selector -> invalid_selector -> not executed -> rollback path
      final Map<String, dynamic> out = simulateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'type': 'browser_click', 'selector': ''},
        ],
      );
      expect(out['rollback_required'], isTrue);
      expect(out['predicted_mutations'], <dynamic>[]);
    });

    test('simulate terminal command blocked by default empty policy', () {
      // simulateRuntimeExecution passes no policy -> default {} blocks
      // terminal_command, so it is NOT executed and rollback is required.
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'terminal');
      final Map<String, dynamic> out = simulateRuntimeExecution(
        <Map<String, dynamic>>[
          <String, dynamic>{'type': 'terminal_command', 'command': 'pwd'},
        ],
        sandbox: sb,
      );
      expect(out['rollback_required'], isTrue);
      expect(out['predicted_mutations'], <dynamic>[]);
    });
  });

  group('runtime_execution_engine', () {
    test('default sandbox path, browser_click executes', () {
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'browser_click', 'selector': '#x'},
      );
      expect(out['executed'], isTrue);
      expect(out['runtime'], 'browser');
    });

    test('sandbox forbidden action', () {
      final Map<String, dynamic> sb =
          buildRuntimeSandbox(allowedActions: <String>['native_focus']);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'browser_click', 'selector': '#x'},
        sandbox: sb,
      );
      expect(out['executed'], isFalse);
      expect(out['reason'], 'sandbox_forbidden');
    });

    test('permission denied when perms present but scope off', () {
      final Map<String, dynamic> perms =
          buildRuntimePermissions(scopes: <String>['native']);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'browser_click', 'selector': '#x'},
        permissions: perms,
      );
      expect(out['executed'], isFalse);
      expect(out['reason'], 'permission_denied');
    });

    test('policy violation for forbidden terminal', () {
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'terminal');
      final Map<String, dynamic> pol = buildRuntimePolicy(allowTerminal: false);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'terminal_command', 'command': 'pwd'},
        sandbox: sb,
        policy: pol,
      );
      expect(out['executed'], isFalse);
      expect(out['reason'], 'policy_violation');
    });

    test('unsafe terminal command rejected', () {
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'terminal');
      final Map<String, dynamic> pol = buildRuntimePolicy(allowTerminal: true);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'terminal_command', 'command': 'rm -rf /'},
        sandbox: sb,
        policy: pol,
      );
      expect(out['executed'], isFalse);
      expect(out['reason'], 'unsafe_terminal');
    });

    test('safe terminal command executes', () {
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'terminal');
      final Map<String, dynamic> pol = buildRuntimePolicy(allowTerminal: true);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'terminal_command', 'command': 'pwd'},
        sandbox: sb,
        policy: pol,
      );
      expect(out['executed'], isTrue);
    });

    test('browser_click invalid (empty) selector rejected', () {
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'browser_click', 'selector': ''},
      );
      expect(out['executed'], isFalse);
      expect(out['reason'], 'invalid_selector');
    });

    test('native_focus executes', () {
      final Map<String, dynamic> sb = buildRuntimeSandbox(runtime: 'native');
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'native_focus', 'window': 'app'},
        sandbox: sb,
      );
      expect(out['executed'], isTrue);
      expect(out['runtime'], 'native');
    });

    test('unknown action type uses payload-map normalization branch', () {
      // sandbox allows the action_type so it executes; payload is a Map ->
      // hits the `pl is Map` branch (lines 31-34).
      final Map<String, dynamic> sb =
          buildRuntimeSandbox(allowedActions: <String>['custom_op']);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{
          'type': 'custom_op',
          'payload': <String, dynamic>{'k': 'v'}
        },
        sandbox: sb,
      );
      expect(out['executed'], isTrue);
      final Map<String, dynamic> action =
          (out['action'] as Map).cast<String, dynamic>();
      expect((action['payload'] as Map<String, dynamic>)['k'], 'v');
    });

    test('unknown action type with non-map payload spreads raw', () {
      final Map<String, dynamic> sb =
          buildRuntimeSandbox(allowedActions: <String>['custom_op']);
      final Map<String, dynamic> out = executeRuntimeAction(
        <String, dynamic>{'type': 'custom_op', 'extra': 'data'},
        sandbox: sb,
      );
      expect(out['executed'], isTrue);
      final Map<String, dynamic> action =
          (out['action'] as Map).cast<String, dynamic>();
      expect((action['payload'] as Map<String, dynamic>)['extra'], 'data');
    });
  });

  group('runtime_worker_engine', () {
    test('build workers sorts by worker_id and applies defaults', () {
      final List<Map<String, dynamic>> out = buildRuntimeWorkers(
        <Map<String, dynamic>>[
          <String, dynamic>{'worker_id': 'wb', 'runtime': 'native'},
          <String, dynamic>{'node_id': 'wa', 'synced': false},
          <String, dynamic>{},
        ],
      );
      expect(out.length, 3);
      // sorted ascending by worker_id; 'wa' < 'wb' < 'worker:2'
      expect(out[0]['worker_id'], 'wa');
      expect(out[0]['synced'], isFalse);
      expect(out[0]['runtime'], 'browser');
      expect(out[1]['worker_id'], 'wb');
      expect(out[2]['worker_id'], 'worker:2');
    });
  });

  group('supporting engines', () {
    test('buildRuntimeSandbox variants', () {
      expect(buildRuntimeSandbox(runtime: 'terminal')['allowed_actions'],
          <String>['terminal_command']);
      expect(buildRuntimeSandbox(runtime: 'native')['allowed_actions'],
          <String>['native_focus']);
      expect(buildRuntimeSandbox(runtime: 'vm')['allowed_actions'],
          <String>['vm_execute']);
      expect(
          (buildRuntimeSandbox()['allowed_actions'] as List<String>).length, 3);
    });

    test('permissions build + validate scope mapping', () {
      final Map<String, dynamic> perms = buildRuntimePermissions();
      expect(
          validateRuntimePermissions(
              perms, 'browser', 'browser_click')['allowed'],
          isTrue);
      expect(
          validateRuntimePermissions(perms, 'native', 'native_focus')['scope'],
          'native');
      expect(
          validateRuntimePermissions(perms, 'x', 'terminal_command')['scope'],
          'terminal');
      expect(validateRuntimePermissions(perms, 'x', 'vm_run')['scope'], 'vm');
      expect(validateRuntimePermissions(perms, 'x', 'connector_call')['scope'],
          'connector');
      expect(validateRuntimePermissions(perms, 'unknownrt', 'plain')['scope'],
          'browser');
    });

    test('policy build + enforce branches', () {
      final Map<String, dynamic> pol = buildRuntimePolicy();
      // browser mutation disabled blocks browser_ actions
      final Map<String, dynamic> noBrowser =
          buildRuntimePolicy(allowBrowserMutation: false);
      expect(
          enforceRuntimePolicy(
              noBrowser,
              <String, dynamic>{'action_type': 'browser_click'},
              0,
              0)['allowed'],
          isFalse);
      // over mutation bound
      expect(
          enforceRuntimePolicy(
              pol,
              <String, dynamic>{'action_type': 'native_focus'},
              200,
              0)['within_bounds'],
          isFalse);
      // allowTerminal true list empty
      expect(buildRuntimePolicy(allowTerminal: true)['forbidden_actions'],
          <String>[]);
    });

    test('buildExecutionState with and without optionals', () {
      final Map<String, dynamic> bare = buildExecutionState();
      expect(bare['active_actions'], <dynamic>[]);
      expect(bare['checkpoint'], <String, dynamic>{});
      final Map<String, dynamic> full = buildExecutionState(
        runtime: 'native',
        activeActions: <dynamic>[1],
        queue: <dynamic>[2],
        mutations: <dynamic>[3],
        checkpoint: <String, dynamic>{'c': 1},
        transaction: <String, dynamic>{'t': 1},
        federation: <String, dynamic>{'f': 1},
      );
      expect(full['current_runtime'], 'native');
      expect((full['checkpoint'] as Map<String, dynamic>)['c'], 1);
    });
  });

  group('execution_runtime_ir', () {
    test('compile + to-graph + merge produce structural graph', () {
      final Map<String, dynamic> ir = compileExecutionRuntimeIr(
        <String, dynamic>{
          'actions': <dynamic>[
            <String, dynamic>{'id': 'a1'},
            <String, dynamic>{'action_id': 'a2'},
            <String, dynamic>{'noid': true},
          ],
          'federation': <String, dynamic>{
            'execution_routes': <dynamic>[
              <String, dynamic>{'worker_id': 'w1'},
              <String, dynamic>{'worker_id': ''},
            ],
          },
          'mutations': <String, dynamic>{
            'mutations': <dynamic>[
              <String, dynamic>{'target': 't1', 'kind': 'dom'},
              <String, dynamic>{'kind': 'native'},
            ],
          },
        },
      );
      expect(ir['ir'], 'execution_runtime');
      final Map<String, dynamic> graph = executionRuntimeIrToGraph(ir);
      expect(graph['ir'], 'execution_runtime_graph');
      final List<dynamic> nodes = graph['nodes'] as List<dynamic>;
      final List<String> ids =
          nodes.map((dynamic n) => '${(n as Map)['id']}').toList();
      expect(ids, contains('execution:root'));
      expect(ids, contains('action:a1'));
      expect(ids, contains('action:a2'));
      expect(ids, contains('worker:w1'));
      expect(ids, contains('mutation:t1'));
      // merge: duplicate node id deduped, edges deduped + sorted
      final Map<String, dynamic> merged =
          mergeRuntimeGraph(<Map<String, dynamic>>[graph, graph]);
      expect(merged['ir'], 'unified_runtime_graph');
      final List<dynamic> mNodes = merged['nodes'] as List<dynamic>;
      // dedup means same count as single graph
      expect(mNodes.length, nodes.length);
    });

    test('compile defaults when payload lacks keys', () {
      final Map<String, dynamic> ir =
          compileExecutionRuntimeIr(<String, dynamic>{});
      expect(ir['actions'], <dynamic>[]);
      expect(ir['queues'], <String, dynamic>{});
      final Map<String, dynamic> graph = executionRuntimeIrToGraph(ir);
      expect((graph['nodes'] as List<dynamic>).length, 1);
    });

    test('merge skips blank node ids and blank edge endpoints', () {
      final Map<String, dynamic> dirty = <String, dynamic>{
        'ir': 'x',
        'nodes': <dynamic>[
          <String, dynamic>{'id': '  '},
          <String, dynamic>{'id': 'n1'},
        ],
        'edges': <dynamic>[
          <String, dynamic>{'from': '', 'to': 'n1', 'relation': 'r'},
          <String, dynamic>{'from': 'n1', 'to': 'n2'},
        ],
      };
      final Map<String, dynamic> merged =
          mergeRuntimeGraph(<Map<String, dynamic>>[dirty]);
      expect((merged['nodes'] as List<dynamic>).length, 1);
      final List<dynamic> edges = merged['edges'] as List<dynamic>;
      expect(edges.length, 1);
      // edge endpoints n1->n2 are valid (relation defaulted only for dedup key)
      expect((edges[0] as Map<String, dynamic>)['from'], 'n1');
      expect((edges[0] as Map<String, dynamic>)['to'], 'n2');
    });
  });

  group('runtime_execution_orchestrator', () {
    test('runExecutionRuntime default browser, non-simulate', () {
      final Map<String, dynamic> out = runExecutionRuntime();
      expect(out['bounded'], isTrue);
      expect(out['execution_ir'], isA<Map<String, dynamic>>());
      expect((out['actions'] as List<dynamic>).isNotEmpty, isTrue);
    });

    test('runExecutionRuntime simulate path', () {
      final Map<String, dynamic> out = runExecutionRuntime(simulate: true);
      expect(out['simulation'], isA<Map<String, dynamic>>());
      expect((out['transition'] as Map<String, dynamic>)['to'], 'simulating');
      expect(out['execution_ir'], isA<Map<String, dynamic>>());
    });

    test('runExecutionRuntime with stored checkpoint state-map + rollback', () {
      final Map<String, dynamic> out = runExecutionRuntime(
        stored: <String, dynamic>{
          'checkpoint': <String, dynamic>{
            'state': <String, dynamic>{
              'browser': <String, dynamic>{'tab': 1}
            }
          }
        },
        rollbackEnabled: true,
      );
      expect((out['rollback'] as Map<String, dynamic>)['rolled_back'], isTrue);
      expect((out['checkpoints'] as List<dynamic>).length, 1);
    });

    test('runExecutionRuntime checkpoint without state key uses prior body',
        () {
      final Map<String, dynamic> out = runExecutionRuntime(
        stored: <String, dynamic>{
          'checkpoint': <String, dynamic>{
            'browser': <String, dynamic>{'tab': 2}
          }
        },
      );
      expect((out['checkpoints'] as List<dynamic>).length, 1);
    });

    test('runExecutionRuntime terminal runtime with sources + workflow', () {
      final Map<String, dynamic> out = runExecutionRuntime(
        runtime: 'terminal',
        sources: <String, dynamic>{
          'actions': <dynamic>[
            <String, dynamic>{'type': 'terminal_command', 'command': 'pwd'}
          ],
          'workflow': <String, dynamic>{'wf': 1},
          'sync': <String, dynamic>{'s': 1},
        },
      );
      expect(
          (out['coordination'] as Map<String, dynamic>)['coordinated'], isTrue);
      expect((out['synchronization'] as Map<String, dynamic>)['s'], 1);
    });

    test('runExecutionForExtraction disabled returns enabled:false', () {
      final Map<String, dynamic> out =
          runExecutionForExtraction(executionRuntime: false);
      expect(out['enabled'], isFalse);
      expect(out['bounded'], isTrue);
    });

    test('runExecutionForExtraction enabled with merge graph', () {
      final Map<String, dynamic> out = runExecutionForExtraction(
        sources: <String, dynamic>{
          'actions': <dynamic>[
            <String, dynamic>{'type': 'browser_click', 'selector': '#go'}
          ],
        },
        mergeGraph: true,
      );
      expect(out['enabled'], isTrue);
      expect(out['unified_graph'], isA<Map<String, dynamic>>());
      expect((out['unified_graph'] as Map<String, dynamic>)['ir'],
          'unified_runtime_graph');
      expect(out['execution_persisted'], isFalse);
    });

    test('runExecutionForExtraction without merge graph', () {
      final Map<String, dynamic> out = runExecutionForExtraction(
        mergeGraph: false,
      );
      expect(out['unified_graph'], <String, dynamic>{});
    });

    test('runExecutionForExtraction simulate path', () {
      final Map<String, dynamic> out = runExecutionForExtraction(
        simulateExecution: true,
      );
      expect(out['simulation'], isA<Map<String, dynamic>>());
      expect((out['simulation'] as Map<String, dynamic>)['simulated'], isTrue);
    });
  });
}
