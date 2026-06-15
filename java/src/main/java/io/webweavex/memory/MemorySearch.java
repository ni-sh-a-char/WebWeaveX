package io.webweavex.memory;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Port of {@code core.memory.runtime_search_engine.search_runtime_memory}. */
public final class MemorySearch {

    private MemorySearch() {
    }

    public static Map<String, Object> searchRuntimeMemory(
            Map<String, Object> index, String term, String searchType) {
        List<Object> matches = new ArrayList<>();
        String normalized = term.toLowerCase(Locale.ROOT).strip();

        switch (searchType) {
            case "semantic":
                for (Map.Entry<String, Object> e : bucket(index, "entity_index").entrySet()) {
                    if (e.getKey().toLowerCase(Locale.ROOT).contains(normalized)) {
                        matches.add(match(e.getKey(), e.getValue(), "entity"));
                    }
                }
                break;
            case "lineage":
                for (Map.Entry<String, Object> e : bucket(index, "workflow_index").entrySet()) {
                    if (e.getKey().toLowerCase(Locale.ROOT).contains(normalized)) {
                        matches.add(match(e.getKey(), e.getValue(), "workflow"));
                    }
                }
                break;
            case "graph":
                for (Map.Entry<String, Object> e : bucket(index, "graph_index").entrySet()) {
                    matches.add(match(e.getKey(), e.getValue(), "graph"));
                }
                break;
            default:
                for (String b : new String[] {"entity_index", "workflow_index", "connector_index"}) {
                    for (Map.Entry<String, Object> e : bucket(index, b).entrySet()) {
                        if (e.getKey().toLowerCase(Locale.ROOT).contains(normalized)
                                || Py.str(e.getValue()).toLowerCase(Locale.ROOT).contains(normalized)) {
                            matches.add(match(e.getKey(), e.getValue(), b));
                        }
                    }
                }
        }

        matches.sort((a, b) -> Normalization.codePointCompare(
                Py.str(Py.get(a, "match", "")), Py.str(Py.get(b, "match", ""))));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("search_type", searchType);
        out.put("term", term);
        out.put("matches", matches);
        out.put("count", (long) matches.size());
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> match(String key, Object value, String kind) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("match", key);
        m.put("value", value);
        m.put("kind", kind);
        return m;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> bucket(Map<String, Object> index, String name) {
        Object b = Py.get(index, name, new LinkedHashMap<>());
        return b instanceof Map ? (Map<String, Object>) b : new LinkedHashMap<>();
    }
}
