package io.webweavex.ast;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-33 AST-subsystem certification: {@link PythonAstEngine#parsePythonAst} and
 * {@link SemanticAstIr#compileSemanticAstIr} (ported from the certified JS scanner) are byte-identical
 * to canonical Python 3.0.0's real {@code ast.walk} summary ({@code ast_vectors_s33.json}) for standard
 * source. Reusable foundation for the AST cluster (query_semantics / reason_semantically /
 * compile_repository); not itself a public manifest API.
 */
class AstEngineUnitTest {

    private static JsonNode golden() {
        try (InputStream in = AstEngineUnitTest.class.getResourceAsStream("/parity/ast_vectors_s33.json")) {
            if (in == null) {
                throw new IllegalStateException("ast_vectors_s33.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load ast vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<String, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("code").asText());
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> astSubsystem() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("parse_python_ast", PythonAstEngine::parsePythonAst));
        t.addAll(section("compile_semantic_ast_ir", SemanticAstIr::compileSemanticAstIr));
        return t;
    }
}

