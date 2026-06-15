package io.webweavex.memory;

import io.webweavex.crypto.Hashing;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Ports of {@code core.memory.runtime_memory_engine.build_runtime_memory} and
 * {@code core.memory.stable_memory_hash.stable_memory_hash}.
 */
public final class RuntimeMemory {

    private RuntimeMemory() {
    }

    public static Map<String, Object> build(
            List<Object> runtimeHistory, List<Object> lineage, List<Object> semanticRelations) {
        List<Object> history = runtimeHistory == null ? new ArrayList<>() : new ArrayList<>(runtimeHistory);
        List<Object> lin = lineage == null ? new ArrayList<>() : new ArrayList<>(lineage);
        List<Object> rel = semanticRelations == null ? new ArrayList<>() : new ArrayList<>(semanticRelations);

        StringBuilder payload = new StringBuilder();
        List<String> parts = new ArrayList<>();
        for (Object item : history) {
            parts.add(Py.str(tickOrStep(item, "")));
        }
        for (Object item : lin) {
            parts.add(Py.str(Py.get(item, "id", "")));
        }
        payload.append(String.join("|", parts));
        String memoryId = Hashing.sha256Hex(payload.toString().getBytes(StandardCharsets.UTF_8))
                .substring(0, 32);

        List<Object> sortedHistory = new ArrayList<>(history);
        sortedHistory.sort(Comparator.comparingLong(it -> toLong(tickOrStep(it, 0L))));

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("memory_id", memoryId);
        result.put("runtime_history", sortedHistory);
        result.put("workflow_history", filterKind(history, "workflow"));
        result.put("synchronization_history", filterKind(history, "sync"));
        result.put("evolution_history", filterKind(history, "evolution"));

        List<Object> sortedLineage = new ArrayList<>(lin);
        sortedLineage.sort(Comparator.comparing(it -> Py.str(Py.get(it, "id", "")),
                Normalization::codePointCompare));
        result.put("lineage", sortedLineage);

        List<Object> sortedRel = new ArrayList<>(rel);
        sortedRel.sort(Comparator
                .comparing((Object it) -> Py.str(Py.get(it, "from", "")), Normalization::codePointCompare)
                .thenComparing(it -> Py.str(Py.get(it, "to", "")), Normalization::codePointCompare));
        result.put("semantic_relations", sortedRel);
        result.put("bounded", true);

        result.put("stable_hash", stableMemoryHash(result));
        return result;
    }

    /** Port of {@code stable_memory_hash(memory)}. */
    public static String stableMemoryHash(Map<String, Object> memory) {
        List<Object> history = listOf(Py.get(memory, "runtime_history", new ArrayList<>()));
        List<Object> lineage = listOf(Py.get(memory, "lineage", new ArrayList<>()));
        List<Object> relations = listOf(Py.get(memory, "semantic_relations", new ArrayList<>()));

        List<Object> sortedHistory = new ArrayList<>(history);
        sortedHistory.sort(Comparator
                .comparingLong((Object h) -> toLong(Py.get(h, "tick", 0L)))
                .thenComparing(h -> Py.str(Py.get(h, "kind", "")), Normalization::codePointCompare)
                .thenComparing(h -> Py.str(Py.get(h, "source", "")), Normalization::codePointCompare));

        List<Object> sortedLineage = new ArrayList<>(lineage);
        sortedLineage.sort(Comparator.comparing(x -> Py.str(Py.get(x, "id", "")),
                Normalization::codePointCompare));

        List<Object> sortedRel = new ArrayList<>(relations);
        sortedRel.sort(Comparator
                .comparing((Object r) -> Py.str(Py.get(r, "from", "")), Normalization::codePointCompare)
                .thenComparing(r -> Py.str(Py.get(r, "to", "")), Normalization::codePointCompare));

        Map<String, Object> canonical = new LinkedHashMap<>();
        canonical.put("memory_id", Py.get(memory, "memory_id", ""));
        canonical.put("runtime_history", sortedHistory);
        canonical.put("lineage", sortedLineage);
        canonical.put("semantic_relations", sortedRel);
        return Kaalka.computeKaalkaHash(PyJson.dumpsCompactAscii(canonical));
    }

    /** {@code item.get("tick", item.get("step", default))}. */
    private static Object tickOrStep(Object item, Object dflt) {
        Map<String, Object> m = Py.asMap(item);
        if (m == null) {
            return dflt;
        }
        if (m.containsKey("tick")) {
            return m.get("tick");
        }
        return m.containsKey("step") ? m.get("step") : dflt;
    }

    private static List<Object> filterKind(List<Object> history, String kind) {
        List<Object> out = new ArrayList<>();
        for (Object item : history) {
            if (kind.equals(Py.get(item, "kind", null))) {
                out.add(item);
            }
        }
        return out;
    }

    private static long toLong(Object o) {
        if (o instanceof Number) {
            return ((Number) o).longValue();
        }
        try {
            return Long.parseLong(String.valueOf(o));
        } catch (NumberFormatException e) {
            return 0L;
        }
    }

    private static List<Object> listOf(Object o) {
        List<Object> l = Py.asList(o);
        return l == null ? new ArrayList<>() : l;
    }
}
