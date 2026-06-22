package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.application.ApplicationCognitionRuntime;
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
 * Session-26 cross-language parity: {@code run_application_cognition}
 * (io.webweavex.application.ApplicationCognitionRuntime) + its pure sub-engines are byte-identical
 * to canonical Python 2.1.0 ({@code golden_vectors_s26.json}) for the portable {@code html=""}
 * contract.
 */
class CrossLanguageParityS26Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS26Test.class
                .getResourceAsStream("/parity/golden_vectors_s26.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s26.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s26 golden vectors", e);
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
    List<DynamicTest> orchestratorAndEngines() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("run_application_cognition", in -> ApplicationCognitionRuntime.runApplicationCognition(
                s(in, "url", ""), l(in, "interactions"), m(in, "memory"), s(in, "objective", "extract_dashboard"),
                b(in, "authenticated", false), m(in, "identity"), m(in, "adaptive_runtime"), l(in, "route_history"),
                l(in, "modals"))));
        t.addAll(section("extract_ui_semantics", in -> ApplicationCognitionRuntime.extractUiSemantics()));
        t.addAll(section("build_form_runtime", in -> ApplicationCognitionRuntime.buildFormRuntime()));
        t.addAll(section("build_dashboard_runtime", in -> ApplicationCognitionRuntime.buildDashboardRuntime()));
        t.addAll(section("build_navigation_semantics", in -> ApplicationCognitionRuntime.buildNavigationSemantics(
                s(in, "route", ""), l(in, "route_history"))));
        t.addAll(section("recover_application_runtime", in -> ApplicationCognitionRuntime.recoverApplicationRuntime(
                m(in, "state"))));
        t.addAll(section("build_application_state", in -> ApplicationCognitionRuntime.buildApplicationState(
                s(in, "route", ""), l(in, "forms"), l(in, "modals"), l(in, "widgets"), l(in, "tabs"),
                b(in, "authenticated", false))));
        t.addAll(section("build_application_transitions", in -> {
            Map<String, Object> w = new LinkedHashMap<>();
            w.put("transitions", ApplicationCognitionRuntime.buildApplicationTransitions(l(in, "states")));
            return w;
        }));
        t.addAll(section("build_action_graph", in -> ApplicationCognitionRuntime.buildActionGraph(l(in, "interactions"))));
        t.addAll(section("build_workflow_graph", in -> ApplicationCognitionRuntime.buildWorkflowGraph(
                l(in, "states"), l(in, "transitions"), l(in, "actions"))));
        t.addAll(section("resolve_application_intent", in -> ApplicationCognitionRuntime.resolveApplicationIntent(
                s(in, "objective", ""))));
        t.addAll(section("build_application_context", in -> ApplicationCognitionRuntime.buildApplicationContext(
                s(in, "url", ""), m(in, "state"), m(in, "identity"))));
        return t;
    }
}
