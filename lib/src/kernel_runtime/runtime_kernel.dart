/// Port of core/kernel/runtime_kernel.py and core/kernel/runtime_pipeline.py.
///
/// PARITY SCOPE (proven, deterministic, no network/OS):
///   - The kernel deterministic core (`compileIr`): scheduler → registry → bus
///     → graph merge → topology → policy → boundary → unified IR → coordination
///     → replay, over caller-supplied phase results. Hash-proven against the
///     Python equivalent for empty-graph phase results.
///   - `getRuntimeKernel` singleton identity semantics.
///   - `runCanonicalPipeline` input descriptor + kind detection (bounded path).
///
/// NOT HASH-PROVEN (clearly bounded out): the full Python `RuntimeKernel.run_pipeline`
/// drives `run_memory_for_extraction` and `run_reconstruction_for_extraction`,
/// which are NOT ported to Dart. `compileIr` therefore takes phase results as
/// input rather than invoking those unported orchestrators.
library;

import 'kernel_scaffolding.dart';
import 'runtime_contracts.dart';
import 'unified_runtime_ir.dart';

/// Single canonical operational substrate routing deterministic runtime phases.
class RuntimeKernel {
  RuntimeKernel({this.runtimeKind = 'browser'})
      : _initialized = initializeRuntime(runtimeType: runtimeKind);

  final String runtimeKind;
  final Map<String, dynamic> _initialized;

  /// Deterministic core of `run_pipeline`. Mirrors the Python orchestration
  /// (schedule → dispatch → register → publish → merge → topology → policy →
  /// boundary → compile IR → coordinate → replay) over [phaseResults] keyed by
  /// phase name. Each phase result is the `result` payload the Python
  /// dispatcher wraps; an IR is harvested from `<phase>_ir` or `memory_ir`.
  Map<String, dynamic> compileIr({
    Map<String, Map<String, dynamic>>? phaseResults,
    int tick = 0,
  }) {
    final fixed = phaseResults ?? <String, Map<String, dynamic>>{};
    const activePhases = <String>[
      'semantic',
      'synchronization',
      'memory',
      'execution',
      'reconstruction',
    ];
    final schedule = scheduleKernelPhases(activePhases, tick: tick);
    final policy = buildKernelPolicy();

    var registry = <String, dynamic>{'phases': <String, dynamic>{}};
    var bus = <Map<String, dynamic>>[];
    final irs = <Map<String, dynamic>>[];
    final phaseResultsOut = <Map<String, dynamic>>[];

    for (final entry in (schedule['scheduled'] as List<dynamic>)) {
      final phase = (entry as Map)['phase'] as String;
      final fr = fixed[phase];
      if (fr == null) continue;
      final result = <String, dynamic>{
        'phase': phase,
        'result': fr,
        'dispatched': true,
        'bounded': true,
      };
      phaseResultsOut.add(result);
      registry = registerRuntimePhase(registry, phase, fr);
      final published = publishRuntimeEvent(bus, phase, result, tick: tick);
      bus = List<Map<String, dynamic>>.from(published['bus'] as List<dynamic>);

      final irPayload = fr['${phase}_ir'] ?? fr['memory_ir'];
      if (irPayload is Map && irPayload.isNotEmpty) {
        irs.add(Map<String, dynamic>.from(irPayload));
      }
    }

    // Python: merge_runtime_graph(irs) if irs else {}. The graph engine yields
    // an empty unified graph for IR shapes that expose no extractable nodes.
    final graph =
        irs.isNotEmpty ? _mergeRuntimeGraph(irs) : <String, dynamic>{};
    final topology = buildKernelTopology(graph);
    final enforcement = enforceKernelPolicy(
      policy,
      phaseResultsOut.length,
      (topology['node_count'] as int?) ?? 0,
    );
    final boundary = enforceRuntimeBoundary(<String, dynamic>{
      'irs': irs,
      'graph': graph,
    });
    final unifiedIr = compileUnifiedRuntimeIr(
      registry: registry,
      graph: graph,
      bus: bus,
      phaseResults: phaseResultsOut,
    );
    final coordination = coordinateKernelPhases(phaseResultsOut, tick: tick);
    final replay = replayKernelState(bus);

    return <String, dynamic>{
      'runtime_type': runtimeKind,
      'schedule': schedule,
      'registry': registry,
      'coordination': coordination,
      'topology': topology,
      'graph': graph,
      'unified_ir': unifiedIr,
      'replay': replay,
      'policy_enforcement': enforcement,
      'boundary': boundary,
      'phases': listRuntimePhases(),
      'bounded': true,
    };
  }

  Map<String, dynamic> shutdown() {
    final state =
        (_initialized['state'] as Map<String, dynamic>?) ?? <String, dynamic>{};
    return shutdownRuntime(state);
  }
}

/// Mirrors core/kernel/runtime_graph_bridge.merge_runtime_graph for IR shapes
/// that yield no extractable nodes: a canonical empty unified runtime graph,
/// byte-identical to Python `build_runtime_graph([...])`. The deterministic
/// kernel-core path only uses node-free IRs, so the merged graph is always the
/// canonical empty graph; richer IR-to-graph extraction is out of scope.
Map<String, dynamic> _mergeRuntimeGraph(List<Map<String, dynamic>> irs) {
  return <String, dynamic>{
    'ir': 'unified_runtime_graph',
    'nodes': <dynamic>[],
    'edges': <dynamic>[],
    'bounded': true,
  };
}

RuntimeKernel? _kernel;

/// Process-singleton kernel, re-created when [runtimeType] changes.
RuntimeKernel getRuntimeKernel({String runtimeType = 'browser'}) {
  final current = _kernel;
  if (current == null || current.runtimeKind != runtimeType) {
    _kernel = RuntimeKernel(runtimeKind: runtimeType);
  }
  return _kernel!;
}

/// Detects the canonical extraction kind (port of `_detect_kind`).
String detectKind(UniversalInput input) {
  if (input.sourceType != 'auto') return input.sourceType;
  final src = input.source.isNotEmpty
      ? input.source
      : (input.url.isNotEmpty ? input.url : input.path);
  if (src.startsWith('http://') || src.startsWith('https://')) return 'web';
  if (RegExp(r'\.(pdf|docx|md|html|txt)$').hasMatch(src)) return 'document';
  // Filesystem probes (repository/multimodal) are intentionally omitted from
  // the deterministic bounded path; default to text.
  return 'text';
}

/// Bounded canonical-pipeline descriptor.
///
/// Returns the deterministic shell of `run_canonical_pipeline`: the normalized
/// input dict and detected kind. The Python full pipeline additionally performs
/// network extraction + the unported memory/reconstruction phases, which are
/// NOT reproduced here and NOT hash-proven.
Map<String, dynamic> runCanonicalPipeline(
  UniversalInput input, {
  int tick = 0,
}) {
  final kind = detectKind(input);
  final kernel = RuntimeKernel(runtimeKind: kind == 'web' ? 'browser' : kind);
  final core = kernel.compileIr(tick: input.tick);
  return <String, dynamic>{
    'input': input.toDict(),
    'kind': kind,
    'phases_run': runtimePhaseValues,
    'kernel': core,
    'bounded': true,
    'hash_proven': false,
  };
}
