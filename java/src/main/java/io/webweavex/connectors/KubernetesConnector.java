package io.webweavex.connectors;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.connectors.kubernetes_connector_engine.extract_kubernetes_runtime} —
 * deterministic transform over a caller-supplied cluster snapshot; no live connection.
 * Dependency-clean (single-module closure).
 */
public final class KubernetesConnector {

    private KubernetesConnector() {
    }

    /** {@code extract_kubernetes_runtime(snapshot=None)}. */
    public static Map<String, Object> extractKubernetesRuntime(Map<String, Object> snapshot) {
        Map<String, Object> snap = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("namespaces", Connectors.sortedByStr(
                Connectors.getList(snap, "namespaces", Connectors.list("default"))));
        out.put("pods", sortedByNameStr(Connectors.getList(snap, "pods", new ArrayList<>())));
        out.put("deployments", sortedByNameStr(Connectors.getList(snap, "deployments", new ArrayList<>())));
        out.put("services", Connectors.getList(snap, "services", new ArrayList<>()));
        out.put("ingress", Connectors.getList(snap, "ingress", new ArrayList<>()));
        out.put("topology", Connectors.getMap(snap, "topology"));
        out.put("events", Connectors.slice(Connectors.getList(snap, "events", new ArrayList<>()), 5000));
        out.put("degraded", Py.get(snap, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    /** {@code sorted(xs, key=lambda item: str(item.get("name", item)))} — stable, code-point order. */
    @SuppressWarnings("unchecked")
    private static List<Object> sortedByNameStr(List<Object> xs) {
        List<Object> c = new ArrayList<>(xs);
        c.sort((a, b) -> Normalization.codePointCompare(nameKey(a), nameKey(b)));
        return c;
    }

    /** {@code str(item.get("name", item))} — Python {@code str()} of the name, or of the item. */
    private static String nameKey(Object item) {
        if (item instanceof Map) {
            Map<String, Object> m = (Map<String, Object>) item;
            if (m.containsKey("name")) {
                return PyRepr.str(m.get("name"));
            }
        }
        return PyRepr.str(item);
    }
}
