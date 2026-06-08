/**
 * Converted from Python: core/connectors/runtime_stream_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractKafkaRuntime } from "./kafkaConnectorEngine.js";
import { extractRedisRuntime } from "./redisConnectorEngine.js";
import { extractWebsocketRuntime } from "./websocketConnectorEngine.js";

export function extractRuntimeStreams(stream_types: any = null, snapshot: any = null): any {
  stream_types = py.or2(stream_types, () => (["kafka", "redis", "websocket"]));
  var snap: any = py.or2(snapshot, () => ({}));
  var streams: any[] = [];
  var stream_type: any;
  for (stream_type of py.iter(py.sorted(stream_types))) {
    try {
      if (py.eq(stream_type, "kafka")) {
        py.listAppend(streams, extractKafkaRuntime(py.get(snap, "kafka")));
      } else if (py.eq(stream_type, "redis")) {
        var redis: any = extractRedisRuntime(py.get(snap, "redis"));
        py.listAppend(streams, {"stream_type": "redis_streams", "topics": py.get(redis, "streams", []), "offsets": {}, "event_lineage": [], "bounded": true});
      } else if (py.eq(stream_type, "websocket")) {
        var ws: any = extractWebsocketRuntime(py.get(snap, "websocket"));
        py.listAppend(streams, {"stream_type": "websocket", "topics": py.get(ws, "connections", []), "offsets": {}, "event_lineage": [], "bounded": true});
      } else if (py.contains(["sse", "queue"], stream_type)) {
        py.listAppend(streams, {"stream_type": stream_type, "topics": [...py.iter(py.get(py.get(snap, stream_type, {}), "topics", []))], "offsets": {}, "event_lineage": [], "bounded": true});
      }
    } catch (_e: any) {
      py.listAppend(streams, {"stream_type": stream_type, "degraded": true, "bounded": true});
    }
  }
  return {"streams": streams, "count": py.len(streams), "bounded": true};
}
export { extractKafkaRuntime, extractRedisRuntime, extractWebsocketRuntime };
