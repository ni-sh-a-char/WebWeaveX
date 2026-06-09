/// Evolution runtime family — native Dart port of Python
/// `core.evolution_runtime` with proven cross-language Kaalka parity.
///
/// Public API parity with Python `webweavex.__all__`:
///   run_evolution_runtime, run_evolution_for_extraction,
///   build_runtime_evolution, evolve_selector_runtime,
///   save_evolution_runtime, load_evolution_runtime
library;

export 'runtime_evolution_orchestrator.dart'
    show runEvolutionRuntime, runEvolutionForExtraction;
export 'runtime_evolution_engine.dart' show buildRuntimeEvolution;
export 'selector_evolution_engine.dart' show evolveSelectorRuntime;
export 'runtime_memory_engine.dart'
    show saveEvolutionRuntime, loadEvolutionRuntime;
