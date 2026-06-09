// Coverage-focused branch tests for the newly-ported runtime-family engines
// under lib/src/workflows, lib/src/evolution, lib/src/causality and
// lib/src/synchronization. Imports the internal engine modules directly and
// exercises BOTH branches of each public top-level function (empty vs
// populated, edge values, memory persist/load round-trips, merge-graph paths).
//
// Assertions are structural (keys, lengths, branch values, bounded:true) — no
// hash assertions.
import 'dart:io';

import 'package:test/test.dart';

// workflows
import 'package:webweavex/src/workflows/workflow_scheduler_engine.dart';
import 'package:webweavex/src/workflows/workflow_runtime_engine.dart';
import 'package:webweavex/src/workflows/workflow_state_engine.dart';
import 'package:webweavex/src/workflows/workflow_transition_engine.dart';
import 'package:webweavex/src/workflows/workflow_execution_engine.dart';
import 'package:webweavex/src/workflows/workflow_federation_engine.dart';
import 'package:webweavex/src/workflows/workflow_graph_engine.dart';
import 'package:webweavex/src/workflows/workflow_navigation_engine.dart';
import 'package:webweavex/src/workflows/workflow_dependency_engine.dart';
import 'package:webweavex/src/workflows/workflow_alignment_engine.dart';
import 'package:webweavex/src/workflows/workflow_recovery_engine.dart';
import 'package:webweavex/src/workflows/workflow_planner_engine.dart';
import 'package:webweavex/src/workflows/workflow_runtime_ir.dart';
import 'package:webweavex/src/workflows/workflow_orchestrator.dart';
import 'package:webweavex/src/workflows/unified_runtime_graph.dart' as wf_graph;

// evolution
import 'package:webweavex/src/evolution/runtime_pattern_engine.dart';
import 'package:webweavex/src/evolution/runtime_memory_engine.dart';
import 'package:webweavex/src/evolution/runtime_workflow_engine.dart';
import 'package:webweavex/src/evolution/runtime_adaptation_engine.dart';
import 'package:webweavex/src/evolution/runtime_strategy_engine.dart';
import 'package:webweavex/src/evolution/runtime_semantic_engine.dart';
import 'package:webweavex/src/evolution/runtime_topology_engine.dart';
import 'package:webweavex/src/evolution/runtime_mutation_engine.dart';
import 'package:webweavex/src/evolution/runtime_repair_engine.dart';
import 'package:webweavex/src/evolution/evolution_runtime_ir.dart';
import 'package:webweavex/src/evolution/runtime_evolution_orchestrator.dart';
import 'package:webweavex/src/evolution/unified_runtime_graph.dart' as ev_graph;

// causality
import 'package:webweavex/src/causality/causality_runtime.dart';

// synchronization
import 'package:webweavex/src/synchronization/synchronization_engines.dart';
import 'package:webweavex/src/synchronization/runtime_sync_memory.dart';

