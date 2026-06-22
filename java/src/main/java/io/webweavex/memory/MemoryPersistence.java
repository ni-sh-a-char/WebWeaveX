package io.webweavex.memory;

import io.webweavex.crypto.Kaalka;
import io.webweavex.crypto.KaalkaSession;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyRepr;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of the four dependency-clean memory-persistence engine pairs —
 * {@code save/load_runtime_memory} ({@code core.memory}), {@code save/load_semantic_memory}
 * ({@code core.semantic}), {@code save/load_adaptive_memory} ({@code core.adaptive}), and
 * {@code save/load_application_memory} ({@code core.application}). All four import cleanly (no
 * eager-{@code __init__} bs4 barrier, verified at runtime). Two encryption envelopes are used by
 * canon: the Kaalka value envelope (runtime/semantic) and the Kaalka session envelope
 * (adaptive/application) — both already certified ({@link Kaalka}, {@link KaalkaSession}). Zero new
 * substrate.
 */
public final class MemoryPersistence {

    private MemoryPersistence() {
    }

    // -------------------------------------------------------------- helpers

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static void writeFile(Path target, String content) {
        try {
            Path parent = target.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            Files.write(target, content.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private static String readFile(Path target) {
        try {
            return new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private static Map<String, Object> savedResult(Path target) {
        Map<String, Object> out = map();
        out.put("saved", true);
        out.put("path", target.toString());
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- empty stores

    private static Map<String, Object> emptyRuntimeStore() {
        Map<String, Object> m = map();
        m.put("runtime", map());
        m.put("knowledge", map());
        m.put("semantic", map());
        m.put("index", map());
        m.put("graph", map());
        m.put("lineage", map());
        m.put("bounded", true);
        return m;
    }

    private static Map<String, Object> emptySemanticMemory() {
        Map<String, Object> m = map();
        m.put("ontology", map());
        m.put("semantic_graph", map());
        m.put("entity_mappings", map());
        m.put("semantic_workflows", map());
        m.put("runtime_semantics", map());
        m.put("bounded", true);
        return m;
    }

    private static Map<String, Object> emptyAdaptiveMemory() {
        Map<String, Object> m = map();
        m.put("selectors", map());
        m.put("healed_selectors", map());
        m.put("pagination_patterns", new ArrayList<>());
        m.put("modal_solutions", new ArrayList<>());
        m.put("interaction_chains", new ArrayList<>());
        m.put("bounded", true);
        return m;
    }

    private static Map<String, Object> emptyApplicationMemory() {
        Map<String, Object> m = map();
        m.put("workflows", map());
        m.put("forms", map());
        m.put("action_graphs", map());
        m.put("navigation_flows", map());
        m.put("dashboard_structures", map());
        m.put("bounded", true);
        return m;
    }

    // -------------------------------------------------------------- Pattern A: Kaalka value envelope

    private static Map<String, Object> saveValueEnvelope(String path, Map<String, Object> memory, String key) {
        String payload = PyJson.dumpsDefaultAscii(memory);
        Map<String, Object> encrypted = Kaalka.encryptValueEnvelope(payload, key);
        Map<String, Object> wrapper = map();
        wrapper.put("encrypted", encrypted.get("encrypted"));
        wrapper.put("algorithm", "kaalka");
        Path target = Paths.get(path);
        writeFile(target, PyJson.dumpsDefaultAscii(wrapper));
        return savedResult(target);
    }

    private static Map<String, Object> loadValueEnvelope(String path, String key, Map<String, Object> emptyStore) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("memory", emptyStore);
            out.put("bounded", true);
            return out;
        }
        Map<String, Object> wrapper = asMap(PyJsonParse.loads(readFile(target)));
        Map<String, Object> decrypted = Kaalka.decryptValueEnvelope(str(wrapper.get("encrypted")), key);
        Object memory = PyJsonParse.loads(str(decrypted.get("decrypted")));
        Map<String, Object> out = map();
        out.put("available", true);
        out.put("memory", memory);
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code save_runtime_memory(path, memory, key)}. */
    public static Map<String, Object> saveRuntimeMemory(String path, Map<String, Object> memory, String key) {
        return saveValueEnvelope(path, memory, key);
    }

    /** {@code load_runtime_memory(path, key)}. */
    public static Map<String, Object> loadRuntimeMemory(String path, String key) {
        return loadValueEnvelope(path, key, emptyRuntimeStore());
    }

    /** {@code save_semantic_memory(path, memory, key)}. */
    public static Map<String, Object> saveSemanticMemory(String path, Map<String, Object> memory, String key) {
        return saveValueEnvelope(path, memory, key);
    }

    /** {@code load_semantic_memory(path, key)}. */
    public static Map<String, Object> loadSemanticMemory(String path, String key) {
        return loadValueEnvelope(path, key, emptySemanticMemory());
    }

    // -------------------------------------------------------------- Pattern B: Kaalka session envelope

    private static Map<String, Object> saveSessionEnvelope(String path, Map<String, Object> memory, String key) {
        Map<String, Object> encrypted = KaalkaSession.encryptSessionState(memory, key);
        Path target = Paths.get(path);
        writeFile(target, PyJson.dumpsDefaultAscii(encrypted));
        return savedResult(target);
    }

    private static Map<String, Object> loadSessionEnvelope(String path, String key, Map<String, Object> emptyStore) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("memory", emptyStore);
            out.put("bounded", true);
            return out;
        }
        Map<String, Object> encrypted = asMap(PyJsonParse.loads(readFile(target)));
        Map<String, Object> decrypted = KaalkaSession.decryptSessionState(encrypted, key);
        Object memory = decrypted.containsKey("session") ? decrypted.get("session") : emptyStore;
        Map<String, Object> out = map();
        out.put("available", true);
        out.put("memory", memory);
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code save_adaptive_memory(path, memory, key)}. */
    public static Map<String, Object> saveAdaptiveMemory(String path, Map<String, Object> memory, String key) {
        return saveSessionEnvelope(path, memory, key);
    }

    /** {@code load_adaptive_memory(path, key)}. */
    public static Map<String, Object> loadAdaptiveMemory(String path, String key) {
        return loadSessionEnvelope(path, key, emptyAdaptiveMemory());
    }

    /** {@code save_application_memory(path, memory, key)}. */
    public static Map<String, Object> saveApplicationMemory(String path, Map<String, Object> memory, String key) {
        return saveSessionEnvelope(path, memory, key);
    }

    /** {@code load_application_memory(path, key)}. */
    public static Map<String, Object> loadApplicationMemory(String path, String key) {
        return loadSessionEnvelope(path, key, emptyApplicationMemory());
    }
}
