export function federateStreamRuntimes(
  streams: Record<string, unknown>[] = [],
): Record<string, unknown> {
  const events = streams.flatMap((s) => {
    const nested = (s.stream_runtime as Record<string, unknown>)?.events;
    return (nested as unknown[]) ?? (s.events as unknown[]) ?? [];
  });
  return {
    events: events.slice(0, 10_000),
    stream_count: streams.length,
    bounded: true,
  };
}
