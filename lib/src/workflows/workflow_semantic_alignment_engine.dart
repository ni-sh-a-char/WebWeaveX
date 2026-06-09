// Port of core/workflows/workflow_semantic_alignment_engine.py

Map<String, dynamic> alignWorkflowSemantics(
  Map<String, dynamic> plan, {
  Map<String, dynamic>? semanticRuntime,
  Map<String, dynamic>? causality,
}) {
  final Map<String, dynamic> semantic = semanticRuntime ?? <String, dynamic>{};
  final dynamic innerRaw = semantic['semantic'];
  final Map<String, dynamic> inner =
      innerRaw is Map ? Map<String, dynamic>.from(innerRaw) : semantic;

  dynamic causalityChains = <String, dynamic>{};
  if (causality != null && causality.isNotEmpty) {
    final dynamic cInnerRaw = causality['causality'];
    final Map<String, dynamic> cInner =
        cInnerRaw is Map ? Map<String, dynamic>.from(cInnerRaw) : causality;
    causalityChains = cInner['propagation'] ?? <String, dynamic>{};
  }

  return <String, dynamic>{
    'ontology': inner['ontology'] ?? <String, dynamic>{},
    'domain': inner['domain'] ?? <String, dynamic>{},
    'causality_chains': causalityChains,
    'workflow_objective': plan['objective'] ?? '',
    'extraction_semantics': inner['semantic_graph'] ?? <String, dynamic>{},
    'aligned': true,
    'bounded': true,
  };
}
