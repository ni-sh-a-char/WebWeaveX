package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.semantic.SemanticRuntime;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-25 cross-language parity: {@code run_semantic_runtime} / {@code run_semantic_for_extraction}
 * (io.webweavex.semantic.SemanticRuntime) + the pure semantic sub-engines are byte-identical to
 * canonical Python 2.1.0 ({@code golden_vectors_s25.json}) for the portable {@code html=""} contract.
 */
class CrossLanguageParityS25Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS25Test.class
                .getResourceAsStream("/parity/golden_vectors_s25.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s25.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s25 golden vectors", e);
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

    private static boolean b(JsonNode in, String f, boolean d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asBoolean();
    }

    @TestFactory
    List<DynamicTest> orchestrator() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("run_semantic_runtime", in -> SemanticRuntime.runSemanticRuntime(
                s(in, "url", ""), s(in, "text", ""), l(in, "interactions"), m(in, "application_result"),
                m(in, "causality_result"), m(in, "native_cognition"), l(in, "repository_files"),
                m(in, "runtime_graph"), m(in, "memory"), s(in, "objective", ""))));
        t.addAll(section("run_semantic_for_extraction", in -> SemanticRuntime.runSemanticForExtraction(
                b(in, "semantic_runtime", true), s(in, "url", ""), l(in, "interactions"), m(in, "application_result"),
                m(in, "causality_result"), m(in, "native_cognition"), m(in, "runtime_graph"), s(in, "objective", ""),
                b(in, "merge_graph", true))));
        return t;
    }

    @TestFactory
    List<DynamicTest> engineSections() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("extract_semantic_entities", in -> SemanticRuntime.extractSemanticEntities(
                s(in, "text", ""), m(in, "structure"))));
        t.addAll(section("resolve_semantic_entities", in -> SemanticRuntime.resolveSemanticEntities(l(in, "entities"))));
        t.addAll(section("classify_semantic_domain", in -> SemanticRuntime.classifySemanticDomain(
                s(in, "text", ""), l(in, "signals"))));
        t.addAll(section("build_semantic_ontology", in -> SemanticRuntime.buildSemanticOntology(
                l(in, "entities"), s(in, "domain", ""))));
        t.addAll(section("build_semantic_graph", in -> SemanticRuntime.buildSemanticGraph(
                l(in, "entities"), l(in, "relations"))));
        t.addAll(section("extract_document_semantics", in -> SemanticRuntime.extractDocumentSemantics(s(in, "text", ""))));
        t.addAll(section("extract_table_semantics", in -> SemanticRuntime.extractTableSemantics()));
        t.addAll(section("extract_ui_semantics", in -> SemanticRuntime.extractUiSemantics(l(in, "actions"))));
        t.addAll(section("extract_repository_semantics", in -> SemanticRuntime.extractRepositorySemantics(
                l(in, "files"), s(in, "text", ""))));
        t.addAll(section("extract_application_semantics", in -> SemanticRuntime.extractApplicationSemantics(
                m(in, "application_result"))));
        t.addAll(section("extract_causality_semantics", in -> SemanticRuntime.extractCausalitySemantics(
                m(in, "causality_result"))));
        t.addAll(section("extract_workflow_semantics", in -> SemanticRuntime.extractWorkflowSemantics(
                m(in, "workflow"), s(in, "objective", ""))));
        t.addAll(section("extract_browser_semantics", in -> SemanticRuntime.extractBrowserSemantics(
                s(in, "url", ""), null)));
        t.addAll(section("extract_runtime_semantics", in -> SemanticRuntime.extractRuntimeSemantics(
                m(in, "runtime_graph"), m(in, "sources"))));
        t.addAll(section("align_semantic_runtimes", in -> SemanticRuntime.alignSemanticRuntimes(
                m(in, "browser"), null, m(in, "repository"), null, null)));
        t.addAll(section("diff_semantic_runtime", in -> SemanticRuntime.diffSemanticRuntime(
                m(in, "previous"), m(in, "current"))));
        return t;
    }
}
