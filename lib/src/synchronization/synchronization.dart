/// WebWeaveX synchronization runtime family (Dart).
///
/// Native port of the Python `core.synchronization` public surface:
///   run_synchronized_runtime, run_sync_for_extraction, build_runtime_delta,
///   save_sync_memory, load_sync_memory, replay_synchronized_runtime.
///
/// Parity-proven against `compute_deterministic_hash` of the Python reference.
library;

export 'synchronization_engines.dart'
    show
        runSynchronizedRuntime,
        runSyncForExtraction,
        buildRuntimeDelta,
        replaySynchronizedRuntime;
export 'runtime_sync_memory.dart' show saveSyncMemory, loadSyncMemory;
