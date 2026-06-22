package io.webweavex.semantic;

import io.webweavex.determinism.Py;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.semantic.semantic_replay_engine.replay_semantic_runtime}. Dependency-clean
 * (0 forbidden, importable — the replay engine does not pull the bs4-coupled semantic stack). Pure
 * dict projection over a memory store. Zero new substrate.
 */
public final class SemanticReplay {

    private SemanticReplay() {
    }

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    /** {@code replay_semantic_runtime(memory)}. */
    public static Map<String, Object> replaySemanticRuntime(Map<String, Object> memory) {
        Map<String, Object> m = memory == null ? map() : memory;
        Map<String, Object> out = map();
        out.put("semantic_graph", Py.get(m, "semantic_graph", map()));
        out.put("ontology_mappings", Py.get(m, "ontology", map()));
        out.put("workflow_meaning", Py.get(m, "semantic_workflows", map()));
        out.put("semantic_propagation", Py.get(m, "runtime_semantics", map()));
        out.put("entity_mappings", Py.get(m, "entity_mappings", map()));
        out.put("replayed", true);
        out.put("bounded", true);
        return out;
    }
}
