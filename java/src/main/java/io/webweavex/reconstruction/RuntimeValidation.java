package io.webweavex.reconstruction;

import io.webweavex.determinism.Py;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.reconstruction.runtime_validation_engine.validate_reconstructed_runtime}. */
public final class RuntimeValidation {

    private RuntimeValidation() {
    }

    public static Map<String, Object> validateReconstructedRuntime(
            Map<String, Object> runtime, Map<String, Object> replay,
            Map<String, Object> topology, Map<String, Object> execution,
            Object mutations) {
        Map<String, Object> rt = runtime == null ? new LinkedHashMap<>() : runtime;
        Map<String, Object> rp = replay == null ? new LinkedHashMap<>() : replay;
        Map<String, Object> topo = topology == null ? new LinkedHashMap<>() : topology;
        Map<String, Object> exec = execution == null ? new LinkedHashMap<>() : execution;

        boolean replayOk = Py.truthy(Py.get(rp, "replay_chains", null))
                || Py.truthy(Py.get(rp, "replay_package", null))
                || Py.truthy(Py.get(rp, "replayed", null));

        boolean syncOk;
        boolean topologyOk;
        if (Py.truthy(topo)) {
            syncOk = Py.truthy(Py.get(topo, "synchronization_topology", null))
                    || Py.truthy(Py.get(topo, "reconstructed", null));
            topologyOk = Py.truthy(Py.get(topo, "runtime_graph", null))
                    || Py.truthy(Py.get(topo, "reconstructed", null));
        } else {
            syncOk = true;
            topologyOk = true;
        }

        boolean executionOk = Py.truthy(Py.get(exec, "executed", null))
                || Py.truthy(Py.get(exec, "actions", null))
                || Py.truthy(Py.get(rt, "reconstructed", null))
                || Py.truthy(Py.get(rt, "fabricated", null));

        List<Object> mutationList;
        if (mutations instanceof Map) {
            mutationList = Py.asList(Py.get(mutations, "mutations", new java.util.ArrayList<>()));
        } else {
            mutationList = Py.asList(mutations);
        }
        if (mutationList == null) {
            mutationList = new java.util.ArrayList<>();
        }
        boolean mutationOk = true;
        if (!mutationList.isEmpty()) {
            for (Object m : mutationList) {
                Map<String, Object> mm = Py.asMap(m);
                boolean has = mm != null && (mm.containsKey("kind") || mm.containsKey("target"));
                if (!has) {
                    mutationOk = false;
                    break;
                }
            }
        }

        boolean c0 = replayOk || Py.truthy(Py.get(rt, "replay_safe", null));
        boolean c1 = syncOk || topologyOk;
        boolean valid;
        if (Py.truthy(Py.get(rt, "reconstructed", null)) || Py.truthy(Py.get(rt, "fabricated", null))) {
            valid = c0 && c1 && topologyOk && executionOk && mutationOk;
        } else {
            valid = Py.truthy(rt) && replayOk;
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("valid", valid);
        out.put("integrity_score", valid ? 1.0 : 0.0);
        out.put("replay_integrity", replayOk);
        out.put("synchronization_integrity", syncOk);
        out.put("topology_integrity", topologyOk);
        out.put("execution_integrity", executionOk);
        out.put("mutation_consistency", mutationOk);
        out.put("bounded", true);
        return out;
    }
}
