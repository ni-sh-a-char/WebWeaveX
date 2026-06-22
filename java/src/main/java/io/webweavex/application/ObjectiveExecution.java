package io.webweavex.application;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.application.objective_execution_engine.execute_runtime_objective} (and its
 * helper {@code build_runtime_goal}). Dependency-clean (0 forbidden, importable). Pure transform.
 * Zero new substrate.
 */
public final class ObjectiveExecution {

    private ObjectiveExecution() {
    }

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

    private static final Map<String, List<String>> OBJECTIVES = new LinkedHashMap<>();

    static {
        OBJECTIVES.put("login", List.of("open_login", "fill_credentials", "submit"));
        OBJECTIVES.put("extract_dashboard", List.of("navigate_dashboard", "capture_widgets", "capture_tables"));
        OBJECTIVES.put("export_report", List.of("open_reports", "select_report", "export"));
        OBJECTIVES.put("extract_invoices", List.of("open_invoices", "paginate", "extract_rows"));
        OBJECTIVES.put("monitor_metrics", List.of("open_dashboard", "observe_metrics", "checkpoint"));
    }

    /** {@code build_runtime_goal(objective)}. */
    public static Map<String, Object> buildRuntimeGoal(String objective) {
        List<String> steps = OBJECTIVES.getOrDefault(objective, List.of("observe", "extract"));
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("steps", new ArrayList<Object>(steps));
        out.put("bounded", true);
        return out;
    }

    /** {@code execute_runtime_objective(objective, workflow_graph, action_graph, navigation, adaptive_runtime)}. */
    public static Map<String, Object> executeRuntimeObjective(String objective, Map<String, Object> workflowGraph,
            Map<String, Object> actionGraph, Map<String, Object> navigation, Map<String, Object> adaptiveRuntime) {
        Map<String, Object> wf = workflowGraph == null ? map() : workflowGraph;
        Map<String, Object> ag = actionGraph == null ? map() : actionGraph;
        Map<String, Object> nav = navigation == null ? map() : navigation;
        Map<String, Object> goal = buildRuntimeGoal(objective);
        List<Object> steps = asList(goal.get("steps"));
        long workflowNodes = asList(wf.get("nodes")).size();
        long actionNodes = asList(ag.get("nodes")).size();
        List<Object> routes = asList(nav.get("routes"));
        String route = routes.isEmpty() ? "" : (String) Py.get(asMap(routes.get(0)), "path", "");
        List<Object> executed = new ArrayList<>();
        for (int index = 0; index < steps.size(); index++) {
            Map<String, Object> e = map();
            e.put("step", (long) index);
            e.put("name", steps.get(index));
            e.put("workflow_nodes", workflowNodes);
            e.put("action_nodes", actionNodes);
            e.put("route", route);
            e.put("adaptive", Py.truthy(adaptiveRuntime));
            e.put("completed", true);
            executed.add(e);
        }
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("goal", goal);
        out.put("executed", executed);
        out.put("bounded", true);
        return out;
    }
}
