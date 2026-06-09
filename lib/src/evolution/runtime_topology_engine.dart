import '_sort_util.dart';

/// Port of core/evolution_runtime/topology_evolution_engine.py
Map<String, dynamic> evolveRuntimeTopology([
  List<dynamic>? workers,
  Map<String, dynamic>? sync,
  Map<String, dynamic>? causality,
]) {
  final w = workers ?? <dynamic>[];
  final workerIds = <String>[];
  for (var index = 0; index < w.length; index++) {
    final worker = w[index] as Map;
    workerIds.add('${worker['worker_id'] ?? worker['id'] ?? 'w:$index'}');
  }
  workerIds.sort(pyStrCompare);

  final causalityTruthy = causality != null && causality.isNotEmpty;

  return <String, dynamic>{
    'worker_routing': workerIds,
    'sync_paths': <String>['browser', 'native', 'distributed'],
    'causality_propagation': causalityTruthy,
    'workflow_routing': <String>['primary', 'distributed'],
    'federation': workerIds.length,
    'bounded': true,
  };
}
