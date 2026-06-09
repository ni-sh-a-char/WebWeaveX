import 'runtime_worker_engine.dart';

/// Port of core/execution/runtime_federation_engine.federate_runtime_execution.
Map<String, dynamic> federateRuntimeExecution(
  List<Map<String, dynamic>> workers, [
  List<Map<String, dynamic>>? actions,
]) {
  final List<Map<String, dynamic>> built = buildRuntimeWorkers(workers);
  final List<Map<String, dynamic>> routes = <Map<String, dynamic>>[];

  // Mirrors Python: actions or [{}] for the modulo index; if actions falsy
  // (None or empty), the per-route action is {} entirely.
  final bool hasActions = actions != null && actions.isNotEmpty;
  final List<Map<String, dynamic>> actionPool =
      hasActions ? actions : <Map<String, dynamic>>[<String, dynamic>{}];

  for (int index = 0; index < built.length; index++) {
    final Map<String, dynamic> worker = built[index];
    final Map<String, dynamic> action = hasActions
        ? actionPool[index % (actionPool.isEmpty ? 1 : actionPool.length)]
        : <String, dynamic>{};
    routes.add(<String, dynamic>{
      'worker_id': worker['worker_id'],
      'runtime': worker['runtime'],
      'action_id': '${action['id'] ?? 'route:$index'}',
      'route_order': index,
    });
  }

  routes.sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      (a['route_order'] as int).compareTo(b['route_order'] as int));

  return <String, dynamic>{
    'workers': built,
    'execution_routes': routes,
    'federated': true,
    'bounded': true,
  };
}
