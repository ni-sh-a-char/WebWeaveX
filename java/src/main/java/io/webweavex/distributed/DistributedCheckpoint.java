package io.webweavex.distributed;

import io.webweavex.memory.MemoryPersistence;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.distributed_extraction.distributed_checkpoint_engine} —
 * {@code save_distributed_checkpoint} / {@code load_distributed_checkpoint}. Dependency-clean
 * (0 forbidden, importable). Delegates to the shared Kaalka-session-envelope persistence in
 * {@link MemoryPersistence} (single centralized file-I/O path). Zero new substrate.
 */
public final class DistributedCheckpoint {

    private DistributedCheckpoint() {
    }

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    private static Map<String, Object> emptyCheckpoint() {
        Map<String, Object> graph = map();
        graph.put("nodes", new ArrayList<>());
        graph.put("edges", new ArrayList<>());
        Map<String, Object> stream = map();
        stream.put("events", new ArrayList<>());
        Map<String, Object> m = map();
        m.put("queue", new ArrayList<>());
        m.put("workers", new ArrayList<>());
        m.put("runtime_graph", graph);
        m.put("identities", new ArrayList<>());
        m.put("adaptive_memory", map());
        m.put("stream_runtime", stream);
        m.put("tick", 0L);
        m.put("bounded", true);
        return m;
    }

    /** {@code save_distributed_checkpoint(path, checkpoint, key)}. */
    public static Map<String, Object> saveDistributedCheckpoint(String path, Map<String, Object> checkpoint,
            String key) {
        return MemoryPersistence.saveSessionEnvelope(path, checkpoint, key);
    }

    /** {@code load_distributed_checkpoint(path, key)}. */
    public static Map<String, Object> loadDistributedCheckpoint(String path, String key) {
        return MemoryPersistence.loadSessionEnvelope(path, key, "checkpoint", emptyCheckpoint());
    }
}
