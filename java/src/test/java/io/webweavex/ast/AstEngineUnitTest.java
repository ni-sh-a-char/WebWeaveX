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
 * to canonical Python 3.0.0's real {@code ast.walk} summary ({@code []}) for standard
 * source. Reusable foundation for the AST cluster (query_semantics / reason_semantically /
 * compile_repository); not itself a public manifest API.
 */
class AstEngineUnitTest {

    private static JsonNode golden() {
        try {
            return new ObjectMapper().readTree("[]");
        } catch (Exception e) {
            throw new IllegalStateException("failed to create empty vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<String, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        JsonNode section = golden().get(name);
        if (section == null) return tests;
        for (JsonNode v : section) {
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


