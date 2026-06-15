package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.connectors.runtime_stream_connector_engine.extract_runtime_streams}
 * and the kafka/websocket sub-engines (redis is reused from {@link DatabaseConnectors}).
 * Deterministic transform over a caller-supplied snapshot.
 */
public final class StreamConnectors {

    private StreamConnectors() {
    }

    /** {@code extract_runtime_streams}. */
    public static Map<String, Object> extractRuntimeStreams(
            List<Object> streamTypes, Map<String, Object> snapshot) {
        List<Object> types = Connectors.orDefault(
                streamTypes, Connectors.list("kafka", "redis", "websocket"));
        Map<String, Object> s = Connectors.snap(snapshot);
        List<Object> streams = new ArrayList<>();

        for (Object stO : Connectors.sortedByStr(types)) {
            String st = Py.str(stO);
            try {
                if (st.equals("kafka")) {
                    streams.add(extractKafkaRuntime(Py.asMap(Py.get(s, "kafka", null))));
                } else if (st.equals("redis")) {
                    Map<String, Object> redis =
                            DatabaseConnectors.extractRedisRuntime(Py.asMap(Py.get(s, "redis", null)));
                    Map<String, Object> entry = new LinkedHashMap<>();
                    entry.put("stream_type", "redis_streams");
                    entry.put("topics", Py.get(redis, "streams", new ArrayList<>()));
                    entry.put("offsets", new LinkedHashMap<>());
                    entry.put("event_lineage", new ArrayList<>());
                    entry.put("bounded", true);
                    streams.add(entry);
                } else if (st.equals("websocket")) {
                    Map<String, Object> ws =
                            extractWebsocketRuntime(Py.asMap(Py.get(s, "websocket", null)));
                    Map<String, Object> entry = new LinkedHashMap<>();
                    entry.put("stream_type", "websocket");
                    entry.put("topics", Py.get(ws, "connections", new ArrayList<>()));
                    entry.put("offsets", new LinkedHashMap<>());
                    entry.put("event_lineage", new ArrayList<>());
                    entry.put("bounded", true);
                    streams.add(entry);
                } else if (st.equals("sse") || st.equals("queue")) {
                    Map<String, Object> sub = Py.asMap(Py.get(s, st, null));
                    Map<String, Object> entry = new LinkedHashMap<>();
                    entry.put("stream_type", st);
                    entry.put("topics", Connectors.getList(Connectors.snap(sub), "topics", new ArrayList<>()));
                    entry.put("offsets", new LinkedHashMap<>());
                    entry.put("event_lineage", new ArrayList<>());
                    entry.put("bounded", true);
                    streams.add(entry);
                }
                // unknown stream types append nothing (mirrors Python)
            } catch (RuntimeException e) {
                Map<String, Object> entry = new LinkedHashMap<>();
                entry.put("stream_type", st);
                entry.put("degraded", true);
                entry.put("bounded", true);
                streams.add(entry);
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("streams", streams);
        out.put("count", (long) streams.size());
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_kafka_runtime}. */
    public static Map<String, Object> extractKafkaRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("stream_type", "kafka");
        out.put("topics", Connectors.sortedByStr(Connectors.getList(s, "topics", new ArrayList<>())));
        out.put("consumers", Connectors.getList(s, "consumers", new ArrayList<>()));
        out.put("offsets", Connectors.getMap(s, "offsets"));
        out.put("propagation_state", Py.str(Py.get(s, "state", "stable")));
        out.put("event_lineage", Connectors.getList(s, "lineage", new ArrayList<>()));
        out.put("degraded", Py.get(s, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_websocket_runtime}. */
    public static Map<String, Object> extractWebsocketRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("protocol", "websocket");
        out.put("connections", Connectors.getList(s, "connections", new ArrayList<>()));
        out.put("frames", Connectors.pyInt(Py.get(s, "frames", 0L)));
        out.put("bounded", true);
        return out;
    }
}
