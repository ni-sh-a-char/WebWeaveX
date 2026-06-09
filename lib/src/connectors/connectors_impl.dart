import 'dart:io';

import '../graph/runtime_graph.dart';

Map<String, dynamic> extractPostgresRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'postgresql',
    'schemas':
        (s['schemas'] as List? ?? ['public']).map((e) => e.toString()).toList(),
    'tables': (s['tables'] as List? ?? []).map((e) => e.toString()).toList()
      ..sort(),
    'indexes': [...(s['indexes'] as List? ?? [])],
    'metrics': Map<String, dynamic>.from((s['metrics'] as Map?) ?? {}),
    'active_connections': s['active_connections'] ?? 0,
    'replication_state': '${s['replication_state'] ?? 'unknown'}',
    'degraded': s['degraded'] == true,
    'bounded': true,
  };
}

Map<String, dynamic> extractMysqlRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'mysql',
    'schemas': [...(s['schemas'] as List? ?? [])],
    'tables': (s['tables'] as List? ?? []).map((e) => e.toString()).toList()
      ..sort(),
    'bounded': true,
  };
}

Map<String, dynamic> extractSqliteRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'sqlite',
    'schemas': ['main'],
    'tables': (s['tables'] as List? ?? []).map((e) => e.toString()).toList()
      ..sort(),
    'bounded': true,
  };
}

Map<String, dynamic> extractRedisRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'redis',
    'tables': (s['keys'] as List? ?? []).take(1000).toList(),
    'replication_state': '${s['role'] ?? 'master'}',
    'bounded': true,
  };
}

Map<String, dynamic> extractKafkaRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'broker_type': 'kafka',
    'topics': (s['topics'] as List? ?? []).map((e) => e.toString()).toList()
      ..sort(),
    'bounded': true,
  };
}

Map<String, dynamic> extractGraphqlRuntime([Map<String, dynamic>? snapshot]) =>
    {
      'protocol': 'graphql',
      'endpoints': snapshot?['endpoints'] ?? ['/graphql'],
      'bounded': true,
    };

Map<String, dynamic> extractGrpcRuntime([Map<String, dynamic>? snapshot]) => {
      'protocol': 'grpc',
      'services': (snapshot?['services'] as List? ?? [])
          .map((e) => e.toString())
          .toList()
        ..sort(),
      'bounded': true,
    };

Map<String, dynamic> extractWebsocketRuntime(
        [Map<String, dynamic>? snapshot]) =>
    {
      'protocol': 'websocket',
      'connections': snapshot?['connections'] ?? <dynamic>[],
      'bounded': true,
    };

Map<String, dynamic> extractDockerRuntime([Map<String, dynamic>? snapshot]) => {
      'runtime': 'docker',
      'containers': snapshot?['containers'] ?? <dynamic>[],
      'bounded': true,
    };

Map<String, dynamic> extractKubernetesRuntime(
        [Map<String, dynamic>? snapshot]) =>
    {
      'namespaces': (snapshot?['namespaces'] as List? ?? ['default'])
          .map((e) => e.toString())
          .toList()
        ..sort(),
      'pods': snapshot?['pods'] ?? <dynamic>[],
      'bounded': true,
    };

Map<String, dynamic> extractFilesystemRuntime(String root,
    [Map<String, dynamic>? snapshot]) {
  if (snapshot != null) {
    return {
      'root': snapshot['root'] ?? root,
      'topology': snapshot['files'] ?? <dynamic>[],
      'bounded': true
    };
  }
  final topology = <String>[];
  try {
    final dir = Directory(root);
    if (dir.existsSync()) {
      for (final e in dir.listSync(recursive: true).take(5000)) {
        if (e is File) topology.add(e.path);
      }
    }
  } catch (_) {
    return {
      'root': root,
      'topology': <String>[],
      'degraded': true,
      'bounded': true
    };
  }
  return {'root': root, 'topology': topology..sort(), 'bounded': true};
}

Map<String, dynamic> extractDatabaseRuntime(String databaseType,
    [Map<String, dynamic>? snapshot]) {
  final n = databaseType.toLowerCase();
  if (n.contains('postgres')) return extractPostgresRuntime(snapshot);
  if (n == 'mysql') return extractMysqlRuntime(snapshot);
  if (n == 'sqlite') return extractSqliteRuntime(snapshot);
  if (n == 'redis') return extractRedisRuntime(snapshot);
  return {'database_type': n, 'degraded': true, 'bounded': true};
}

Map<String, dynamic> runLiveRuntime([Map<String, dynamic>? config]) {
  final c = config ?? {};
  final parts = {
    'database': extractDatabaseRuntime('${c['database_type'] ?? 'postgresql'}'),
    'filesystem': extractFilesystemRuntime('${c['root'] ?? '.'}'),
  };
  return {'graph': buildRuntimeGraph(parts), 'parts': parts, 'bounded': true};
}
