package io.webweavex.memory;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.native.native_memory_engine} — {@code save_native_runtime} /
 * {@code load_native_runtime}. Dependency-clean (0 forbidden, importable; the persistence path is
 * not OS-coupled — only {@code run_native_cognition}/{@code extract_native} are platform-bound).
 * Delegates to the shared Kaalka-session-envelope persistence in {@link MemoryPersistence}.
 * (Placed in the {@code memory} package since {@code native} is a reserved Java keyword.) Zero new
 * substrate.
 */
public final class NativeRuntimePersistence {

    private NativeRuntimePersistence() {
    }

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    private static Map<String, Object> emptyRuntime() {
        Map<String, Object> m = map();
        m.put("accessibility_trees", map());
        m.put("windows", map());
        m.put("workflows", map());
        m.put("runtime_graphs", map());
        m.put("electron_state", map());
        m.put("terminal_streams", map());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_native_runtime(path, runtime, key)}. */
    public static Map<String, Object> saveNativeRuntime(String path, Map<String, Object> runtime, String key) {
        return MemoryPersistence.saveSessionEnvelope(path, runtime, key);
    }

    /** {@code load_native_runtime(path, key)}. */
    public static Map<String, Object> loadNativeRuntime(String path, String key) {
        return MemoryPersistence.loadSessionEnvelope(path, key, "runtime", emptyRuntime());
    }
}
