/// Execution family — native Dart port of the Python `webweavex` execution
/// public APIs with proven cross-language determinism parity.
///
/// Parity-proven (matching computeDeterministicHash vs Python reference):
///   - runExecutionRuntime      (run_execution_runtime)
///   - runExecutionForExtraction(run_execution_for_extraction)
///   - executeRuntimeAction     (execute_runtime_action)
///   - buildRuntimeSandbox      (build_runtime_sandbox)
///   - simulateRuntimeExecution (simulate_runtime_execution)
///   - replayRuntimeExecution   (replay_runtime_execution)
library;

export 'runtime_execution_orchestrator.dart'
    show runExecutionRuntime, runExecutionForExtraction;
export 'runtime_execution_engine.dart' show executeRuntimeAction;
export 'runtime_sandbox_engine.dart' show buildRuntimeSandbox;
export 'runtime_simulation_engine.dart' show simulateRuntimeExecution;
export 'runtime_replay_engine.dart' show replayRuntimeExecution;
