export function federateStreamRuntimes(
  streams: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const events = streams.flatMap((s) => (s.events as unknown[]) ?? []);
  return {
    events: events.slice(0, 10000),
    worker_count: streams.length,
    bounded: true,
  };
}
