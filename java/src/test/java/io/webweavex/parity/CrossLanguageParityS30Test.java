package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.distributed.AutonomousExtraction;
import io.webweavex.kernel.RuntimeKernel;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-30 cross-language parity: the 3 PORT-APPROVED aggregators are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s30.json}). {@code RuntimeKernel.run_pipeline} routes to the five
 * already-certified runtime orchestrators; {@code get_runtime_kernel} is certified via run_pipeline
 * projection parity; {@code run_autonomous_extraction} is the pure distributed scheduler (portable
 * flag contract).
 */
class CrossLanguageParityS30Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS30Test.class
                .getResourceAsStream("/parity/golden_vectors_s30.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s30.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s30 golden vectors", e);
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

    private static List<String> phases(JsonNode in) {
        JsonNode n = in.get("phases");
        if (n == null || n.isNull()) {
            return null;
        }
        List<String> out = new ArrayList<>();
        for (JsonNode e : n) {
            out.add(e.asText());
        }
        return out;
    }

    private static Object runtimeKernel(JsonNode in) {
        RuntimeKernel k = new RuntimeKernel(s(in, "runtime_type", "browser"));
        Map<String, Object> sources = m(in, "sources");
        return k.runPipeline(sources == null ? new java.util.LinkedHashMap<>() : sources,
                lng(in, "tick", 0), phases(in), m(in, "options"));
    }

    @TestFactory
    List<DynamicTest> portApprovedAggregators() {
        List<DynamicTest> t = new ArrayList<>();

        t.addAll(section("RuntimeKernel", CrossLanguageParityS30Test::runtimeKernel));

        // get_runtime_kernel — projection parity: fresh singleton's run_pipeline == fresh kernel's.
        t.addAll(section("get_runtime_kernel", in -> {
            RuntimeKernel.resetSingletonForTest();
            return RuntimeKernel.getRuntimeKernel(s(in, "runtime_type", "browser"))
                    .runPipeline(new java.util.LinkedHashMap<>(), lng(in, "tick", 0));
        }));

        t.addAll(section("run_autonomous_extraction", in -> AutonomousExtraction.runAutonomousExtraction(
                l(in, "tasks"), l(in, "workers"), lng(in, "tick", 0),
                in.has("objective_execution") && in.get("objective_execution").asBoolean(),
                "monitor_metrics")));

        return t;
    }
}
