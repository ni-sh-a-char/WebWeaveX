import { extractKafkaRuntime } from "./kafkaConnector.js";
import { extractRedisRuntime } from "./redisConnector.js";
import { extractWebsocketRuntime } from "./websocketConnector.js";

export function extractRuntimeStreamRuntime(
  streamTypes: string[] = ["kafka", "redis", "websocket"],
  snapshot: Record<string, unknown> = {},
): Record<string, unknown> {
  const streams: Record<string, unknown>[] = [];
  for (const t of [...streamTypes].sort()) {
    if (t === "kafka") streams.push(extractKafkaRuntime((snapshot.kafka as Record<string, unknown>) ?? {}));
    else if (t === "redis") {
      const r = extractRedisRuntime((snapshot.redis as Record<string, unknown>) ?? {});
      streams.push({ stream_type: "redis_streams", ...r });
    } else if (t === "websocket") {
      streams.push(extractWebsocketRuntime((snapshot.websocket as Record<string, unknown>) ?? {}));
    }
  }
  return { streams, bounded: true };
}
