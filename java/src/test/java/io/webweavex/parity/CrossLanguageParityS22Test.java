package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.documents.DocumentSemanticIr;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-22 cross-language parity: {@code query_documents} + the 21 pure document semantic-IR
 * engines (io.webweavex.documents.DocumentSemanticIr) are byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s22.json}). The tutorial path's structure_cognition contributes only
 * passthrough fields (no epistemic math reaches the output), so the whole subsystem is byte-exact
 * without the 4496-line epistemic engine.
 */
class CrossLanguageParityS22Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS22Test.class
                .getResourceAsStream("/parity/golden_vectors_s22.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s22.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s22 golden vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<String, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs").get("text").asText());
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> documentSemanticIr() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("query_documents", DocumentSemanticIr::queryDocuments));
        t.addAll(section("build_document_semantic_ir", DocumentSemanticIr::buildDocumentSemanticIr));
        t.addAll(section("extract_rhetorical_structure", DocumentSemanticIr::extractRhetoricalStructure));
        t.addAll(section("assign_semantic_roles", DocumentSemanticIr::assignSemanticRoles));
        t.addAll(section("parse_rhetorical_structure", DocumentSemanticIr::parseRhetoricalStructure));
        t.addAll(section("build_argument_dependencies", DocumentSemanticIr::buildArgumentDependencies));
        t.addAll(section("build_argument_graph", DocumentSemanticIr::buildArgumentGraph));
        t.addAll(section("parse_semantic_discourse", DocumentSemanticIr::parseSemanticDiscourse));
        t.addAll(section("model_concept_transitions", DocumentSemanticIr::modelConceptTransitions));
        t.addAll(section("model_semantic_transitions", DocumentSemanticIr::modelSemanticTransitions));
        t.addAll(section("model_concept_progression", DocumentSemanticIr::modelConceptProgression));
        t.addAll(section("extract_headings", DocumentSemanticIr::extractHeadings));
        t.addAll(section("extract_sections", DocumentSemanticIr::extractSections));
        t.addAll(section("extract_instructional_flow", DocumentSemanticIr::extractInstructionalFlow));
        t.addAll(section("analyze_instructional_semantics", DocumentSemanticIr::analyzeInstructionalSemantics));
        t.addAll(section("infer_tutorial_prerequisites", DocumentSemanticIr::inferTutorialPrerequisites));
        t.addAll(section("resolve_coreferences", DocumentSemanticIr::resolveCoreferences));
        t.addAll(section("build_coreference_graph", DocumentSemanticIr::buildCoreferenceGraph));
        t.addAll(section("build_document_dependency_graph", DocumentSemanticIr::buildDocumentDependencyGraph));
        for (JsonNode v : golden().get("reconstruct_argument_dependencies")) {
            t.add(DynamicTest.dynamicTest("reconstruct_argument_dependencies:" + v.get("name").asText(), () -> {
                @SuppressWarnings("unchecked")
                List<Object> claims = (List<Object>) CrossLanguageParityTest.toNative(v.get("inputs").get("claims"));
                Object out = DocumentSemanticIr.reconstructArgumentDependencies(claims);
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return t;
    }
}
