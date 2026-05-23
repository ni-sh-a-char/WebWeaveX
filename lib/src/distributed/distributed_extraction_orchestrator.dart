import '../connectors/connectors_impl.dart' show extractPostgresRuntime;
import '../graph/runtime_graph.dart';

Map<String, dynamic> createExtractionWorker(String workerId) => {
      'worker_id': workerId,
      'status': 'idle',
      'bounded': true,
    };

Map<String, dynamic> runDistributedExtraction(
  List<Map<String, dynamic>> tasks, {
  List<Map<String, dynamic>>? workers,
  Map<String, dynamic>? checkpoint,
  int tick = 0,
}) {
  final workerList = workers ?? [createExtractionWorker('worker_0')];
  final queue = <Map<String, dynamic>>[
    for (final t in tasks)
      {'task_id': t['task_id'] ?? 'task', 'url': t['url'] ?? '', 'bounded': true}
  ];
  final graph = buildRuntimeGraph({'workers': workerList.length, 'tasks': tasks.length});
  return {
    'workers': workerList,
    'queue': queue,
    'distributed_graph': graph.toJson(),
    'checkpoint': {'tick': tick + 1, 'bounded': true},
    'bounded': true,
  };
}
