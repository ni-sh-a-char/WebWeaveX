package io.webweavex.reconstruction;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.reconstruction.runtime_memory_reconstruction.reconstruct_runtime_memory}. */
public final class MemoryReconstruction {

    private MemoryReconstruction() {
    }

    public static Map<String, Object> reconstructRuntimeMemory(
            Map<String, Object> memoryIr, Map<String, Object> semantic, Map<String, Object> lineage) {
        Map<String, Object> mem = memoryIr == null ? new LinkedHashMap<>() : memoryIr;
        Map<String, Object> sem = semantic == null ? new LinkedHashMap<>() : semantic;
        Map<String, Object> lin = lineage == null ? new LinkedHashMap<>() : lineage;

        // history_list
        Object runtimeHistory = Py.get(mem, "runtime_history", new LinkedHashMap<>());
        List<Object> historyList;
        if (runtimeHistory instanceof Map) {
            historyList = Py.asList(Py.get(runtimeHistory, "runtime_history", new ArrayList<>()));
            if (historyList == null) {
                historyList = new ArrayList<>();
            }
        } else if (runtimeHistory instanceof List) {
            historyList = Py.asList(runtimeHistory);
        } else {
            historyList = new ArrayList<>();
        }

        // lineage_entries = (lineage or memory_ir["lineage"]); if dict -> .get("lineage", body)
        Object lineageBody = Py.truthy(lin) ? lin : Py.get(mem, "lineage", new LinkedHashMap<>());
        Object lineageEntries = lineageBody instanceof Map
                ? Py.get(lineageBody, "lineage", lineageBody) : lineageBody;

        List<Object> lineageList = lineageEntries instanceof List
                ? new ArrayList<>((List<Object>) lineageEntries) : new ArrayList<>();
        lineageList.sort(java.util.Comparator.comparing(
                it -> Py.str(Py.get(it, "id", "")), Normalization::codePointCompare));

        List<Object> syncHistory = new ArrayList<>();
        for (Object item : historyList) {
            if ("sync".equals(Py.get(item, "kind", null))) {
                syncHistory.add(item);
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("semantic_memory", new LinkedHashMap<>(
                Py.truthy(sem) ? sem : asMap(Py.get(mem, "semantic", new LinkedHashMap<>()))));
        out.put("lineage", lineageList);
        out.put("continuity", new LinkedHashMap<>(asMap(Py.get(mem, "knowledge", new LinkedHashMap<>()))));
        out.put("runtime_graph_memory",
                new LinkedHashMap<>(asMap(Py.get(mem, "memory_graphs", new LinkedHashMap<>()))));
        out.put("synchronization_history", syncHistory);
        out.put("bounded", true);
        return out;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }
}
