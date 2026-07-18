package io.webweavex.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-35 parser-pipeline certification: the remaining pure, non-epistemic parser engines that feed
 * {@code compile_repository_ir}'s observable output — {@code resolveApiSurface}, {@code buildSemanticGraph},
 * {@code requireParserEvidence} — are byte-identical to Python 3.0.0 ({@code parser_vectors_s35.json}).
 * The epistemic {@code normalize_parser_output} is discarded downstream (FRONTIER_ANALYSIS) and not ported;
 * {@code parse_ast} composes with the S33 AST foundation later.
 */
class ParserEnginesS35Test {

    private static JsonNode golden() {
        try (InputStream in = ParserEnginesS35Test.class.getResourceAsStream("/parity/parser_vectors_s35.json")) {
            if (in == null) {
                throw new IllegalStateException("parser_vectors_s35.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s35 parser vectors", e);
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

    private static String s(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return n == null || n.isNull() ? "" : n.asText();
    }

    private static Object toNative(JsonNode n) {
        if (n == null || n.isNull()) {
            return null;
        }
        if (n.isObject()) {
            Map<String, Object> m = new LinkedHashMap<>();
            n.fields().forEachRemaining(e -> m.put(e.getKey(), toNative(e.getValue())));
            return m;
        }
        if (n.isArray()) {
            List<Object> l = new ArrayList<>();
            n.forEach(e -> l.add(toNative(e)));
            return l;
        }
        if (n.isBoolean()) {
            return n.asBoolean();
        }
        if (n.isIntegralNumber()) {
            return n.asLong();
        }
        if (n.isNumber()) {
            return n.asDouble();
        }
        return n.asText();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> m(JsonNode in, String f) {
        return (Map<String, Object>) toNative(in.get(f));
    }

    @TestFactory
    List<DynamicTest> parserPipeline() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("resolve_api_surface", in -> ParserEngines.resolveApiSurface(s(in, "source"), "text")));
        t.addAll(section("build_semantic_graph", in -> ParserEngines.buildSemanticGraph(m(in, "parsed"))));
        t.addAll(section("require_parser_evidence", in -> ParserEngines.requireParserEvidence(m(in, "parsed"))));
        return t;
    }
}

