/// Kernel-runtime family barrel — native Dart port of the Python kernel,
/// contracts, and unified-IR public APIs.
///
/// Targets (mirror `webweavex.__all__`):
///   - RuntimeKernel           (class)        ← core/kernel/runtime_kernel.py
///   - getRuntimeKernel        (get_runtime_kernel)
///   - runCanonicalPipeline    (run_canonical_pipeline, bounded path)
///   - compileUnifiedRuntimeIr (compile_unified_runtime_ir)
///   - UniversalInput          (class)        ← core/contracts/runtime_contracts.py
library;

export 'kernel_scaffolding.dart'
    show
        scheduleKernelPhases,
        registerRuntimePhase,
        listRuntimePhases,
        publishRuntimeEvent,
        buildKernelTopology,
        coordinateKernelPhases,
        replayKernelState,
        buildKernelPolicy,
        enforceKernelPolicy,
        buildRuntimeContext,
        buildKernelState,
        mergeKernelState,
        initializeRuntime,
        shutdownRuntime,
        enforceRuntimeBoundary;
export 'runtime_contracts.dart' show UniversalInput, runtimePhaseValues;
export 'runtime_kernel.dart'
    show RuntimeKernel, getRuntimeKernel, runCanonicalPipeline, detectKind;
export 'unified_runtime_ir.dart' show compileUnifiedRuntimeIr;
