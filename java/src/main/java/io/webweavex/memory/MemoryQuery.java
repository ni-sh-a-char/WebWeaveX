package io.webweavex.memory;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.memory.runtime_query_engine.query_runtime_memory}. */
public final class MemoryQuery {

    private MemoryQuery() {
    }

    public static Map<String, Object> queryRuntimeMemory(
            Map<String, Object> memory, String queryType, String term) {
        List<Object> results = new ArrayList<>();

        switch (queryType) {
            case "semantic":
                for (Object r : list(memory, "semantic_relations")) {
                    if (Py.str(Py.get(r, "from", "")).contains(term)
                            || Py.str(Py.get(r, "to", "")).contains(term)) {
                        results.add(r);
                    }
                }
                break;
            case "lineage":
                for (Object it : list(memory, "lineage")) {
                    if (Py.str(Py.get(it, "id", "")).contains(term)) {
                        results.add(it);
                    }
                }
                break;
            case "topology":
                for (Object it : list(memory, "runtime_history")) {
                    if (Py.str(Py.get(it, "runtime", "")).contains(term)) {
                        results.add(it);
                    }
                }
                break;
            case "sync":
                results.addAll(list(memory, "synchronization_history"));
                break;
            default:
                for (Object it : list(memory, "runtime_history")) {
                    if (PyRepr.str(it).contains(term)) {
                        results.add(it);
                    }
                }
        }

        results.sort((a, b) -> Normalization.codePointCompare(PyRepr.str(a), PyRepr.str(b)));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("query_type", queryType);
        out.put("term", term);
        out.put("results", results);
        out.put("count", (long) results.size());
        out.put("bounded", true);
        return out;
    }

    private static List<Object> list(Map<String, Object> memory, String key) {
        List<Object> l = Py.asList(Py.get(memory, key, new ArrayList<>()));
        return l == null ? new ArrayList<>() : l;
    }
}
