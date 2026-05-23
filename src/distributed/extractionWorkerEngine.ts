export function createExtractionWorker(
  workerId: string,
  runtimeState: Record<string, unknown> = {},
  identity: Record<string, unknown> = {},
  adaptiveRuntime: Record<string, unknown> = {},
  streamRuntime: Record<string, unknown> = {},
  status = "idle",
): Record<string, unknown> {
  return {
    worker_id: String(workerId),
    runtime_state: { ...runtimeState },
    identity: { ...identity },
    adaptive_runtime: { ...adaptiveRuntime },
    stream_runtime: { ...streamRuntime },
    status: String(status),
    bounded: true,
  };
}
