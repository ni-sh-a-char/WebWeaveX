package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.streaming.StreamingRuntime;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-14 cross-language parity: the dependency-clean, serializable subset of the
 * {@code core.streaming} + {@code core.connectors.live_runtime} family
 * (io.webweavex.streaming.StreamingRuntime) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s14.json}) via {@code stable_serialize} + {@code compute_kaalka_hash}.
 *
 * <p>{@code run_live_runtime} is intentionally excluded: its output is self-referential
 * (payload.memory.snapshots == payload), so {@code stable_serialize} recurses infinitely in
 * Python itself — it is not byte-exact-certifiable. The Java port remains in source (faithful)
 * but is not a parity-proven manifest API. Engine-level vectors exercise the same code paths via
 * a non-cyclic {@code live} dict.
 */
class CrossLanguageParityS14Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS14Test.class
                .getResourceAsStream("/parity/golden_vectors_s14.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s14.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s14 golden vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs"));
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> m(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> l(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    private static long lng(JsonNode in, String f, long d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asLong();
    }

    @SuppressWarnings("unchecked")
    private static Object resolve(Object obj, String path) {
        Object cur = obj;
        for (String part : path.split("\\.")) {
            cur = (cur instanceof Map) ? ((Map<String, Object>) cur).getOrDefault(part, new java.util.LinkedHashMap<>())
                    : new java.util.LinkedHashMap<>();
        }
        return cur;
    }

    /** Projection-parity: compare every non-cyclic output path against the Python oracle. */
    private List<DynamicTest> projection(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object result = fn.apply(v.get("inputs"));
                for (JsonNode p : v.get("projections")) {
                    Object value = resolve(result, p.get("path").asText());
                    assertEquals(p.get("serialized").asText(), StableSerialize.stableSerialize(value),
                            "path=" + p.get("path").asText());
                    assertEquals(p.get("hash").asText(), Kaalka.computeKaalkaHash(value),
                            "path=" + p.get("path").asText());
                }
            }));
        }
        return tests;
    }

    // ---- manifest APIs ----

    @TestFactory
    List<DynamicTest> buildStreamTimeline() {
        return section("build_stream_timeline", in -> StreamingRuntime.buildStreamTimeline(l(in, "events")));
    }

    @TestFactory
    List<DynamicTest> replayStreamEvents() {
        return section("replay_stream_events", in -> StreamingRuntime.replayStreamEvents(l(in, "stream_log")));
    }

    @TestFactory
    List<DynamicTest> runLiveRuntime() {
        return projection("run_live_runtime", in -> StreamingRuntime.runLiveRuntime(
                m(in, "config"), m(in, "snapshot"), m(in, "memory"), lng(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> saveLiveRuntime() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_live_runtime")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = StreamingRuntime.saveLiveRuntime(
                        target.toString(), m(in, "memory"), in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
                assertEquals(target.toString(), ret.get("path"));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> loadLiveRuntime() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_live_runtime")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = StreamingRuntime.loadLiveRuntime(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = StreamingRuntime.loadLiveRuntime(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }

    // ---- engine-level parity ----

    @TestFactory
    List<DynamicTest> engineSections() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("extract_filesystem_runtime", in -> StreamingRuntime.extractFilesystemRuntime(
                s(in, "root", "."), m(in, "snapshot"))));
        t.addAll(section("extract_cicd_runtime", in -> StreamingRuntime.extractCicdRuntime(
                s(in, "provider", "github_actions"), m(in, "snapshot"))));
        t.addAll(section("build_live_topology_graph", in -> StreamingRuntime.buildLiveTopologyGraph(m(in, "live"))));
        t.addAll(section("compile_live_runtime_ir", in -> StreamingRuntime.compileLiveRuntimeIr(m(in, "live"))));
        t.addAll(section("live_runtime_ir_to_graph", in -> StreamingRuntime.liveRuntimeIrToGraph(m(in, "live_ir"))));
        t.addAll(section("remember_live_runtime", in -> StreamingRuntime.rememberLiveRuntime(
                m(in, "memory"), m(in, "update"))));
        return t;
    }

    /** Null-snapshot FS walk over a real flat temp dir; root normalized to {@code <ROOT>}. */
    @TestFactory
    List<DynamicTest> extractFilesystemWalk() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("extract_filesystem_walk")) {
            tests.add(DynamicTest.dynamicTest("fs_walk:" + v.get("name").asText(), () -> {
                for (JsonNode f : v.get("files")) {
                    Files.write(tempDir.resolve(f.asText()), new byte[0]);
                }
                Map<String, Object> result = StreamingRuntime.extractFilesystemRuntime(tempDir.toString(), null);
                result.put("root", "<ROOT>");
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(result));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(result));
            }));
        }
        return tests;
    }
}
