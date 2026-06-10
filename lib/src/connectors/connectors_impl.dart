import 'dart:io';

import '../graph/runtime_graph.dart';

// --- Python-faithful helpers (parity with core.connectors snapshot extractors).
// Python sorts keep the ORIGINAL element types, ordered by `str(...)`; these
// helpers preserve element identity and replicate `sorted(..., key=str)` /
// `key=lambda i: str(i.get("name", i))` with a stable index tiebreak.

String _pyStr(Object? v) {
  if (v is String) return v;
  if (v is bool) return v ? 'True' : 'False';
  if (v == null) return 'None';
  return v.toString();
}

List<dynamic> _pyList(Object? v, [List<dynamic> dflt = const <dynamic>[]]) =>
    v is List ? List<dynamic>.from(v) : List<dynamic>.from(dflt);

List<dynamic> _sortedByStr(Object? v, List<dynamic> dflt) {
  final items = _pyList(v, dflt);
  final indexed = <List<dynamic>>[
    for (var i = 0; i < items.length; i++) <dynamic>[items[i], i]
  ];
  indexed.sort((a, b) {
    final c = _pyStr(a[0]).compareTo(_pyStr(b[0]));
    return c != 0 ? c : (a[1] as int).compareTo(b[1] as int);
  });
  return [for (final pair in indexed) pair[0]];
}

List<dynamic> _sortedByName(Object? v) {
  final items = _pyList(v);
  String key(dynamic i) => i is Map ? _pyStr(i['name'] ?? i) : _pyStr(i);
  final indexed = <List<dynamic>>[
    for (var i = 0; i < items.length; i++) <dynamic>[items[i], i]
  ];
  indexed.sort((a, b) {
    final c = key(a[0]).compareTo(key(b[0]));
    return c != 0 ? c : (a[1] as int).compareTo(b[1] as int);
  });
  return [for (final pair in indexed) pair[0]];
}

Map<String, dynamic> _dict(Object? v) =>
    v is Map ? Map<String, dynamic>.from(v) : <String, dynamic>{};

int _pyInt(Object? v, int dflt) {
  if (v is int) return v;
  if (v is num) return v.toInt();
  if (v is String) return int.tryParse(v) ?? dflt;
  return dflt;
}

dynamic _degradedOr(Map<String, dynamic> s) =>
    s.containsKey('degraded') ? s['degraded'] : false;

Map<String, dynamic> extractPostgresRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'postgresql',
    'schemas': _pyList(s['schemas'], <dynamic>['public']),
    'tables': _sortedByStr(s['tables'], <dynamic>[]),
    'indexes': _pyList(s['indexes']),
    'metrics': _dict(s['metrics']),
    'active_connections': _pyInt(s['active_connections'], 0),
    'replication_state': _pyStr(s['replication_state'] ?? 'unknown'),
    'degraded': _degradedOr(s),
    'bounded': true,
  };
}

Map<String, dynamic> extractMysqlRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'mysql',
    'schemas': _pyList(s['schemas']),
    'tables': _sortedByStr(s['tables'], <dynamic>[]),
    'indexes': _pyList(s['indexes']),
    'metrics': _dict(s['metrics']),
    'active_connections': _pyInt(s['active_connections'], 0),
    'replication_state': _pyStr(s['replication_state'] ?? ''),
    'degraded': _degradedOr(s),
    'bounded': true,
  };
}

Map<String, dynamic> extractSqliteRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'sqlite',
    'schemas': <dynamic>['main'],
    'tables': _sortedByStr(s['tables'], <dynamic>[]),
    'indexes': _pyList(s['indexes']),
    'metrics': _dict(s['metrics']),
    'active_connections': 1,
    'replication_state': 'local',
    'degraded': _degradedOr(s),
    'bounded': true,
  };
}

Map<String, dynamic> extractRedisRuntime([Map<String, dynamic>? snapshot]) {
  final s = snapshot ?? {};
  return {
    'database_type': 'redis',
    'schemas': <dynamic>[],
    'tables': _pyList(s['keys']).take(1000).toList(),
    'indexes': <dynamic>[],
    'metrics': _dict(s['metrics']),
    'active_connections': _pyInt(s['clients'], 0),
    'replication_state': _pyStr(s['role'] ?? 'master'),
    'streams': _pyList(s['streams']),
    'degraded': _degradedOr(s),
    'bounded': true,
  };
}

