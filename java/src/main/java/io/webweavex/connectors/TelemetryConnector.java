package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.connectors.telemetry_connector_engine.extract_telemetry_runtime}.
 * Fully self-contained deterministic transform over a caller-supplied snapshot.
 */
public final class TelemetryConnector {

    private TelemetryConnector() {
    }

    /** {@code extract_telemetry_runtime}. */
    public static Map<String, Object> extractTelemetryRuntime(
            List<Object> backends, Map<String, Object> snapshot) {
        List<Object> backendList = Connectors.orDefault(
                backends, Connectors.list("opentelemetry", "prometheus", "jaeger"));
        Map<String, Object> snap = Connectors.snap(snapshot);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("backends", Connectors.sortedByStr(backendList));
        out.put("metrics", Connectors.getList(snap, "metrics", new ArrayList<>()));
        out.put("traces", Connectors.getList(snap, "traces", new ArrayList<>()));
        out.put("spans", Connectors.slice(Connectors.getList(snap, "spans", new ArrayList<>()), 10000));
        out.put("logs", Connectors.slice(Connectors.getList(snap, "logs", new ArrayList<>()), 10000));
        out.put("distributed_correlations", Connectors.getList(snap, "correlations", new ArrayList<>()));
        out.put("degraded", Py.get(snap, "degraded", false));
        out.put("bounded", true);
        return out;
    }
}
