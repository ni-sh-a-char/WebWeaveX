export function extractTelemetryRuntime(
  backends: string[] = ["opentelemetry", "prometheus", "jaeger"],
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    backends: [...backends].sort(),
    metrics: [...((snapshot.metrics as unknown[]) ?? [])],
    traces: [...((snapshot.traces as unknown[]) ?? [])],
    spans: [...((snapshot.spans as unknown[]) ?? [])].slice(0, 10000),
    logs: [...((snapshot.logs as unknown[]) ?? [])].slice(0, 10000),
    distributed_correlations: [...((snapshot.correlations as unknown[]) ?? [])],
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