Map<String, dynamic> _degradedDatabase(String databaseType) => {
      'database_type': databaseType,
      'schemas': <dynamic>[],
      'tables': <dynamic>[],
      'metrics': <String, dynamic>{},
      'degraded': true,
      'reason': 'connector_unavailable',
      'bounded': true,
    };

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

Map<String, dynamic> extractDockerRuntime([Map<String, dynamic>? snapshot]) {
  final snap = snapshot ?? {};
  return {
    'runtime': 'docker',
    'containers': _pyList(snap['containers']),
    'images': _sortedByStr(snap['images'], <dynamic>[]),
    'volumes': _pyList(snap['volumes']),
    'networks': _pyList(snap['networks']),
    'states': _dict(snap['states']),
    'health': _dict(snap['health']),
    'degraded': _degradedOr(snap),
    'bounded': true,
  };
}

/// Port of webweavex.extract_container_runtime(runtime, snapshot).
Map<String, dynamic> extractContainerRuntime(
    [String runtime = 'docker', Map<String, dynamic>? snapshot]) {
  final n = runtime.toLowerCase();
  final snap = snapshot ?? {};
  if (n == 'docker' || n == 'podman' || n == 'oci') {
    final result = extractDockerRuntime(snap);
    result['runtime'] = n;
    return result;
  }
  return {
    'runtime': n,
    'containers': <dynamic>[],
    'images': <dynamic>[],
    'volumes': <dynamic>[],
    'networks': <dynamic>[],
    'degraded': true,
    'bounded': true,
  };
}

/// Port of webweavex.extract_ide_runtime(ide, snapshot).
Map<String, dynamic> extractIdeRuntime(
    [String ide = 'vscode', Map<String, dynamic>? snapshot]) {
  final snap = snapshot ?? {};
  return {
    'ide': ide,
    'open_files': _sortedByStr(snap['open_files'], <dynamic>[]),
    'terminals': _pyList(snap['terminals']),
    'tabs': _pyList(snap['tabs']),
    'workspace_topology': _dict(snap['workspace']),
    'debug_sessions': _pyList(snap['debug_sessions']),
    'degraded': _degradedOr(snap),
    'bounded': true,
  };
}

Map<String, dynamic> extractKubernetesRuntime(
    [Map<String, dynamic>? snapshot]) {
  final snap = snapshot ?? {};
  return {
    'namespaces': _sortedByStr(snap['namespaces'], <dynamic>['default']),
    'pods': _sortedByName(snap['pods']),
    'deployments': _sortedByName(snap['deployments']),
    'services': _pyList(snap['services']),
    'ingress': _pyList(snap['ingress']),
    'topology': _dict(snap['topology']),
    'events': _pyList(snap['events']).take(5000).toList(),
    'degraded': _degradedOr(snap),
    'bounded': true,
  };
}

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

Map<String, dynamic> extractDatabaseRuntime(
    [String databaseType = 'postgresql', Map<String, dynamic>? snapshot]) {
  final n = databaseType.toLowerCase();
  try {
    if (n == 'postgres' || n == 'postgresql') {
      return extractPostgresRuntime(snapshot);
    }
    if (n == 'mysql') return extractMysqlRuntime(snapshot);
    if (n == 'sqlite') return extractSqliteRuntime(snapshot);
    if (n == 'redis') return extractRedisRuntime(snapshot);
  } catch (_) {
    return _degradedDatabase(n);
  }
  return _degradedDatabase(n);
}

Map<String, dynamic> runLiveRuntime([Map<String, dynamic>? config]) {
  final c = config ?? {};
  final parts = {
    'database': extractDatabaseRuntime('${c['database_type'] ?? 'postgresql'}'),
    'filesystem': extractFilesystemRuntime('${c['root'] ?? '.'}'),
  };
  return {'graph': buildRuntimeGraph(parts), 'parts': parts, 'bounded': true};
}
