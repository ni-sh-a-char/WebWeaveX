package io.webweavex.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.LinkedHashMap;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-34 parser-engine certification: {@link ParserEngines} (text-path regex engines ported from
 * canonical Python {@code core.parsers.*}) is byte-identical to Python 2.1.0
 * ({@code parser_vectors_s34.json}). Reusable foundation of the repository IR / AST cluster.
 */
class ParserEnginesUnitTest {

    private static JsonNode golden() {
        try (InputStream in = ParserEnginesUnitTest.class.getResourceAsStream("/parity/parser_vectors_s34.json")) {
            if (in == null) {
                throw new IllegalStateException("parser_vectors_s34.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load parser vectors", e);
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

    @SuppressWarnings("unchecked")
    private static List<Object> l(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return n == null || n.isNull() ? new ArrayList<>() : (List<Object>) toNative(n);
    }

    @TestFactory
    List<DynamicTest> parserEngines() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("resolve_symbols", in -> ParserEngines.resolveSymbols(s(in, "source"), "text")));
        t.addAll(section("build_call_graph", in -> ParserEngines.buildCallGraph(s(in, "source"), "text")));
        t.addAll(section("resolve_dependencies", in -> ParserEngines.resolveDependencies(s(in, "source"), "")));
        t.addAll(section("recover_syntax", in -> ParserEngines.recoverSyntax(s(in, "source"), s(in, "language"))));
        t.addAll(section("enforce_budget", in -> ParserEngines.enforceBudget(s(in, "source"))));
        t.addAll(section("resolve_imports", in -> ParserEngines.resolveImports(m(in, "symbols"), "mod")));
        t.addAll(section("resolve_runtime", in -> ParserEngines.resolveRuntime(l(in, "deps"), l(in, "imports"))));
        t.addAll(section("resolve_frameworks",
                in -> ParserEngines.resolveFrameworks(l(in, "deps"), l(in, "imports"), new ArrayList<>())));
        return t;
    }
}
