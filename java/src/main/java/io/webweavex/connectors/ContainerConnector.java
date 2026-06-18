package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Port of {@code core.connectors.container_connector_engine.extract_container_runtime} and its
 * {@code docker_connector_engine.extract_docker_runtime} sub-engine. Deterministic transform over
 * a caller-supplied snapshot; no live connection. Dependency-clean (2-module closure).
 */
public final class ContainerConnector {

    private ContainerConnector() {
    }

    /** {@code extract_container_runtime(runtime="docker", snapshot=None)}. */
    public static Map<String, Object> extractContainerRuntime(String runtime, Map<String, Object> snapshot) {
        String normalized = runtime.toLowerCase(Locale.ROOT);
        Map<String, Object> snap = Connectors.snap(snapshot);
        try {
            if (normalized.equals("docker") || normalized.equals("podman") || normalized.equals("oci")) {
                Map<String, Object> result = extractDockerRuntime(snap);
                result.put("runtime", normalized);
                return result;
            }
        } catch (RuntimeException e) {
            return degraded(normalized);
        }
        return degraded(normalized);
    }

    private static Map<String, Object> degraded(String runtime) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("runtime", runtime);
        out.put("containers", new ArrayList<>());
        out.put("images", new ArrayList<>());
        out.put("volumes", new ArrayList<>());
        out.put("networks", new ArrayList<>());
        out.put("degraded", true);
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_docker_runtime(snapshot=None)}. */
    public static Map<String, Object> extractDockerRuntime(Map<String, Object> snapshot) {
        Map<String, Object> snap = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("runtime", "docker");
        out.put("containers", Connectors.getList(snap, "containers", new ArrayList<>()));
        out.put("images", Connectors.sortedByStr(Connectors.getList(snap, "images", new ArrayList<>())));
        out.put("volumes", Connectors.getList(snap, "volumes", new ArrayList<>()));
        out.put("networks", Connectors.getList(snap, "networks", new ArrayList<>()));
        out.put("states", Connectors.getMap(snap, "states"));
        out.put("health", Connectors.getMap(snap, "health"));
        out.put("degraded", Py.get(snap, "degraded", false));
        out.put("bounded", true);
        return out;
    }
}
