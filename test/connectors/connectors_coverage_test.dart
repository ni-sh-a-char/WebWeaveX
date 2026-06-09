import 'dart:io';

import 'package:test/test.dart';
import 'package:webweavex/webweavex.dart';

void main() {
  group('extractPostgresRuntime', () {
    test('default branch (no snapshot)', () {
      final r = extractPostgresRuntime();
      expect(r['database_type'], 'postgresql');
      expect(r['schemas'], <String>['public']);
      expect(r['tables'], <String>[]);
      expect(r['indexes'], <dynamic>[]);
      expect(r['metrics'], <String, dynamic>{});
      expect(r['active_connections'], 0);
      expect(r['replication_state'], 'unknown');
      expect(r['degraded'], false);
      expect(r['bounded'], true);
    });

    test('populated snapshot covers sort + override branches', () {
      final r = extractPostgresRuntime(<String, dynamic>{
        'schemas': <dynamic>['public', 'analytics'],
        'tables': <dynamic>['zebra', 'alpha', 'mid'],
        'indexes': <dynamic>['idx_a'],
        'metrics': <String, dynamic>{'qps': 10},
        'active_connections': 42,
        'replication_state': 'streaming',
        'degraded': true,
      });
      expect(r['database_type'], 'postgresql');
      expect(r['schemas'], <String>['public', 'analytics']);
      expect(r['tables'], <String>['alpha', 'mid', 'zebra']);
      expect(r['indexes'], <dynamic>['idx_a']);
      expect(r['metrics'], <String, dynamic>{'qps': 10});
      expect(r['active_connections'], 42);
      expect(r['replication_state'], 'streaming');
      expect(r['degraded'], true);
      expect(r['bounded'], true);
    });
  });

  group('extractMysqlRuntime', () {
    test('default branch', () {
      final r = extractMysqlRuntime();
      expect(r['database_type'], 'mysql');
      expect(r['schemas'], <dynamic>[]);
      expect(r['tables'], <String>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot', () {
      final r = extractMysqlRuntime(<String, dynamic>{
        'schemas': <dynamic>['app'],
        'tables': <dynamic>['users', 'accounts'],
      });
      expect(r['schemas'], <dynamic>['app']);
      expect(r['tables'], <String>['accounts', 'users']);
    });
  });

  group('extractSqliteRuntime', () {
    test('default branch', () {
      final r = extractSqliteRuntime();
      expect(r['database_type'], 'sqlite');
      expect(r['schemas'], <String>['main']);
      expect(r['tables'], <String>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot', () {
      final r = extractSqliteRuntime(<String, dynamic>{
        'tables': <dynamic>['t2', 't1'],
      });
      expect(r['tables'], <String>['t1', 't2']);
    });
  });

  group('extractRedisRuntime', () {
    test('default branch', () {
      final r = extractRedisRuntime();
      expect(r['database_type'], 'redis');
      expect(r['tables'], <dynamic>[]);
      expect(r['replication_state'], 'master');
      expect(r['bounded'], true);
    });

    test('populated snapshot with role + keys', () {
      final r = extractRedisRuntime(<String, dynamic>{
        'keys': <dynamic>['k1', 'k2'],
        'role': 'replica',
      });
      expect(r['tables'], <dynamic>['k1', 'k2']);
      expect(r['replication_state'], 'replica');
    });
  });

  group('extractKafkaRuntime', () {
    test('default branch', () {
      final r = extractKafkaRuntime();
      expect(r['broker_type'], 'kafka');
      expect(r['topics'], <String>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot sorts topics', () {
      final r = extractKafkaRuntime(<String, dynamic>{
        'topics': <dynamic>['orders', 'events'],
      });
      expect(r['topics'], <String>['events', 'orders']);
    });
  });

  group('extractGraphqlRuntime', () {
    test('default branch', () {
      final r = extractGraphqlRuntime();
      expect(r['protocol'], 'graphql');
      expect(r['endpoints'], <String>['/graphql']);
      expect(r['bounded'], true);
    });

    test('populated snapshot', () {
      final r = extractGraphqlRuntime(<String, dynamic>{
        'endpoints': <dynamic>['/api/graphql'],
      });
      expect(r['endpoints'], <dynamic>['/api/graphql']);
    });
  });

  group('extractGrpcRuntime', () {
    test('default branch', () {
      final r = extractGrpcRuntime();
      expect(r['protocol'], 'grpc');
      expect(r['services'], <String>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot sorts services', () {
      final r = extractGrpcRuntime(<String, dynamic>{
        'services': <dynamic>['SvcB', 'SvcA'],
      });
      expect(r['services'], <String>['SvcA', 'SvcB']);
    });
  });

  group('extractWebsocketRuntime', () {
    test('default branch', () {
      final r = extractWebsocketRuntime();
      expect(r['protocol'], 'websocket');
      expect(r['connections'], <dynamic>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot', () {
      final r = extractWebsocketRuntime(<String, dynamic>{
        'connections': <dynamic>['c1'],
      });
      expect(r['connections'], <dynamic>['c1']);
    });
  });

  group('extractDockerRuntime', () {
    test('default branch', () {
      final r = extractDockerRuntime();
      expect(r['runtime'], 'docker');
      expect(r['containers'], <dynamic>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot', () {
      final r = extractDockerRuntime(<String, dynamic>{
        'containers': <dynamic>['web', 'db'],
      });
      expect(r['containers'], <dynamic>['web', 'db']);
    });
  });

  group('extractKubernetesRuntime', () {
    test('default branch', () {
      final r = extractKubernetesRuntime();
      expect(r['namespaces'], <String>['default']);
      expect(r['pods'], <dynamic>[]);
      expect(r['bounded'], true);
    });

    test('populated snapshot sorts namespaces', () {
      final r = extractKubernetesRuntime(<String, dynamic>{
        'namespaces': <dynamic>['kube-system', 'default'],
        'pods': <dynamic>['pod-1'],
      });
      expect(r['namespaces'], <String>['default', 'kube-system']);
      expect(r['pods'], <dynamic>['pod-1']);
    });
  });

  group('extractFilesystemRuntime', () {
    test('snapshot branch with overrides', () {
      final r = extractFilesystemRuntime('/ignored', <String, dynamic>{
        'root': '/snap',
        'files': <dynamic>['a', 'b'],
      });
      expect(r['root'], '/snap');
      expect(r['topology'], <dynamic>['a', 'b']);
      expect(r['bounded'], true);
    });

    test('snapshot branch falls back to root + empty files', () {
      final r = extractFilesystemRuntime('/fallback', <String, dynamic>{});
      expect(r['root'], '/fallback');
      expect(r['topology'], <dynamic>[]);
      expect(r['bounded'], true);
    });

    test('real temp directory walk + sort', () {
      final dir = Directory.systemTemp.createTempSync('wwx_fs_test_');
      try {
        File('${dir.path}${Platform.pathSeparator}zeta.txt')
            .writeAsStringSync('z');
        File('${dir.path}${Platform.pathSeparator}alpha.txt')
            .writeAsStringSync('a');
        final sub = Directory('${dir.path}${Platform.pathSeparator}nested')
          ..createSync();
        File('${sub.path}${Platform.pathSeparator}mid.txt')
            .writeAsStringSync('m');

        final r = extractFilesystemRuntime(dir.path);
        expect(r['bounded'], true);
        expect(r.containsKey('degraded'), false);
        final topology = (r['topology'] as List).cast<String>();
        expect(topology.length, 3);
        // Verify sorted ascending.
        final sortedCopy = <String>[...topology]..sort();
        expect(topology, sortedCopy);
        // All are files, directory itself excluded.
        for (final p in topology) {
          expect(File(p).existsSync(), true);
        }
      } finally {
        dir.deleteSync(recursive: true);
      }
    });

    test('non-existent path yields empty topology (not degraded)', () {
      final missing =
          '${Directory.systemTemp.path}${Platform.pathSeparator}wwx_missing_${DateTime.now().microsecondsSinceEpoch}';
      final r = extractFilesystemRuntime(missing);
      expect(r['root'], missing);
      expect(r['topology'], <String>[]);
      expect(r['bounded'], true);
    });
  });

  group('extractDatabaseRuntime', () {
    test('postgres dispatch (contains match)', () {
      final r = extractDatabaseRuntime('PostgreSQL');
      expect(r['database_type'], 'postgresql');
    });

    test('mysql dispatch', () {
      final r = extractDatabaseRuntime('mysql');
      expect(r['database_type'], 'mysql');
    });

    test('sqlite dispatch', () {
      final r = extractDatabaseRuntime('sqlite');
      expect(r['database_type'], 'sqlite');
    });

    test('redis dispatch', () {
      final r = extractDatabaseRuntime('redis');
      expect(r['database_type'], 'redis');
    });

    test('unknown dispatch is degraded', () {
      final r = extractDatabaseRuntime('Cassandra');
      expect(r['database_type'], 'cassandra');
      expect(r['degraded'], true);
      expect(r['bounded'], true);
    });

    test('passes snapshot through to specific extractor', () {
      final r = extractDatabaseRuntime('postgres', <String, dynamic>{
        'tables': <dynamic>['b', 'a'],
      });
      expect(r['tables'], <String>['a', 'b']);
    });
  });

  group('runLiveRuntime', () {
    test('default config branch', () {
      final r = runLiveRuntime();
      expect(r['bounded'], true);
      expect(r.containsKey('graph'), true);
      final parts = r['parts'] as Map<String, dynamic>;
      expect((parts['database'] as Map)['database_type'], 'postgresql');
      expect((parts['filesystem'] as Map)['root'], '.');
    });

    test('explicit config branch', () {
      final r = runLiveRuntime(<String, dynamic>{
        'database_type': 'mysql',
        'root': '.',
      });
      final parts = r['parts'] as Map<String, dynamic>;
      expect((parts['database'] as Map)['database_type'], 'mysql');
      expect(r['bounded'], true);
    });
  });

  group('postgres_connector export', () {
    test('extractPostgresRuntime reachable via barrel', () {
      // postgres_connector.dart re-exports extractPostgresRuntime; the barrel
      // exposes it. Exercising it confirms the export wiring.
      final r = extractPostgresRuntime(<String, dynamic>{
        'tables': <dynamic>['c', 'a', 'b'],
      });
      expect(r['tables'], <String>['a', 'b', 'c']);
    });
  });

  group('distributed_extraction_orchestrator', () {
    test('createExtractionWorker', () {
      final w = createExtractionWorker('worker_7');
      expect(w['worker_id'], 'worker_7');
      expect(w['status'], 'idle');
      expect(w['bounded'], true);
    });

    test('runDistributedExtraction default workers + tick', () {
      final r = runDistributedExtraction(<Map<String, dynamic>>[
        <String, dynamic>{'task_id': 't1', 'url': 'u1'},
        <String, dynamic>{},
      ]);
      final workers = r['workers'] as List;
      expect(workers.length, 1);
      expect((workers.first as Map)['worker_id'], 'worker_0');
      final queue = (r['queue'] as List).cast<Map<String, dynamic>>();
      expect(queue.length, 2);
      expect(queue[0]['task_id'], 't1');
      expect(queue[0]['url'], 'u1');
      // Defaults applied to empty task map.
      expect(queue[1]['task_id'], 'task');
      expect(queue[1]['url'], '');
      expect((r['checkpoint'] as Map)['tick'], 1);
      expect(r.containsKey('distributed_graph'), true);
      expect(r['bounded'], true);
    });

    test('runDistributedExtraction explicit workers/checkpoint/tick', () {
      final r = runDistributedExtraction(
        <Map<String, dynamic>>[
          <String, dynamic>{'task_id': 'a', 'url': 'x'},
        ],
        workers: <Map<String, dynamic>>[
          createExtractionWorker('w1'),
          createExtractionWorker('w2'),
        ],
        checkpoint: <String, dynamic>{'tick': 5},
        tick: 9,
      );
      expect((r['workers'] as List).length, 2);
      expect((r['checkpoint'] as Map)['tick'], 10);
    });
  });

  group('orchestration_engine', () {
    test('orchestrate', () {
      final r = orchestrate('seed-1');
      expect(r['seed'], 'seed-1');
      final plan = r['plan'] as Map<String, dynamic>;
      expect(plan['steps'], <String>['ingest', 'extract', 'graph']);
      expect(plan['bounded'], true);
      expect(r['bounded'], true);
    });
  });

  group('semantic_memory', () {
    test('SemanticMemory put/get', () {
      final mem = SemanticMemory();
      mem.put('k', 'v');
      expect(mem.get('k'), 'v');
      expect(mem.get('missing'), isNull);
    });

    test('SemanticMemory evicts oldest at capacity', () {
      final mem = SemanticMemory(maxEntries: 2);
      mem.put('a', 1);
      mem.put('b', 2);
      // This put triggers eviction of the first key ('a').
      mem.put('c', 3);
      expect(mem.get('a'), isNull);
      expect(mem.get('b'), 2);
      expect(mem.get('c'), 3);
    });

    test('buildSemanticMemory default branch', () {
      final r = buildSemanticMemory();
      expect(r.containsKey('semantic_id'), true);
      expect(r['bounded'], true);
    });

    test('buildSemanticMemory with semantic payload is deterministic', () {
      final r1 = buildSemanticMemory(<String, dynamic>{'topic': 'x'});
      final r2 = buildSemanticMemory(<String, dynamic>{'topic': 'x'});
      expect(r1['semantic_id'], r2['semantic_id']);
    });
  });
}
