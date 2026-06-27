package io.webweavex.repository;

import io.webweavex.ast.PythonAstEngine;
import io.webweavex.ast.SemanticAstIr;
import io.webweavex.determinism.Normalization;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Port of the canonical Python Repository-IR layer — the full runtime closure of
 * {@code core.ir.repository_ir.compile_repository_ir} and the two public APIs that bottom out at it
 * ({@code query_semantics("repository",…)} via {@code core.query.repository_query_engine.query_repository},
 * {@code reason_semantically("runtime",…)} via {@code core.reasoning.runtime_reasoning_engine}).
 *
 * <p>Composes the S34/S35 {@link ParserEngines} (text/regex parser path) and the S33
 * {@link SemanticAstIr} (semantic_ast). Certified byte-exact vs Python 2.1.0 on the PORTABLE contract:
 * every language except {@code .py}-suffixed python source. {@code resolve_symbols}/{@code build_call_graph}
 * special-case only {@code language=="python"} (CPython {@code ast.walk}/{@code NodeVisitor}); all other
 * languages take the regex path. The python (.py) contract is the documented residual — see
 * {@code JAVA_SESSION_36_CERTIFICATION.md}. The epistemic {@code normalize_parser_output} is discarded by
 * this layer (it reads only parsed.{language,symbols,calls,dependencies,runtime,parser_grounding}).
 */
public final class RepositoryIr {

    private RepositoryIr() {
    }

    // ============================================================ helpers
    @SuppressWarnings("unchecked")
    static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static String str(Object o) {
        return o == null ? "" : String.valueOf(o);
    }

    private static boolean truthy(Object o) {
        if (o == null) {
            return false;
        }
        if (o instanceof List) {
            return !((List<?>) o).isEmpty();
        }
        if (o instanceof Map) {
            return !((Map<?, ?>) o).isEmpty();
        }
        if (o instanceof String) {
            return !((String) o).isEmpty();
        }
        if (o instanceof Boolean) {
            return (Boolean) o;
        }
        return true;
    }

    private static TreeSet<String> cpSet() {
        return new TreeSet<>(Normalization::codePointCompare);
    }

    private static List<Object> sortedUnique(List<String> items) {
        TreeSet<String> s = cpSet();
        for (String i : items) {
            s.add(i);
        }
        return new ArrayList<>(s);
    }

