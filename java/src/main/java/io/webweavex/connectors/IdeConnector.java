package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.connectors.ide_connector_engine.extract_ide_runtime} — deterministic
 * transform over a caller-supplied IDE snapshot; no live connection. Dependency-clean
 * (single-module closure).
 */
public final class IdeConnector {

    private IdeConnector() {
    }

    /** {@code extract_ide_runtime(ide="vscode", snapshot=None)}. */
    public static Map<String, Object> extractIdeRuntime(String ide, Map<String, Object> snapshot) {
        Map<String, Object> snap = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ide", ide);
        out.put("open_files", Connectors.sortedByStr(Connectors.getList(snap, "open_files", new ArrayList<>())));
        out.put("terminals", Connectors.getList(snap, "terminals", new ArrayList<>()));
        out.put("tabs", Connectors.getList(snap, "tabs", new ArrayList<>()));
        out.put("workspace_topology", Connectors.getMap(snap, "workspace"));
        out.put("debug_sessions", Connectors.getList(snap, "debug_sessions", new ArrayList<>()));
        out.put("degraded", Py.get(snap, "degraded", false));
        out.put("bounded", true);
        return out;
    }
}
