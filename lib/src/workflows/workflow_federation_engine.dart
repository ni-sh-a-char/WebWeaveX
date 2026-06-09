// Port of core/workflows/workflow_federation_engine.py

Map<String, dynamic> federateWorkflowRuntime({
  Map<String, dynamic>? browser,
  Map<String, dynamic>? native,
  Map<String, dynamic>? distributed,
  Map<String, dynamic>? semantic,
  List<dynamic>? workers,
}) {
  final List<dynamic> workerList = workers ?? <dynamic>[];

  final List<Map<String, dynamic>> mappedWorkers = <Map<String, dynamic>>[];
  int index = 0;
  for (final dynamic workerRaw in workerList.take(1000)) {
    final Map<String, dynamic> worker = workerRaw is Map
        ? Map<String, dynamic>.from(workerRaw)
        : <String, dynamic>{};
    final dynamic wid = worker['worker_id'] ?? worker['id'] ?? 'w:$index';
    mappedWorkers.add(<String, dynamic>{
      'worker_id': '$wid',
      'synced': true,
    });
    index++;
  }

  dynamic semanticCheckpoints = <String, dynamic>{};
  if (semantic != null && semantic.isNotEmpty) {
    final dynamic semInnerRaw = semantic['semantic'];
    final Map<String, dynamic> semInner = semInnerRaw is Map
        ? Map<String, dynamic>.from(semInnerRaw)
        : <String, dynamic>{};
    semanticCheckpoints = semInner['memory'] ?? <String, dynamic>{};
  }

  return <String, dynamic>{
    'workers': mappedWorkers,
    'semantic_checkpoints': semanticCheckpoints,
    'browser_runtime': browser != null && browser.isNotEmpty,
    'native_runtime': native != null && native.isNotEmpty,
    'extraction_agents': workerList.length,
    'distributed_sync': distributed != null && distributed.isNotEmpty,
    'bounded': true,
  };
}
