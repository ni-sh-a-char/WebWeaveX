// Port of core/workflows/workflow_runtime_engine.py

Map<String, dynamic> buildWorkflowRuntimeContext({
  String url = '',
  String runtime = 'browser',
  Map<String, dynamic>? sources,
}) {
  final Map<String, dynamic> src = sources ?? <String, dynamic>{};
  final List<String> sortedKeys = src.keys.toList()..sort();

  return <String, dynamic>{
    'url': url,
    'primary_runtime': runtime,
    'sources': sortedKeys,
    'bounded': true,
  };
}
