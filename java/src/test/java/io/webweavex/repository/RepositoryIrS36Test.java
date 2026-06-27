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
 * Session-36 Repository-IR certification: the entire repository-IR layer + the three public APIs that
 * bottom out at {@code compile_repository_ir} are byte-identical to Python 2.1.0
 * ({@code repository_vectors_s36.json}) on the PORTABLE contract (every language except .py-python).
 * The {@code _python_contract_residual} section is recorded in the oracle for evidence and is NOT
 * asserted here (CPython ast branch — see JAVA_SESSION_36_CERTIFICATION.md).
 */
class RepositoryIrS36Test {

    private static final List<Object> FILES_INFRA = listOf(
            "docker-compose.yml", "k8s/deployment.yaml", "src/main.py", ".github/workflows/ci.yml");

    private static List<Object> listOf(Object... xs) {
        List<Object> l = new ArrayList<>();
        for (Object x : xs) {
            l.add(x);
        }
        return l;
    }

    private static JsonNode golden() {
        try (InputStream in = RepositoryIrS36Test.class.getResourceAsStream("/parity/repository_vectors_s36.json")) {
            if (in == null) {
                throw new IllegalStateException("repository_vectors_s36.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s36 vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs"));
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output),
                        "serialize mismatch " + name + ":" + v.get("name").asText());
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output),
                        "hash mismatch " + name + ":" + v.get("name").asText());
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
        Object o = toNative(in.get(f));
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> l(JsonNode in, String f) {
        Object o = toNative(in.get(f));
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static Map<String, Object> parsed(JsonNode in) {
        return RepositoryIr.parseSourceObservable(s(in, "source"), s(in, "path"));
    }

    private static Map<String, Object> parsedOrEmpty(JsonNode in) {
        String src = s(in, "source");
        return src.isEmpty() ? new LinkedHashMap<>() : parsed(in);
    }

    @TestFactory
    List<DynamicTest> repositoryIr() {
        List<DynamicTest> t = new ArrayList<>();
        // IR base
        t.addAll(section("merge_evidence", in -> RepositoryIr.mergeEvidence(l(in, "parts"))));
        t.addAll(section("empty_confidence", in -> RepositoryIr.emptyConfidence()));
        t.addAll(section("empty_lineage", in -> RepositoryIr.emptyLineage("repository_ir")));
        t.addAll(section("empty_repository_ir", in -> RepositoryIr.emptyRepositoryIr()));
        // per-engine
        t.addAll(section("resolve_runtime_dependencies",
                in -> RepositoryIr.resolveRuntimeDependencies(parsedOrEmpty(in), s(in, "source"))));
        t.addAll(section("reconstruct_execution_flow",
                in -> RepositoryIr.reconstructExecutionFlow(parsedOrEmpty(in))));
        t.addAll(section("infer_service_interactions",
                in -> RepositoryIr.inferServiceInteractions(parsedOrEmpty(in), FILES_INFRA)));
        t.addAll(section("analyze_runtime_semantics",
                in -> RepositoryIr.analyzeRuntimeSemantics(s(in, "source"), s(in, "path"))));
        t.addAll(section("model_execution_dependencies",
                in -> RepositoryIr.modelExecutionDependencies(s(in, "source"), s(in, "path"))));
        t.addAll(section("reason_runtime_flow",
                in -> RepositoryIr.reasonRuntimeFlow(s(in, "source"), s(in, "path"))));
        t.addAll(section("build_service_runtime_graph",
                in -> RepositoryIr.buildServiceRuntimeGraph(s(in, "source"), s(in, "path"), new ArrayList<>())));
        t.addAll(section("detect_infra_signals", in -> RepositoryIr.detectInfraSignals(l(in, "files"))));
        t.addAll(section("model_infra_relationships", in -> RepositoryIr.modelInfraRelationships(l(in, "files"))));
        t.addAll(section("analyze_deployment_semantics", in -> RepositoryIr.analyzeDeploymentSemantics(l(in, "files"))));
        t.addAll(section("reason_api_surface", in -> RepositoryIr.reasonApiSurface(m(in, "spec"))));
        t.addAll(section("reason_api_contract", in -> RepositoryIr.reasonApiContract(m(in, "spec"))));
        t.addAll(section("analyze_runtime_execution",
                in -> RepositoryIr.analyzeRuntimeExecution(s(in, "source"), s(in, "path"))));
        t.addAll(section("model_runtime_state",
                in -> RepositoryIr.modelRuntimeState(s(in, "source"), s(in, "path"))));
        t.addAll(section("build_repository_semantic_ir",
                in -> RepositoryIr.buildRepositorySemanticIr(s(in, "source"), s(in, "path"), null)));
        t.addAll(section("build_repository_execution_ir", in -> {
            Map<String, Object> openapi = in.has("openapi") ? OPENAPI() : null;
            return RepositoryIr.buildRepositoryExecutionIr(s(in, "source"), s(in, "path"), null, openapi);
        }));
        // hub + public APIs
        t.addAll(section("compile_repository_ir", in -> {
            List<Object> files = in.has("files") ? FILES_INFRA : null;
            Map<String, Object> openapi = in.has("openapi") ? OPENAPI() : null;
            return RepositoryIr.compileRepositoryIr(s(in, "source"), s(in, "path"), files, openapi);
        }));
        t.addAll(section("compile_repository",
                in -> RepositoryIr.compileRepository(s(in, "source"), s(in, "path"), null)));
        t.addAll(section("query_semantics_repository",
                in -> RepositoryIr.querySemanticsRepository(s(in, "source"), s(in, "path"), s(in, "target"))));
        t.addAll(section("reason_semantically_runtime",
                in -> RepositoryIr.reasonSemanticallyRuntime(s(in, "source"), s(in, "path"))));
        return t;
    }

    private static Map<String, Object> OPENAPI() {
        Map<String, Object> users = new LinkedHashMap<>();
        users.put("get", new LinkedHashMap<>());
        users.put("post", new LinkedHashMap<>());
        Map<String, Object> items = new LinkedHashMap<>();
        items.put("delete", new LinkedHashMap<>());
        Map<String, Object> paths = new LinkedHashMap<>();
        paths.put("/users", users);
        paths.put("/items/{id}", items);
        Map<String, Object> spec = new LinkedHashMap<>();
        spec.put("paths", paths);
        return spec;
    }
}
