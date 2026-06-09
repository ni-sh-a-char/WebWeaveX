/// Port of core/execution/runtime_worker_engine.build_runtime_workers.
List<Map<String, dynamic>> buildRuntimeWorkers(
    List<Map<String, dynamic>> nodes) {
  final List<Map<String, dynamic>> workers = <Map<String, dynamic>>[];
  final List<Map<String, dynamic>> bounded =
      nodes.length > 1000 ? nodes.sublist(0, 1000) : nodes;
  for (int index = 0; index < bounded.length; index++) {
    final Map<String, dynamic> node = bounded[index];
    workers.add(<String, dynamic>{
      'worker_id': '${node['worker_id'] ?? node['node_id'] ?? 'worker:$index'}',
      'runtime': '${node['runtime'] ?? 'browser'}',
      'synced': node.containsKey('synced') ? node['synced'] == true : true,
      'bounded': true,
    });
  }
  workers.sort((Map<String, dynamic> a, Map<String, dynamic> b) =>
      '${a['worker_id']}'.compareTo('${b['worker_id']}'));
  return workers;
}
