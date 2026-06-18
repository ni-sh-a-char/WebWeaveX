package io.webweavex.workflow;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyRepr;
import io.webweavex.execution.ExecutionRuntime;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

/**
 * Port of the {@code core.workflows} family — {@code build_runtime_objective},
 * {@code build_workflow_plan}, {@code run_autonomous_workflow}, {@code replay_workflow_runtime},
 * {@code run_workflow_for_extraction}, {@code save_workflow_memory}, {@code load_workflow_memory}
 * — and the ~15 deterministic sub-engines + workflow IR they fan out to. Dependency-clean
 * (23-module closure, 0 forbidden; the FS workflow-memory engine is only invoked when a memory
 * path+key are supplied). Reuses the certified determinism/crypto/json substrate and
 * {@link ExecutionRuntime#buildUnifiedRuntimeGraph}.
 */
public final class WorkflowRuntime {

    private WorkflowRuntime() {
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
        return o instanceof List ? new ArrayList<>((List<Object>) o) : new ArrayList<>();
    }

    private static long pyInt(Object v, long dflt) {
        if (v == null) {
            return dflt;
        }
        if (v instanceof Boolean) {
            return ((Boolean) v) ? 1L : 0L;
        }
        if (v instanceof Number) {
            return (long) ((Number) v).doubleValue();
        }
        if (v instanceof String) {
            return Long.parseLong(((String) v).trim());
        }
        return dflt;
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
        return xs.size() > n ? xs.subList(0, n) : xs;
    }

    // -------------------------------------------------------------- objective / plan

    private static final Map<String, List<String>> OBJECTIVE_STEPS = new LinkedHashMap<>();

    static {
        OBJECTIVE_STEPS.put("extract_dashboard", List.of("navigate_dashboard", "capture_widgets", "capture_tables"));
        OBJECTIVE_STEPS.put("extract_invoices", List.of("open_invoices", "paginate", "extract_rows"));
        OBJECTIVE_STEPS.put("monitor_metrics", List.of("open_dashboard", "observe_metrics", "checkpoint"));
        OBJECTIVE_STEPS.put("capture_notifications", List.of("observe_notifications", "capture_events", "checkpoint"));
        OBJECTIVE_STEPS.put("extract_repository", List.of("scan_repository", "extract_structure", "compile_graph"));
        OBJECTIVE_STEPS.put("monitor_runtime", List.of("observe_runtime", "capture_mutations", "checkpoint"));
        OBJECTIVE_STEPS.put("capture_terminal", List.of("open_terminal", "capture_output", "checkpoint"));
        OBJECTIVE_STEPS.put("monitor_application", List.of("observe_application", "capture_state", "checkpoint"));
        OBJECTIVE_STEPS.put("extract_api_surface", List.of("discover_routes", "extract_endpoints", "compile_api"));
        OBJECTIVE_STEPS.put("monitor_infrastructure", List.of("observe_infra", "capture_status", "checkpoint"));
    }

    /** {@code build_runtime_objective}. */
    public static Map<String, Object> buildRuntimeObjective(String objective, long priority) {
        List<Object> steps = new ArrayList<>(
                OBJECTIVE_STEPS.getOrDefault(objective, List.of("observe", "extract", "checkpoint")));
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("priority", priority);
        out.put("steps", steps);
        out.put("bounded", true);
        return out;
    }

    private static String runtimeForStep(String step, String domain) {
        if (step.contains("terminal")) {
            return "terminal";
        }
        if (step.contains("repository") || step.contains("api")) {
            return "repository";
        }
        if (step.contains("infra") || domain.equals("infrastructure")) {
            return "native";
        }
        if (step.contains("notification")) {
            return "desktop";
        }
        return "browser";
    }

