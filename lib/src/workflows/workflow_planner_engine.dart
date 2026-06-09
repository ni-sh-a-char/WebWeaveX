// Port of core/workflows/workflow_planner_engine.py
import 'objective_engine.dart';

String _runtimeForStep(String step, String domain) {
  if (step.contains('terminal')) {
    return 'terminal';
  }
  if (step.contains('repository') || step.contains('api')) {
    return 'repository';
  }
  if (step.contains('infra') || domain == 'infrastructure') {
    return 'native';
  }
  if (step.contains('notification')) {
    return 'desktop';
  }
  return 'browser';
}

Map<String, dynamic> buildWorkflowPlan(
  String objective, {
  Map<String, dynamic>? semanticRuntime,
  Map<String, dynamic>? causality,
  Map<String, dynamic>? applicationRuntime,
}) {
  final Map<String, dynamic> runtimeObjective =
      buildRuntimeObjective(objective);
  final Map<String, dynamic> semantic = semanticRuntime ?? <String, dynamic>{};
  final dynamic domainOuter = semantic['domain'];
  final String domain = (domainOuter is Map && domainOuter['domain'] is String)
      ? domainOuter['domain'] as String
      : 'saas';

  final List<Map<String, dynamic>> planSteps = <Map<String, dynamic>>[];
  final List<dynamic> objSteps =
      List<dynamic>.from(runtimeObjective['steps'] as List<dynamic>);
  for (int index = 0; index < objSteps.length; index++) {
    final String step = objSteps[index] as String;
    planSteps.add(<String, dynamic>{
      'id': 'step:$index',
      'action': step,
      'runtime': _runtimeForStep(step, domain),
      'depends_on': index > 0 ? 'step:${index - 1}' : '',
    });
  }

  if (applicationRuntime != null && applicationRuntime.isNotEmpty) {
    final dynamic wf = applicationRuntime['workflow'];
    final Map<String, dynamic> workflow =
        wf is Map ? Map<String, dynamic>.from(wf) : <String, dynamic>{};
    final List<dynamic> edges = workflow['edges'] is List
        ? List<dynamic>.from(workflow['edges'] as List<dynamic>)
        : <dynamic>[];
    for (final dynamic edgeRaw in edges.take(100)) {
      final Map<String, dynamic> edge = edgeRaw is Map
          ? Map<String, dynamic>.from(edgeRaw)
          : <String, dynamic>{};
      planSteps.add(<String, dynamic>{
        'id': 'app:${planSteps.length}',
        'action': '${edge['relation'] ?? 'transition'}',
        'runtime': 'application',
        'depends_on':
            planSteps.isNotEmpty ? planSteps.last['id'] as String : '',
      });
    }
  }

  if (causality != null && causality.isNotEmpty) {
    final dynamic innerRaw = causality['causality'];
    final Map<String, dynamic> inner =
        innerRaw is Map ? Map<String, dynamic>.from(innerRaw) : causality;
    final dynamic propRaw = inner['propagation'];
    final Map<String, dynamic> prop = propRaw is Map
        ? Map<String, dynamic>.from(propRaw)
        : <String, dynamic>{};
    final List<dynamic> handoffs = prop['handoffs'] is List
        ? List<dynamic>.from(prop['handoffs'] as List<dynamic>)
        : <dynamic>[];
    for (final dynamic handoffRaw in handoffs.take(50)) {
      final Map<String, dynamic> handoff = handoffRaw is Map
          ? Map<String, dynamic>.from(handoffRaw)
          : <String, dynamic>{};
      planSteps.add(<String, dynamic>{
        'id': 'causal:${planSteps.length}',
        'action': 'cross_runtime_handoff',
        'runtime': '${handoff['to'] ?? 'native'}',
        'depends_on':
            planSteps.isNotEmpty ? planSteps.last['id'] as String : '',
      });
    }
  }

  return <String, dynamic>{
    'objective': objective,
    'domain': domain,
    'steps': planSteps,
    'bounded': true,
  };
}
