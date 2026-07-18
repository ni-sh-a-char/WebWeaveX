/// Phase A.2 (semantic pressure leaves) of the Category-A semantic-IR port.
/// Canonical ports of the 10 core.semantic.*_pressure_engine leaf functions,
/// proven Python ≡ JavaScript ≡ Dart by execution (validation/semantic_ir/).
/// All `round(x, 3)` sites use [pythonRound] (round-half-to-even, bit-exact).
library;

import 'dart:math' as math;

import 'py_compat.dart';

/// Port of core.semantic.ambiguity_pressure_engine.compute_ambiguity_pressure.
Map<String, dynamic> computeAmbiguityPressure(List<dynamic> ambiguities) {
  final pressure = pythonRound(math.min(1.0, ambiguities.length * 0.12), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'suppress_expansion': pressure >= 0.2,
    'confidence_reduction': pythonRound(math.min(0.25, pressure * 0.3), 3),
    'preserved': true,
  };
}

/// Port of core.semantic.contradiction_pressure_engine.compute_contradiction_pressure.
Map<String, dynamic> computeContradictionPressure(dynamic contradicted) {
  final pairs = contradicted is Map
      ? pyGet(contradicted, 'pairs', <dynamic>[])
      : <dynamic>[];
  final preserved =
      contradicted is Map ? pyGet(contradicted, 'preserved', false) : false;
  final count = (pairs as List).length;
  final pressure = pythonRound(math.min(1.0, count * 0.25), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'pair_count': count,
    'preserved': preserved,
    'suppress_propagation': count > 0,
    'suppress_reconciliation': count > 0,
    'suppress_ontology_expansion': count > 0,
    'suppress_topology_expansion': count > 0,
    'confidence_reduction': pythonRound(math.min(0.4, count * 0.15), 3),
  };
}

/// Port of core.semantic.evidence_boundary_pressure_engine.compute_evidence_boundary_pressure.
Map<String, dynamic> computeEvidenceBoundaryPressure(int evidenceCount,
    [int minEvidence = 2]) {
  final gap = math.max(0, minEvidence - evidenceCount);
  final pressure = pythonRound(math.min(1.0, gap * 0.35), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'violation': gap > 0,
    'gap': gap,
  };
}

/// Port of core.semantic.evidence_decay_pressure_engine.compute_evidence_decay_pressure.
Map<String, dynamic> computeEvidenceDecayPressure(int evidenceCount,
    [int minEvidence = 2]) {
  final gap = math.max(0, minEvidence - evidenceCount);
  return <String, dynamic>{
    'pressure': pythonRound(math.min(1.0, gap * 0.4), 3),
    'incomplete': gap > 0,
  };
}

/// Port of core.semantic.recursive_boundary_pressure_engine.compute_recursive_boundary_pressure.
Map<String, dynamic> computeRecursiveBoundaryPressure(
    num boundaryErosion, int depth) {
  return <String, dynamic>{
    'pressure': pythonRound(math.min(1.0, boundaryErosion + depth * 0.06), 3),
    'violation': boundaryErosion >= 0.3,
  };
}

/// Port of core.semantic.recursive_convergence_pressure_engine.compute_recursive_convergence_pressure.
Map<String, dynamic> computeRecursiveConvergencePressure(
    int depth, num diversityScore) {
  final pressure = pythonRound(
      math.min(1.0, depth * 0.08 + math.max(0.0, 0.5 - diversityScore)), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'suppress': pressure >= 0.3,
  };
}

/// Port of core.semantic.recursive_dependency_pressure_engine.compute_recursive_dependency_pressure.
Map<String, dynamic> computeRecursiveDependencyPressure(
    int depth, int interpretationCount) {
  final pressure = pythonRound(
      math.min(
          1.0,
          math.max(0, depth - 1) * 0.15 +
              (interpretationCount <= 1 ? 0.2 : 0.0)),
      3);
  return <String, dynamic>{
    'pressure': pressure,
    'violation': pressure >= 0.3,
  };
}

/// Port of core.semantic.semantic_boundary_pressure_engine.compute_semantic_boundary_pressure.
Map<String, dynamic> computeSemanticBoundaryPressure(
    num boundaryPressure, num driftPressure) {
  final pressure =
      pythonRound(math.min(1.0, boundaryPressure + driftPressure * 0.5), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'suppress_continuation': pressure >= 0.25,
  };
}

/// Port of core.semantic.truth_boundary_pressure_engine.compute_truth_boundary_pressure.
Map<String, dynamic> computeTruthBoundaryPressure(
    bool truthBounded, num entropy) {
  final pressure = pythonRound((truthBounded ? 0.0 : 0.5) + entropy * 0.3, 3);
  return <String, dynamic>{
    'pressure': math.min(1.0, pressure),
    'violation': !truthBounded,
  };
}

/// Port of core.semantic.uncertainty_pressure_engine.compute_uncertainty_pressure.
Map<String, dynamic> computeUncertaintyPressure(
    List<dynamic> uncertainties, List<dynamic> ambiguities) {
  final count = uncertainties.length + ambiguities.length;
  final pressure = pythonRound(math.min(1.0, count * 0.1), 3);
  return <String, dynamic>{
    'pressure': pressure,
    'suppress_propagation': pressure >= 0.25,
    'confidence_reduction': pythonRound(math.min(0.3, pressure * 0.35), 3),
    'preserved': true,
  };
}
