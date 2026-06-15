package io.webweavex.reconstruction;

import io.webweavex.crypto.Hashing;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.reconstruction.runtime_reconstruction_engine.reconstruct_runtime}. */
public final class RuntimeReconstruction {

    private RuntimeReconstruction() {
    }

    public static Map<String, Object> reconstructRuntime(
            Map<String, Object> semanticIr,
            Map<String, Object> workflowIr,
            Map<String, Object> synchronizationIr,
            Map<String, Object> executionIr,
            Map<String, Object> memoryIr,
            Map<String, Object> runtimeGraph,
            String runtimeType,
            long tick) {

        List<Object> nodes = Py.asList(Py.get(runtimeGraph == null ? Map.of() : runtimeGraph,
                "nodes", new ArrayList<>()));

        Map<String, Object> canonical = new LinkedHashMap<>();
        canonical.put("semantic", orEmpty(semanticIr));
        canonical.put("workflow", orEmpty(workflowIr));
        canonical.put("sync", orEmpty(synchronizationIr));
        canonical.put("execution", orEmpty(executionIr));
        canonical.put("memory", orEmpty(memoryIr));
        canonical.put("graph_nodes", (long) (nodes == null ? 0 : nodes.size()));
        canonical.put("runtime_type", runtimeType);
        canonical.put("tick", tick);

        String json = PyJson.dumpsDefaultAscii(canonical);
        String runtimeId = Hashing.sha256Hex(json.getBytes(StandardCharsets.UTF_8)).substring(0, 32);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("runtime_id", runtimeId);
        out.put("runtime_type", runtimeType);
        out.put("reconstructed", true);
        out.put("graph_grounded", Py.truthy(runtimeGraph));
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> orEmpty(Map<String, Object> m) {
        return m == null ? new LinkedHashMap<>() : m;
    }
}
