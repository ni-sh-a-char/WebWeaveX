/// Reconstruction runtime family — Dart port with proven cross-language parity.
///
/// Exposes the 5 public APIs that mirror the Python `webweavex` reconstruction
/// exports (run_reconstruction_runtime, run_reconstruction_for_extraction,
/// fabricate_runtime_reality, clone_runtime_environment,
/// validate_reconstructed_runtime).
library;

export 'reconstruction_runtime_orchestrator.dart'
    show
        runReconstructionRuntime,
        runReconstructionForExtraction,
        fabricateRuntimeReality,
        cloneRuntimeEnvironment,
        validateReconstructedRuntime,
        saveReconstructionSnapshot,
        loadReconstructionSnapshot;