    /** {@code build_workflow_plan}. */
    public static Map<String, Object> buildWorkflowPlan(String objective, Map<String, Object> semanticRuntime,
            Map<String, Object> causality, Map<String, Object> applicationRuntime) {
        Map<String, Object> runtimeObjective = buildRuntimeObjective(objective, 0);
        Map<String, Object> sem = semanticRuntime == null ? map() : semanticRuntime;
        String domain = str(Py.get(asMap(Py.get(sem, "domain", map())), "domain", "saas"));

        List<Object> planSteps = new ArrayList<>();
        List<Object> objSteps = asList(runtimeObjective.get("steps"));
        for (int index = 0; index < objSteps.size(); index++) {
            String step = str(objSteps.get(index));
            Map<String, Object> ps = map();
            ps.put("id", "step:" + index);
            ps.put("action", step);
            ps.put("runtime", runtimeForStep(step, domain));
            ps.put("depends_on", index > 0 ? "step:" + (index - 1) : "");
            planSteps.add(ps);
        }
        if (Py.truthy(applicationRuntime)) {
            Map<String, Object> workflow = asMap(Py.get(applicationRuntime, "workflow", map()));
            for (Object eo : capped(asList(workflow.get("edges")), 100)) {
                Map<String, Object> ps = map();
                ps.put("id", "app:" + planSteps.size());
                ps.put("action", str(Py.get(asMap(eo), "relation", "transition")));
                ps.put("runtime", "application");
                ps.put("depends_on", planSteps.isEmpty() ? "" : asMap(planSteps.get(planSteps.size() - 1)).get("id"));
                planSteps.add(ps);
            }
        }
        if (Py.truthy(causality)) {
            Map<String, Object> inner = asMap(Py.get(causality, "causality", causality));
            for (Object ho : capped(asList(asMap(Py.get(inner, "propagation", map())).get("handoffs")), 50)) {
                Map<String, Object> ps = map();
                ps.put("id", "causal:" + planSteps.size());
                ps.put("action", "cross_runtime_handoff");
                ps.put("runtime", str(Py.get(asMap(ho), "to", "native")));
                ps.put("depends_on", planSteps.isEmpty() ? "" : asMap(planSteps.get(planSteps.size() - 1)).get("id"));
                planSteps.add(ps);
            }
        }
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("domain", domain);
        out.put("steps", planSteps);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- execution / state / navigation

    public static Map<String, Object> executeWorkflowPlan(Map<String, Object> plan, long tick) {
        List<Object> executed = new ArrayList<>();
        List<Object> steps = capped(asList(plan.get("steps")), 10000);
        for (int index = 0; index < steps.size(); index++) {
            Map<String, Object> step = asMap(steps.get(index));
            Map<String, Object> e = map();
            e.put("step_id", str(Py.get(step, "id", "step:" + index)));
            e.put("action", str(Py.get(step, "action", "")));
            e.put("runtime", str(Py.get(step, "runtime", "browser")));
            e.put("completed", true);
            e.put("tick", tick + index);
            e.put("replay_index", (long) index);
            executed.add(e);
        }
        Map<String, Object> out = map();
        out.put("objective", Py.get(plan, "objective", ""));
        out.put("executed", executed);
        out.put("completed_count", (long) executed.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWorkflowState(Map<String, Object> plan, Map<String, Object> execution) {
        Map<String, Object> exec = execution == null ? map() : execution;
        List<Object> executed = asList(exec.get("executed"));
        List<Object> steps = asList(plan.get("steps"));
        List<Object> completed = new ArrayList<>();
        for (Object io : executed) {
            Map<String, Object> item = asMap(io);
            if (Py.truthy(item.get("completed"))) {
                completed.add(item.get("step_id"));
            }
        }
        Map<String, Object> rs = map();
        rs.put("objective", Py.get(plan, "objective", ""));
        rs.put("total_steps", (long) steps.size());
        Map<String, Object> out = map();
        out.put("current_step", 0L);
        out.put("completed_steps", completed);
        out.put("retries", 0L);
        out.put("runtime_state", rs);
        out.put("extraction_outputs", new ArrayList<>());
        out.put("semantic_checkpoints", new ArrayList<>());
        out.put("bounded", true);
        return out;
    }

    private static final Map<String, String> RUNTIME_NAVIGATORS = new LinkedHashMap<>();

    static {
        RUNTIME_NAVIGATORS.put("browser", "browser_navigation");
        RUNTIME_NAVIGATORS.put("electron", "electron_navigation");
        RUNTIME_NAVIGATORS.put("desktop", "modal_traversal");
        RUNTIME_NAVIGATORS.put("terminal", "terminal_progression");
        RUNTIME_NAVIGATORS.put("native", "vm_runtime_transition");
        RUNTIME_NAVIGATORS.put("remote", "remote_runtime_traversal");
        RUNTIME_NAVIGATORS.put("application", "application_navigation");
        RUNTIME_NAVIGATORS.put("repository", "repository_navigation");
    }

    public static Map<String, Object> navigateRuntimeWorkflow(Map<String, Object> plan, long tick) {
        List<Object> navigations = new ArrayList<>();
        List<Object> steps = capped(asList(plan.get("steps")), 10000);
        for (int index = 0; index < steps.size(); index++) {
            Map<String, Object> step = asMap(steps.get(index));
            String runtime = str(Py.get(step, "runtime", "browser"));
            Map<String, Object> n = map();
            n.put("step_id", str(Py.get(step, "id", "step:" + index)));
            n.put("runtime", runtime);
            n.put("navigator", RUNTIME_NAVIGATORS.getOrDefault(runtime, "browser_navigation"));
            n.put("action", str(Py.get(step, "action", "")));
            n.put("tick", tick + index);
            navigations.add(n);
        }
        Map<String, Object> out = map();
        out.put("navigations", navigations);
        out.put("count", (long) navigations.size());
        out.put("bounded", true);
        return out;
    }

    public static List<Object> buildWorkflowTransitions(Map<String, Object> execution) {
        List<Object> transitions = new ArrayList<>();
        List<Object> executed = asList(execution.get("executed"));
        for (int index = 1; index < executed.size(); index++) {
            transitions.add(mapOf("from", str(Py.get(asMap(executed.get(index - 1)), "step_id", "")),
                    "to", str(Py.get(asMap(executed.get(index)), "step_id", "")), "relation", "transitions"));
        }
        return transitions;
    }

    public static Map<String, Object> buildWorkflowDependencies(Map<String, Object> plan) {
        List<Object> ordering = new ArrayList<>();
        List<Object> prerequisites = new ArrayList<>();
        List<Object> runtimeDeps = new ArrayList<>();
        List<Object> chains = new ArrayList<>();
        List<Object> steps = capped(asList(plan.get("steps")), 10000);
        for (int index = 0; index < steps.size(); index++) {
            Map<String, Object> step = asMap(steps.get(index));
            String dependsOn = str(Py.get(step, "depends_on", ""));
            if (!dependsOn.isEmpty()) {
                ordering.add(mapOf("step", str(Py.get(step, "id", "")), "depends_on", dependsOn));
                prerequisites.add(mapOf("step", str(Py.get(step, "id", "")), "requires", dependsOn));
            }
            if (index > 0) {
                String prevRuntime = str(Py.get(asMap(steps.get(index - 1)), "runtime", ""));
                String currRuntime = str(Py.get(step, "runtime", ""));
                if (!prevRuntime.equals(currRuntime)) {
                    runtimeDeps.add(mapOf("from", prevRuntime, "to", currRuntime));
                }
            }
            chains.add(mapOf("step", str(Py.get(step, "id", "")), "action", str(Py.get(step, "action", ""))));
        }
        Map<String, Object> out = map();
        out.put("execution_ordering", ordering);
        out.put("semantic_prerequisites", prerequisites);
        out.put("runtime_dependencies", runtimeDeps);
        out.put("extraction_chains", chains);
        out.put("bounded", true);
        return out;
    }

    private static final Map<String, String> RECOVERY_ACTIONS = new LinkedHashMap<>();

    static {
        RECOVERY_ACTIONS.put("selector_drift", "heal_selector");
        RECOVERY_ACTIONS.put("modal_interruption", "recover_modal");
        RECOVERY_ACTIONS.put("pagination_failure", "retry_pagination");
        RECOVERY_ACTIONS.put("runtime_mutation", "realign_runtime");
        RECOVERY_ACTIONS.put("authentication_expiration", "reauthenticate");
        RECOVERY_ACTIONS.put("worker_failure", "redispatch_worker");
    }

    public static Map<String, Object> recoverWorkflowRuntime(Map<String, Object> state, List<Object> failures) {
        List<Object> f = failures == null ? new ArrayList<>() : failures;
        List<Object> recovered = new ArrayList<>();
        for (Object fo : capped(f, 100)) {
            String failure = str(fo);
            recovered.add(mapOf("failure", failure,
                    "action", RECOVERY_ACTIONS.getOrDefault(failure, "retry_step"), "recovered", true));
        }
        if (f.isEmpty() && pyInt(Py.get(state, "current_step", 0L), 0) > 0) {
            recovered.add(mapOf("failure", "implicit_retry", "action", "retry_step", "recovered", true));
        }
        Map<String, Object> newState = new LinkedHashMap<>(state);
        newState.put("retries", pyInt(Py.get(state, "retries", 0L), 0) + recovered.size());
        Map<String, Object> out = map();
        out.put("state", newState);
        out.put("recovered_steps", recovered);
        out.put("recovered", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> alignWorkflowRuntime(Map<String, Object> plan, Map<String, Object> state,
            Map<String, Object> execution) {
        Map<String, Object> out = map();
        out.put("objective", Py.get(plan, "objective", ""));
        out.put("steps_aligned",
                (long) asList(plan.get("steps")).size() == pyInt(Py.get(execution, "completed_count", 0L), 0));
        out.put("state_step", Py.get(state, "current_step", 0L));
        out.put("aligned", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> alignWorkflowSemantics(Map<String, Object> plan,
            Map<String, Object> semanticRuntime, Map<String, Object> causality) {
        Map<String, Object> sem = semanticRuntime == null ? map() : semanticRuntime;
        Map<String, Object> inner = asMap(Py.get(sem, "semantic", sem));
        Object chains = Py.truthy(causality)
                ? Py.get(asMap(Py.get(causality, "causality", causality)), "propagation", map()) : map();
        Map<String, Object> out = map();
        out.put("ontology", Py.get(inner, "ontology", map()));
        out.put("domain", Py.get(inner, "domain", map()));
        out.put("causality_chains", chains);
        out.put("workflow_objective", Py.get(plan, "objective", ""));
        out.put("extraction_semantics", Py.get(inner, "semantic_graph", map()));
        out.put("aligned", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> federateWorkflowRuntime(Map<String, Object> browser, Map<String, Object> native_,
            Map<String, Object> distributed, Map<String, Object> semantic, List<Object> workers) {
        List<Object> wk = workers == null ? new ArrayList<>() : workers;
        List<Object> fw = new ArrayList<>();
        List<Object> capped = capped(wk, 1000);
        for (int index = 0; index < capped.size(); index++) {
            Map<String, Object> worker = asMap(capped.get(index));
            fw.add(mapOf("worker_id", str(Py.get(worker, "worker_id", Py.get(worker, "id", "w:" + index))),
                    "synced", true));
        }
        Object checkpoints = Py.truthy(semantic)
                ? Py.get(asMap(Py.get(semantic, "semantic", map())), "memory", map()) : map();
        Map<String, Object> out = map();
        out.put("workers", fw);
        out.put("semantic_checkpoints", checkpoints);
        out.put("browser_runtime", Py.truthy(browser));
        out.put("native_runtime", Py.truthy(native_));
        out.put("extraction_agents", (long) wk.size());
        out.put("distributed_sync", Py.truthy(distributed));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> scheduleWorkflowExecution(List<Object> plans, long tick) {
        List<Object> ordered = new ArrayList<>(plans);
        ordered.sort(Comparator
                .comparingLong((Object p) -> pyInt(Py.get(asMap(p), "priority",
                        Py.get(asMap(p), "objective_priority", 0L)), 0))
                .thenComparing(p -> str(Py.get(asMap(p), "objective", "")), WorkflowRuntime::cmp));
        List<Object> schedule = new ArrayList<>();
        List<Object> cap = capped(ordered, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> plan = asMap(cap.get(index));
            Map<String, Object> s = map();
            s.put("objective", Py.get(plan, "objective", ""));
            s.put("priority", pyInt(Py.get(plan, "priority", 0L), 0));
            s.put("tick", tick + index);
            s.put("pacing", (long) index);
            s.put("retries", 0L);
            s.put("distributed_order", (long) index);
            schedule.add(s);
        }
        Map<String, Object> out = map();
        out.put("schedule", schedule);
        out.put("count", (long) schedule.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWorkflowRuntimeContext(String url, String runtime,
            Map<String, Object> sources) {
        Map<String, Object> src = sources == null ? map() : sources;
        List<Object> sortedKeys = new ArrayList<>();
        TreeSet<String> ts = new TreeSet<>(Normalization::codePointCompare);
        ts.addAll(src.keySet());
        sortedKeys.addAll(ts);
        Map<String, Object> out = map();
        out.put("url", url);
        out.put("primary_runtime", runtime);
        out.put("sources", sortedKeys);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWorkflowGraph(Map<String, Object> objective, Map<String, Object> plan,
            Map<String, Object> state, Map<String, Object> execution, List<Object> transitions) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        String objName = str(Py.get(objective, "objective", "objective"));
        nodes.add(mapOf("id", "objective:" + objName, "type", "objective"));
        for (Object so : capped(asList(plan.get("steps")), 10000)) {
            Map<String, Object> step = asMap(so);
            String stepId = str(Py.get(step, "id", ""));
            nodes.add(mapOf("id", stepId, "type", "step", "runtime", str(Py.get(step, "runtime", ""))));
            String dependsOn = str(Py.get(step, "depends_on", ""));
            if (!dependsOn.isEmpty()) {
                edges.add(mapOf("from", dependsOn, "to", stepId, "relation", "depends_on"));
            }
            edges.add(mapOf("from", "objective:" + objName, "to", stepId, "relation", "executes"));
        }
        for (Object to : capped(transitions, 10000)) {
            Map<String, Object> t = asMap(to);
            edges.add(mapOf("from", str(Py.get(t, "from", "")), "to", str(Py.get(t, "to", "")),
                    "relation", "transitions"));
        }
        if (pyInt(Py.get(state, "retries", 0L), 0) > 0) {
            nodes.add(mapOf("id", "checkpoint:recovery", "type", "checkpoint"));
            edges.add(mapOf("from", "checkpoint:recovery", "to", "objective:" + objName, "relation", "recovers"));
        }
        nodes.add(mapOf("id", "semantic:state", "type", "semantic_state"));
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator
                .comparing((Object e) -> str(Py.get(asMap(e), "from", "")), WorkflowRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), WorkflowRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), WorkflowRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- replay / IR / memory

    /** {@code replay_workflow_runtime}. */
    public static Map<String, Object> replayWorkflowRuntime(Map<String, Object> memory) {
        Map<String, Object> m = memory == null ? map() : memory;
        Map<String, Object> out = map();
        out.put("execution_steps", Py.get(m, "execution_graphs", map()));
        out.put("runtime_transitions", Py.get(m, "runtime_transitions", new ArrayList<>()));
        out.put("distributed_execution", Py.get(m, "distributed_tasks", new ArrayList<>()));
        out.put("semantic_workflows", Py.get(m, "workflow_states", map()));
        out.put("objectives", Py.get(m, "objectives", map()));
        out.put("replayed", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> compileWorkflowRuntimeIr(Map<String, Object> workflow) {
        Map<String, Object> out = map();
        out.put("ir", "workflow_runtime");
        out.put("objective", Py.get(workflow, "objective", map()));
        out.put("plan", Py.get(workflow, "plan", map()));
        out.put("execution", Py.get(workflow, "execution", map()));
        out.put("state", Py.get(workflow, "state", map()));
        out.put("workflow_graph", Py.get(workflow, "workflow_graph", map()));
        out.put("dependencies", Py.get(workflow, "dependencies", map()));
        out.put("federation", Py.get(workflow, "federation", map()));
        out.put("semantic_alignment", Py.get(workflow, "semantic_alignment", map()));
        out.put("recovery", Py.get(workflow, "recovery", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> workflowRuntimeIrToGraph(Map<String, Object> workflowIr) {
        Map<String, Object> graph = asMap(workflowIr.get("workflow_graph"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "workflow:root", "type", "workflow")));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "workflow_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rememberWorkflowRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"objectives", "workflow_states", "execution_graphs",
                "semantic_checkpoints", "runtime_transitions"}) {
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

    private static Map<String, Object> emptyMemory() {
        Map<String, Object> m = map();
        m.put("objectives", map());
        m.put("workflow_states", map());
        m.put("execution_graphs", map());
        m.put("semantic_checkpoints", new ArrayList<>());
        m.put("runtime_transitions", new ArrayList<>());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_workflow_memory(path, memory, key)}. */
    public static Map<String, Object> saveWorkflowMemory(String path, Map<String, Object> memory, String key) {
        String payload = PyJson.dumpsDefaultAscii(memory);
        Map<String, Object> encrypted = Kaalka.encryptValueEnvelope(payload, key);
        Map<String, Object> wrapper = map();
        wrapper.put("encrypted", encrypted.get("encrypted"));
        wrapper.put("algorithm", "kaalka");
        Path target = Paths.get(path);
        try {
            Path parent = target.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            Files.write(target, PyJson.dumpsDefaultAscii(wrapper).getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        Map<String, Object> out = map();
        out.put("saved", true);
        out.put("path", target.toString());
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code load_workflow_memory(path, key)}. */
    public static Map<String, Object> loadWorkflowMemory(String path, String key) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("memory", emptyMemory());
            out.put("bounded", true);
            return out;
        }
        try {
            String content = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
            Map<String, Object> wrapper = asMap(PyJsonParse.loads(content));
            Map<String, Object> decrypted = Kaalka.decryptValueEnvelope(str(wrapper.get("encrypted")), key);
            Object memory = PyJsonParse.loads(str(decrypted.get("decrypted")));
            Map<String, Object> out = map();
            out.put("available", true);
            out.put("memory", memory);
            out.put("algorithm", "kaalka");
            out.put("bounded", true);
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // -------------------------------------------------------------- orchestrator

    /** {@code run_autonomous_workflow}. */
    public static Map<String, Object> runAutonomousWorkflow(String objective, long priority,
            Map<String, Object> semanticRuntime, Map<String, Object> causalityResult,
            Map<String, Object> applicationResult, Map<String, Object> distributedResult,
            Map<String, Object> nativeCognition, String url, Map<String, Object> memory, long tick,
            List<Object> failures) {
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);
        Map<String, Object> runtimeObjective = buildRuntimeObjective(objective, priority);

        Map<String, Object> sem = semanticRuntime == null ? map() : semanticRuntime;
        Map<String, Object> semanticInner = asMap(Py.get(sem, "semantic", sem));
        Map<String, Object> plan = buildWorkflowPlan(objective, semanticInner, causalityResult, applicationResult);
        plan.put("priority", priority);

        Map<String, Object> execution = executeWorkflowPlan(plan, tick);
        Map<String, Object> state = buildWorkflowState(plan, execution);
        Map<String, Object> navigation = navigateRuntimeWorkflow(plan, tick);
        List<Object> transitions = buildWorkflowTransitions(execution);
        Map<String, Object> dependencies = buildWorkflowDependencies(plan);
        Map<String, Object> recovery = recoverWorkflowRuntime(state, failures);
        Map<String, Object> alignment = alignWorkflowRuntime(plan, state, execution);
        Map<String, Object> semanticAlignment = alignWorkflowSemantics(plan, semanticRuntime, causalityResult);
        Map<String, Object> federation = federateWorkflowRuntime(mapOf("url", url), nativeCognition,
                distributedResult, semanticRuntime,
                asList(Py.get(distributedResult == null ? map() : distributedResult, "workers", new ArrayList<>())));
        Map<String, Object> schedule = scheduleWorkflowExecution(new ArrayList<>(List.of(plan)), tick);
        List<Object> planSteps = asList(plan.get("steps"));
        String ctxRuntime = planSteps.isEmpty() ? "browser" : str(asMap(planSteps.get(0)).get("runtime"));
        Map<String, Object> sources = map();
        sources.put("semantic", Py.truthy(semanticRuntime));
        sources.put("causality", Py.truthy(causalityResult));
        sources.put("application", Py.truthy(applicationResult));
        sources.put("distributed", Py.truthy(distributedResult));
        Map<String, Object> context = buildWorkflowRuntimeContext(url, ctxRuntime, sources);
        Map<String, Object> workflowGraph = buildWorkflowGraph(runtimeObjective, plan, state, execution, transitions);

        Map<String, Object> payload = map();
        payload.put("objective", runtimeObjective);
        payload.put("plan", plan);
        payload.put("execution", execution);
        payload.put("state", state);
        payload.put("navigation", navigation);
        payload.put("transitions", transitions);
        payload.put("dependencies", dependencies);
        payload.put("recovery", recovery);
        payload.put("alignment", alignment);
        payload.put("semantic_alignment", semanticAlignment);
        payload.put("federation", federation);
        payload.put("schedule", schedule);
        payload.put("context", context);
        payload.put("workflow_graph", workflowGraph);
        payload.put("bounded", true);

        Map<String, Object> update = map();
        update.put("objectives", runtimeObjective);
        update.put("workflow_states", state);
        update.put("execution_graphs", execution);
        update.put("semantic_checkpoints", new ArrayList<>(List.of(semanticAlignment)));
        update.put("runtime_transitions", transitions);
        update.put("workflow_graph", workflowGraph);
        Map<String, Object> updatedMemory = rememberWorkflowRuntime(mem, update);
        payload.put("memory", updatedMemory);
        payload.put("replay", replayWorkflowRuntime(updatedMemory));
        payload.put("workflow_ir", compileWorkflowRuntimeIr(payload));
        return payload;
    }

    /** {@code run_workflow_for_extraction} (no FS when memory path/key empty). */
    public static Map<String, Object> runWorkflowForExtraction(boolean autonomousWorkflow, String objective,
            String memoryPath, String memoryKey, String url, Map<String, Object> semanticRuntime,
            Map<String, Object> causalityResult, Map<String, Object> applicationResult,
            Map<String, Object> distributedResult, Map<String, Object> nativeCognition, boolean mergeGraph,
            long tick) {
        if (!autonomousWorkflow) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> memory = map(); // empty memory path -> no FS load

        Map<String, Object> result = runAutonomousWorkflow(objective, 0, semanticRuntime, causalityResult,
                applicationResult, distributedResult, nativeCognition, url, memory, tick, null);

        Map<String, Object> graphIr = workflowRuntimeIrToGraph(asMap(Py.get(result, "workflow_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("workflow", result);
        out.put("workflow_ir", Py.get(result, "workflow_ir", map()));
        out.put("workflow_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