    private static Map<String, Object> map(Object... kv) {
        Map<String, Object> m = new LinkedHashMap<>();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    // ============================================================ core/ir/_base.py
    static Map<String, Object> emptyConfidence() {
        return map("score", 0L, "basis", new ArrayList<>(), "deterministic", true);
    }

    static Map<String, Object> emptyLineage(String stage) {
        List<Object> stages = new ArrayList<>();
        stages.add(map("stage", stage));
        return map("stages", stages, "depth", 1L);
    }

    /** {@code merge_evidence(*parts)}: sorted unique non-empty strings + count. */
    static Map<String, Object> mergeEvidence(List<Object> parts) {
        TreeSet<String> items = cpSet();
        for (Object part : parts) {
            for (Object e : asList(part)) {
                String s = str(e);
                if (!s.isEmpty()) {
                    items.add(s);
                }
            }
        }
        return map("items", new ArrayList<>(items), "count", (long) items.size());
    }

    // ============================================================ language detection / parse_source
    private static final Map<String, String> EXT_LANG = new LinkedHashMap<>();

    static {
        EXT_LANG.put(".py", "python");
        EXT_LANG.put(".js", "javascript");
        EXT_LANG.put(".jsx", "javascript");
        EXT_LANG.put(".ts", "typescript");
        EXT_LANG.put(".tsx", "typescript");
        EXT_LANG.put(".java", "java");
        EXT_LANG.put(".kt", "kotlin");
        EXT_LANG.put(".go", "go");
        EXT_LANG.put(".rs", "rust");
        EXT_LANG.put(".dart", "dart");
    }

    /** {@code ParserRegistry.detect_language} — Path(path).suffix.lower() lookup. */
    static String detectLanguage(String path) {
        String p = path == null ? "" : path;
        int slash = Math.max(p.lastIndexOf('/'), p.lastIndexOf('\\'));
        String name = slash >= 0 ? p.substring(slash + 1) : p;
        int dot = name.lastIndexOf('.');
        String ext = dot > 0 ? name.substring(dot).toLowerCase() : ""; // Path.suffix: none for dotfiles
        return EXT_LANG.getOrDefault(ext, "text");
    }

    /**
     * The subset of {@code parse_source}'s output that the repository layer observes, for the PORTABLE
     * (non-python) contract: language, symbols, calls, dependencies, runtime, parser_grounding.
     * Throws for the python (.py) contract — the documented residual.
     */
    @SuppressWarnings("unchecked")
    static Map<String, Object> parseSourceObservable(String source, String path) {
        String language = detectLanguage(path);
        if (language.equals("python")) {
            throw new UnsupportedOperationException(
                    "python (.py) contract residual: resolve_symbols/build_call_graph require CPython ast — see S36 cert");
        }
        String bounded = ParserEngines.enforceBudget(source == null ? "" : source);
        String recovered = ParserEngines.recoverSyntax(bounded, language);
        Map<String, Object> symbols = ParserEngines.resolveSymbols(recovered, language);
        Map<String, Object> calls = ParserEngines.buildCallGraph(recovered, language);
        Map<String, Object> deps = ParserEngines.resolveDependencies(recovered, path == null ? "" : path);
        Map<String, Object> runtime = ParserEngines.resolveRuntime(
                asList(deps.get("dependencies")), asList(symbols.get("imports")));
        // evidence dict — its values never reach the observable output (grounding only checks
        // non-emptiness, always true); built faithfully for the require_parser_evidence flags input.
        Map<String, Object> evidence = map(
                "ast", false,
                "symbols", truthy(symbols.get("symbols")),
                "calls", truthy(calls.get("calls")),
                "dependencies", truthy(deps.get("dependencies")),
                "tree_sitter", false);
        evidence.put("parse_error", true);
        Map<String, Object> groundingInput = map("language", language, "symbols", symbols, "evidence", evidence);
        Map<String, Object> grounding = ParserEngines.requireParserEvidence(groundingInput);
        return map(
                "language", language,
                "symbols", symbols,
                "calls", calls,
                "dependencies", deps,
                "runtime", runtime,
                "parser_grounding", grounding);
    }

    private static Map<String, Object> parsedOrEmpty(String source, String path) {
        return (source != null && !source.isEmpty()) ? parseSourceObservable(source, path) : new LinkedHashMap<>();
    }

    // ============================================================ runtime_dependency_engine
    private static final Pattern RE_REQ_FALLBACK =
            Pattern.compile("^([A-Za-z0-9_.\\-]+)\\s*(?:==|>=)", Pattern.MULTILINE);

    static Map<String, Object> resolveRuntimeDependencies(Map<String, Object> parsed, String textFallback) {
        List<String> deps = new ArrayList<>();
        List<String> evidence = new ArrayList<>();
        boolean parsedNonEmpty = parsed != null && !parsed.isEmpty();
        if (parsedNonEmpty) {
            Map<String, Object> d = asMap(parsed.get("dependencies"));
            for (Object x : asList(d.get("dependencies"))) {
                deps.add(str(x));
            }
            if (!deps.isEmpty()) {
                evidence.add("parser:dependencies");
            }
            Map<String, Object> runtime = asMap(parsed.get("runtime"));
            for (String k : new String[] {"packages", "modules"}) {
                List<Object> items = asList(runtime.get(k));
                if (!items.isEmpty()) {
                    for (int i = 0; i < Math.min(100, items.size()); i++) {
                        deps.add(str(items.get(i)));
                    }
                    evidence.add("parser:runtime_" + k);
                }
            }
        }
        if (deps.isEmpty() && textFallback != null && !textFallback.isEmpty()) {
            Matcher m = RE_REQ_FALLBACK.matcher(textFallback);
            while (m.find()) {
                deps.add(m.group(1));
                evidence.add("fallback:requirements_line");
            }
        }
        List<Object> depsOut = sortedUnique(deps);
        if (depsOut.size() > 200) {
            depsOut = depsOut.subList(0, 200);
        }
        boolean parserFirst = parsedNonEmpty && !evidence.isEmpty() && evidence.get(0).startsWith("parser");
        return map("dependencies", depsOut, "evidence", sortedUnique(evidence), "parser_first", parserFirst);
    }

    // ============================================================ execution_flow_engine
    static Map<String, Object> reconstructExecutionFlow(Map<String, Object> parsed) {
        Map<String, Object> sym = asMap(asMap(parsed).get("symbols"));
        List<Object> funcs = asList(sym.get("functions"));
        List<Object> calls = asList(asMap(asMap(parsed).get("calls")).get("calls"));
        List<Object> entrypoints = new ArrayList<>();
        for (Object f : funcs) {
            String s = str(f);
            if (s.startsWith("main") || s.startsWith("run_") || s.startsWith("handle_")) {
                entrypoints.add(f);
            }
        }
        List<Object> flow = new ArrayList<>();
        int limit = Math.min(50, calls.size());
        for (int i = 0; i < limit; i++) {
            if (calls.get(i) instanceof Map) {
                flow.add(map("step", (long) i, "call", calls.get(i)));
            }
        }
        List<Object> ep = entrypoints.size() > 20 ? new ArrayList<>(entrypoints.subList(0, 20)) : entrypoints;
        List<Object> ev = new ArrayList<>();
        if (!funcs.isEmpty()) {
            ev.add("parser:functions");
            ev.add("parser:call_graph");
        }
        return map("entrypoints", ep, "flow", flow, "evidence", ev);
    }

    // ============================================================ service_interaction_engine
    static Map<String, Object> inferServiceInteractions(Map<String, Object> parsed, List<Object> files) {
        List<Object> callList = asList(asMap(asMap(parsed).get("calls")).get("calls"));
        TreeSet<String> services = cpSet();
        for (Object f : files) {
            String fs = str(f);
            if (fs.contains("docker-compose") || fs.contains("k8s") || fs.contains("deployment")) {
                services.add(fs);
            }
        }
        List<Object> interactions = new ArrayList<>();
        int limit = Math.min(100, callList.size());
        for (int i = 0; i < limit; i++) {
            Map<String, Object> c = asMap(callList.get(i));
            if (callList.get(i) instanceof Map && truthy(c.get("caller"))) {
                List<Object> ev = new ArrayList<>();
                ev.add("parser:call_graph");
                interactions.add(map("from", str(c.get("caller")), "to", str(c.get("callee")), "evidence", ev));
            }
        }
        List<Object> ev = new ArrayList<>();
        if (!interactions.isEmpty()) {
            ev.add("parser:call_graph");
        }
        return map("interactions", interactions, "service_files", new ArrayList<>(services), "evidence", ev);
    }

    // ============================================================ runtime_semantics_engine
    static Map<String, Object> analyzeRuntimeSemantics(String source, String path) {
        Map<String, Object> parsed = parsedOrEmpty(source, path);
        Map<String, Object> deps = resolveRuntimeDependencies(parsed, source);
        Map<String, Object> runtime = parsed.isEmpty() ? new LinkedHashMap<>() : asMap(parsed.get("runtime"));
        Object di = asMap(parsed.get("parser_grounding")).get("deterministic_inputs");
        return map(
                "dependencies", deps.get("dependencies"),
                "runtime", runtime,
                "parser_first", deps.get("parser_first"),
                "evidence", deps.get("evidence"),
                "deterministic_inputs", di == null ? new ArrayList<>() : di);
    }

    // ============================================================ execution_dependency_engine
    static Map<String, Object> modelExecutionDependencies(String source, String path) {
        Map<String, Object> parsed = parsedOrEmpty(source, path);
        Map<String, Object> flow = reconstructExecutionFlow(parsed);
        List<Object> edges = new ArrayList<>();
        String prev = null;
        for (Object stepObj : asList(flow.get("flow"))) {
            Map<String, Object> step = asMap(stepObj);
            Map<String, Object> call = step.get("call") instanceof Map ? asMap(step.get("call")) : new LinkedHashMap<>();
            String cur = "";
            if (truthy(call.get("callee"))) {
                cur = str(call.get("callee"));
            } else if (truthy(call.get("caller"))) {
                cur = str(call.get("caller"));
            }
            if (prev != null && !prev.isEmpty() && !cur.isEmpty()) {
                List<Object> ev = new ArrayList<>();
                ev.add("parser:call_graph");
                edges.add(map("from", prev, "to", cur, "evidence", ev));
            }
            prev = !cur.isEmpty() ? cur : prev;
        }
        return map("edges", edges, "entrypoints", flow.get("entrypoints"), "evidence", flow.get("evidence"));
    }

    // ============================================================ runtime_flow_reasoner
    static Map<String, Object> reasonRuntimeFlow(String source, String path) {
        Map<String, Object> runtime = analyzeRuntimeSemantics(source, path);
        Map<String, Object> execDeps = modelExecutionDependencies(source, path);
        List<String> evParts = new ArrayList<>();
        for (Object e : asList(runtime.get("evidence"))) {
            evParts.add(str(e));
        }
        for (Object e : asList(execDeps.get("evidence"))) {
            evParts.add(str(e));
        }
        return map(
                "runtime", runtime,
                "execution_flow", execDeps,
                "topology", map("edges", execDeps.get("edges")),
                "evidence", sortedUnique(evParts));
    }

    // ============================================================ service_runtime_graph_engine
    static Map<String, Object> buildServiceRuntimeGraph(String source, String path, List<Object> files) {
        Map<String, Object> parsed = parsedOrEmpty(source, path);
        Map<String, Object> interactions = inferServiceInteractions(parsed, files);
        // Python: nodes = sorted({from}) + sorted({to}); then sorted(set(str(n) for n if n))[:200]
        List<String> nodeCollect = new ArrayList<>();
        for (Object iObj : asList(interactions.get("interactions"))) {
            Object from = asMap(iObj).get("from");
            if (truthy(from)) {
                nodeCollect.add(str(from));
            }
        }
        for (Object iObj : asList(interactions.get("interactions"))) {
            Object to = asMap(iObj).get("to");
            if (truthy(to)) {
                nodeCollect.add(str(to));
            }
        }
        List<Object> nodes = sortedUnique(nodeCollect);
        if (nodes.size() > 200) {
            nodes = nodes.subList(0, 200);
        }
        List<Object> edges = asList(interactions.get("interactions"));
        if (edges.size() > 200) {
            edges = new ArrayList<>(edges.subList(0, 200));
        }
        return map("nodes", nodes, "edges", edges,
                "service_files", interactions.get("service_files"), "evidence", interactions.get("evidence"));
    }

    // ============================================================ infra_semantic_engine
    private static final String[] INFRA_MARKERS = {
        "docker-compose", "Dockerfile", "kubernetes", "k8s/", "deployment.yaml",
        "helm/", ".github/workflows", "terraform", "pulumi"};

    static Map<String, Object> detectInfraSignals(List<Object> files) {
        List<Object> signals = new ArrayList<>();
        List<Object> evidence = new ArrayList<>();
        for (Object fObj : files) {
            String f = str(fObj);
            String fl = f.replace("\\", "/").toLowerCase();
            for (String m : INFRA_MARKERS) {
                if (fl.contains(m.toLowerCase())) {
                    signals.add(map("file", f, "signal", m));
                    evidence.add("infra:" + m);
                    break;
                }
            }
        }
        return map("signals", signals, "evidence", evidence,
                "deterministic_inputs", listOf("signals=" + signals.size()));
    }

    private static List<Object> listOf(Object... xs) {
        List<Object> l = new ArrayList<>();
        for (Object x : xs) {
            l.add(x);
        }
        return l;
    }

    // ============================================================ infra_relationship_engine
    static Map<String, Object> modelInfraRelationships(List<Object> files) {
        Map<String, Object> signals = detectInfraSignals(files);
        List<Object> sigList = asList(signals.get("signals"));
        List<String> names = new ArrayList<>();
        for (Object s : sigList) {
            names.add(str(asMap(s).get("file")));
        }
        List<Object> edges = new ArrayList<>();
        for (int i = 0; i < names.size() - 1; i++) {
            edges.add(map("from", names.get(i), "to", names.get(i + 1),
                    "relation", "co_deployed", "evidence", listOf("infra:signal")));
        }
        return map("signals", sigList, "edges", edges, "evidence", signals.get("evidence"));
    }

    // ============================================================ deployment_semantics_engine
    private static final String[] DEPLOY_KEYS = {"docker", "k8s", "helm", "deploy", "workflow"};

    static Map<String, Object> analyzeDeploymentSemantics(List<Object> files) {
        Map<String, Object> infra = modelInfraRelationships(files);
        List<Object> deployFiles = new ArrayList<>();
        for (Object fObj : files) {
            String fl = str(fObj).replace("\\", "/").toLowerCase();
            for (String k : DEPLOY_KEYS) {
                if (fl.contains(k)) {
                    deployFiles.add(fObj);
                    break;
                }
            }
        }
        List<Object> ev = new ArrayList<>();
        for (Object e : asList(infra.get("evidence"))) {
            ev.add(e);
        }
        ev.add("deploy:" + deployFiles.size());
        return map(
                "deployment_artifacts", deployFiles,
                "infra", infra,
                "semantics", deployFiles.isEmpty() ? "unknown" : "container_orchestration",
                "evidence", ev);
    }

    // ============================================================ api_surface_reasoning_engine
    @SuppressWarnings("unchecked")
    static Map<String, Object> reasonApiSurface(Map<String, Object> spec) {
        Map<String, Object> paths = asMap(spec == null ? null : spec.get("paths"));
        List<Object> endpoints = new ArrayList<>();
        for (Map.Entry<String, Object> e : paths.entrySet()) {
            if (e.getValue() instanceof Map) {
                for (String method : ((Map<String, Object>) e.getValue()).keySet()) {
                    endpoints.add(map("path", e.getKey(), "method", method.toUpperCase()));
                }
            }
        }
        List<Object> ev = new ArrayList<>();
        if (!endpoints.isEmpty()) {
            ev.add("openapi:paths");
        }
        return map("paths", endpoints, "path_count", (long) endpoints.size(),
                "evidence", ev, "deterministic_inputs", listOf("paths=" + endpoints.size()));
    }

    // ============================================================ api_contract_reasoning_engine
    static Map<String, Object> reasonApiContract(Map<String, Object> spec) {
        Map<String, Object> surface = reasonApiSurface(spec);
        List<Object> contracts = new ArrayList<>();
        for (Object pObj : asList(surface.get("paths"))) {
            Map<String, Object> p = asMap(pObj);
            contracts.add(map("path", p.get("path"), "method", p.get("method"),
                    "contract", "http", "evidence", listOf("openapi:paths")));
        }
        Map<String, Object> out = new LinkedHashMap<>(surface);
        out.put("contracts", contracts);
        out.put("contract_count", (long) contracts.size());
        return out;
    }

    // ============================================================ repository_semantic_ir_engine
    static Map<String, Object> buildRepositorySemanticIr(String source, String path, List<Object> files) {
        Map<String, Object> parsed = parsedOrEmpty(source, path);
        Object di = asMap(parsed.get("parser_grounding")).get("deterministic_inputs");
        return map(
                "language", parsed.isEmpty() ? "text" : parsed.getOrDefault("language", "text"),
                "symbols", parsed.isEmpty() ? new LinkedHashMap<>() : asMap(parsed.get("symbols")),
                "runtime_dependencies", resolveRuntimeDependencies(parsed, source),
                "execution_flow", reconstructExecutionFlow(parsed),
                "service_interactions", inferServiceInteractions(parsed, files == null ? new ArrayList<>() : files),
                "parser_grounding", parsed.isEmpty() ? new LinkedHashMap<>() : asMap(parsed.get("parser_grounding")),
                "evidence", di == null ? new ArrayList<>() : di);
    }

    // ============================================================ repository_execution_ir_engine
    static Map<String, Object> buildRepositoryExecutionIr(String source, String path, List<Object> files,
            Map<String, Object> openapi) {
        Map<String, Object> base = buildRepositorySemanticIr(source, path, files);
        Map<String, Object> flow = reasonRuntimeFlow(source, path);
        Map<String, Object> services = buildServiceRuntimeGraph(source, path, files == null ? new ArrayList<>() : files);
        Map<String, Object> deploy = analyzeDeploymentSemantics(files == null ? new ArrayList<>() : files);
        Map<String, Object> api = (openapi != null && !openapi.isEmpty()) ? reasonApiContract(openapi) : new LinkedHashMap<>();
        List<String> evParts = new ArrayList<>();
        for (Object e : asList(base.get("evidence"))) {
            evParts.add(str(e));
        }
        for (Object e : asList(flow.get("evidence"))) {
            evParts.add(str(e));
        }
        Map<String, Object> out = new LinkedHashMap<>(base);
        out.put("execution", flow);
        out.put("services", services);
        out.put("deployment", deploy);
        out.put("api_contracts", api);
        out.put("evidence", sortedUnique(evParts));
        return out;
    }

    // ============================================================ core/ir/repository_ir.py
    static Map<String, Object> emptyRepositoryIr() {
        Map<String, Object> ir = new LinkedHashMap<>();
        for (String k : new String[] {"services", "runtimes", "dependencies", "events", "queues", "apis",
                "deployments", "infra", "execution_flows", "topology", "runtime_constraints"}) {
            ir.put(k, new ArrayList<>());
        }
        ir.put("semantic_evidence", new LinkedHashMap<>());
        ir.put("graph", new LinkedHashMap<>());
        ir.put("lineage", emptyLineage("repository_ir"));
        ir.put("confidence", emptyConfidence());
        return ir;
    }

    public static Map<String, Object> compileRepositoryIr(String source, String path, List<Object> files,
            Map<String, Object> openapi) {
        Map<String, Object> raw = buildRepositoryExecutionIr(source, path, files, openapi);
        Map<String, Object> deps = asMap(raw.get("runtime_dependencies"));
        Map<String, Object> flow = asMap(raw.get("execution"));
        Map<String, Object> services = asMap(raw.get("services"));
        Map<String, Object> deploy = asMap(raw.get("deployment"));
        Map<String, Object> api = asMap(raw.get("api_contracts"));
        Map<String, Object> ir = emptyRepositoryIr();
        ir.put("dependencies", deps.getOrDefault("dependencies", new ArrayList<>()));
        ir.put("runtimes", listOf(map("language", raw.getOrDefault("language", "text"),
                "evidence", deps.getOrDefault("evidence", new ArrayList<>()))));
        ir.put("execution_flows", asMap(flow.get("execution_flow")).getOrDefault("flow", new ArrayList<>()));
        ir.put("services", services.getOrDefault("nodes", new ArrayList<>()));
        ir.put("topology", asMap(flow.get("topology")).getOrDefault("edges", new ArrayList<>()));
        ir.put("deployments", deploy.getOrDefault("deployment_artifacts", new ArrayList<>()));
        List<Object> infraSignals = asList(asMap(deploy.get("infra")).get("signals"));
        List<Object> infraFiles = new ArrayList<>();
        for (Object s : infraSignals) {
            if (s instanceof Map) {
                infraFiles.add(asMap(s).get("file"));
            }
        }
        ir.put("infra", infraFiles);
        ir.put("apis", api.getOrDefault("contracts", new ArrayList<>()));
        ir.put("graph", map("nodes", services.getOrDefault("nodes", new ArrayList<>()),
                "edges", services.getOrDefault("edges", new ArrayList<>())));
        ir.put("semantic_evidence", mergeEvidence(listOf(raw.getOrDefault("evidence", new ArrayList<>()))));
        ir.put("lineage", emptyLineage("repository_execution_ir"));
        boolean parserFirst = truthy(deps.get("parser_first"));
        ir.put("confidence", map("score", parserFirst ? (Object) 0.8 : (Object) 0.4,
                "basis", raw.getOrDefault("evidence", new ArrayList<>()), "deterministic", true));
        Map<String, Object> semanticAst;
        try {
            semanticAst = SemanticAstIr.compileSemanticAstIr(source == null ? "" : source);
        } catch (PythonAstEngine.PySyntaxError e) {
            semanticAst = map("semantic_grounded", false, "deterministic", true);
        }
        ir.put("semantic_ast", semanticAst);
        ir.put("_raw", raw);
        return ir;
    }

    // ============================================================ runtime_execution_engine / runtime_state
    static Map<String, Object> analyzeRuntimeExecution(String source, String path) {
        Map<String, Object> parsed = parsedOrEmpty(source, path);
        Map<String, Object> runtime = analyzeRuntimeSemantics(source, path);
        Map<String, Object> flow = reconstructExecutionFlow(parsed);
        List<String> evParts = new ArrayList<>();
        for (Object e : asList(runtime.get("evidence"))) {
            evParts.add(str(e));
        }
        for (Object e : asList(flow.get("evidence"))) {
            evParts.add(str(e));
        }
        return map("runtime", runtime, "execution", flow,
                "evidence", sortedUnique(evParts), "parser_backed", truthy(runtime.get("parser_first")));
    }

    static Map<String, Object> modelRuntimeState(String source, String path) {
        Map<String, Object> ex = analyzeRuntimeExecution(source, path);
        boolean backed = truthy(ex.get("parser_backed"));
        return map(
                "state", backed ? "active" : "unknown",
                "dependencies", asMap(ex.get("runtime")).getOrDefault("dependencies", new ArrayList<>()),
                "execution", ex.getOrDefault("execution", new LinkedHashMap<>()),
                "evidence", ex.getOrDefault("evidence", new ArrayList<>()),
                "transitions", listOf(map("from", "init", "to", backed ? "parsed" : "text")));
    }

    // ============================================================ public APIs
    /** {@code webweavex.compile_repository(source, path, **kwargs)}. */
    public static Map<String, Object> compileRepository(String source, String path, List<Object> files) {
        return compileRepositoryIr(source, path, files, null);
    }

    /** {@code core.query.repository_query_engine.query_repository(source, path)}. */
    static Map<String, Object> queryRepositorySemantic(String source, String path) {
        Map<String, Object> ir = compileRepositoryIr(source, path, null, null);
        return map("ir", ir, "evidence", ir.getOrDefault("semantic_evidence", new LinkedHashMap<>()),
                "explainable", true, "bounded", true);
    }

    /** {@code core.ir.semantic_query_ir.compile_semantic_query_ir}. */
    static Map<String, Object> compileSemanticQueryIr(String queryType, String target, Map<String, Object> result) {
        Object evidence = result.containsKey("evidence") ? result.get("evidence")
                : result.getOrDefault("semantic_evidence", new LinkedHashMap<>());
        return map("query_type", queryType, "target", target, "result", result,
                "evidence", evidence, "explainable", true, "deterministic", true);
    }

    /** {@code query_semantics("repository", {source, path})}. */
    public static Map<String, Object> querySemanticsRepository(String source, String path, String target) {
        return compileSemanticQueryIr("repository", target, queryRepositorySemantic(source, path));
    }

    /** {@code core.reasoning.runtime_reasoning_engine.reason_runtime_semantic} + dispatcher wrap. */
    static Map<String, Object> reasonRuntimeSemantic(String source, String path) {
        Map<String, Object> ir = compileRepositoryIr(source, path, null, null);
        Map<String, Object> state = modelRuntimeState(source, path);
        return map("ir", ir, "state", state,
                "evidence", ir.getOrDefault("semantic_evidence", new LinkedHashMap<>()), "explainable", true);
    }

    /** {@code reason_semantically("runtime", {source, path})}. */
    public static Map<String, Object> reasonSemanticallyRuntime(String source, String path) {
        Map<String, Object> r = new LinkedHashMap<>(reasonRuntimeSemantic(source, path));
        r.put("domain", "runtime");
        r.put("deterministic", true);
        return r;
    }
}
