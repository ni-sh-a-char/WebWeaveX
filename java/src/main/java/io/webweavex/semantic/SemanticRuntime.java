package io.webweavex.semantic;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import io.webweavex.execution.ExecutionRuntime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeSet;
import java.util.regex.Pattern;

/**
 * Port of {@code core.semantic.semantic_orchestrator} — {@code run_semantic_runtime} /
 * {@code run_semantic_for_extraction} — and its pure semantic sub-engines + IR, for the proven
 * portable {@code html=""} contract. The orchestrator calls {@code extract_table_semantics} /
 * {@code extract_ui_semantics} (BeautifulSoup), but on {@code html=""} BeautifulSoup parses an empty
 * document and contributes nothing observable (tables empty; UI html-derived fields all
 * empty/False) — verified — so the output is bs4-independent and byte-exact without the Soup engine.
 * Reuses {@link io.webweavex.semantic.SemanticReplay} (replay) and
 * {@link ExecutionRuntime#buildUnifiedRuntimeGraph} (merge). Zero new substrate.
 */
public final class SemanticRuntime {

    private SemanticRuntime() {
    }

    // -------------------------------------------------------------- helpers

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static int cmp(String a, String b) {
        return Normalization.codePointCompare(a, b);
    }

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    private static List<Object> capped(List<Object> xs, int n) {
        return xs.size() > n ? new ArrayList<>(xs.subList(0, n)) : xs;
    }

    private static boolean search(Pattern p, String text) {
        return p.matcher(text).find();
    }

    private static int countMatches(Pattern p, String text) {
        java.util.regex.Matcher m = p.matcher(text);
        int c = 0;
        while (m.find()) {
            c++;
        }
        return c;
    }

    private static final int CI = Pattern.CASE_INSENSITIVE;

    // -------------------------------------------------------------- entity extraction

    private static final String[][] ENTITY_PATTERNS = {
        {"organization", "\\b(inc|corp|llc|ltd|company)\\b"},
        {"api", "\\b(api|endpoint|rest|graphql)\\b"},
        {"metric", "\\b(kpi|metric|latency|throughput|error rate)\\b"},
        {"user", "\\b(user|account|profile|login)\\b"},
        {"service", "\\b(service|microservice|worker|queue)\\b"},
        {"workflow", "\\b(workflow|pipeline|job|task)\\b"},
        {"infrastructure", "\\b(kubernetes|docker|vm|cluster|deploy)\\b"},
    };

