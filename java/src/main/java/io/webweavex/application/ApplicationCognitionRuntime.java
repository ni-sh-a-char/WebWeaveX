package io.webweavex.application;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.application.application_cognition_orchestrator.run_application_cognition} +
 * its application sub-engines, for the proven portable {@code html=""} contract. Five sub-engines
 * (ui/form/dashboard/navigation/recovery) call BeautifulSoup, but on {@code html=""} they parse an
 * empty document and contribute nothing observable (verified: ui all-empty, forms empty, dashboard
 * empty, navigation derived only from {@code url}/{@code route_history}). So the output is
 * bs4-independent and byte-exact for the {@code html=""} contract. Reuses the certified
 * {@link ObjectiveExecution#executeRuntimeObjective}. Zero new substrate.
 */
public final class ApplicationCognitionRuntime {

    private ApplicationCognitionRuntime() {
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

    private static String sliceStr(String s, int n) {
        return s.length() > n ? s.substring(0, n) : s;
    }

    // -------------------------------------------------------------- bs4 engines (html="" contract)

    /** {@code extract_ui_semantics(html="")} — empty document yields all-empty semantics. */
    public static Map<String, Object> extractUiSemantics() {
        Map<String, Object> semantics = map();
        for (String k : new String[] {"dashboards", "forms", "navigation_menus", "tables", "charts",
                "filters", "search_bars", "sidebars", "tabs"}) {
            semantics.put(k, new ArrayList<>());
        }
        Map<String, Object> out = map();
        out.put("semantics", semantics);
        out.put("bounded", true);
        return out;
    }

    /** {@code build_form_runtime(html="")}. */
    public static Map<String, Object> buildFormRuntime() {
        Map<String, Object> out = map();
        out.put("forms", new ArrayList<>());
        out.put("form_count", 0L);
        out.put("bounded", true);
        return out;
    }

    /** {@code build_dashboard_runtime(html="")}. */
    public static Map<String, Object> buildDashboardRuntime() {
        Map<String, Object> out = map();
        out.put("widgets", new ArrayList<>());
        out.put("metrics", new ArrayList<>());
        out.put("tables", new ArrayList<>());
        out.put("filters", new ArrayList<>());
        out.put("charts", new ArrayList<>());
        out.put("update_interval", 30L);
        out.put("bounded", true);
        return out;
    }

    /** {@code build_navigation_semantics(html="", route, route_history)} — html-independent part. */
    public static Map<String, Object> buildNavigationSemantics(String route, List<Object> routeHistory) {
        List<Object> routes;
        if (routeHistory != null && !routeHistory.isEmpty()) {
            routes = capped(routeHistory, 500);
        } else {
            routes = new ArrayList<>(List.of(mapOf("path", route, "order", 0L)));
        }
        Map<String, Object> out = map();
        out.put("menus", new ArrayList<>());
        out.put("breadcrumbs", new ArrayList<>());
        out.put("routes", routes);
        out.put("spa_transitions", routes.size() > 1);
        out.put("tab_hierarchy", new ArrayList<>());
        out.put("bounded", true);
        return out;
    }

    /** {@code recover_application_runtime(html="", state)} — forms empty on empty HTML. */
    public static Map<String, Object> recoverApplicationRuntime(Map<String, Object> state) {
        Map<String, Object> out = map();
        out.put("route", Py.get(state, "route", "/"));
        out.put("forms_recovered", new ArrayList<>());
        out.put("modals_cleared", asList(state.get("modals")).isEmpty());
        out.put("session_valid", Py.get(state, "authenticated", false));
        out.put("workflow_resumed", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- pure engines

    public static Map<String, Object> buildApplicationState(String route, List<Object> forms, List<Object> modals,
            List<Object> widgets, List<Object> tabs, boolean authenticated) {
        Map<String, Object> out = map();
        out.put("route", sliceStr(route, 2000));
        out.put("forms", capped(forms == null ? new ArrayList<>() : forms, 500));
        out.put("modals", capped(modals == null ? new ArrayList<>() : modals, 200));
        out.put("widgets", capped(widgets == null ? new ArrayList<>() : widgets, 1000));
        out.put("tabs", capped(tabs == null ? new ArrayList<>() : tabs, 100));
        out.put("authenticated", authenticated);
        out.put("runtime_state", map());
        out.put("bounded", true);
        return out;
    }

    public static List<Object> buildApplicationTransitions(List<Object> states) {
        List<Object> transitions = new ArrayList<>();
        for (int index = 0; index < states.size() - 1; index++) {
            transitions.add(mapOf("from", str(Py.get(asMap(states.get(index)), "route", "")),
                    "to", str(Py.get(asMap(states.get(index + 1)), "route", "")),
                    "relation", "transition", "order", (long) index));
        }
        return capped(transitions, 10000);
    }

    public static Map<String, Object> buildActionGraph(List<Object> interactions) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        List<Object> cap = capped(interactions == null ? new ArrayList<>() : interactions, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> action = asMap(cap.get(index));
            String nodeId = "action_" + index;
            nodes.add(mapOf("id", nodeId, "type", str(Py.get(action, "action", Py.get(action, "type", "action"))),
                    "selector", str(Py.get(action, "selector", ""))));
            if (index > 0) {
                edges.add(mapOf("from", "action_" + (index - 1), "to", nodeId, "relation", "sequential"));
            }
        }
        Map<String, Object> out = map();
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWorkflowGraph(List<Object> states, List<Object> transitions,
            List<Object> actions) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        List<Object> stateCap = capped(states, 5000);
        for (int index = 0; index < stateCap.size(); index++) {
            nodes.add(mapOf("id", str(Py.get(asMap(stateCap.get(index)), "route", "state_" + index)), "type", "page"));
        }
        for (Object to : capped(transitions, 10000)) {
            Map<String, Object> t = asMap(to);
            edges.add(mapOf("from", str(Py.get(t, "from", "")), "to", str(Py.get(t, "to", "")),
                    "relation", str(Py.get(t, "relation", "transition"))));
        }
        for (Object ao : capped(actions == null ? new ArrayList<>() : actions, 10000)) {
            Map<String, Object> action = asMap(ao);
            String actionType = str(Py.get(action, "action", Py.get(action, "type", "")));
            String relation = "submit";
            if (actionType.equals("click")) {
                relation = "navigate";
            } else if (actionType.contains("modal")) {
                relation = "open_modal";
            }
            edges.add(mapOf("from", str(Py.get(action, "from", "")), "to", str(Py.get(action, "to", "")),
                    "relation", relation));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), ApplicationCognitionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), ApplicationCognitionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), ApplicationCognitionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    private static final Map<String, String> INTENT_MAP = new LinkedHashMap<>();

    static {
        INTENT_MAP.put("extract_dashboard", "observe_metrics");
        INTENT_MAP.put("login", "authenticate");
        INTENT_MAP.put("export_report", "export_data");
        INTENT_MAP.put("extract_invoices", "collect_records");
        INTENT_MAP.put("monitor_metrics", "continuous_observe");
    }

    public static Map<String, Object> resolveApplicationIntent(String objective) {
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("intent", INTENT_MAP.getOrDefault(objective, "observe"));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildApplicationContext(String url, Map<String, Object> state,
            Map<String, Object> identity) {
        Map<String, Object> out = map();
        out.put("url", url);
        out.put("route", Py.get(state, "route", url));
        out.put("authenticated", Py.get(state, "authenticated", false));
        out.put("identity_profile", Py.get(identity, "profile_id", "default"));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rememberApplicationRuntime(Map<String, Object> memory,
            Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"workflows", "forms", "action_graphs", "navigation_flows",
                "dashboard_structures"}) {
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

    // -------------------------------------------------------------- orchestrator

    /** {@code run_application_cognition} for the portable {@code html=""} contract. */
    public static Map<String, Object> runApplicationCognition(String url, List<Object> interactions,
            Map<String, Object> memory, String objective, boolean authenticated, Map<String, Object> identity,
            Map<String, Object> adaptiveRuntime, List<Object> routeHistory, List<Object> modals) {
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);
        List<Object> ix = interactions == null ? new ArrayList<>() : interactions;
        Map<String, Object> id = identity == null ? map() : identity;

        Map<String, Object> ui = extractUiSemantics();
        Map<String, Object> formsRuntime = buildFormRuntime();
        Map<String, Object> dashboard = buildDashboardRuntime();
        Map<String, Object> navigation = buildNavigationSemantics(url, routeHistory);

        Map<String, Object> state = buildApplicationState(url, asList(formsRuntime.get("forms")),
                modals == null ? new ArrayList<>() : modals, asList(dashboard.get("widgets")),
                asList(navigation.get("tab_hierarchy")), authenticated);

        List<Object> states;
        if (Py.truthy(mem.get("application_state"))) {
            states = new ArrayList<>(List.of(mem.get("application_state"), state));
        } else {
            states = new ArrayList<>(List.of(state));
        }

        List<Object> transitions = buildApplicationTransitions(states);
        Map<String, Object> actionGraph = buildActionGraph(ix);
        Map<String, Object> workflow = buildWorkflowGraph(states, transitions, ix);

        Map<String, Object> intent = resolveApplicationIntent(objective);
        Map<String, Object> execution = ObjectiveExecution.executeRuntimeObjective(objective, workflow, actionGraph,
                navigation, adaptiveRuntime);

        Map<String, Object> recovery = recoverApplicationRuntime(state);
        Map<String, Object> context = buildApplicationContext(url, state, id);

        Map<String, Object> update = map();
        update.put("application_state", state);
        update.put("workflows", workflow);
        update.put("forms", formsRuntime);
        update.put("action_graphs", actionGraph);
        update.put("navigation_flows", navigation);
        update.put("dashboard_structures", dashboard);
        update.put("objectives", new ArrayList<>(List.of(objective)));
        update.put("ui_semantics", ui);
        Map<String, Object> updatedMemory = rememberApplicationRuntime(mem, update);

        Map<String, Object> out = map();
        out.put("application_state", state);
        out.put("ui_semantics", ui);
        out.put("forms", formsRuntime);
        out.put("dashboard", dashboard);
        out.put("navigation", navigation);
        out.put("workflow", workflow);
        out.put("action_graph", actionGraph);
        out.put("intent", intent);
        out.put("execution", execution);
        out.put("recovery", recovery);
        out.put("context", context);
        out.put("memory", updatedMemory);
        out.put("bounded", true);
        return out;
    }
}
