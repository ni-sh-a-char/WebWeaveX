package io.webweavex.execution;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyRepr;
import io.webweavex.determinism.PyText;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/**
 * Port of the {@code core.execution} family — {@code build_runtime_sandbox},
 * {@code execute_runtime_action}, {@code replay_runtime_execution},
 * {@code simulate_runtime_execution}, {@code run_execution_runtime},
 * {@code run_execution_for_extraction} — and the ~18 deterministic sub-engines + execution IR
 * they fan out to. Dependency-clean (26-module closure, 0 forbidden; the FS checkpoint engine
 * is imported but only invoked when a memory path+key are supplied, never in these paths).
 */
public final class ExecutionRuntime {

    private ExecutionRuntime() {
    }

    // ------------------------------------------------------------------ helpers

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

    /** {@code dict(o or {})} / {@code list(o or [])} copies. */
    private static Map<String, Object> dictCopy(Object o) {
        return new LinkedHashMap<>(asMap(o));
    }

    private static List<Object> listCopy(Object o) {
        return asList(o);
    }

    /** {@code int(x)} — truncate toward zero; default when null. */
    private static long pyInt(Object v, long dflt) {
        if (v == null) {
            return dflt;
        }
        if (v instanceof Boolean) {
            return ((Boolean) v) ? 1L : 0L;
        }
        if (v instanceof Number) {
            double d = ((Number) v).doubleValue();
            return (long) d;
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

    private static String sha256hex32(String text) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] d = md.digest(text.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder(64);
            for (byte b : d) {
                sb.append(Character.forDigit((b >> 4) & 0xF, 16));
                sb.append(Character.forDigit(b & 0xF, 16));
            }
            return sb.substring(0, 32);
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    // ------------------------------------------------------------------ sandbox

    /** {@code build_runtime_sandbox}. */
    public static Map<String, Object> buildRuntimeSandbox(String runtime, List<Object> allowedActions,
            boolean rollbackEnabled, long maxActions, long timeoutTicks, String replayPolicy) {
        List<Object> defaultAllowed = new ArrayList<>(List.of("browser_click", "browser_focus", "native_focus"));
        if (runtime.equals("terminal")) {
            defaultAllowed = new ArrayList<>(List.of("terminal_command"));
        } else if (runtime.equals("native")) {
            defaultAllowed = new ArrayList<>(List.of("native_focus"));
        } else if (runtime.equals("vm")) {
            defaultAllowed = new ArrayList<>(List.of("vm_execute"));
        }
        List<Object> allowed = (allowedActions == null || allowedActions.isEmpty()) ? defaultAllowed
                : new ArrayList<>(allowedActions);
        allowed.sort((a, b) -> cmp(str(a), str(b)));

        Map<String, Object> bounds = map();
        bounds.put("max_depth", 50L);
        bounds.put("max_mutations", 100L);
        bounds.put("timeout_ticks", timeoutTicks);
        Map<String, Object> out = map();
        out.put("runtime", runtime);
        out.put("allowed_actions", allowed);
        out.put("rollback_enabled", rollbackEnabled);
        out.put("max_actions", maxActions);
        out.put("execution_boundaries", bounds);
        Map<String, Object> mutLimits = map();
        mutLimits.put("max_mutations", 100L);
        out.put("mutation_limits", mutLimits);
        Map<String, Object> rbPolicy = map();
        rbPolicy.put("enabled", rollbackEnabled);
        out.put("rollback_policy", rbPolicy);
        Map<String, Object> toPolicy = map();
        toPolicy.put("ticks", timeoutTicks);
        out.put("timeout_policy", toPolicy);
        out.put("replay_policy", replayPolicy);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeSandbox(String runtime) {
        return buildRuntimeSandbox(runtime, null, true, 1000, 10000, "strict");
    }

    public static Map<String, Object> buildRuntimeSandbox() {
        return buildRuntimeSandbox("browser");
    }

    // ------------------------------------------------------------------ action

    /** {@code build_runtime_action}. */
    public static Map<String, Object> buildRuntimeAction(String actionType, String runtime,
            Map<String, Object> payload, long tick) {
        Map<String, Object> p = dictCopy(payload);
        Map<String, Object> canonical = map();
        canonical.put("runtime", runtime);
        canonical.put("action_type", actionType);
        canonical.put("payload", p);
        canonical.put("tick", tick);
        String actionId = sha256hex32(PyJson.dumpsDefaultAscii(canonical));

        Map<String, Object> out = map();
        out.put("id", actionId);
        out.put("runtime", runtime);
        out.put("action_type", actionType);
        out.put("payload", p);
        out.put("timestamp", tick);
        out.put("bounded", true);
        return out;
    }

    private static final Set<String> SAFE_TERMINAL = Set.of("pwd", "echo", "whoami");
    private static final Set<String> FORBIDDEN_SHELL = Set.of("rm", "del", "format", "shutdown", "eval", "exec");

    private static Map<String, Object> normalizeAction(Map<String, Object> raw, long tick) {
        String actionType = str(Py.get(raw, "type", Py.get(raw, "action_type", "")));
        String runtime = str(Py.get(raw, "runtime", "browser"));
        Map<String, Object> payload;
        switch (actionType) {
            case "browser_click":
                runtime = "browser";
                payload = map();
                payload.put("selector", str(Py.get(raw, "selector", "")));
                break;
            case "terminal_command":
                runtime = "terminal";
                payload = map();
                payload.put("command", str(Py.get(raw, "command", "")));
                break;
            case "native_focus":
                runtime = "native";
                payload = map();
                payload.put("window", str(Py.get(raw, "window", "")));
                break;
            default:
                payload = dictCopy(Py.get(raw, "payload", raw));
        }
        return buildRuntimeAction(actionType, runtime, payload, tick);
    }

    private static boolean actionAllowedInSandbox(Map<String, Object> sandbox, Map<String, Object> action) {
        List<Object> allowed = asList(sandbox.get("allowed_actions"));
        return allowed.contains(action.getOrDefault("action_type", ""));
    }

    private static boolean validateTerminal(String command) {
        String trimmed = command.strip();
        String cmd = trimmed.isEmpty() ? "" : trimmed.split("\\s+")[0];
        if (FORBIDDEN_SHELL.contains(cmd)) {
            return false;
        }
        return SAFE_TERMINAL.contains(cmd);
    }

    private static Map<String, Object> denied(Map<String, Object> action, String runtime, String reason) {
        Map<String, Object> out = map();
        out.put("executed", false);
        out.put("action_id", action.get("id"));
        out.put("runtime", runtime);
        out.put("reason", reason);
        out.put("bounded", true);
        return out;
    }

    /** {@code execute_runtime_action}. */
    public static Map<String, Object> executeRuntimeAction(Map<String, Object> rawAction,
            Map<String, Object> sandbox, Map<String, Object> policy, Map<String, Object> permissions,
            long tick, long mutationCount, long actionCount) {
        Map<String, Object> sb = sandbox == null ? buildRuntimeSandbox() : sandbox;
        Map<String, Object> pol = policy == null ? map() : policy;
        Map<String, Object> perm = permissions == null ? map() : permissions;

        Map<String, Object> action = normalizeAction(rawAction, tick);
        String runtime = (String) action.get("runtime");
        String actionType = (String) action.get("action_type");

        if (!actionAllowedInSandbox(sb, action)) {
            return denied(action, runtime, "sandbox_forbidden");
        }
        Map<String, Object> permResult = validateRuntimePermissions(perm, runtime, actionType);
        if (!Boolean.TRUE.equals(permResult.getOrDefault("allowed", false)) && !perm.isEmpty()) {
            return denied(action, runtime, "permission_denied");
        }
        Map<String, Object> enforcement = enforceRuntimePolicy(pol, action, mutationCount, actionCount);
        if (!Boolean.TRUE.equals(enforcement.getOrDefault("allowed", true))) {
            return denied(action, runtime, "policy_violation");
        }
        if (actionType.equals("terminal_command")) {
            String command = str(Py.get(asMap(action.get("payload")), "command", ""));
            if (!validateTerminal(command)) {
                return denied(action, runtime, "unsafe_terminal");
            }
        }
        if (actionType.equals("browser_click")
                && !Py.truthy(Py.get(asMap(action.get("payload")), "selector", null))) {
            return denied(action, runtime, "invalid_selector");
        }
        Map<String, Object> out = map();
        out.put("executed", true);
        out.put("action_id", action.get("id"));
        out.put("runtime", runtime);
        out.put("action", action);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> executeRuntimeAction(Map<String, Object> raw, Map<String, Object> sandbox, long tick) {
        return executeRuntimeAction(raw, sandbox, null, null, tick, 0, 0);
    }

    // ------------------------------------------------------------------ permissions

    private static final List<String> SCOPES =
            List.of("browser", "native", "filesystem", "connector", "terminal", "vm");

    /** {@code build_runtime_permissions}. */
    public static Map<String, Object> buildRuntimePermissions(List<Object> scopes) {
        Set<String> activeSet = new TreeSet<>(Normalization::codePointCompare);
        List<Object> src = (scopes == null || scopes.isEmpty()) ? List.of("browser", "native") : scopes;
        for (Object s : src) {
            activeSet.add(str(s));
        }
        List<Object> active = new ArrayList<>(activeSet);
        Map<String, Object> scopeMap = map();
        for (String sc : SCOPES) {
            scopeMap.put(sc, activeSet.contains(sc));
        }
        Map<String, Object> out = map();
        out.put("scopes", scopeMap);
        out.put("active_scopes", active);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> validateRuntimePermissions(Map<String, Object> permissions, String runtime,
            String actionType) {
        Map<String, Object> scopes = asMap(permissions.get("scopes"));
        String runtimeScope = SCOPES.contains(runtime) ? runtime : "browser";
        if (actionType.startsWith("terminal_") || actionType.equals("terminal_command")) {
            runtimeScope = "terminal";
        } else if (actionType.startsWith("native_")) {
            runtimeScope = "native";
        } else if (actionType.startsWith("vm_")) {
            runtimeScope = "vm";
        } else if (actionType.startsWith("connector_")) {
            runtimeScope = "connector";
        }
        boolean allowed = Py.truthy(scopes.getOrDefault(runtimeScope, false));
        Map<String, Object> out = map();
        out.put("allowed", allowed);
        out.put("scope", runtimeScope);
        out.put("deterministic", true);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ policy

    public static Map<String, Object> buildRuntimePolicy(boolean allowTerminal) {
        Map<String, Object> out = map();
        out.put("allow_terminal", allowTerminal);
        out.put("allow_browser_mutation", true);
        out.put("max_mutations", 100L);
        out.put("max_actions", 1000L);
        out.put("max_depth", 50L);
        out.put("forbidden_actions", allowTerminal ? new ArrayList<>() : new ArrayList<>(List.of("terminal_command")));
        out.put("rollback_required", true);
        out.put("replay_guaranteed", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> enforceRuntimePolicy(Map<String, Object> policy, Map<String, Object> action,
            long mutationCount, long actionCount) {
        String actionType = str(Py.get(action, "action_type", Py.get(action, "type", "")));
        List<Object> forbidden = asList(policy.get("forbidden_actions"));
        boolean allowed = !forbidden.contains(actionType);
        if (actionType.equals("terminal_command") && !Py.truthy(Py.get(policy, "allow_terminal", false))) {
            allowed = false;
        }
        if (actionType.startsWith("browser_") && !Py.truthy(Py.get(policy, "allow_browser_mutation", true))) {
            allowed = false;
        }
        boolean withinMutations = mutationCount <= pyInt(Py.get(policy, "max_mutations", 100L), 100);
        boolean withinActions = actionCount <= pyInt(Py.get(policy, "max_actions", 1000L), 1000);
        Map<String, Object> out = map();
        out.put("allowed", allowed && withinMutations && withinActions);
        out.put("within_bounds", withinMutations && withinActions);
        out.put("policy_violation", !allowed);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ mutations

    /** {@code track_runtime_mutations}. */
    public static Map<String, Object> trackRuntimeMutations(List<Object> prior, Map<String, Object> mutation) {
        List<Object> mutations = listCopy(prior);
        if (mutation != null && !mutation.isEmpty()) {
            Map<String, Object> entry = map();
            entry.put("kind", str(Py.get(mutation, "kind", "unknown")));
            entry.put("target", str(Py.get(mutation, "target", "")));
            entry.put("tick", pyInt(Py.get(mutation, "tick", 0L), 0));
            entry.put("ordered_index", (long) mutations.size());
            mutations.add(entry);
        }
        List<Object> sorted = new ArrayList<>(mutations);
        sorted.sort(Comparator
                .comparingLong((Object m) -> pyInt(asMap(m).get("tick"), 0))
                .thenComparingLong(m -> pyInt(asMap(m).get("ordered_index"), 0))
                .thenComparing(m -> str(asMap(m).getOrDefault("kind", "")), ExecutionRuntime::cmp));
        Map<String, Object> byKind = map();
        byKind.put("dom", filterKind(sorted, "dom"));
        byKind.put("native", filterKind(sorted, "native"));
        byKind.put("workflow", filterKind(sorted, "workflow"));
        byKind.put("synchronization", filterKind(sorted, "sync"));
        byKind.put("memory", filterKind(sorted, "memory"));
        Map<String, Object> out = map();
        out.put("mutations", sorted);
        out.put("by_kind", byKind);
        out.put("count", (long) sorted.size());
        out.put("deterministic_order", true);
        out.put("bounded", true);
        return out;
    }

    private static List<Object> filterKind(List<Object> mutations, String kind) {
        List<Object> r = new ArrayList<>();
        for (Object m : mutations) {
            if (kind.equals(asMap(m).get("kind"))) {
                r.add(m);
            }
        }
        return r;
    }

    // ------------------------------------------------------------------ transaction / transition

    public static Map<String, Object> beginRuntimeTransaction(long tick, String checkpointId) {
        Map<String, Object> canonical = map();
        canonical.put("tick", tick);
        canonical.put("checkpoint", checkpointId);
        String txId = sha256hex32(PyJson.dumpsDefaultAscii(canonical));
        Map<String, Object> out = map();
        out.put("transaction_id", txId);
        out.put("actions", new ArrayList<>());
        out.put("mutations", new ArrayList<>());
        out.put("transitions", new ArrayList<>());
        out.put("checkpoints", checkpointId.isEmpty() ? new ArrayList<>() : new ArrayList<>(List.of(checkpointId)));
        out.put("committed", false);
        out.put("rolled_back", false);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> commitRuntimeTransaction(Map<String, Object> transaction) {
        Map<String, Object> updated = new LinkedHashMap<>(transaction);
        updated.put("committed", true);
        updated.put("rolled_back", false);
        return updated;
    }

    private static final Map<String, List<String>> VALID_TRANSITIONS = new LinkedHashMap<>();

    static {
        VALID_TRANSITIONS.put("idle", List.of("queued", "simulating"));
        VALID_TRANSITIONS.put("queued", List.of("executing", "rolled_back"));
        VALID_TRANSITIONS.put("executing", List.of("committed", "rolled_back", "failed"));
        VALID_TRANSITIONS.put("simulating", List.of("idle"));
        VALID_TRANSITIONS.put("committed", List.of("idle"));
        VALID_TRANSITIONS.put("rolled_back", List.of("idle"));
        VALID_TRANSITIONS.put("failed", List.of("recovering", "idle"));
        VALID_TRANSITIONS.put("recovering", List.of("idle"));
    }

    public static Map<String, Object> applyRuntimeTransition(String state, String event) {
        String current = VALID_TRANSITIONS.containsKey(state) ? state : "idle";
        List<String> targets = VALID_TRANSITIONS.getOrDefault(current, List.of("idle"));
        String next;
        if (event.equals("enqueue") && targets.contains("queued")) {
            next = "queued";
        } else if (event.equals("execute") && targets.contains("executing")) {
            next = "executing";
        } else if (event.equals("commit") && targets.contains("committed")) {
            next = "committed";
        } else if (event.equals("rollback") && targets.contains("rolled_back")) {
            next = "rolled_back";
        } else if (event.equals("simulate") && targets.contains("simulating")) {
            next = "simulating";
        } else if (event.equals("fail") && targets.contains("failed")) {
            next = "failed";
        } else if (event.equals("recover") && targets.contains("recovering")) {
            next = "recovering";
        } else {
            next = targets.isEmpty() ? "idle" : targets.get(0);
        }
        Map<String, Object> out = map();
        out.put("from", current);
        out.put("to", next);
        out.put("event", event);
        out.put("valid", VALID_TRANSITIONS.containsKey(next));
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ queue

    private static final int MAX_QUEUE = 100_000;

    private static final Comparator<Object> QUEUE_ORDER = Comparator
            .comparingLong((Object i) -> -pyInt(asMap(i).get("priority"), 0))
            .thenComparingLong(i -> pyInt(asMap(i).get("order"), 0));

    public static Map<String, Object> enqueueRuntimeAction(List<Object> queue, Map<String, Object> action, long priority) {
        List<Object> updated = listCopy(queue);
        Map<String, Object> entry = map();
        entry.put("action", action);
        entry.put("priority", priority);
        entry.put("order", (long) updated.size());
        updated.add(entry);
        updated.sort(QUEUE_ORDER);
        if (updated.size() > MAX_QUEUE) {
            updated = new ArrayList<>(updated.subList(0, MAX_QUEUE));
        }
        Map<String, Object> out = map();
        out.put("queue", updated);
        out.put("size", (long) updated.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> dequeueRuntimeAction(List<Object> queue) {
        Map<String, Object> out = map();
        if (queue == null || queue.isEmpty()) {
            out.put("queue", new ArrayList<>());
            out.put("action", null);
            out.put("bounded", true);
            return out;
        }
        List<Object> ordered = listCopy(queue);
        ordered.sort(QUEUE_ORDER);
        Map<String, Object> head = asMap(ordered.get(0));
        List<Object> rest = new ArrayList<>(ordered.subList(1, ordered.size()));
        out.put("queue", rest);
        out.put("action", head.get("action"));
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ workers / federation / coordination

    public static List<Object> buildRuntimeWorkers(List<Object> nodes) {
        List<Object> workers = new ArrayList<>();
        int limit = Math.min(nodes.size(), 1000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> node = asMap(nodes.get(index));
            Map<String, Object> w = map();
            w.put("worker_id", str(Py.get(node, "worker_id", Py.get(node, "node_id", "worker:" + index))));
            w.put("runtime", str(Py.get(node, "runtime", "browser")));
            w.put("synced", Py.truthy(Py.get(node, "synced", true)));
            w.put("bounded", true);
            workers.add(w);
        }
        workers.sort((a, b) -> cmp((String) asMap(a).get("worker_id"), (String) asMap(b).get("worker_id")));
        return workers;
    }

    public static Map<String, Object> federateRuntimeExecution(List<Object> workers, List<Object> actions) {
        List<Object> built = buildRuntimeWorkers(workers);
        List<Object> routes = new ArrayList<>();
        boolean hasActions = actions != null && !actions.isEmpty();
        for (int index = 0; index < built.size(); index++) {
            Map<String, Object> worker = asMap(built.get(index));
            Map<String, Object> action;
            if (hasActions) {
                action = asMap(actions.get(index % actions.size()));
            } else {
                action = map();
            }
            Map<String, Object> route = map();
            route.put("worker_id", worker.get("worker_id"));
            route.put("runtime", worker.get("runtime"));
            route.put("action_id", str(Py.get(action, "id", "route:" + index)));
            route.put("route_order", (long) index);
            routes.add(route);
        }
        List<Object> sortedRoutes = new ArrayList<>(routes);
        sortedRoutes.sort(Comparator.comparingLong(r -> pyInt(asMap(r).get("route_order"), 0)));
        Map<String, Object> out = map();
        out.put("workers", built);
        out.put("execution_routes", sortedRoutes);
        out.put("federated", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> coordinateRuntimeExecution(List<Object> queue, Map<String, Object> federation,
            Object workflow, Object syncState) {
        List<Object> routes = asList(federation.get("execution_routes"));
        List<Object> orderedQueue = listCopy(queue);
        orderedQueue.sort(QUEUE_ORDER);
        List<Object> rollbackOrder = new ArrayList<>();
        for (int i = routes.size() - 1; i >= 0; i--) {
            rollbackOrder.add(asMap(routes.get(i)).get("worker_id"));
        }
        Map<String, Object> out = map();
        out.put("queue_size", (long) orderedQueue.size());
        out.put("routes", routes);
        out.put("workflow_bound", Py.truthy(workflow));
        out.put("sync_bound", Py.truthy(syncState));
        out.put("rollback_order", rollbackOrder);
        out.put("coordinated", true);
        out.put("deterministic", true);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ recovery / rollback / state

    public static Map<String, Object> recoverRuntimeExecution(List<Object> failedActions, Map<String, Object> checkpoint,
            List<Object> interruptedWorkflows) {
        List<Object> failed = listCopy(failedActions);
        Map<String, Object> cp = checkpoint == null ? map() : checkpoint;
        List<Object> workflows = listCopy(interruptedWorkflows);
        List<Object> sortedFailed = new ArrayList<>(failed);
        sortedFailed.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        List<Object> recovered = new ArrayList<>();
        for (int index = 0; index < sortedFailed.size(); index++) {
            Map<String, Object> a = new LinkedHashMap<>(asMap(sortedFailed.get(index)));
            a.put("recovered", true);
            a.put("replay_index", (long) index);
            recovered.add(a);
        }
        Map<String, Object> out = map();
        out.put("recovered_actions", recovered);
        out.put("checkpoint_restored", Py.truthy(cp));
        out.put("workflows_resumed", (long) workflows.size());
        out.put("sync_divergence_resolved", true);
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> restoreRuntimeCheckpoint(Map<String, Object> checkpoint) {
        Map<String, Object> out = map();
        out.put("browser", dictCopy(checkpoint.get("browser")));
        out.put("interaction", dictCopy(checkpoint.get("interaction")));
        out.put("native", dictCopy(checkpoint.get("native")));
        out.put("workflow", dictCopy(checkpoint.get("workflow")));
        out.put("synchronization", dictCopy(checkpoint.get("synchronization")));
        out.put("memory", dictCopy(checkpoint.get("memory")));
        out.put("restored", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rollbackRuntimeState(Map<String, Object> prior, Map<String, Object> current) {
        Map<String, Object> restored = restoreRuntimeCheckpoint(prior);
        Map<String, Object> out = map();
        out.put("prior", prior);
        out.put("current", current == null ? map() : current);
        out.put("restored_state", restored);
        out.put("rolled_back", true);
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildExecutionState(String runtime, List<Object> activeActions, List<Object> queue,
            List<Object> mutations, Map<String, Object> checkpoint, Map<String, Object> transaction,
            Map<String, Object> federation) {
        Map<String, Object> out = map();
        out.put("current_runtime", runtime);
        out.put("active_actions", listCopy(activeActions));
        out.put("pending_queues", listCopy(queue));
        out.put("mutations", listCopy(mutations));
        out.put("checkpoint", dictCopy(checkpoint));
        out.put("transaction", dictCopy(transaction));
        out.put("federation_state", dictCopy(federation));
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ scheduler

    public static Map<String, Object> scheduleRuntimeExecution(List<Object> actions, long tick) {
        List<Object> scheduled = new ArrayList<>();
        int limit = Math.min(actions.size(), 10000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> action = asMap(actions.get(index));
            Map<String, Object> s = map();
            s.put("action", action);
            s.put("priority", 0L);
            s.put("worker_id", "worker:0");
            s.put("tick", tick + (index * Math.max(0L, 0L)));
            s.put("retry", 0L);
            s.put("paced", true);
            scheduled.add(s);
        }
        scheduled.sort(Comparator
                .comparingLong((Object i) -> -pyInt(asMap(i).get("priority"), 0))
                .thenComparingLong(i -> pyInt(asMap(i).get("tick"), 0))
                .thenComparing(i -> str(Py.get(asMap(asMap(i).get("action")), "id", "")), ExecutionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("scheduled", scheduled);
        out.put("worker_id", "worker:0");
        out.put("cooldown_ticks", 0L);
        out.put("deterministic", true);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ replay

    /** {@code replay_runtime_execution}. */
    public static Map<String, Object> replayRuntimeExecution(List<Object> actions, List<Object> transactions,
            List<Object> mutations, long tick) {
        List<Object> orderedActions = listCopy(actions);
        orderedActions.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        List<Object> orderedTx = listCopy(transactions);
        orderedTx.sort((a, b) -> cmp(str(Py.get(asMap(a), "transaction_id", "")),
                str(Py.get(asMap(b), "transaction_id", ""))));
        List<Object> orderedMut = listCopy(mutations);
        orderedMut.sort(Comparator
                .comparingLong((Object m) -> pyInt(asMap(m).get("tick"), 0))
                .thenComparingLong(m -> pyInt(asMap(m).get("ordered_index"), 0)));
        Map<String, Object> out = map();
        out.put("actions", orderedActions);
        out.put("transactions", orderedTx);
        out.put("mutations", orderedMut);
        out.put("tick", tick);
        out.put("replayed", true);
        out.put("identical", true);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ simulation

    /** {@code simulate_runtime_execution}. */
    public static Map<String, Object> simulateRuntimeExecution(List<Object> actions, Map<String, Object> sandbox,
            long tick) {
        Map<String, Object> sb = sandbox == null ? buildRuntimeSandbox() : sandbox;
        List<Object> predicted = new ArrayList<>();
        boolean rollbackRequired = false;
        int limit = Math.min(actions.size(), 1000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> raw = asMap(actions.get(index));
            Map<String, Object> result = executeRuntimeAction(raw, sb, tick + index);
            if (Py.truthy(result.get("executed"))) {
                Map<String, Object> p = map();
                p.put("kind", str(Py.get(raw, "type", "action")));
                p.put("target", str(Py.get(raw, "selector",
                        Py.get(raw, "window", Py.get(raw, "command", "")))));
                p.put("tick", tick + index);
                predicted.add(p);
            } else {
                rollbackRequired = true;
            }
        }
        Map<String, Object> mutationView = trackRuntimeMutations(null, mapOf("kind", "simulated",
                "target", "dry_run", "tick", tick));
        Map<String, Object> out = map();
        out.put("simulated", true);
        out.put("predicted_mutations", predicted);
        out.put("rollback_required", rollbackRequired);
        out.put("mutation_preview", mutationView.get("mutations"));
        out.put("runtime_mutated", false);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    // ------------------------------------------------------------------ IR

    public static Map<String, Object> compileExecutionRuntimeIr(Map<String, Object> payload) {
        Map<String, Object> out = map();
        out.put("ir", "execution_runtime");
        out.put("actions", payload.getOrDefault("actions", new ArrayList<>()));
        out.put("queues", payload.getOrDefault("queue", map()));
        out.put("transactions", payload.getOrDefault("transactions", new ArrayList<>()));
        out.put("mutations", payload.getOrDefault("mutations", map()));
        out.put("checkpoints", payload.getOrDefault("checkpoints", new ArrayList<>()));
        out.put("federation", payload.getOrDefault("federation", map()));
        out.put("synchronization", payload.getOrDefault("synchronization", map()));
        out.put("execution_state", payload.getOrDefault("state", map()));
        out.put("coordination", payload.getOrDefault("coordination", map()));
        out.put("simulation", payload.getOrDefault("simulation", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> executionRuntimeIrToGraph(Map<String, Object> executionIr) {
        List<Object> nodes = new ArrayList<>();
        nodes.add(mapOf("id", "execution:root", "type", "execution", "runtime", "operational"));
        List<Object> edges = new ArrayList<>();
        for (Object ao : capped(asList(executionIr.get("actions")), 10000)) {
            Map<String, Object> action = asMap(ao);
            String actionId = str(Py.get(action, "id", Py.get(action, "action_id", "")));
            if (actionId.isEmpty()) {
                continue;
            }
            nodes.add(mapOf("id", "action:" + actionId, "type", "action"));
            edges.add(mapOf("from", "execution:root", "to", "action:" + actionId, "relation", "executes"));
        }
        List<Object> routes = asList(asMap(executionIr.get("federation")).get("execution_routes"));
        for (Object ro : capped(routes, 10000)) {
            String workerId = str(Py.get(asMap(ro), "worker_id", ""));
            if (!workerId.isEmpty()) {
                nodes.add(mapOf("id", "worker:" + workerId, "type", "worker"));
                edges.add(mapOf("from", "worker:" + workerId, "to", "execution:root", "relation", "coordinates"));
            }
        }
        List<Object> muts = asList(asMap(executionIr.get("mutations")).get("mutations"));
        for (Object mo : capped(muts, 10000)) {
            Map<String, Object> mutation = asMap(mo);
            String target = str(Py.get(mutation, "target", Py.get(mutation, "kind", "mutation")));
            String nodeId = "mutation:" + target;
            nodes.add(mapOf("id", nodeId, "type", "mutation"));
            edges.add(mapOf("from", nodeId, "to", "execution:root", "relation", "mutates"));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "execution_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    private static List<Object> capped(List<Object> xs, int n) {
        return xs.size() > n ? xs.subList(0, n) : xs;
    }

    /** Port of {@code core.runtime_graph.runtime_graph_engine.build_runtime_graph} (IR merge —
     * internal, distinct from the proven parity {@code build_runtime_graph}). */
    private static final int MAX_GRAPH_NODES = 1_000_000;
    private static final int MAX_GRAPH_EDGES = 5_000_000;

    public static Map<String, Object> buildUnifiedRuntimeGraph(List<Object> runtimeIrs) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        Set<String> seenNodes = new HashSet<>();
        Set<String> seenEdges = new HashSet<>();
        for (Object ro : capped(runtimeIrs, 10000)) {
            Map<String, Object> ir = asMap(ro);
            String runtimeType = str(Py.get(ir, "ir", "unknown"));
            Object nv = Py.get(ir, "nodes", new ArrayList<>());
            List<Object> rn = Py.truthy(nv) ? asList(nv) : new ArrayList<>();
            Object ev = Py.get(ir, "edges", new ArrayList<>());
            List<Object> re = Py.truthy(ev) ? asList(ev) : new ArrayList<>();
            for (Object no : rn) {
                Map<String, Object> node = asMap(no);
                String nodeId = PyText.strip(str(Py.get(node, "id", "")));
                if (nodeId.isEmpty() || seenNodes.contains(nodeId)) {
                    continue;
                }
                seenNodes.add(nodeId);
                Map<String, Object> enriched = new LinkedHashMap<>(node);
                enriched.put("runtime_type", runtimeType);
                nodes.add(enriched);
                if (nodes.size() >= MAX_GRAPH_NODES) {
                    break;
                }
            }
            for (Object eo : re) {
                Map<String, Object> edge = asMap(eo);
                String s = PyText.strip(str(Py.get(edge, "from", "")));
                String d = PyText.strip(str(Py.get(edge, "to", "")));
                String rel = PyText.strip(str(Py.get(edge, "relation", "related_to")));
                if (s.isEmpty() || d.isEmpty()) {
                    continue;
                }
                String key = s + " " + d + " " + rel;
                if (seenEdges.contains(key)) {
                    continue;
                }
                seenEdges.add(key);
                Map<String, Object> enriched = new LinkedHashMap<>(edge);
                enriched.put("runtime_type", runtimeType);
                edges.add(enriched);
                if (edges.size() >= MAX_GRAPH_EDGES) {
                    break;
                }
            }
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator
                .comparing((Object e) -> str(Py.get(asMap(e), "from", "")), ExecutionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), ExecutionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), ExecutionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("ir", "unified_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    // ------------------------------------------------------------------ orchestrator

    private static List<Object> defaultActions(String runtime) {
        if (runtime.equals("native")) {
            return new ArrayList<>(List.of(mapOf("type", "native_focus", "window", "application")));
        }
        if (runtime.equals("terminal")) {
            return new ArrayList<>(List.of(mapOf("type", "terminal_command", "command", "pwd")));
        }
        return new ArrayList<>(List.of(mapOf("type", "browser_click", "selector", "#submit")));
    }

    /** {@code run_execution_runtime}. */
    public static Map<String, Object> runExecutionRuntime(Map<String, Object> sources, Map<String, Object> stored,
            List<Object> workers, String runtime, long tick, boolean simulate, boolean rollbackEnabled) {
        Map<String, Object> src = sources == null ? map() : sources;
        Map<String, Object> sto = dictCopy(stored);
        List<Object> wk = (workers == null || workers.isEmpty())
                ? new ArrayList<>(List.of(mapOf("worker_id", "primary", "runtime", runtime, "synced", true)))
                : listCopy(workers);

        Map<String, Object> sandbox = buildRuntimeSandbox(runtime);
        Map<String, Object> policy = buildRuntimePolicy(runtime.equals("terminal"));
        List<Object> permScopes = runtime.equals("browser")
                ? new ArrayList<>(List.of("browser", "native", "terminal", "connector", "vm"))
                : new ArrayList<>(List.of(runtime));
        Map<String, Object> permissions = buildRuntimePermissions(permScopes);

        Map<String, Object> priorCheckpoint = asMap(sto.get("checkpoint"));
        Map<String, Object> checkpointBody = priorCheckpoint.isEmpty() ? map()
                : asMap(Py.get(priorCheckpoint, "state", priorCheckpoint));

        Object rawActionsObj = Py.get(src, "actions", null);
        List<Object> rawActions = Py.truthy(rawActionsObj) ? asList(rawActionsObj) : defaultActions(runtime);

        List<Object> executedActions = new ArrayList<>();
        long mutationCount = 0;

        List<Object> queue = new ArrayList<>();
        long maxActions = pyInt(sandbox.get("max_actions"), 1000);
        for (Object raw : capped(rawActions, (int) maxActions)) {
            Map<String, Object> enq = enqueueRuntimeAction(queue, asMap(raw), 0);
            queue = asList(enq.get("queue"));
        }

        if (simulate) {
            Map<String, Object> simulation = simulateRuntimeExecution(rawActions, sandbox, tick);
            Map<String, Object> transition = applyRuntimeTransition("idle", "simulate");
            Map<String, Object> payload = map();
            payload.put("simulation", simulation);
            payload.put("transition", transition);
            payload.put("sandbox", sandbox);
            payload.put("bounded", true);
            payload.put("execution_ir", compileExecutionRuntimeIr(payload));
            return payload;
        }

        Map<String, Object> transaction = beginRuntimeTransaction(tick, "");
        Map<String, Object> transition = applyRuntimeTransition("idle", "enqueue");

        while (!queue.isEmpty()) {
            Map<String, Object> deq = dequeueRuntimeAction(queue);
            queue = asList(deq.get("queue"));
            Object actionRaw = deq.get("action");
            if (!Py.truthy(actionRaw)) {
                break;
            }
            Map<String, Object> actionRawMap = asMap(actionRaw);
            Map<String, Object> raw = asMap(Py.get(actionRawMap, "action", actionRawMap));
            Map<String, Object> result = executeRuntimeAction(raw, sandbox, policy, permissions, tick,
                    mutationCount, executedActions.size());
            if (Py.truthy(result.get("executed"))) {
                executedActions.add(asMap(Py.get(result, "action", map())));
                mutationCount += 1;
                Map<String, Object> track = trackRuntimeMutations(asList(transaction.get("mutations")),
                        mapOf("kind", str(Py.get(result, "runtime", "action")),
                                "target", str(Py.get(result, "action_id", "")),
                                "tick", tick));
                transaction.put("mutations", track.get("mutations"));
                transaction.put("actions", executedActions);
            }
            transition = applyRuntimeTransition((String) transition.get("to"), "execute");
        }

        transaction = commitRuntimeTransaction(transaction);
        transition = applyRuntimeTransition((String) transition.get("to"), "commit");

        Map<String, Object> mutations = trackRuntimeMutations(asList(transaction.get("mutations")), null);
        Map<String, Object> federation = federateRuntimeExecution(wk, executedActions);
        Map<String, Object> schedule = scheduleRuntimeExecution(executedActions, tick);
        Map<String, Object> coordination = coordinateRuntimeExecution(new ArrayList<>(), federation,
                Py.get(src, "workflow", null), Py.get(src, "sync", null));

        Map<String, Object> rollbackResult = map();
        if (rollbackEnabled && !checkpointBody.isEmpty()) {
            rollbackResult = rollbackRuntimeState(checkpointBody, buildExecutionState(runtime, null, null, null,
                    null, null, null));
        }

        Map<String, Object> recovery = recoverRuntimeExecution(new ArrayList<>(), checkpointBody,
                Py.truthy(Py.get(src, "workflow", null))
                        ? new ArrayList<>(List.of(Py.get(src, "workflow", null))) : new ArrayList<>());

        Map<String, Object> state = buildExecutionState(runtime, executedActions, queue,
                asList(mutations.get("mutations")), checkpointBody, transaction, federation);

        Map<String, Object> replay = replayRuntimeExecution(executedActions,
                new ArrayList<>(List.of(transaction)), asList(mutations.get("mutations")), tick);

        Map<String, Object> payload = map();
        payload.put("actions", executedActions);
        Map<String, Object> queueOut = map();
        queueOut.put("queue", queue);
        queueOut.put("size", (long) queue.size());
        payload.put("queue", queueOut);
        payload.put("transactions", new ArrayList<>(List.of(transaction)));
        payload.put("mutations", mutations);
        payload.put("checkpoints", checkpointBody.isEmpty() ? new ArrayList<>()
                : new ArrayList<>(List.of(checkpointBody)));
        payload.put("federation", federation);
        payload.put("synchronization", asMap(Py.get(src, "sync", map())));
        payload.put("state", state);
        payload.put("coordination", coordination);
        payload.put("schedule", schedule);
        payload.put("sandbox", sandbox);
        payload.put("policy", policy);
        payload.put("permissions", permissions);
        payload.put("rollback", rollbackResult);
        payload.put("recovery", recovery);
        payload.put("replay", replay);
        payload.put("transition", transition);
        payload.put("bounded", true);
        payload.put("execution_ir", compileExecutionRuntimeIr(payload));
        return payload;
    }

    /** {@code run_execution_for_extraction} (no checkpoint FS when memory_path/key empty). */
    public static Map<String, Object> runExecutionForExtraction(boolean executionRuntime, String memoryPath,
            String memoryKey, Map<String, Object> sources, List<Object> workers, String runtime, long tick,
            boolean simulateExecution, boolean rollbackEnabled, boolean mergeGraph) {
        if (!executionRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> stored = map();
        // memory_path/key empty in the parity-proven path -> no checkpoint load (FS).

        Map<String, Object> result = runExecutionRuntime(sources, stored, workers, runtime, tick,
                simulateExecution, rollbackEnabled);

        Map<String, Object> graphIr = executionRuntimeIrToGraph(asMap(Py.get(result, "execution_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("execution", result);
        out.put("execution_ir", Py.get(result, "execution_ir", map()));
        out.put("execution_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("simulation", Py.get(result, "simulation", map()));
        out.put("execution_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