    public static Map<String, Object> extractSemanticEntities(String text, Map<String, Object> structure) {
        Map<String, Object> st = structure == null ? map() : structure;
        List<Object> entities = new ArrayList<>();
        int index = 0;
        for (String[] pr : ENTITY_PATTERNS) {
            if (search(Pattern.compile(pr[1], CI), text)) {
                entities.add(mapOf("id", "entity:" + pr[0] + ":" + index, "type", pr[0], "label", pr[0],
                        "source", "pattern"));
                index++;
            }
        }
        for (Object ao : capped(asList(st.get("actions")), 5000)) {
            Map<String, Object> action = asMap(ao);
            entities.add(mapOf("id", "entity:ui_action:" + index, "type", "ui_action",
                    "label", str(Py.get(action, "label", Py.get(action, "type", ""))), "source", "structure"));
            index++;
        }
        for (Object artifact : capped(asList(st.get("artifacts")), 5000)) {
            entities.add(mapOf("id", "entity:runtime:" + index, "type", "runtime_artifact",
                    "label", str(artifact), "source", "runtime"));
            index++;
        }
        entities.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> relations = new ArrayList<>();
        for (int i = 1; i < entities.size(); i++) {
            relations.add(mapOf("from", asMap(entities.get(i - 1)).get("id"), "to", asMap(entities.get(i)).get("id"),
                    "relation", "related_to"));
        }
        Map<String, Object> out = map();
        out.put("entities", entities);
        out.put("relations", relations);
        out.put("ontology", map());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> resolveSemanticEntities(List<Object> entities) {
        Map<String, Object> canonical = map();
        List<Object> resolved = new ArrayList<>();
        List<Object> ordered = new ArrayList<>(entities);
        ordered.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        for (Object eo : ordered) {
            Map<String, Object> entity = asMap(eo);
            String label = str(Py.get(entity, "label", Py.get(entity, "type", ""))).toLowerCase(Locale.ROOT).strip();
            Object canonicalId = canonical.get(label);
            if (!Py.truthy(canonicalId)) {
                canonicalId = str(Py.get(entity, "id", ""));
                canonical.put(label, canonicalId);
            }
            Map<String, Object> r = new LinkedHashMap<>(entity);
            r.put("canonical_id", canonicalId);
            r.put("resolved", true);
            resolved.add(r);
        }
        Map<String, Object> out = map();
        out.put("entities", resolved);
        out.put("canonical_map", canonical);
        out.put("bounded", true);
        return out;
    }

    private static final String[][] DOMAIN_RULES = {
        {"saas", "\\b(saas|subscription|tenant|workspace)\\b"},
        {"finance", "\\b(invoice|ledger|payment|billing|revenue)\\b"},
        {"analytics", "\\b(analytics|dashboard|kpi|metrics|report)\\b"},
        {"infrastructure", "\\b(kubernetes|terraform|infra|cluster|deploy)\\b"},
        {"devops", "\\b(ci/cd|pipeline|build|release|deploy)\\b"},
        {"crm", "\\b(crm|customer|lead|opportunity|contact)\\b"},
        {"ecommerce", "\\b(cart|checkout|product|order|sku)\\b"},
        {"support", "\\b(ticket|support|helpdesk|incident)\\b"},
        {"security", "\\b(security|auth|oauth|permission|role)\\b"},
        {"developer_tooling", "\\b(ide|repository|api|sdk|debug)\\b"},
    };

    public static Map<String, Object> classifySemanticDomain(String text, List<Object> signals) {
        List<Object> sig = signals == null ? new ArrayList<>() : signals;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < sig.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(str(sig.get(i)));
        }
        String combined = text + " " + sb;
        Map<String, Object> scores = map();
        for (String[] dr : DOMAIN_RULES) {
            int n = countMatches(Pattern.compile(dr[1], CI), combined);
            if (n > 0) {
                scores.put(dr[0], (long) n);
            }
        }
        String primary;
        if (scores.isEmpty()) {
            primary = "saas";
        } else {
            List<Map.Entry<String, Object>> entries = new ArrayList<>(scores.entrySet());
            entries.sort(Comparator.comparingLong((Map.Entry<String, Object> e) -> -((Number) e.getValue()).longValue())
                    .thenComparing(Map.Entry::getKey, Normalization::codePointCompare));
            primary = entries.get(0).getKey();
        }
        Map<String, Object> out = map();
        out.put("domain", primary);
        out.put("scores", scores);
        out.put("signals", sig);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildSemanticOntology(List<Object> entities, String domain) {
        TreeSet<String> types = new TreeSet<>(Normalization::codePointCompare);
        for (Object eo : entities) {
            types.add(str(Py.get(asMap(eo), "type", "")));
        }
        List<Object> entityTaxonomy = new ArrayList<>(types);
        Map<String, Object> taxonomy = map();
        taxonomy.put("entity", entityTaxonomy);
        taxonomy.put("runtime", new ArrayList<>(List.of("browser", "native", "distributed", "application")));
        taxonomy.put("workflow", new ArrayList<>(List.of("transition", "submit", "navigate", "objective")));
        taxonomy.put("ui", new ArrayList<>(List.of("form", "dashboard", "navigation", "authentication")));
        taxonomy.put("infrastructure", new ArrayList<>(List.of("service", "api", "deployment", "monitoring")));
        Map<String, Object> out = map();
        out.put("entity_taxonomy", entityTaxonomy);
        out.put("runtime_ontology", taxonomy.get("runtime"));
        out.put("workflow_ontology", taxonomy.get("workflow"));
        out.put("ui_ontology", taxonomy.get("ui"));
        out.put("infrastructure_ontology", taxonomy.get("infrastructure"));
        out.put("primary_domain", domain);
        out.put("taxonomy", taxonomy);
        out.put("bounded", true);
        return out;
    }

    private static final Map<String, String> RELATION_MAP = new LinkedHashMap<>();

    static {
        RELATION_MAP.put("organization", "owns");
        RELATION_MAP.put("service", "deploys");
        RELATION_MAP.put("api", "exposes");
        RELATION_MAP.put("metric", "monitors");
        RELATION_MAP.put("user", "authenticates");
        RELATION_MAP.put("workflow", "triggers");
        RELATION_MAP.put("infrastructure", "depends_on");
        RELATION_MAP.put("ui_action", "mutates");
    }

    public static Map<String, Object> buildSemanticGraph(List<Object> entities, List<Object> relations) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        for (Object eo : capped(entities, 10000)) {
            Map<String, Object> e = asMap(eo);
            nodes.add(mapOf("id", str(Py.get(e, "id", "")), "type", str(Py.get(e, "type", "entity")),
                    "label", str(Py.get(e, "label", ""))));
        }
        for (Object ro : capped(relations, 10000)) {
            Map<String, Object> r = asMap(ro);
            edges.add(mapOf("from", str(Py.get(r, "from", "")), "to", str(Py.get(r, "to", "")),
                    "relation", str(Py.get(r, "relation", "related_to"))));
        }
        for (Object eo : capped(entities, 10000)) {
            Map<String, Object> e = asMap(eo);
            String mapped = RELATION_MAP.get(str(Py.get(e, "type", "")));
            if (mapped != null && nodes.size() > 1) {
                edges.add(mapOf("from", str(Py.get(e, "id", "")), "to", asMap(nodes.get(0)).get("id"),
                        "relation", mapped));
            }
        }
        if (nodes.isEmpty()) {
            nodes.add(mapOf("id", "semantic:root", "type", "semantic"));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), SemanticRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), SemanticRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), SemanticRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    private static final String[][] DOC_KIND_RULES = {
        {"contract", "agreement|terms|party|signature"},
        {"technical_doc", "architecture|module|implementation"},
        {"api_reference", "endpoint|request|response|openapi"},
        {"invoice", "invoice|amount due|tax"},
        {"report", "summary|findings|quarter|annual"},
        {"resume", "experience|education|skills"},
        {"legal", "whereas|jurisdiction|liability"},
        {"specification", "requirements|shall|must|specification"},
    };

    public static Map<String, Object> extractDocumentSemantics(String text) {
        List<String> kinds = new ArrayList<>();
        for (String[] dr : DOC_KIND_RULES) {
            if (search(Pattern.compile(dr[1], CI), text)) {
                kinds.add(dr[0]);
            }
        }
        if (kinds.isEmpty()) {
            kinds.add("document");
        }
        kinds.sort(Normalization::codePointCompare);
        Map<String, Object> out = map();
        out.put("kinds", new ArrayList<Object>(kinds));
        out.put("primary_kind", kinds.get(0));
        out.put("length", (long) text.length());
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_table_semantics(html="")} — empty document yields no tables. */
    public static Map<String, Object> extractTableSemantics() {
        Map<String, Object> out = map();
        out.put("tables", new ArrayList<>());
        out.put("primary_kind", "none");
        out.put("bounded", true);
        return out;
    }

    private static final String[] UI_INTENT_KEYS =
            {"destructive", "authentication", "billing", "monitoring", "settings", "admin_panel"};

    /** {@code extract_ui_semantics(html="", actions)} — html-derived fields are empty for empty HTML. */
    public static Map<String, Object> extractUiSemantics(List<Object> actions) {
        List<Object> acts = actions == null ? new ArrayList<>() : actions;
        Map<String, Object> out = map();
        out.put("destructive_actions", new ArrayList<>());
        out.put("primary_workflows", new ArrayList<>());
        out.put("navigation_intent", false);
        out.put("dashboards", false);
        out.put("forms", 0L);
        out.put("admin_panels", false);
        out.put("settings", false);
        out.put("authentication", false);
        out.put("billing", false);
        out.put("monitoring", false);
        out.put("actions", capped(acts, 1000));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractRepositorySemantics(List<Object> files, String text) {
        List<Object> fs = files == null ? new ArrayList<>() : files;
        StringBuilder sb = new StringBuilder(text).append(' ');
        for (int i = 0; i < fs.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(str(fs.get(i)));
        }
        String combined = sb.toString();
        List<String> roles = new ArrayList<>();
        if (search(Pattern.compile("api|routes|controller", CI), combined)) {
            roles.add("api_surface");
        }
        if (search(Pattern.compile("docker|k8s|helm|terraform", CI), combined)) {
            roles.add("deployment_topology");
        }
        if (search(Pattern.compile("service|worker|queue", CI), combined)) {
            roles.add("service_boundary");
        }
        if (search(Pattern.compile("react|vue|angular|next", CI), combined)) {
            roles.add("frontend_framework");
        }
        if (search(Pattern.compile("django|flask|fastapi|express", CI), combined)) {
            roles.add("backend_framework");
        }
        String purpose = "application";
        String lower = combined.toLowerCase(Locale.ROOT);
        if (lower.contains("docs")) {
            purpose = "documentation";
        } else if (lower.contains("infra")) {
            purpose = "infrastructure";
        }
        TreeSet<String> roleSet = new TreeSet<>(Normalization::codePointCompare);
        roleSet.addAll(roles);
        List<Object> serviceBoundaries = new ArrayList<>();
        List<Object> frameworks = new ArrayList<>();
        for (String r : roles) {
            if (r.equals("service_boundary")) {
                serviceBoundaries.add(r);
            }
            if (r.contains("framework")) {
                frameworks.add(r);
            }
        }
        Map<String, Object> out = map();
        out.put("architecture_roles", new ArrayList<Object>(roleSet));
        out.put("service_boundaries", serviceBoundaries);
        out.put("api_ownership", roles.contains("api_surface"));
        out.put("deployment_topology", roles.contains("deployment_topology"));
        out.put("framework_semantics", frameworks);
        out.put("repository_purpose", purpose);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractApplicationSemantics(Map<String, Object> applicationResult) {
        Map<String, Object> ar = applicationResult == null ? map() : applicationResult;
        Map<String, Object> workflow = asMap(ar.get("workflow"));
        Map<String, Object> execution = asMap(ar.get("execution"));
        Map<String, Object> forms = asMap(ar.get("forms"));
        List<Object> operations = new ArrayList<>();
        for (Object so : asList(execution.get("executed"))) {
            operations.add(str(Py.get(asMap(so), "action", "")));
        }
        List<Object> uiFunc = new ArrayList<>(asMap(ar.get("ui_semantics")).keySet());
        Map<String, Object> out = map();
        out.put("workflow_purpose", str(Py.get(asMap(ar.get("intent")), "intent", "operate")));
        out.put("runtime_intent", str(Py.get(execution, "objective", "")));
        out.put("business_operations", operations);
        out.put("ui_functionality", uiFunc);
        out.put("operational_actions", (long) asList(workflow.get("edges")).size());
        out.put("form_operations", (long) asList(forms.get("forms")).size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractCausalitySemantics(Map<String, Object> causalityResult) {
        Map<String, Object> causality = causalityResult == null ? map() : causalityResult;
        Map<String, Object> inner = asMap(Py.get(causality, "causality", causality));
        Map<String, Object> propagation = asMap(inner.get("propagation"));
        Map<String, Object> alignment = asMap(inner.get("alignment"));
        List<Object> chains = new ArrayList<>();
        for (Object ho : capped(asList(propagation.get("handoffs")), 1000)) {
            Map<String, Object> h = asMap(ho);
            chains.add(mapOf("from", str(Py.get(h, "from", "")), "to", str(Py.get(h, "to", "")),
                    "impact", "cross_runtime_propagation"));
        }
        Map<String, Object> out = map();
        out.put("workflow_propagation_meaning", "sequential_runtime_handoff");
        out.put("operational_impact", (long) chains.size());
        out.put("runtime_significance", Py.get(alignment, "runtime_count", 0L));
        out.put("critical_event_chains", chains);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractWorkflowSemantics(Map<String, Object> workflow, String objective) {
        Map<String, Object> wf = workflow == null ? map() : workflow;
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("workflow_steps", (long) asList(wf.get("nodes")).size());
        out.put("transitions", (long) asList(wf.get("edges")).size());
        out.put("semantic_intent", objective.isEmpty() ? "operational_flow" : objective);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractBrowserSemantics(String url, Map<String, Object> extraction) {
        Map<String, Object> ex = extraction == null ? map() : extraction;
        Map<String, Object> out = map();
        out.put("origin", url);
        out.put("page_role", "web_application");
        out.put("network_artifacts", (long) asList(ex.get("requests")).size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> extractRuntimeSemantics(Map<String, Object> runtimeGraph,
            Map<String, Object> sources) {
        Map<String, Object> rg = runtimeGraph == null ? map() : runtimeGraph;
        Map<String, Object> src = sources == null ? map() : sources;
        TreeSet<String> layers = new TreeSet<>(Normalization::codePointCompare);
        layers.addAll(src.keySet());
        Map<String, Object> out = map();
        out.put("node_count", (long) asList(rg.get("nodes")).size());
        out.put("edge_count", (long) asList(rg.get("edges")).size());
        out.put("runtime_layers", new ArrayList<Object>(layers));
        out.put("meaning", "unified_runtime_cognition");
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> alignSemanticRuntimes(Map<String, Object> browser, Map<String, Object> native_,
            Map<String, Object> repository, Map<String, Object> document, Map<String, Object> runtime) {
        Map<String, Object> layers = map();
        layers.put("browser", browser == null ? map() : browser);
        layers.put("native", native_ == null ? map() : native_);
        layers.put("repository", repository == null ? map() : repository);
        layers.put("document", document == null ? map() : document);
        layers.put("multimodal", map());
        layers.put("runtime", runtime == null ? map() : runtime);
        List<Object> aligned = new ArrayList<>();
        for (Map.Entry<String, Object> e : layers.entrySet()) {
            Map<String, Object> payload = asMap(e.getValue());
            if (Py.truthy(payload)) {
                aligned.add(mapOf("layer", e.getKey(),
                        "domain", str(Py.get(payload, "domain", Py.get(payload, "primary_kind", "")))));
            }
        }
        Map<String, Object> out = map();
        out.put("layers", layers);
        out.put("aligned_domains", aligned);
        out.put("aligned", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> diffSemanticRuntime(Map<String, Object> previous, Map<String, Object> current) {
        TreeSet<String> prevIds = new TreeSet<>(Normalization::codePointCompare);
        for (Object i : asList(asMap(previous.get("entities")).get("entities"))) {
            prevIds.add(str(Py.get(asMap(i), "id", "")));
        }
        TreeSet<String> currIds = new TreeSet<>(Normalization::codePointCompare);
        for (Object i : asList(asMap(current.get("entities")).get("entities"))) {
            currIds.add(str(Py.get(asMap(i), "id", "")));
        }
        List<Object> added = new ArrayList<>();
        for (String id : currIds) {
            if (!prevIds.contains(id)) {
                added.add(id);
            }
        }
        List<Object> removed = new ArrayList<>();
        for (String id : prevIds) {
            if (!currIds.contains(id)) {
                removed.add(id);
            }
        }
        Map<String, Object> out = map();
        out.put("entities_added", added);
        out.put("entities_removed", removed);
        out.put("domain_changed", !java.util.Objects.equals(
                Py.get(asMap(previous.get("domain")), "domain", ""), Py.get(asMap(current.get("domain")), "domain", "")));
        out.put("ontology_evolved", !java.util.Objects.equals(previous.get("ontology"), current.get("ontology")));
        out.put("workflow_mutated", !java.util.Objects.equals(previous.get("workflow"), current.get("workflow")));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rememberSemanticRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"ontology", "semantic_graph", "entity_mappings", "semantic_workflows",
                "runtime_semantics"}) {
            if (!merged.containsKey(field)) {
                Object v = update.containsKey(field) ? update.get(field)
                        : (merged.containsKey(field) ? merged.get(field) : map());
                merged.put(field, v);
            }
        }
        merged.putAll(update);
        merged.put("bounded", true);
        return merged;
    }

    public static Map<String, Object> compileSemanticRuntimeIr(Map<String, Object> cognition) {
        Map<String, Object> out = map();
        out.put("ir", "semantic_runtime");
        out.put("ontology", Py.get(cognition, "ontology", map()));
        out.put("entities", Py.get(cognition, "entities", map()));
        out.put("semantic_graph", Py.get(cognition, "semantic_graph", map()));
        out.put("domain", Py.get(cognition, "domain", map()));
        out.put("ui_semantics", Py.get(cognition, "ui", map()));
        out.put("table_semantics", Py.get(cognition, "tables", map()));
        out.put("document_semantics", Py.get(cognition, "document", map()));
        out.put("repository_semantics", Py.get(cognition, "repository", map()));
        out.put("application_semantics", Py.get(cognition, "application", map()));
        out.put("causality_semantics", Py.get(cognition, "causality", map()));
        out.put("workflow_semantics", Py.get(cognition, "workflow", map()));
        out.put("alignment", Py.get(cognition, "alignment", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> semanticRuntimeIrToGraph(Map<String, Object> semanticIr) {
        Map<String, Object> graph = asMap(semanticIr.get("semantic_graph"));
        List<Object> nodes = new ArrayList<>(asList(graph.get("nodes")));
        List<Object> edges = asList(graph.get("edges"));
        Map<String, Object> ontology = asMap(semanticIr.get("ontology"));
        if (Py.truthy(ontology.get("primary_domain"))) {
            nodes.add(mapOf("id", "domain:" + str(ontology.get("primary_domain")), "type", "domain"));
        }
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "semantic:root", "type", "semantic")));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "semantic_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- orchestrator (html="" contract)

    /** {@code run_semantic_runtime} for the portable {@code html=""} contract. */
    public static Map<String, Object> runSemanticRuntime(String url, String text, List<Object> interactions,
            Map<String, Object> applicationResult, Map<String, Object> causalityResult,
            Map<String, Object> nativeCognition, List<Object> repositoryFiles, Map<String, Object> runtimeGraph,
            Map<String, Object> memory, String objective) {
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);
        List<Object> ix = interactions == null ? new ArrayList<>() : interactions;
        String combinedText = (text + " ");
        if (combinedText.length() > 100000) {
            combinedText = combinedText.substring(0, 100000);
        }

        List<Object> actions = new ArrayList<>();
        for (Object io : ix) {
            Map<String, Object> i = asMap(io);
            actions.add(mapOf("label", Py.get(i, "action", ""), "type", Py.get(i, "action", "")));
        }
        List<Object> artifacts = new ArrayList<>();
        if (Py.truthy(nativeCognition)) {
            artifacts.add(str(Py.get(nativeCognition, "runtime", "")));
        }
        Map<String, Object> structure = map();
        structure.put("actions", actions);
        structure.put("artifacts", artifacts);

        Map<String, Object> entitiesRaw = extractSemanticEntities(combinedText, structure);
        Map<String, Object> resolved = resolveSemanticEntities(asList(entitiesRaw.get("entities")));
        entitiesRaw.put("entities", resolved.get("entities"));

        List<Object> signals = new ArrayList<>();
        if (!objective.isEmpty()) {
            signals.add(objective);
        }
        Map<String, Object> domain = classifySemanticDomain(combinedText, signals);
        Map<String, Object> ontology = buildSemanticOntology(asList(entitiesRaw.get("entities")),
                str(domain.get("domain")));
        entitiesRaw.put("ontology", ontology);

        Map<String, Object> ui = extractUiSemantics(ix);
        Map<String, Object> tables = extractTableSemantics();
        Map<String, Object> document = extractDocumentSemantics(combinedText);
        Map<String, Object> repository = extractRepositorySemantics(repositoryFiles, combinedText);
        Map<String, Object> application = extractApplicationSemantics(applicationResult);
        Map<String, Object> causality = extractCausalitySemantics(causalityResult);
        Map<String, Object> workflow = extractWorkflowSemantics(
                asMap(Py.get(applicationResult == null ? map() : applicationResult, "workflow", null)), objective);
        Map<String, Object> browser = extractBrowserSemantics(url, null);
        Map<String, Object> rtSources = map();
        rtSources.put("browser", Py.truthy(browser));
        rtSources.put("native", Py.truthy(nativeCognition));
        rtSources.put("application", Py.truthy(applicationResult));
        Map<String, Object> runtime = extractRuntimeSemantics(runtimeGraph, rtSources);

        Map<String, Object> semanticGraph = buildSemanticGraph(asList(entitiesRaw.get("entities")),
                asList(entitiesRaw.get("relations")));

        Map<String, Object> browserAligned = new LinkedHashMap<>(browser);
        browserAligned.put("domain", domain.get("domain"));
        Map<String, Object> alignment = alignSemanticRuntimes(browserAligned, nativeCognition, repository, document,
                runtime);

        Map<String, Object> diff = map();
        if (Py.truthy(mem.get("entities"))) {
            Map<String, Object> cur = map();
            cur.put("entities", entitiesRaw);
            cur.put("domain", domain);
            cur.put("ontology", ontology);
            cur.put("workflow", workflow);
            diff = diffSemanticRuntime(mem, cur);
        }

        Map<String, Object> payload = map();
        payload.put("entities", entitiesRaw);
        payload.put("domain", domain);
        payload.put("ontology", ontology);
        payload.put("ui", ui);
        payload.put("tables", tables);
        payload.put("document", document);
        payload.put("repository", repository);
        payload.put("application", application);
        payload.put("causality", causality);
        payload.put("workflow", workflow);
        payload.put("browser", browser);
        payload.put("runtime", runtime);
        payload.put("semantic_graph", semanticGraph);
        payload.put("alignment", alignment);
        payload.put("diff", diff);
        payload.put("bounded", true);

        Map<String, Object> update = map();
        update.put("ontology", ontology);
        update.put("semantic_graph", semanticGraph);
        update.put("entity_mappings", resolved.get("canonical_map"));
        update.put("semantic_workflows", workflow);
        update.put("runtime_semantics", runtime);
        update.put("entities", entitiesRaw);
        update.put("domain", domain);
        Map<String, Object> updatedMemory = rememberSemanticRuntime(mem, update);
        payload.put("memory", updatedMemory);
        payload.put("replay", SemanticReplay.replaySemanticRuntime(updatedMemory));
        payload.put("semantic_ir", compileSemanticRuntimeIr(payload));
        return payload;
    }

    /** {@code run_semantic_for_extraction} (html="" contract; no FS on the empty memory path; text=""). */
    public static Map<String, Object> runSemanticForExtraction(boolean semanticRuntime, String url,
            List<Object> interactions, Map<String, Object> applicationResult, Map<String, Object> causalityResult,
            Map<String, Object> nativeCognition, Map<String, Object> runtimeGraph, String objective,
            boolean mergeGraph) {
        if (!semanticRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> memory = map();
        Map<String, Object> result = runSemanticRuntime(url, "", interactions, applicationResult, causalityResult,
                nativeCognition, null, runtimeGraph, memory, objective);
        Map<String, Object> graphIr = semanticRuntimeIrToGraph(asMap(Py.get(result, "semantic_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("semantic", result);
        out.put("semantic_ir", Py.get(result, "semantic_ir", map()));
        out.put("semantic_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