void main() {
  late Directory tmp;

  setUp(() {
    tmp = Directory.systemTemp.createTempSync('wwx_cov_');
  });

  tearDown(() {
    if (tmp.existsSync()) {
      tmp.deleteSync(recursive: true);
    }
  });

  String tmpPath(String name) => '${tmp.path}${Platform.pathSeparator}$name';

  // -------------------------------------------------------------------------
  // workflows/workflow_scheduler_engine.dart
  // -------------------------------------------------------------------------
  group('scheduleWorkflowExecution', () {
    test('empty plans → empty schedule', () {
      final out = scheduleWorkflowExecution(<Map<String, dynamic>>[]);
      expect(out['count'], 0);
      expect((out['schedule'] as List).isEmpty, isTrue);
      expect(out['bounded'], isTrue);
    });

    test('sorts by priority then objective; coerces int/num/string priorities',
        () {
      final out = scheduleWorkflowExecution(<Map<String, dynamic>>[
        <String, dynamic>{'objective': 'z', 'priority': 2},
        <String, dynamic>{'objective': 'a', 'priority': 1},
        // num (double) priority → toIntValue num branch
        <String, dynamic>{'objective': 'b', 'priority': 1.0},
        // string-parsable priority → int.tryParse branch
        <String, dynamic>{'objective': 'c', 'priority': '0'},
        // unparsable priority → fallback 0; objective_priority fallback path
        <String, dynamic>{'objective': 'd', 'priority': 'NaNish'},
        // no priority but objective_priority present (sort fallback chain)
        <String, dynamic>{'objective': 'e', 'objective_priority': 5},
      ], tick: 100);
      final schedule = out['schedule'] as List<dynamic>;
      expect(out['count'], 6);
      // First items have effective sort-priority 0: c('0'->0), d(NaN->0), e? no
      // e has objective_priority 5 so sort key 5. c and d are 0 → sorted by
      // objective: 'c' before 'd'.
      final firstObj = (schedule[0] as Map)['objective'];
      expect(firstObj, anyOf('c', 'd'));
      // tick + index applied
      expect((schedule[0] as Map)['tick'], 100);
      expect((schedule[1] as Map)['tick'], 101);
      // distributed_order / pacing equal to index
      expect((schedule[2] as Map)['distributed_order'], 2);
      expect((schedule[2] as Map)['pacing'], 2);
      // output priority uses only 'priority' (fallback 0): the entry that only
      // had objective_priority gets out priority 0.
      final eEntry = schedule
          .firstWhere((dynamic s) => (s as Map)['objective'] == 'e') as Map;
      expect(eEntry['priority'], 0);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_runtime_engine.dart
  // -------------------------------------------------------------------------
  group('buildWorkflowRuntimeContext', () {
    test('default null sources → empty sorted list', () {
      final out = buildWorkflowRuntimeContext();
      expect(out['url'], '');
      expect(out['primary_runtime'], 'browser');
      expect((out['sources'] as List).isEmpty, isTrue);
      expect(out['bounded'], isTrue);
    });

    test('populated sources → sorted keys', () {
      final out = buildWorkflowRuntimeContext(
        url: 'https://x',
        runtime: 'electron',
        sources: <String, dynamic>{'z': true, 'a': false, 'm': true},
      );
      expect(out['sources'], <String>['a', 'm', 'z']);
      expect(out['primary_runtime'], 'electron');
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_state_engine.dart
  // -------------------------------------------------------------------------
  group('buildWorkflowState', () {
    test('null execution + non-list steps → defaults', () {
      final out = buildWorkflowState(<String, dynamic>{'objective': 'o'});
      expect((out['completed_steps'] as List).isEmpty, isTrue);
      expect((out['runtime_state'] as Map)['total_steps'], 0);
      expect((out['runtime_state'] as Map)['objective'], 'o');
      expect(out['bounded'], isTrue);
    });

    test('executed entries: completed map, incomplete map, and non-map item',
        () {
      final out = buildWorkflowState(
        <String, dynamic>{
          'objective': 'O',
          'steps': <dynamic>[
            <String, dynamic>{'id': 's0'},
            <String, dynamic>{'id': 's1'},
          ],
        },
        <String, dynamic>{
          'executed': <dynamic>[
            <String, dynamic>{'step_id': 's0', 'completed': true},
            <String, dynamic>{'step_id': 's1', 'completed': false},
            'not-a-map',
          ],
        },
        3,
      );
      expect(out['current_step'], 3);
      expect(out['completed_steps'], <dynamic>['s0']);
      expect((out['runtime_state'] as Map)['total_steps'], 2);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_transition_engine.dart
  // -------------------------------------------------------------------------
  group('buildWorkflowTransitions', () {
    test('non-list executed → empty', () {
      final out = buildWorkflowTransitions(<String, dynamic>{});
      expect(out.isEmpty, isTrue);
    });

    test('builds n-1 transitions; handles non-map entries', () {
      final out = buildWorkflowTransitions(<String, dynamic>{
        'executed': <dynamic>[
          <String, dynamic>{'step_id': 'a'},
          <String, dynamic>{'step_id': 'b'},
          'x', // non-map curr → empty step_id
        ],
      });
      expect(out.length, 2);
      expect(out[0]['from'], 'a');
      expect(out[0]['to'], 'b');
      expect(out[1]['from'], 'b');
      expect(out[1]['to'], '');
      expect(out[1]['relation'], 'transitions');
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_execution_engine.dart
  // -------------------------------------------------------------------------
  group('executeWorkflowPlan', () {
    test('non-list steps → empty executed', () {
      final out = executeWorkflowPlan(<String, dynamic>{'objective': 'o'});
      expect(out['completed_count'], 0);
      expect((out['executed'] as List).isEmpty, isTrue);
    });

    test('list steps incl. non-map step → executed entries', () {
      final out = executeWorkflowPlan(
        <String, dynamic>{
          'objective': 'O',
          'steps': <dynamic>[
            <String, dynamic>{'id': 's0', 'action': 'a', 'runtime': 'electron'},
            'not-a-map',
          ],
        },
        tick: 5,
      );
      expect(out['completed_count'], 2);
      final executed = out['executed'] as List<dynamic>;
      expect((executed[0] as Map)['step_id'], 's0');
      expect((executed[0] as Map)['tick'], 5);
      // non-map step gets default step_id and browser runtime
      expect((executed[1] as Map)['step_id'], 'step:1');
      expect((executed[1] as Map)['runtime'], 'browser');
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_federation_engine.dart
  // -------------------------------------------------------------------------
  group('federateWorkflowRuntime', () {
    test('all-empty/null → falsey flags, empty checkpoints', () {
      final out = federateWorkflowRuntime();
      expect((out['workers'] as List).isEmpty, isTrue);
      expect(out['browser_runtime'], isFalse);
      expect(out['native_runtime'], isFalse);
      expect(out['distributed_sync'], isFalse);
      expect((out['semantic_checkpoints'] as Map).isEmpty, isTrue);
      expect(out['extraction_agents'], 0);
    });

    test('populated workers + semantic.memory + runtime maps', () {
      final out = federateWorkflowRuntime(
        browser: <String, dynamic>{'url': 'x'},
        native: <String, dynamic>{'k': 1},
        distributed: <String, dynamic>{'w': 1},
        semantic: <String, dynamic>{
          'semantic': <String, dynamic>{
            'memory': <String, dynamic>{'m': 1}
          }
        },
        workers: <dynamic>[
          <String, dynamic>{'worker_id': 'w0'},
          <String, dynamic>{'id': 'w1'},
          'not-a-map',
        ],
      );
      expect((out['workers'] as List).length, 3);
      expect((out['workers'] as List)[0]['worker_id'], 'w0');
      expect((out['workers'] as List)[1]['worker_id'], 'w1');
      // non-map worker → fallback id w:2
      expect((out['workers'] as List)[2]['worker_id'], 'w:2');
      expect(out['browser_runtime'], isTrue);
      expect(out['native_runtime'], isTrue);
      expect(out['distributed_sync'], isTrue);
      expect((out['semantic_checkpoints'] as Map)['m'], 1);
      expect(out['extraction_agents'], 3);
    });

    test('semantic present but inner not a map → empty checkpoints', () {
      final out = federateWorkflowRuntime(
        semantic: <String, dynamic>{'semantic': 'scalar'},
      );
      expect((out['semantic_checkpoints'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_graph_engine.dart
  // -------------------------------------------------------------------------
  group('buildWorkflowGraph', () {
    test('no steps, no retries → objective + semantic nodes only', () {
      final out = buildWorkflowGraph(
        <String, dynamic>{'objective': 'obj'},
        <String, dynamic>{},
        <String, dynamic>{'retries': 0},
        <String, dynamic>{},
        <Map<String, dynamic>>[],
      );
      final nodes = out['nodes'] as List<dynamic>;
      final ids = nodes.map((dynamic n) => (n as Map)['id']).toList();
      expect(ids.contains('objective:obj'), isTrue);
      expect(ids.contains('semantic:state'), isTrue);
      expect(ids.contains('checkpoint:recovery'), isFalse);
    });

    test('steps with depends_on, transitions, and retries>0 → recovery node',
        () {
      final out = buildWorkflowGraph(
        <String, dynamic>{'objective': 'obj'},
        <String, dynamic>{
          'steps': <dynamic>[
            <String, dynamic>{'id': 'step:0', 'runtime': 'browser'},
            <String, dynamic>{
              'id': 'step:1',
              'runtime': 'electron',
              'depends_on': 'step:0',
            },
            'not-a-map',
          ],
        },
        <String, dynamic>{'retries': 2},
        <String, dynamic>{},
        <Map<String, dynamic>>[
          <String, dynamic>{'from': 'step:0', 'to': 'step:1'},
        ],
      );
      final nodeIds =
          (out['nodes'] as List).map((dynamic n) => (n as Map)['id']).toList();
      expect(nodeIds.contains('checkpoint:recovery'), isTrue);
      final relations = (out['edges'] as List)
          .map((dynamic e) => (e as Map)['relation'])
          .toSet();
      expect(relations.contains('depends_on'), isTrue);
      expect(relations.contains('executes'), isTrue);
      expect(relations.contains('transitions'), isTrue);
      expect(relations.contains('recovers'), isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_navigation_engine.dart
  // -------------------------------------------------------------------------
  group('navigateRuntimeWorkflow', () {
    test('non-list steps → empty', () {
      final out = navigateRuntimeWorkflow(<String, dynamic>{});
      expect(out['count'], 0);
    });

    test('known + unknown runtimes select navigator; non-map step', () {
      final out = navigateRuntimeWorkflow(
        <String, dynamic>{
          'steps': <dynamic>[
            <String, dynamic>{'id': 's0', 'runtime': 'terminal'},
            <String, dynamic>{'id': 's1', 'runtime': 'unknown_runtime'},
            'not-a-map',
          ],
        },
        tick: 7,
      );
      final navs = out['navigations'] as List<dynamic>;
      expect(out['count'], 3);
      expect((navs[0] as Map)['navigator'], 'terminal_progression');
      // unknown runtime → fallback browser_navigation
      expect((navs[1] as Map)['navigator'], 'browser_navigation');
      // non-map step → default runtime browser → browser_navigation
      expect((navs[2] as Map)['navigator'], 'browser_navigation');
      expect((navs[0] as Map)['tick'], 7);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_dependency_engine.dart
  // -------------------------------------------------------------------------
  group('buildWorkflowDependencies', () {
    test('non-list steps → empty groups', () {
      final out = buildWorkflowDependencies(<String, dynamic>{});
      expect((out['execution_ordering'] as List).isEmpty, isTrue);
      expect((out['runtime_dependencies'] as List).isEmpty, isTrue);
    });

    test('depends_on + runtime change between consecutive steps', () {
      final out = buildWorkflowDependencies(<String, dynamic>{
        'steps': <dynamic>[
          <String, dynamic>{'id': 's0', 'runtime': 'browser', 'action': 'a'},
          <String, dynamic>{
            'id': 's1',
            'runtime': 'electron',
            'depends_on': 's0',
            'action': 'b',
          },
          'not-a-map',
        ],
      });
      expect((out['execution_ordering'] as List).length, 1);
      expect((out['semantic_prerequisites'] as List).length, 1);
      // runtime changed browser→electron, and electron→'' (non-map)
      expect((out['runtime_dependencies'] as List).isNotEmpty, isTrue);
      expect((out['extraction_chains'] as List).length, 3);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_alignment_engine.dart
  // -------------------------------------------------------------------------
  group('alignWorkflowRuntime', () {
    test('aligned when steps length == completed_count', () {
      final out = alignWorkflowRuntime(
        <String, dynamic>{
          'objective': 'o',
          'steps': <dynamic>[1, 2],
        },
        <String, dynamic>{'current_step': 4},
        <String, dynamic>{'completed_count': 2},
      );
      expect(out['steps_aligned'], isTrue);
      expect(out['state_step'], 4);
    });

    test('not aligned, non-list steps, missing completed_count', () {
      final out = alignWorkflowRuntime(
        <String, dynamic>{'objective': 'o'},
        <String, dynamic>{},
        <String, dynamic>{},
      );
      expect(out['steps_aligned'], isTrue); // 0 == 0
      expect(out['state_step'], 0);
      final out2 = alignWorkflowRuntime(
        <String, dynamic>{
          'steps': <dynamic>[1]
        },
        <String, dynamic>{},
        <String, dynamic>{'completed_count': 0},
      );
      expect(out2['steps_aligned'], isFalse);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_recovery_engine.dart
  // -------------------------------------------------------------------------
  group('recoverWorkflowRuntime', () {
    test('failures present (known + unknown) → recovered steps', () {
      final out = recoverWorkflowRuntime(
        <String, dynamic>{'current_step': 0, 'retries': 1},
        <String>['selector_drift', 'unknown_failure'],
      );
      final steps = out['recovered_steps'] as List<dynamic>;
      expect(steps.length, 2);
      expect((steps[0] as Map)['action'], 'heal_selector');
      expect((steps[1] as Map)['action'], 'retry_step');
      expect((out['state'] as Map)['retries'], 3); // 1 + 2
    });

    test('no failures but current_step>0 → implicit retry', () {
      final out = recoverWorkflowRuntime(
        <String, dynamic>{'current_step': 5},
      );
      final steps = out['recovered_steps'] as List<dynamic>;
      expect(steps.length, 1);
      expect((steps[0] as Map)['failure'], 'implicit_retry');
    });

    test('no failures and current_step==0 → no recovered steps', () {
      final out = recoverWorkflowRuntime(<String, dynamic>{});
      expect((out['recovered_steps'] as List).isEmpty, isTrue);
      expect((out['state'] as Map)['retries'], 0);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_planner_engine.dart (branch coverage of _runtimeForStep)
  // -------------------------------------------------------------------------
  group('buildWorkflowPlan', () {
    test('default objective → saas domain; runtime fallback browser', () {
      final out = buildWorkflowPlan('extract_dashboard');
      expect(out['domain'], 'saas');
      expect((out['steps'] as List).isNotEmpty, isTrue);
    });

    test('domain from semantic + application edges + causality handoffs', () {
      final out = buildWorkflowPlan(
        'monitor_infrastructure',
        semanticRuntime: <String, dynamic>{
          'domain': <String, dynamic>{'domain': 'infrastructure'}
        },
        applicationRuntime: <String, dynamic>{
          'workflow': <String, dynamic>{
            'edges': <dynamic>[
              <String, dynamic>{'relation': 'navigates'},
              'not-a-map',
            ],
          },
        },
        causality: <String, dynamic>{
          'causality': <String, dynamic>{
            'propagation': <String, dynamic>{
              'handoffs': <dynamic>[
                <String, dynamic>{'to': 'electron'},
                'not-a-map',
              ],
            },
          },
        },
      );
      expect(out['domain'], 'infrastructure');
      final steps = out['steps'] as List<dynamic>;
      final ids = steps.map((dynamic s) => (s as Map)['id']).toList();
      expect(ids.any((dynamic i) => '$i'.startsWith('app:')), isTrue);
      expect(ids.any((dynamic i) => '$i'.startsWith('causal:')), isTrue);
      // infra step → native runtime
      final runtimes = steps.map((dynamic s) => (s as Map)['runtime']).toSet();
      expect(runtimes.contains('native'), isTrue);
    });

    test('runtime classification for terminal/repository/notification steps',
        () {
      final term = buildWorkflowPlan('capture_terminal');
      final termRuntimes = (term['steps'] as List)
          .map((dynamic s) => (s as Map)['runtime'])
          .toSet();
      expect(termRuntimes.contains('terminal'), isTrue);

      final repo = buildWorkflowPlan('extract_repository');
      final repoRuntimes = (repo['steps'] as List)
          .map((dynamic s) => (s as Map)['runtime'])
          .toSet();
      expect(repoRuntimes.contains('repository'), isTrue);

      final notif = buildWorkflowPlan('capture_notifications');
      final notifRuntimes = (notif['steps'] as List)
          .map((dynamic s) => (s as Map)['runtime'])
          .toSet();
      expect(notifRuntimes.contains('desktop'), isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_runtime_ir.dart
  // -------------------------------------------------------------------------
  group('workflow runtime IR', () {
    test('compileWorkflowRuntimeIr defaults when keys absent', () {
      final out = compileWorkflowRuntimeIr(<String, dynamic>{});
      expect(out['ir'], 'workflow_runtime');
      expect(out['bounded'], isTrue);
    });

    test('workflowRuntimeIrToGraph empty nodes → injects root', () {
      final out = workflowRuntimeIrToGraph(<String, dynamic>{});
      final nodes = out['nodes'] as List<dynamic>;
      expect(nodes.length, 1);
      expect((nodes[0] as Map)['id'], 'workflow:root');
    });

    test('workflowRuntimeIrToGraph sorts present nodes incl. non-map', () {
      final out = workflowRuntimeIrToGraph(<String, dynamic>{
        'workflow_graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'z'},
            <String, dynamic>{'id': 'a'},
            'not-a-map',
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'a', 'to': 'z'}
          ],
        },
      });
      final nodes = out['nodes'] as List<dynamic>;
      // non-map sorts as '' first, then 'a', then 'z'
      expect((nodes.last as Map)['id'], 'z');
      expect((out['edges'] as List).length, 1);
    });
  });

  // -------------------------------------------------------------------------
  // workflows/unified_runtime_graph.dart
  // -------------------------------------------------------------------------
  group('workflows buildUnifiedRuntimeGraph', () {
    test('empty list → empty graph', () {
      final out = wf_graph.buildUnifiedRuntimeGraph(<Map<String, dynamic>>[]);
      expect((out['nodes'] as List).isEmpty, isTrue);
      expect((out['edges'] as List).isEmpty, isTrue);
    });

    test('dedup nodes/edges, skip blank ids, non-map entries, default relation',
        () {
      final out = wf_graph.buildUnifiedRuntimeGraph(<Map<String, dynamic>>[
        <String, dynamic>{
          'ir': 'g',
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': 'n1'}, // dup
            <String, dynamic>{'id': '   '}, // blank → skipped
            'not-a-map', // → empty id skipped
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'a', 'to': 'b'}, // default relation
            <String, dynamic>{'from': 'a', 'to': 'b'}, // dup
            <String, dynamic>{'from': '', 'to': 'b'}, // blank src skipped
            'not-a-map',
          ],
        },
      ]);
      expect((out['nodes'] as List).length, 1);
      // edges with no relation use 'related_to' for dedup; the stored edge
      // keeps its original keys plus runtime_type tag.
      expect((out['edges'] as List).length, 1);
      expect((out['edges'] as List)[0]['runtime_type'], 'g');
      expect((out['nodes'] as List)[0]['runtime_type'], 'g');
    });
  });

  // -------------------------------------------------------------------------
  // workflows/workflow_orchestrator.dart — both run* funcs, both branches
  // -------------------------------------------------------------------------
  group('workflow orchestrator', () {
    test('runAutonomousWorkflow with rich inputs', () {
      final out = runAutonomousWorkflow(
        objective: 'extract_dashboard',
        priority: 3,
        semanticRuntime: <String, dynamic>{
          'semantic': <String, dynamic>{
            'domain': <String, dynamic>{'domain': 'saas'}
          }
        },
        causalityResult: <String, dynamic>{'causality': <String, dynamic>{}},
        applicationResult: <String, dynamic>{'workflow': <String, dynamic>{}},
        distributedResult: <String, dynamic>{
          'workers': <dynamic>[
            <String, dynamic>{'worker_id': 'w0'}
          ]
        },
        nativeCognition: <String, dynamic>{'desktop': <String, dynamic>{}},
        url: 'https://app',
        tick: 1,
        failures: <String>['selector_drift'],
      );
      expect(out['bounded'], isTrue);
      expect((out['plan'] as Map)['priority'], 3);
      expect(out.containsKey('workflow_ir'), isTrue);
      expect(out.containsKey('memory'), isTrue);
    });

    test('runWorkflowForExtraction disabled branch', () {
      final out = runWorkflowForExtraction(autonomousWorkflow: false);
      expect(out['enabled'], isFalse);
    });

    test('runWorkflowForExtraction persist+load+merge graph branch', () {
      final path = tmpPath('wf_mem.json');
      final first = runWorkflowForExtraction(
        objective: 'extract_dashboard',
        memoryPath: path,
        memoryKey: 'k-workflow',
        url: 'https://app',
        mergeGraph: true,
      );
      expect(first['enabled'], isTrue);
      expect(first['memory_persisted'], isTrue);
      expect(File(path).existsSync(), isTrue);
      expect((first['unified_graph'] as Map)['ir'], 'unified_runtime_graph');

      // second call loads persisted memory (available==true branch)
      final second = runWorkflowForExtraction(
        objective: 'extract_dashboard',
        memoryPath: path,
        memoryKey: 'k-workflow',
        url: 'https://app',
        mergeGraph: false,
      );
      expect(second['memory_persisted'], isTrue);
      expect((second['unified_graph'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_pattern_engine.dart
  // -------------------------------------------------------------------------
  group('buildRuntimePatterns', () {
    test('all null → empty structures', () {
      final out = buildRuntimePatterns();
      expect((out['ui_structures'] as List).isEmpty, isTrue);
      expect((out['workflow_patterns'] as List).isEmpty, isTrue);
      expect(out['sync_histories'], 0);
    });

    test('populated ui/workflows/semantic/sync', () {
      final out = buildRuntimePatterns(
        ui: <String, dynamic>{'b': 1, 'a': 2},
        workflows: <dynamic>[
          <String, dynamic>{'objective': 'obj0'},
          <String, dynamic>{'action': 'act1'}, // objective absent → action
        ],
        semantic: <String, dynamic>{'layout1': 1, 'layout2': 2},
        syncHistory: <dynamic>[1, 2, 3],
      );
      expect(out['ui_structures'], <String>['a', 'b']);
      expect(out['workflow_patterns'], <String>['obj0', 'act1']);
      expect((out['semantic_layouts'] as List).length, 2);
      expect(out['sync_histories'], 3);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_memory_engine.dart — save/load roundtrip + remember
  // -------------------------------------------------------------------------
  group('evolution memory engine', () {
    test('pyJsonDumpsSorted covers all value kinds', () {
      final s = pyJsonDumpsSorted(<String, dynamic>{
        'b': <dynamic>[1, 2.0, 2.5, true, false, null, 'tab\tnl\n"q"\\'],
        'a': <String, dynamic>{'z': 1, 'a': 2},
        // non-ASCII (>0x7E) and a control char and an astral codepoint
        'u': 'é\u{1F600}',
      });
      expect(s.startsWith('{'), isTrue);
      expect(s.contains('"a": '), isTrue);
      expect(s.contains('2.0'), isTrue); // integral double
      expect(s.contains('2.5'), isTrue);
      // backslash char used to build escape-sequence needles without literal
      // backslashes in source (avoids tooling escape mangling).
      final bs = String.fromCharCode(0x5C);
      // e-acute (U+00E9) escaped via ensure_ascii path.
      expect(s.contains('${bs}u00e9'), isTrue);
      expect(s.contains('${bs}t'), isTrue); // tab escape
      expect(s.contains('${bs}n'), isTrue); // newline escape
      // astral codepoint U+1F600 emitted as a surrogate pair.
      expect(s.contains('${bs}ud83d'), isTrue);
    });

    test('emptyEvolutionMemory shape', () {
      final m = emptyEvolutionMemory();
      expect(m.containsKey('evolution_histories'), isTrue);
      expect(m['bounded'], isTrue);
    });

    test('save → load roundtrip', () {
      final path = tmpPath('ev_mem.json');
      final memory = <String, dynamic>{
        'evolution_histories': <dynamic>[
          <String, dynamic>{'id': 'e1'}
        ],
        'note': 'roundtrip',
      };
      final saved = saveEvolutionRuntime(path, memory, 'ev-key');
      expect(saved['saved'], isTrue);
      expect(File(path).existsSync(), isTrue);

      final loaded = loadEvolutionRuntime(path, 'ev-key');
      expect(loaded['available'], isTrue);
      final m = loaded['memory'] as Map;
      expect(m['note'], 'roundtrip');
    });

    test('load missing file → unavailable with empty memory', () {
      final loaded = loadEvolutionRuntime(tmpPath('nope.json'), 'k');
      expect(loaded['available'], isFalse);
      expect(
          (loaded['memory'] as Map).containsKey('evolution_histories'), isTrue);
    });

    test('rememberEvolutionRuntime: setdefault fields + update overrides', () {
      // memory missing fields; update provides one and omits the rest.
      final merged = rememberEvolutionRuntime(
        <String, dynamic>{'existing': 1},
        <String, dynamic>{
          'evolution_histories': <dynamic>['h'],
          'extra': true,
        },
      );
      expect(merged['existing'], 1);
      expect(merged['evolution_histories'], <dynamic>['h']);
      // omitted field defaulted to empty map
      expect(merged['selector_lineage'], <String, dynamic>{});
      expect(merged['extra'], isTrue);
      expect(merged['bounded'], isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_workflow_engine.dart
  // -------------------------------------------------------------------------
  group('evolveWorkflowRuntime', () {
    test('all null → defaults', () {
      final out = evolveWorkflowRuntime();
      expect(out['score'], 0);
      expect(out['pacing'], 0);
      expect(out['sync_timing'], 0);
      expect(out['retries'], 0);
      expect(out['bounded'], isTrue);
    });

    test('steps + executed + long history → ordering and clamped retries', () {
      final out = evolveWorkflowRuntime(
        <String, dynamic>{
          'steps': <dynamic>[
            <String, dynamic>{'id': 'b', 'priority': 1},
            <String, dynamic>{'id': 'a', 'priority': 5},
            <String, dynamic>{'id': 'c'}, // priority absent → 0
          ],
        },
        <String, dynamic>{
          'executed': <dynamic>[1]
        },
        <dynamic>[1, 2, 3, 4], // length 4 → retries clamps to 3
      );
      // sorted by -priority then id: a(5), b(1), c(0)
      expect(out['execution_ordering'], <dynamic>['a', 'b', 'c']);
      expect(out['retries'], 3);
      expect(out['score'], 1);
      expect(out['pacing'], 2); // 3 steps - 1 score
      expect(out['sync_timing'], 3);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_adaptation_engine.dart
  // -------------------------------------------------------------------------
  group('adaptRuntimeStrategy', () {
    test('no gain, no pressure → only adapted/bounded flags', () {
      final out = adaptRuntimeStrategy(
        <String, dynamic>{'base': 1},
        <String, dynamic>{},
      );
      expect(out['base'], 1);
      expect(out.containsKey('synchronization_path'), isFalse);
      expect(out.containsKey('extraction_path'), isFalse);
      expect(out['adapted'], isTrue);
    });

    test('convergence_gain + runtime_pressure>0 → both paths set', () {
      final out = adaptRuntimeStrategy(
        <String, dynamic>{},
        <String, dynamic>{'convergence_gain': true, 'runtime_pressure': 5},
      );
      expect(out['synchronization_path'], 'continuous');
      expect(out['extraction_path'], 'repair_then_extract');
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_strategy_engine.dart
  // -------------------------------------------------------------------------
  group('buildRuntimeStrategy', () {
    test('no evidence → browser_first / continuous', () {
      final out = buildRuntimeStrategy();
      expect(out['extraction_path'], 'browser_first');
      expect(out['synchronization_path'], 'continuous');
    });

    test('drift + failed steps → repair / converge', () {
      final out = buildRuntimeStrategy(<String, dynamic>{
        'drift_count': 2,
        'failed_steps': 1,
      });
      expect(out['extraction_path'], 'repair_then_extract');
      expect(out['synchronization_path'], 'converge_then_sync');
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_semantic_engine.dart
  // -------------------------------------------------------------------------
  group('evolveSemanticRuntime', () {
    test('all null → empty/zero', () {
      final out = evolveSemanticRuntime();
      expect((out['recurring_entities'] as List).isEmpty, isTrue);
      expect(out['semantic_convergence'], 0);
      expect(out['domain_stabilized'], isFalse);
      expect(out['history_length'], 0);
    });

    test('nested semantic with entities and map domain', () {
      final out = evolveSemanticRuntime(
        <String, dynamic>{
          'semantic': <String, dynamic>{
            'entities': <String, dynamic>{
              'entities': <dynamic>[
                <String, dynamic>{'label': 'X'},
                <String, dynamic>{'type': 'Y'}, // label absent → type
              ],
            },
            'ontology': <String, dynamic>{'o': 1},
            'domain': <String, dynamic>{'domain': 'fin'},
          },
        },
        <dynamic>[1, 2],
      );
      expect((out['recurring_entities'] as List).toSet(), <String>{'X', 'Y'});
      expect(out['semantic_convergence'], 2);
      expect((out['stable_ontology'] as Map)['o'], 1);
      expect(out['domain'], 'fin');
      expect(out['domain_stabilized'], isTrue);
      expect(out['history_length'], 2);
    });

    test('non-map domain truthy string branch', () {
      final out = evolveSemanticRuntime(<String, dynamic>{
        'domain': 'present',
      });
      // inner == sem (no nested 'semantic'); domain not a map → stabilized via
      // string-truthiness; domain output '' because not a map.
      expect(out['domain_stabilized'], isTrue);
      expect(out['domain'], '');
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_topology_engine.dart
  // -------------------------------------------------------------------------
  group('evolveRuntimeTopology', () {
    test('null workers + null causality → empty routing, false propagation',
        () {
      final out = evolveRuntimeTopology();
      expect((out['worker_routing'] as List).isEmpty, isTrue);
      expect(out['causality_propagation'], isFalse);
      expect(out['federation'], 0);
    });

    test('workers (id fallbacks) + non-empty causality', () {
      final out = evolveRuntimeTopology(
        <dynamic>[
          <String, dynamic>{'worker_id': 'wb'},
          <String, dynamic>{'id': 'wa'},
          <String, dynamic>{}, // → w:2
        ],
        <String, dynamic>{},
        <String, dynamic>{'k': 1},
      );
      expect(out['worker_routing'], <String>['w:2', 'wa', 'wb']);
      expect(out['causality_propagation'], isTrue);
      expect(out['federation'], 3);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_mutation_engine.dart
  // -------------------------------------------------------------------------
  group('buildRuntimeMutations', () {
    test('all empty → no mutations', () {
      final out = buildRuntimeMutations(
        <String, dynamic>{},
        <String, dynamic>{},
        <String, dynamic>{},
        <String, dynamic>{},
      );
      expect(out.isEmpty, isTrue);
    });

    test('selectors + workflow ordering + domain + convergence', () {
      final out = buildRuntimeMutations(
        <String, dynamic>{
          'selectors': <dynamic>[
            <String, dynamic>{'original': 'o', 'evolved': 'e'}
          ],
        },
        <String, dynamic>{
          'execution_ordering': <dynamic>['a']
        },
        <String, dynamic>{'domain': 'fin'},
        <String, dynamic>{'convergence': true},
      );
      final kinds = out.map((m) => m['kind']).toSet();
      expect(kinds, <String>{'selector', 'workflow', 'semantic', 'sync'});
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_repair_engine.dart
  // -------------------------------------------------------------------------
  group('repairRuntimeFailures', () {
    test('null args → empty repairs', () {
      final out = repairRuntimeFailures();
      expect(out['repair_count'], 0);
    });

    test('failures (known+unknown) + selectors', () {
      final out = repairRuntimeFailures(
        <String>['failed_workflow', 'mystery'],
        <String, dynamic>{'sel1': 'healed1'},
      );
      final repairs = out['repairs'] as List<dynamic>;
      // 2 failures + 1 selector
      expect(repairs.length, 3);
      final actions = repairs.map((dynamic r) => (r as Map)['action']).toSet();
      expect(actions.contains('reorder_workflow'), isTrue);
      expect(actions.contains('retry_step'), isTrue);
      expect(actions.contains('heal_selector'), isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/evolution_runtime_ir.dart
  // -------------------------------------------------------------------------
  group('evolution runtime IR', () {
    test('compileEvolutionRuntimeIr defaults', () {
      final out = compileEvolutionRuntimeIr(<String, dynamic>{});
      expect(out['ir'], 'evolution_runtime');
      expect(out['lineage'], <dynamic>[]);
    });

    test('evolutionRuntimeIrToGraph empty → root node', () {
      final out = evolutionRuntimeIrToGraph(<String, dynamic>{});
      final nodes = out['nodes'] as List<dynamic>;
      expect((nodes[0] as Map)['id'], 'evolution:root');
    });

    test('evolutionRuntimeIrToGraph with nodes sorts them', () {
      final out = evolutionRuntimeIrToGraph(<String, dynamic>{
        'graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'z'},
            <String, dynamic>{'id': 'a'},
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'a', 'to': 'z'}
          ],
        },
      });
      final nodes = out['nodes'] as List<dynamic>;
      expect((nodes.first as Map)['id'], 'a');
      expect((out['edges'] as List).length, 1);
    });
  });

  // -------------------------------------------------------------------------
  // evolution/unified_runtime_graph.dart
  // -------------------------------------------------------------------------
  group('evolution buildUnifiedRuntimeGraph', () {
    test('empty list → empty', () {
      final out = ev_graph.buildUnifiedRuntimeGraph(<Map<String, dynamic>>[]);
      expect((out['nodes'] as List).isEmpty, isTrue);
    });

    test('dedup + blank skip + default relation', () {
      final out = ev_graph.buildUnifiedRuntimeGraph(<Map<String, dynamic>>[
        <String, dynamic>{
          'ir': 'ev',
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': '  '},
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': 'a', 'to': ''},
          ],
        },
      ]);
      expect((out['nodes'] as List).length, 1);
      expect((out['edges'] as List).length, 1);
      expect((out['edges'] as List)[0]['runtime_type'], 'ev');
    });
  });

  // -------------------------------------------------------------------------
  // evolution/runtime_evolution_orchestrator.dart
  // -------------------------------------------------------------------------
  group('evolution orchestrator', () {
    test('runEvolutionRuntime rich inputs', () {
      final out = runEvolutionRuntime(
        adaptiveMemory: <String, dynamic>{
          'selectors': <String, dynamic>{'s': 1},
          'healed_selectors': <String, dynamic>{'h': 'x'},
        },
        workflowResult: <String, dynamic>{
          'workflow': <String, dynamic>{
            'plan': <String, dynamic>{
              'steps': <dynamic>[
                <String, dynamic>{'id': 's0', 'priority': 1}
              ]
            },
            'execution': <String, dynamic>{
              'executed': <dynamic>[1]
            },
          },
        },
        semanticResult: <String, dynamic>{
          'semantic': <String, dynamic>{
            'ui': <String, dynamic>{'panel': 1}
          }
        },
        syncResult: <String, dynamic>{
          'synchronization': <String, dynamic>{
            'drift': <String, dynamic>{
              'drifts': <dynamic>[1]
            },
            'deltas': <dynamic>[1, 2],
            'convergence': <String, dynamic>{'converged': true},
          },
          'causality': <String, dynamic>{'c': 1},
        },
        distributedResult: <String, dynamic>{
          'workers': <dynamic>[
            <String, dynamic>{'worker_id': 'w0'}
          ]
        },
        failures: <String>['failed_workflow'],
        tick: 2,
      );
      expect(out['bounded'], isTrue);
      expect(out.containsKey('evolution_ir'), isTrue);
      expect((out['evidence'] ?? out['strategy']) != null, isTrue);
    });

    test('runEvolutionForExtraction disabled branch', () {
      final out = runEvolutionForExtraction(evolvingRuntime: false);
      expect(out['enabled'], isFalse);
    });

    test('runEvolutionForExtraction persist+load+merge branches', () {
      final path = tmpPath('ev_orch_mem.json');
      final first = runEvolutionForExtraction(
        memoryPath: path,
        memoryKey: 'ev-orch',
        mergeGraph: true,
      );
      expect(first['enabled'], isTrue);
      expect(first['memory_persisted'], isTrue);
      expect((first['unified_graph'] as Map)['ir'], 'unified_runtime_graph');

      final second = runEvolutionForExtraction(
        memoryPath: path,
        memoryKey: 'ev-orch',
        mergeGraph: false,
      );
      expect(second['memory_persisted'], isTrue);
      expect((second['unified_graph'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // causality/causality_runtime.dart (+ engines via orchestrator)
  // -------------------------------------------------------------------------
  group('causality runtime', () {
    test('runCausalityRuntime via interactions normalization branch', () {
      final out = runCausalityRuntime(
        interactions: <dynamic>[
          <String, dynamic>{'action': 'click', 'from': 'a', 'to': 'b'},
          <String, dynamic>{'type': 'mutation'},
        ],
        nativeCognition: <String, dynamic>{
          'runtime': 'desktop',
          'interactions': <dynamic>[
            <String, dynamic>{'action': 'focus'}
          ],
          'terminal': <String, dynamic>{
            'output': <dynamic>['line1']
          },
          'electron': <String, dynamic>{
            'routes': <dynamic>['/r']
          },
          'desktop': <String, dynamic>{
            'notifications': <dynamic>[
              <String, dynamic>{'id': 'n1', 'interaction': true},
              'plain-notif',
            ]
          },
          'processes': <String, dynamic>{
            'processes': <dynamic>[
              <String, dynamic>{'name': 'proc', 'parent': 'p'}
            ]
          },
        },
        applicationResult: <String, dynamic>{
          'workflow': <String, dynamic>{
            'nodes': <dynamic>[
              <String, dynamic>{'id': 'wn0'}
            ]
          }
        },
        distributedResult: <String, dynamic>{
          'workers': <dynamic>[
            <String, dynamic>{'worker_id': 'w0'}
          ],
          'autonomous': true,
        },
      );
      expect(out['bounded'], isTrue);
      expect(out.containsKey('causality'), isTrue);
      expect(out.containsKey('replay'), isTrue);
      expect(out.containsKey('causal_ir'), isTrue);
    });

    test('runCausalityRuntime with explicit browserEvents (skip normalize)',
        () {
      final out = runCausalityRuntime(
        browserEvents: <Map<String, dynamic>>[
          <String, dynamic>{'id': 'b0', 'runtime': 'browser', 'step': 0}
        ],
        applicationResult: <String, dynamic>{}, // empty → _truthyMap false
      );
      expect(out['bounded'], isTrue);
    });

    test('replayCausalRuntime maps memory fields', () {
      final out = replayCausalRuntime(<String, dynamic>{
        'runtime_propagation': <String, dynamic>{'p': 1},
        'event_chains': <String, dynamic>{'c': 1},
      });
      expect((out['event_propagation'] as Map)['p'], 1);
      expect(out['replayed'], isTrue);
    });

    test('rememberCausalRuntime defaults + save/load roundtrip', () {
      final path = tmpPath('causal_mem.json');
      final saved = saveCausalMemory(
        path,
        <String, dynamic>{
          'event_chains': <String, dynamic>{'x': 1},
          'note': 'r',
        },
        'causal-key',
      );
      expect(saved['saved'], isTrue);
      final loaded = loadCausalMemory(path, 'causal-key');
      expect(loaded['available'], isTrue);
      expect((loaded['memory'] as Map)['note'], 'r');

      final missing = loadCausalMemory(tmpPath('absent.json'), 'k');
      expect(missing['available'], isFalse);
    });

    test('runCausalityForExtraction disabled + persist/merge branches', () {
      expect(runCausalityForExtraction(causalityRuntime: false)['enabled'],
          isFalse);

      final path = tmpPath('causal_orch.json');
      final first = runCausalityForExtraction(
        memoryPath: path,
        memoryKey: 'causal-orch',
        interactions: <dynamic>[
          <String, dynamic>{'action': 'click'}
        ],
        mergeGraph: true,
      );
      expect(first['enabled'], isTrue);
      expect(first['memory_persisted'], isTrue);
      expect((first['unified_graph'] as Map)['ir'], 'unified_runtime_graph');

      final second = runCausalityForExtraction(
        memoryPath: path,
        memoryKey: 'causal-orch',
        interactions: <dynamic>[
          <String, dynamic>{'action': 'click'}
        ],
        mergeGraph: false,
      );
      expect(second['memory_persisted'], isTrue);
      expect((second['unified_graph'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // synchronization/synchronization_engines.dart — orchestrators both branches
  // -------------------------------------------------------------------------
  group('synchronization orchestrator', () {
    test('runSynchronizedRuntime with distributed reality branch', () {
      final out = runSynchronizedRuntime(
        tick: 1,
        browser: <String, dynamic>{
          'dom': <String, dynamic>{'d': 1},
          'runtime': <String, dynamic>{'r': 1}
        },
        native: <String, dynamic>{'n': 1},
        semanticResult: <String, dynamic>{
          'semantic': <String, dynamic>{'s': 1}
        },
        workflowResult: <String, dynamic>{
          'workflow': <String, dynamic>{'w': 1}
        },
        causalityResult: <String, dynamic>{
          'causality': <String, dynamic>{'c': 1}
        },
        distributedResult: <String, dynamic>{
          'workers': <dynamic>[
            <String, dynamic>{'worker_id': 'w0'}
          ]
        },
        session: <String, dynamic>{'sid': 1},
        identity: <String, dynamic>{'uid': 1},
      );
      expect(out['bounded'], isTrue);
      expect(out.containsKey('sync_ir'), isTrue);
      expect(out.containsKey('consistency'), isTrue);
    });

    test('runSynchronizedRuntime no distributed branch', () {
      final out = runSynchronizedRuntime();
      expect(out['bounded'], isTrue);
      expect((out['convergence'] as Map)['converged'], isTrue);
    });

    test('runSyncForExtraction disabled + persist/merge branches', () {
      expect(
          runSyncForExtraction(synchronizedRuntime: false)['enabled'], isFalse);

      final path = tmpPath('sync_mem.json');
      final first = runSyncForExtraction(
        memoryPath: path,
        memoryKey: 'sync-key',
        browser: <String, dynamic>{
          'dom': <String, dynamic>{'a': 1}
        },
        mergeGraph: true,
      );
      expect(first['enabled'], isTrue);
      expect(first['memory_persisted'], isTrue);
      expect((first['unified_graph'] as Map)['ir'], 'unified_runtime_graph');

      final second = runSyncForExtraction(
        memoryPath: path,
        memoryKey: 'sync-key',
        browser: <String, dynamic>{
          'dom': <String, dynamic>{'a': 2}
        },
        mergeGraph: false,
      );
      expect(second['memory_persisted'], isTrue);
      expect((second['unified_graph'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // synchronization individual engines (target both branches)
  // -------------------------------------------------------------------------
  group('synchronization engines branches', () {
    test('buildRuntimeDelta null args + change classification', () {
      final empty = buildRuntimeDelta(null, null);
      expect((empty['changes'] as List).isEmpty, isTrue);

      final delta = buildRuntimeDelta(
        <String, dynamic>{'semantic_x': 1, 'dom_y': 1, 'state_z': 1},
        <String, dynamic>{
          'semantic_x': 2,
          'dom_y': 2,
          'state_z': 2,
          'workflow_w': 9,
          'misc': 1,
        },
        tick: 4,
      );
      final kinds = (delta['changes'] as List)
          .map((dynamic c) => (c as Map)['kind'])
          .toSet();
      expect(kinds.contains('semantic_change'), isTrue);
      expect(kinds.contains('ui_mutation'), isTrue);
      expect(kinds.contains('application_state_mutation'), isTrue);
      expect(kinds.contains('workflow_change'), isTrue);
      expect(kinds.contains('runtime_transition'), isTrue);
      expect(delta['timestamp'], 4);
    });

    test('replicateRuntimeReality worker id fallbacks', () {
      final out = replicateRuntimeReality(
        <String, dynamic>{'reality_id': 'R'},
        <dynamic>[
          <String, dynamic>{'worker_id': 'w0'},
          <String, dynamic>{'id': 'w1'},
          <String, dynamic>{}, // → worker:2
        ],
      );
      expect(out['replica_count'], 3);
      expect((out['replicas'] as List)[2]['worker_id'], 'worker:2');
    });

    test('alignRuntimeLayers truthy/falsey', () {
      final t = alignRuntimeLayers(
        <String, dynamic>{'a': 1},
        null,
        <String, dynamic>{},
        <String, dynamic>{'b': 1},
      );
      expect(t['browser'], isTrue);
      expect(t['native'], isFalse);
      expect(t['semantic'], isFalse); // empty map falsey
      expect(t['workflow'], isTrue);
    });

    test('convergeRuntimeState merges + conflict override', () {
      final out = convergeRuntimeState(<Map<String, dynamic>>[
        <String, dynamic>{'reality_id': 'b', 'shared': 1, 'only_b': 9},
        <String, dynamic>{'reality_id': 'a', 'shared': 2}, // conflict override
      ]);
      expect(out['reality_count'], 2);
      // sorted by reality_id: a first sets shared=2; b sets only_b and
      // conflicts shared (override to 1).
      expect((out['converged_state'] as Map).containsKey('only_b'), isTrue);
      expect(out['histories'], <String>['a', 'b']);
    });

    test('diffRuntimeState buckets', () {
      final out = diffRuntimeState(
        <String, dynamic>{
          'semantic_a': 1,
          'workflow_b': 1,
          'worker_c': 1,
          'plain': 1,
        },
        <String, dynamic>{
          'semantic_a': 2,
          'workflow_b': 2,
          'worker_c': 2,
          'plain': 2,
        },
      );
      expect((out['semantic_mutations'] as List).length, 1);
      expect((out['workflow_mutations'] as List).length, 1);
      expect((out['distributed_changes'] as List).length, 1);
      expect((out['runtime_changes'] as List).length, 1);
    });

    test('detectRuntimeDrift none vs some', () {
      final none = detectRuntimeDrift(
        <String, dynamic>{'selectors': 1},
        <String, dynamic>{'selectors': 1},
      );
      expect(none['diverged'], isFalse);
      final some = detectRuntimeDrift(
        <String, dynamic>{'selectors': 1, 'semantic': 1},
        <String, dynamic>{'selectors': 2, 'semantic': 2},
      );
      expect(some['drift_count'], 2);
      expect(some['diverged'], isTrue);
    });

    test('federateRuntimeRealities populated + empty', () {
      final out = federateRuntimeRealities(
        workers: <dynamic>[
          <String, dynamic>{'worker_id': 'w0'},
          <String, dynamic>{}, // → w:1
        ],
        browser: <String, dynamic>{'b': 1},
        native: <String, dynamic>{},
      );
      expect((out['workers'] as List).length, 2);
      expect((out['workers'] as List)[1]['worker_id'], 'w:1');
      expect(out['browser_runtime'], isTrue);
      expect(out['native_runtime'], isFalse);
      final empty = federateRuntimeRealities();
      expect((empty['workers'] as List).isEmpty, isTrue);
    });

    test('buildRuntimeHistory with semantic_change mutations', () {
      final out = buildRuntimeHistory(
        <Map<String, dynamic>>[
          <String, dynamic>{
            'timestamp': 2,
            'changes': <dynamic>[
              <String, dynamic>{'kind': 'semantic_change'},
              <String, dynamic>{'kind': 'ui_mutation'},
            ],
          },
          <String, dynamic>{'timestamp': 1, 'changes': <dynamic>[]},
        ],
        transitions: <dynamic>['t'],
        workflows: <dynamic>['w'],
      );
      expect(out['length'], 2);
      expect((out['semantic_evolution'] as List).length, 1);
      expect((out['mutations'] as List).length, 2);
      // sorted by timestamp ascending
      expect((out['deltas'] as List)[0]['timestamp'], 1);
    });

    test('mergeRuntimeRealities accumulates', () {
      final out = mergeRuntimeRealities(<Map<String, dynamic>>[
        <String, dynamic>{
          'reality_id': 'r1',
          'tick': 2,
          'semantic': <String, dynamic>{'s': 1},
          'workflow': <String, dynamic>{'w': 1},
          'application': <String, dynamic>{'a': 1},
        },
        <String, dynamic>{'reality_id': 'r2', 'tick': 1},
      ]);
      expect(out['reality_count'], 2);
      expect((out['semantic'] as Map)['s'], 1);
      expect((out['timelines'] as List)[0]['tick'], 1); // sorted
    });

    test('trackRuntimeMutations sorts incl. non-map entries', () {
      final out = trackRuntimeMutations(
        <dynamic>[
          <String, dynamic>{'field': 'z'},
          <String, dynamic>{'field': 'a'},
          'not-a-map',
        ],
        tick: 3,
      );
      expect(out['count'], 3);
      expect(out['tick'], 3);
    });

    test('captureRuntimeSnapshot null + populated', () {
      final out = captureRuntimeSnapshot(tick: 9);
      expect(out['snapshot_id'], 'snapshot:9');
      expect((out['browser_runtime'] as Map).isEmpty, isTrue);
    });

    test('buildRuntimeStateGraph with and without changes', () {
      final withChanges = buildRuntimeStateGraph(
        <String, dynamic>{'snapshot_id': 'snap:1'},
        <String, dynamic>{
          'delta_id': 'd1',
          'changes': <dynamic>[
            <String, dynamic>{'field': 'f1'},
            'not-a-map',
          ],
        },
        <String, dynamic>{'converged': true},
      );
      final relsWith = (withChanges['edges'] as List)
          .map((dynamic e) => (e as Map)['relation'])
          .toSet();
      expect(relsWith.contains('synchronizes'), isTrue);

      final noChanges = buildRuntimeStateGraph(
        <String, dynamic>{},
        <String, dynamic>{},
        <String, dynamic>{},
      );
      final relsNo = (noChanges['edges'] as List)
          .map((dynamic e) => (e as Map)['relation'])
          .toSet();
      expect(relsNo.contains('synchronizes'), isFalse);
    });

    test('synchronizeRuntime synced/empty payloads', () {
      final out = synchronizeRuntime(<Map<String, dynamic>>[
        <String, dynamic>{
          'browser_runtime': <String, dynamic>{'b': 1},
          'native_runtime': <String, dynamic>{'n': 1},
          'terminal_runtime': <String, dynamic>{'t': 1},
          'vm_runtime': <String, dynamic>{'v': 1},
          'remote_runtime': <String, dynamic>{'r': 1},
        },
      ], tick: 2);
      expect((out['synchronized'] as List).length, 5);
      expect(out['count'], greaterThan(0));

      // scalar value branch (wraps under 'data')
      final scalar = synchronizeRuntime(<Map<String, dynamic>>[
        <String, dynamic>{'browser_runtime': 'scalar'},
      ]);
      expect((scalar['synchronized'] as List)[0]['runtime'], 'browser');
    });

    test('verifyRuntimeConsistency consistent vs issues', () {
      final ok = verifyRuntimeConsistency(
        <String, dynamic>{
          'deltas': <dynamic>[
            <String, dynamic>{'timestamp': 1},
            <String, dynamic>{'timestamp': 2},
          ],
          'semantic_evolution': <dynamic>[],
        },
        <String, dynamic>{'converged': true},
        <String, dynamic>{'replayed': true},
      );
      expect(ok['consistent'], isTrue);

      final bad = verifyRuntimeConsistency(
        <String, dynamic>{
          'deltas': <dynamic>[
            <String, dynamic>{'timestamp': 5},
            <String, dynamic>{'timestamp': 1}, // out of order
          ],
        },
        <String, dynamic>{'converged': false},
        <String, dynamic>{'replayed': false},
      );
      expect(bad['consistent'], isFalse);
      expect(
          (bad['issues'] as List).contains('convergence_incomplete'), isTrue);
      expect((bad['issues'] as List).contains('replay_not_ready'), isTrue);
      expect(
          (bad['issues'] as List).contains('timeline_order_violation'), isTrue);
    });

    test('buildSyncTimeline sorts entries', () {
      final out = buildSyncTimeline(<String, dynamic>{
        'deltas': <dynamic>[
          <String, dynamic>{
            'timestamp': 2,
            'delta_id': 'd2',
            'changes': <dynamic>[]
          },
          <String, dynamic>{
            'timestamp': 1,
            'delta_id': 'd1',
            'changes': <dynamic>[1]
          },
        ],
      });
      expect((out['timeline'] as List)[0]['tick'], 1);
    });

    test('compile + irToGraph + mergeRuntimeIrGraph', () {
      final ir = compileSynchronizationRuntimeIr(<String, dynamic>{});
      expect(ir['ir'], 'synchronization_runtime');

      final graphEmpty = synchronizationRuntimeIrToGraph(<String, dynamic>{});
      expect((graphEmpty['nodes'] as List)[0]['id'], 'sync:root');

      final graphWithNodes = synchronizationRuntimeIrToGraph(<String, dynamic>{
        'state_graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'z'},
            <String, dynamic>{'id': 'a'},
          ],
          'edges': <dynamic>[],
        },
      });
      expect((graphWithNodes['nodes'] as List).first['id'], 'a');

      final merged = mergeRuntimeIrGraph(<dynamic>[
        <String, dynamic>{
          'ir': 'g',
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': '  '},
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': 'a', 'to': 'b'},
            <String, dynamic>{'from': '', 'to': 'b'},
          ],
        },
      ]);
      expect((merged['nodes'] as List).length, 1);
      expect((merged['edges'] as List).length, 1);
      expect((merged['edges'] as List)[0]['runtime_type'], 'g');
    });

    test('rememberSyncRuntime + emptySyncMemory', () {
      final m = emptySyncMemory();
      expect(m.containsKey('deltas'), isTrue);

      final merged = rememberSyncRuntime(
        <String, dynamic>{'existing': 1},
        <String, dynamic>{
          'deltas': <dynamic>['d'],
          'extra': true
        },
      );
      expect(merged['deltas'], <dynamic>['d']);
      expect(merged['history'], <String, dynamic>{}); // setdefault empty
      expect(merged['bounded'], isTrue);
    });

    test('replaySynchronizedRuntime maps fields', () {
      final out = replaySynchronizedRuntime(<String, dynamic>{
        'history': <String, dynamic>{'h': 1},
        'deltas': <dynamic>[1],
      });
      expect((out['synchronized_histories'] as Map)['h'], 1);
      expect(out['replayed'], isTrue);
    });

    test('maintainRuntimeContinuity defaults', () {
      final out = maintainRuntimeContinuity();
      expect(out['continuous'], isTrue);
      expect((out['authenticated_session'] as Map).isEmpty, isTrue);
    });
  });

  // -------------------------------------------------------------------------
  // synchronization/runtime_sync_memory.dart
  // -------------------------------------------------------------------------
  group('sync memory engine', () {
    test('pythonJsonDumpsSorted value kinds + normalizeForEncryption', () {
      final s = pythonJsonDumpsSorted(<String, dynamic>{
        'b': <dynamic>[1, 2.0, 2.5, true, false, null, 'str'],
        'a': <String, dynamic>{'k': 1},
      });
      expect(s.contains('"a": '), isTrue);
      expect(s.contains('2.0'), isTrue);
      expect(s.contains('2.5'), isTrue);
      expect(s.contains('true'), isTrue);
      expect(s.contains('null'), isTrue);

      final norm = normalizeForEncryption('hello');
      expect(norm, isA<String>());
    });

    test('save → load roundtrip and missing-file branch', () {
      final path = tmpPath('sync_direct_mem.json');
      final saved = saveSyncMemory(
        path,
        <String, dynamic>{
          'deltas': <dynamic>[1, 2],
          'note': 'roundtrip',
        },
        'sync-direct-key',
      );
      expect(saved['saved'], isTrue);
      expect(File(path).existsSync(), isTrue);

      final loaded = loadSyncMemory(path, 'sync-direct-key');
      expect(loaded['available'], isTrue);
      expect((loaded['memory'] as Map)['note'], 'roundtrip');

      final missing = loadSyncMemory(tmpPath('absent_sync.json'), 'k');
      expect(missing['available'], isFalse);
      expect((missing['memory'] as Map).containsKey('deltas'), isTrue);
    });
  });
}
