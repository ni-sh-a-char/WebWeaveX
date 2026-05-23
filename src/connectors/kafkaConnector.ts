/** Port of core/connectors/kafka_connector_engine.py */
export function extractKafkaRuntime(
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    broker_type: "kafka",
    topics: [...((snapshot.topics as unknown[]) ?? [])].map(String).sort(),
    partitions: [...((snapshot.partitions as unknown[]) ?? [])],
    consumer_groups: [...((snapshot.consumer_groups as unknown[]) ?? [])],
    metrics: { ...((snapshot.metrics as Record<string, unknown>) ?? {}) },
    degraded: Boolean(snapshot.degraded ?? false),
    bounded: true,
  };
}
