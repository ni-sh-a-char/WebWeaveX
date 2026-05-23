export function recoverDistributedRuntime(
  checkpoint: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    recovered: true,
    queue: checkpoint.queue ?? [],
    workers: checkpoint.workers ?? [],
    tick: Number(checkpoint.tick ?? 0),
    bounded: true,
  };
}
