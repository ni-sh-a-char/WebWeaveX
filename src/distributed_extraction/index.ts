/**
 * Barrel converted from core/distributed_extraction/__init__.py
 * @generated — WebWeaveX python→javascript library port
 */

export { runAutonomousExtraction } from "./autonomousExtractionEngine.js";
export { loadDistributedCheckpoint, saveDistributedCheckpoint } from "./distributedCheckpointEngine.js";
export { runDistributedExtraction } from "./distributedExtractionOrchestrator.js";
export { failoverExtractionRuntime } from "./distributedFailoverEngine.js";
export { balanceExtractionWorkloads } from "./distributedLoadBalancer.js";
export { createExtractionWorker } from "./extractionWorkerEngine.js";
export { federateExtractionRuntimes } from "./runtimeFederationEngine.js";
