// Wave-2 branch coverage tests for four internal engines.
//
// Imports the internal `src/` files directly to drive otherwise-uncovered
// branches (empty vs populated inputs, `?? default` arms, fallback type
// coercions, sort tiebreaks). Assertions are structural only.
import 'package:test/test.dart';

import 'package:webweavex/src/persistence/fingerprint_hex.dart';
import 'package:webweavex/src/connectors_runtime/stream_replay.dart';
import 'package:webweavex/src/kernel_runtime/kernel_scaffolding.dart';
import 'package:webweavex/src/semantic/semantic_engines.dart';

void main() {
  group('fingerprint_hex', () {
    test('dumpsDeterministic coerces NaN/Infinity floats to 0', () {
      final out = dumpsDeterministic(<String, dynamic>{
        'nan': double.nan,
        'inf': double.infinity,
        'ninf': double.negativeInfinity,
      });
      // Non-finite doubles collapse to integer 0 in compact JSON
      // (cross-language contract: matches Python and JavaScript).
      expect(out, equals('{"inf":0,"nan":0,"ninf":0}'));
    });

    test('dumpsDeterministic formats a finite non-integral float (line 81)',
        () {
      final out = dumpsDeterministic(<String, dynamic>{'pi': 3.14159});
      expect(out, equals('{"pi":3.14159}'));
    });

    test('_format15g strips trailing zeros on fractional value (123-130)', () {
      // A value whose .15g representation has trailing zeros to strip.
      final out = dumpsDeterministic(<String, dynamic>{'v': 0.5});
      expect(out, equals('{"v":0.5}'));
    });

    test('integral-valued double canonicalizes to int', () {
      // Cross-language contract: JavaScript cannot distinguish 2.0 from 2,
      // so integral doubles serialize as integers in every language.
      final out = dumpsDeterministic(<String, dynamic>{'v': 2.0});
      expect(out, equals('{"v":2}'));
    });

    test('_format15g large/precise float keeps decimal form (127-130)', () {
      final out = dumpsDeterministic(<String, dynamic>{'v': 1.0 / 3.0});
      expect(out.startsWith('{"v":0.3333'), isTrue);
      expect(out.contains('.'), isTrue);
    });

    test('_stable falls back to toString for unknown types (line 100)', () {
      // A Duration is none of String/bool/null/int/double/Map/List, so it
      // hits the terminal `_normStr(value.toString())` fallback.
      final out = dumpsDeterministic(<String, dynamic>{
        'd': const Duration(seconds: 1),
      });
      expect(out, contains('"d":'));
      expect(out, contains('0:00:01.000000'));
    });

    test('string and bytes payloads pass through hexFingerprint', () {
      final fromStr = hexFingerprint('hello');
      final fromBytes = hexFingerprint(<int>[104, 101, 108, 108, 111]);
      expect(fromStr, equals(fromBytes));
      expect(fromStr.length, equals(10)); // 5 bytes -> 10 hex chars
    });
  });

  group('stream_replay', () {
    test('buildStreamTimeline coerces num timestamp via _asInt (line 9)', () {
      final out = buildStreamTimeline(<Map<String, dynamic>>[
        <String, dynamic>{'id': 'a', 'timestamp': 2.0},
        <String, dynamic>{'id': 'b', 'timestamp': 1.0},
      ]);
      final events = out['events'] as List<dynamic>;
      expect((events.first as Map<String, dynamic>)['id'], equals('b'));
      expect(out['bounded'], isTrue);
    });

    test('buildStreamTimeline coerces string timestamp via _asInt (line 10)',
        () {
      final out = buildStreamTimeline(<Map<String, dynamic>>[
        <String, dynamic>{'id': 'a', 'timestamp': '5'},
        <String, dynamic>{'id': 'b', 'timestamp': 'not-a-number'},
        <String, dynamic>{'id': 'c', 'timestamp': '1'},
      ]);
      final events = out['events'] as List<dynamic>;
      // 'not-a-number' -> 0, '1' -> 1, '5' -> 5
      expect((events[0] as Map<String, dynamic>)['id'], equals('b'));
      expect((events[1] as Map<String, dynamic>)['id'], equals('c'));
      expect((events[2] as Map<String, dynamic>)['id'], equals('a'));
    });

    test('buildStreamTimeline uses source tiebreak (lines 64-66)', () {
      // Same timestamp, same id -> falls through to the `source` comparison.
      final out = buildStreamTimeline(<Map<String, dynamic>>[
        <String, dynamic>{'id': 'x', 'timestamp': 1, 'source': 'zeta'},
        <String, dynamic>{'id': 'x', 'timestamp': 1, 'source': 'alpha'},
      ]);
      final events = out['events'] as List<dynamic>;
      expect((events.first as Map<String, dynamic>)['source'], equals('alpha'));
    });

    test('buildStreamTimeline index tiebreak when all keys equal (line 66)',
        () {
      // Identical id/timestamp/source -> final tiebreak returns index compare.
      final out = buildStreamTimeline(<Map<String, dynamic>>[
        <String, dynamic>{'id': 'x', 'timestamp': 1, 'source': 's', 'n': 0},
        <String, dynamic>{'id': 'x', 'timestamp': 1, 'source': 's', 'n': 1},
      ]);
      final events = out['events'] as List<dynamic>;
      expect((events[0] as Map<String, dynamic>)['n'], equals(0));
      expect((events[1] as Map<String, dynamic>)['n'], equals(1));
    });

    test('replayStreamEvents bounds the replay list', () {
      final out = replayStreamEvents(
        null,
        <Map<String, dynamic>>[
          <String, dynamic>{'e': 1},
          <String, dynamic>{'e': 2},
        ],
      );
      expect((out['replay'] as List<dynamic>).length, equals(2));
      expect(out['bounded'], isTrue);
    });
  });

  group('kernel_scaffolding', () {
    test('registerRuntimePhase fresh registry uses empty-map arm (line 60)',
        () {
      // No 'phases' key -> priorRaw is null -> falls to <String,dynamic>{}.
      final out = registerRuntimePhase(
        <String, dynamic>{},
        'browser',
        <String, dynamic>{'ok': true},
      );
      expect((out['registered'] as List<dynamic>), equals(<String>['browser']));
      final phases = out['phases'] as Map<String, dynamic>;
      expect(phases.containsKey('browser'), isTrue);
    });

    test('registerRuntimePhase reuses existing Map phases', () {
      final out = registerRuntimePhase(
        <String, dynamic>{
          'phases': <String, dynamic>{'semantic': <String, dynamic>{}},
        },
        'browser',
        <String, dynamic>{'ok': true},
      );
      expect(
        (out['registered'] as List<dynamic>),
        equals(<String>['browser', 'semantic']),
      );
    });

    test('publishRuntimeEvent order tiebreak with equal tick+order (line 94)',
        () {
      // Seed the bus with two events sharing tick AND order so the sort must
      // fall through to the index tiebreak (line 94).
      final out = publishRuntimeEvent(
        <Map<String, dynamic>>[
          <String, dynamic>{
            'type': 'a',
            'tick': 0,
            'payload': <String, dynamic>{},
            'order': 0,
          },
          <String, dynamic>{
            'type': 'b',
            'tick': 0,
            'payload': <String, dynamic>{},
            'order': 0,
          },
        ],
        'c',
        <String, dynamic>{},
        tick: 0,
      );
      final bus = out['bus'] as List<dynamic>;
      expect(bus.length, equals(3));
      expect(out['size'], equals(3));
    });

    test('buildKernelTopology with no argument uses empty-graph default (102)',
        () {
      final out = buildKernelTopology();
      expect((out['nodes'] as List<dynamic>), isEmpty);
      expect(out['node_count'], equals(0));
    });

    test('buildKernelTopology edge relation tiebreak (lines 123-124)', () {
      // Two edges identical on from/to so the sort must compare `relation`.
      final out = buildKernelTopology(<String, dynamic>{
        'nodes': <dynamic>[
          <String, dynamic>{'id': 'n1'},
          <String, dynamic>{'id': 'n1'},
        ],
        'edges': <dynamic>[
          <String, dynamic>{'from': 'a', 'to': 'b', 'relation': 'zeta'},
          <String, dynamic>{'from': 'a', 'to': 'b', 'relation': 'alpha'},
        ],
      });
      final edges = out['edges'] as List<dynamic>;
      expect(
          (edges.first as Map<String, dynamic>)['relation'], equals('alpha'));
    });

    test('replayKernelState order tiebreak with equal tick+order (line 165)',
        () {
      final out = replayKernelState(<Map<String, dynamic>>[
        <String, dynamic>{'tick': 1, 'order': 0, 'name': 'first'},
        <String, dynamic>{'tick': 1, 'order': 0, 'name': 'second'},
      ]);
      final events = out['events'] as List<dynamic>;
      expect((events[0] as Map<String, dynamic>)['name'], equals('first'));
      expect((events[1] as Map<String, dynamic>)['name'], equals('second'));
    });

    test('enforceRuntimeBoundary encodes mixed types (289-355)', () {
      // Drives every arm of the Python-JSON encoder:
      //  null, bool, int, finite-integral double, fractional double, string
      //  with all escapes + a control char + a non-JSON object (default=str).
      final out = enforceRuntimeBoundary(<String, dynamic>{
        'n': null,
        'b': true,
        'i': 7,
        'fInt': 4.0,
        'fFrac': 2.5,
        's': 'quote" back\\ \b \f \n \r \t  end',
        'obj': const Duration(seconds: 2),
        'list': <dynamic>[1, 'x', false],
        'nested': <String, dynamic>{'z': 1, 'a': 2},
        'irs': <dynamic>[
          <String, dynamic>{'ir': 1},
        ],
      });
      expect(out['within_size'], isTrue);
      expect(out['within_ir_count'], isTrue);
      expect(out['ir_count'], equals(1));
      expect((out['size'] as int) > 0, isTrue);
    });

    test('scheduleKernelPhases / coordinate / lifecycle smoke', () {
      final sch = scheduleKernelPhases(<String>['a', 'b'], tick: 2);
      expect((sch['scheduled'] as List<dynamic>).length, equals(2));
      final coord = coordinateKernelPhases(<Map<String, dynamic>>[
        <String, dynamic>{'phase': 'b'},
        <String, dynamic>{'phase': 'a'},
      ]);
      expect((coord['phases'] as List<dynamic>).length, equals(2));
      expect(listRuntimePhases().length, equals(9));
      final init = initializeRuntime();
      expect(init['initialized'], isTrue);
      expect(shutdownRuntime(<String, dynamic>{'tick': 5})['final_tick'],
          equals(5));
      final st = buildKernelState(<String, dynamic>{'tick': 3});
      final merged = mergeKernelState(
        st,
        <String, dynamic>{
          'irs': <dynamic>[
            <String, dynamic>{'x': 1},
          ],
        },
      );
      expect(merged['irs'], isA<List<dynamic>>());
      final pol = buildKernelPolicy();
      expect(enforceKernelPolicy(pol, 1, 1)['allowed'], isTrue);
    });
  });

  group('semantic_engines', () {
    test('_compareKeys equal-length tuples hit length compare (line 18)', () {
      // Two identical edges force the edge sort comparator to exhaust the
      // tuple and return the length comparison (line 18).
      final out = buildSemanticGraph(
        <dynamic>[
          <String, dynamic>{'id': 'e1', 'type': 'service', 'label': 'svc'},
          <String, dynamic>{'id': 'e2', 'type': 'service', 'label': 'svc'},
        ],
        <dynamic>[
          <String, dynamic>{'from': 'e1', 'to': 'e2', 'relation': 'r'},
          <String, dynamic>{'from': 'e1', 'to': 'e2', 'relation': 'r'},
        ],
      );
      expect((out['nodes'] as List<dynamic>).length, equals(2));
      expect(out['bounded'], isTrue);
    });

    test('extractSemanticEntities default structure arm (line 43)', () {
      // Called with no structure -> `structure ?? {}` default executes.
      final out = extractSemanticEntities('user login api endpoint');
      expect((out['entities'] as List<dynamic>).isNotEmpty, isTrue);
      expect(out['ontology'], isA<Map<String, dynamic>>());
    });

    test('extractSemanticEntities with actions and artifacts', () {
      final out = extractSemanticEntities(
        'service queue',
        <String, dynamic>{
          'actions': <dynamic>[
            <String, dynamic>{'label': 'Save'},
            <String, dynamic>{'type': 'click'},
          ],
          'artifacts': <dynamic>['art1'],
        },
      );
      final entities = out['entities'] as List<dynamic>;
      expect(entities.any((e) => (e as Map)['type'] == 'ui_action'), isTrue);
      expect(entities.any((e) => (e as Map)['type'] == 'runtime_artifact'),
          isTrue);
    });

    test('resolveSemanticEntities empty canonical-id arm (line 121)', () {
      // First entity per label sets the canonical id (canonical[label] null).
      final out = resolveSemanticEntities(<dynamic>[
        <String, dynamic>{'id': 'e1', 'label': 'Alpha'},
        <String, dynamic>{'id': 'e2', 'label': 'Alpha'},
        <String, dynamic>{'id': 'e3', 'label': 'Beta'},
      ]);
      final canonical = out['canonical_map'] as Map<String, dynamic>;
      expect(canonical['alpha'], equals('e1'));
      expect(canonical['beta'], equals('e3'));
    });

    test('extractUiSemantics empty HTML; non-empty throws (line 269)', () {
      final ok = extractUiSemantics('   ', <dynamic>['a']);
      expect(ok['forms'], equals(0));
      expect(() => extractUiSemantics('<div/>'), throwsUnsupportedError);
    });

    test('extractTableSemantics empty HTML; non-empty throws (line 297)', () {
      final ok = extractTableSemantics('');
      expect(ok['primary_kind'], equals('none'));
      expect(() => extractTableSemantics('<table/>'), throwsUnsupportedError);
    });

    test('extractDocumentSemantics default + matched kinds', () {
      final none = extractDocumentSemantics('plain words');
      expect(none['kinds'], equals(<String>['document']));
      final matched = extractDocumentSemantics('this agreement and invoice');
      expect((matched['kinds'] as List<dynamic>).isNotEmpty, isTrue);
    });

    test('extractRepositorySemantics docs purpose (line 388)', () {
      final out = extractRepositorySemantics(
        <String>['docs/readme.md'],
        'api routes controller',
      );
      expect(out['repository_purpose'], equals('documentation'));
      expect(out['api_ownership'], isTrue);
    });

    test('extractRepositorySemantics infra purpose (line 392)', () {
      final out = extractRepositorySemantics(
        <String>['infra/terraform.tf'],
        'docker k8s terraform service worker react django',
      );
      expect(out['repository_purpose'], equals('infrastructure'));
      expect(out['deployment_topology'], isTrue);
      expect((out['framework_semantics'] as List<dynamic>).isNotEmpty, isTrue);
      expect((out['service_boundaries'] as List<dynamic>).isNotEmpty, isTrue);
    });

    test('extractApplicationSemantics populated (lines 450-451)', () {
      final out = extractApplicationSemantics(<String, dynamic>{
        'intent': <String, dynamic>{'intent': 'checkout'},
        'execution': <String, dynamic>{
          'objective': 'pay',
          'executed': <dynamic>[
            <String, dynamic>{'action': 'click'},
            <String, dynamic>{'action': 'submit'},
          ],
        },
        'forms': <String, dynamic>{
          'forms': <dynamic>[
            <String, dynamic>{'f': 1},
          ],
        },
        'workflow': <String, dynamic>{
          'edges': <dynamic>[
            <String, dynamic>{'e': 1},
          ],
        },
        'ui_semantics': <String, dynamic>{'forms': 1},
      });
      expect(out['workflow_purpose'], equals('checkout'));
      expect((out['business_operations'] as List<dynamic>).length, equals(2));
      expect(out['form_operations'], equals(1));
      expect(out['operational_actions'], equals(1));
    });

    test('extractApplicationSemantics default arm', () {
      final out = extractApplicationSemantics(null);
      expect(out['workflow_purpose'], equals('operate'));
    });

    test('extractCausalitySemantics with handoffs (lines 477-479)', () {
      final out = extractCausalitySemantics(<String, dynamic>{
        'causality': <String, dynamic>{
          'propagation': <String, dynamic>{
            'handoffs': <dynamic>[
              <String, dynamic>{'from': 'a', 'to': 'b'},
              <String, dynamic>{'from': 'b', 'to': 'c'},
            ],
          },
          'alignment': <String, dynamic>{'runtime_count': 3},
        },
      });
      expect(out['operational_impact'], equals(2));
      expect(out['runtime_significance'], equals(3));
      expect((out['critical_event_chains'] as List<dynamic>).length, equals(2));
    });

    test('extractWorkflowSemantics + browser + runtime defaults (line 542)',
        () {
      final wf = extractWorkflowSemantics(null, '');
      expect(wf['semantic_intent'], equals('operational_flow'));
      final wf2 = extractWorkflowSemantics(
        <String, dynamic>{
          'nodes': <dynamic>[<String, dynamic>{}],
          'edges': <dynamic>[<String, dynamic>{}],
        },
        'goal',
      );
      expect(wf2['workflow_steps'], equals(1));
      final br = extractBrowserSemantics('https://x', '');
      expect(br['page_role'], equals('web_application'));
      // runtimeGraph + sources both null -> defaults (line 542 etc).
      final rt = extractRuntimeSemantics(null, null);
      expect(rt['node_count'], equals(0));
      expect(rt['runtime_layers'], isEmpty);
    });

    test('alignSemanticRuntimes all-null default arms (568-573)', () {
      final out = alignSemanticRuntimes();
      final layers = out['layers'] as Map<String, dynamic>;
      expect(layers.length, equals(6));
      expect((out['aligned_domains'] as List<dynamic>), isEmpty);
    });

    test('alignSemanticRuntimes with populated layers', () {
      final out = alignSemanticRuntimes(
        browser: <String, dynamic>{'domain': 'saas'},
        document: <String, dynamic>{'primary_kind': 'invoice'},
      );
      final aligned = out['aligned_domains'] as List<dynamic>;
      expect(aligned.length, equals(2));
    });

    test('diffSemanticRuntime structural diff', () {
      final out = diffSemanticRuntime(
        <String, dynamic>{
          'entities': <String, dynamic>{
            'entities': <dynamic>[
              <String, dynamic>{'id': 'a'},
            ],
          },
          'domain': <String, dynamic>{'domain': 'saas'},
          'ontology': <String, dynamic>{'x': 1},
        },
        <String, dynamic>{
          'entities': <String, dynamic>{
            'entities': <dynamic>[
              <String, dynamic>{'id': 'b'},
            ],
          },
          'domain': <String, dynamic>{'domain': 'finance'},
          'ontology': <String, dynamic>{'x': 2},
        },
      );
      expect(out['entities_added'], equals(<String>['b']));
      expect(out['entities_removed'], equals(<String>['a']));
      expect(out['domain_changed'], isTrue);
      expect(out['ontology_evolved'], isTrue);
    });

    test('buildSemanticOntology + compile + classifyDomain', () {
      final onto = buildSemanticOntology(
        <dynamic>[
          <String, dynamic>{'type': 'service'},
        ],
        'saas',
      );
      expect(onto['primary_domain'], equals('saas'));
      final ir = compileSemanticRuntimeIr(<String, dynamic>{});
      expect(ir['ir'], equals('semantic_runtime'));
      final dom = classifySemanticDomain('invoice billing revenue ledger');
      expect(dom['domain'], equals('finance'));
      final empty = classifySemanticDomain('zzz nothing matches here');
      expect(empty['domain'], equals('saas'));
    });

    test('semanticRuntimeIrToGraph adds domain node (lines 777-778)', () {
      final out = semanticRuntimeIrToGraph(<String, dynamic>{
        'semantic_graph': <String, dynamic>{
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n1', 'type': 'entity'},
          ],
          'edges': <dynamic>[],
        },
        'ontology': <String, dynamic>{'primary_domain': 'saas'},
      });
      final nodes = out['nodes'] as List<dynamic>;
      expect(nodes.any((n) => (n as Map)['id'] == 'domain:saas'), isTrue);
    });

    test('semanticRuntimeIrToGraph empty -> root node', () {
      final out = semanticRuntimeIrToGraph(<String, dynamic>{});
      final nodes = out['nodes'] as List<dynamic>;
      expect((nodes.first as Map)['id'], equals('semantic:root'));
    });

    test('mergeRuntimeIrsToGraph populated nodes+edges (830-857)', () {
      final out = mergeRuntimeIrsToGraph(<dynamic>[
        <String, dynamic>{
          'ir': 'browser',
          'nodes': <dynamic>[
            <String, dynamic>{'id': 'n1'},
            <String, dynamic>{'id': ''}, // empty id -> skipped (line 819)
            <String, dynamic>{'id': 'n1'}, // duplicate -> skipped
            <String, dynamic>{'id': 'n2'},
          ],
          'edges': <dynamic>[
            <String, dynamic>{'from': 'n1', 'to': 'n2', 'relation': 'r'},
            <String, dynamic>{'from': '', 'to': 'n2'}, // empty src -> skipped
            <String, dynamic>{'from': 'n1', 'to': 'n2', 'relation': 'r'}, // dup
            <String, dynamic>{'from': 'n2', 'to': 'n1'},
          ],
        },
      ]);
      final nodes = out['nodes'] as List<dynamic>;
      final edges = out['edges'] as List<dynamic>;
      expect(nodes.length, equals(2));
      expect(edges.length, equals(2));
      expect(out['ir'], equals('unified_runtime_graph'));
    });
  });
}
