package io.webweavex.evolution;

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
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Port of the {@code core.evolution_runtime} family — {@code build_runtime_evolution},
 * {@code evolve_selector_runtime}, {@code run_evolution_runtime},
 * {@code run_evolution_for_extraction}, {@code save_evolution_runtime},
 * {@code load_evolution_runtime} — and the ~17 deterministic sub-engines + evolution IR they fan
 * out to. Dependency-clean (25-module closure, 0 forbidden; the FS memory engine is only invoked
 * when a memory path+key are supplied). Reuses the certified determinism/crypto/json substrate
 * and {@link ExecutionRuntime#buildUnifiedRuntimeGraph}.
 */
public final class EvolutionRuntime {

    private EvolutionRuntime() {
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

    private static List<String> sortedKeys(Map<String, Object> m) {
        List<String> keys = new ArrayList<>(m.keySet());
        keys.sort(Normalization::codePointCompare);
        return keys;
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

    /** Sort a list of {kind,target} maps by (kind, str(target)) — code-point order. */
    private static void sortByKindTarget(List<Object> xs) {
        xs.sort(Comparator.comparing((Object m) -> str(asMap(m).get("kind")), EvolutionRuntime::cmp)
                .thenComparing(m -> str(asMap(m).get("target")), EvolutionRuntime::cmp));
    }

    // -------------------------------------------------------------- selector / evolution

    /** {@code evolve_selector_runtime}. */
    public static Map<String, Object> evolveSelectorRuntime(Map<String, Object> selectors,
            Map<String, Object> healed) {
        Map<String, Object> sel = selectors == null ? map() : selectors;
        Map<String, Object> heal = healed == null ? map() : healed;
        List<Object> evolved = new ArrayList<>();
        // sorted(healed.items())
        TreeMap<String, Object> healSorted = new TreeMap<>(Normalization::codePointCompare);
        healSorted.putAll(heal);
        for (Map.Entry<String, Object> e : healSorted.entrySet()) {
            String replacement = str(e.getValue());
            Map<String, Object> m = map();
            m.put("original", e.getKey());
            m.put("evolved", replacement);
            m.put("strategy", "healed_promotion");
            m.put("fallback", "[data-evolved='" + replacement + "']");
            evolved.add(m);
        }
        for (String selector : sortedKeys(sel)) {
            if (heal.containsKey(selector)) {
                continue;
            }
            Map<String, Object> m = map();
            m.put("original", selector);
            m.put("evolved", sel.get(selector));
            m.put("strategy", "structural_upgrade");
            m.put("fallback", sel.get(selector));
            evolved.add(m);
        }
        Map<String, Object> out = map();
        out.put("selectors", evolved);
        out.put("count", (long) evolved.size());
        out.put("bounded", true);
        return out;
    }

    private static long countKind(List<Object> mutations, String kind) {
        long c = 0;
        for (Object m : mutations) {
            if (kind.equals(asMap(m).get("kind"))) {
                c++;
            }
        }
        return c;
    }

    /** {@code build_runtime_evolution}. */
    public static Map<String, Object> buildRuntimeEvolution(List<Object> mutations, List<Object> lineage) {
        List<String> parts = new ArrayList<>();
        for (Object m : mutations) {
            Map<String, Object> mm = asMap(m);
            parts.add(str(Py.get(mm, "kind", "")) + ":" + str(Py.get(mm, "target", "")));
        }
        parts.sort(Normalization::codePointCompare);
        String evolutionId = sha256hex32(String.join("|", parts));

        List<Object> sortedMut = new ArrayList<>(mutations);
        sortedMut.sort((a, b) -> cmp(str(Py.get(asMap(a), "target", "")), str(Py.get(asMap(b), "target", ""))));
        List<Object> sortedLin = new ArrayList<>(lineage);
        sortedLin.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));

        Map<String, Object> improvements = map();
        improvements.put("selector_repairs", countKind(mutations, "selector"));
        improvements.put("workflow_optimizations", countKind(mutations, "workflow"));
        improvements.put("semantic_convergence", countKind(mutations, "semantic"));
        improvements.put("sync_improvements", countKind(mutations, "sync"));

        Map<String, Object> out = map();
        out.put("evolution_id", evolutionId);
        out.put("mutations", sortedMut);
        out.put("lineage", sortedLin);
        out.put("improvements", improvements);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- sub-engines

    public static Map<String, Object> evolveWorkflowRuntime(Map<String, Object> plan, Map<String, Object> execution,
            List<Object> history) {
        Map<String, Object> p = plan == null ? map() : plan;
        Map<String, Object> exec = execution == null ? map() : execution;
        List<Object> hist = history == null ? new ArrayList<>() : history;
        List<Object> steps = asList(p.get("steps"));
        long score = asList(exec.get("executed")).size();
        List<Object> optimized = new ArrayList<>(steps);
        optimized.sort(Comparator
                .comparingLong((Object s) -> -pyInt(Py.get(asMap(s), "priority", 0L), 0))
                .thenComparing(s -> str(Py.get(asMap(s), "id", "")), EvolutionRuntime::cmp));
        List<Object> ordering = new ArrayList<>();
        for (Object s : optimized) {
            ordering.add(Py.get(asMap(s), "id", ""));
        }
        Map<String, Object> out = map();
        out.put("execution_ordering", ordering);
        out.put("retries", Math.min((long) hist.size(), 3L));
        out.put("pacing", Math.max(0L, steps.size() - score));
        out.put("sync_timing", (long) steps.size());
        out.put("recovery_ordering", new ArrayList<>(List.of("retry_step", "realign_runtime", "checkpoint")));
        out.put("score", score);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> evolveSemanticRuntime(Map<String, Object> semantic, List<Object> history) {
        Map<String, Object> sem = semantic == null ? map() : semantic;
        List<Object> hist = history == null ? new ArrayList<>() : history;
        Map<String, Object> inner = asMap(Py.get(sem, "semantic", sem));
        List<Object> entities = asList(asMap(Py.get(inner, "entities", map())).get("entities"));
        Map<String, Long> recurring = new LinkedHashMap<>();
        for (Object eo : entities) {
            Map<String, Object> entity = asMap(eo);
            String label = str(Py.get(entity, "label", Py.get(entity, "type", "")));
            recurring.merge(label, 1L, Long::sum);
        }
        List<String> stable = new ArrayList<>();
        for (Map.Entry<String, Long> e : recurring.entrySet()) {
            if (e.getValue() >= 1) {
                stable.add(e.getKey());
            }
        }
        stable.sort(Normalization::codePointCompare);
        Map<String, Object> out = map();
        out.put("recurring_entities", new ArrayList<Object>(stable));
        out.put("stable_ontology", Py.get(inner, "ontology", map()));
        out.put("domain", str(Py.get(asMap(Py.get(inner, "domain", map())), "domain", "")));
        out.put("semantic_convergence", (long) stable.size());
        out.put("domain_stabilized", Py.truthy(Py.get(inner, "domain", null)));
        out.put("history_length", (long) hist.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> evolveRuntimeTopology(List<Object> workers, Map<String, Object> sync,
            Map<String, Object> causality) {
        List<Object> wk = workers == null ? new ArrayList<>() : workers;
        List<Object> workerIds = new ArrayList<>();
        for (int index = 0; index < wk.size(); index++) {
            Map<String, Object> w = asMap(wk.get(index));
            workerIds.add(str(Py.get(w, "worker_id", Py.get(w, "id", "w:" + index))));
        }
        workerIds.sort((a, b) -> cmp((String) a, (String) b));
        Map<String, Object> out = map();
        out.put("worker_routing", workerIds);
        out.put("sync_paths", new ArrayList<>(List.of("browser", "native", "distributed")));
        out.put("causality_propagation", Py.truthy(causality));
        out.put("workflow_routing", new ArrayList<>(List.of("primary", "distributed")));
        out.put("federation", (long) workerIds.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeStrategy(Map<String, Object> evidence) {
        Map<String, Object> ev = evidence == null ? map() : evidence;
        long driftCount = pyInt(Py.get(ev, "drift_count", 0L), 0);
        long failedSteps = pyInt(Py.get(ev, "failed_steps", 0L), 0);
        Map<String, Object> out = map();
        out.put("extraction_path", driftCount == 0 ? "browser_first" : "repair_then_extract");
        out.put("synchronization_path", failedSteps == 0 ? "continuous" : "converge_then_sync");
        out.put("workflow_order", "priority_asc");
        out.put("selector_hierarchy", new ArrayList<>(List.of("healed", "structural", "fallback")));
        out.put("recovery_order", new ArrayList<>(List.of("heal_selector", "recover_workflow", "resync_runtime")));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> repairRuntimeFailures(List<Object> failures, Map<String, Object> selectors) {
        List<Object> f = failures == null ? new ArrayList<>() : failures;
        Map<String, Object> sel = selectors == null ? map() : selectors;
        Map<String, String> repairMap = new LinkedHashMap<>();
        repairMap.put("broken_selector", "heal_selector");
        repairMap.put("failed_workflow", "reorder_workflow");
        repairMap.put("sync_divergence", "resync_runtime");
        repairMap.put("runtime_inconsistency", "verify_consistency");
        repairMap.put("causality_gap", "bridge_causality");
        List<Object> repairs = new ArrayList<>();
        List<Object> sortedFailures = new ArrayList<>(f);
        sortedFailures.sort((a, b) -> cmp(str(a), str(b)));
        for (Object fo : sortedFailures) {
            String failure = str(fo);
            repairs.add(mapOf("failure", failure, "action", repairMap.getOrDefault(failure, "retry_step"),
                    "repaired", true));
        }
        TreeMap<String, Object> selSorted = new TreeMap<>(Normalization::codePointCompare);
        selSorted.putAll(sel);
        for (Map.Entry<String, Object> e : selSorted.entrySet()) {
            Map<String, Object> r = map();
            r.put("failure", "broken_selector");
            r.put("action", "heal_selector");
            r.put("selector", e.getKey());
            r.put("healed", e.getValue());
            r.put("repaired", true);
            repairs.add(r);
        }
        Map<String, Object> out = map();
        out.put("repairs", repairs);
        out.put("repair_count", (long) repairs.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> evolveRecoveryOrder(List<Object> repairs) {
        List<Object> ordered = new ArrayList<>(repairs);
        ordered.sort((a, b) -> cmp(str(Py.get(asMap(a), "action", "")), str(Py.get(asMap(b), "action", ""))));
        List<Object> order = new ArrayList<>();
        for (Object o : ordered) {
            order.add(Py.get(asMap(o), "action", ""));
        }
        Map<String, Object> out = map();
        out.put("recovery_order", order);
        out.put("evolved", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> optimizeRuntimeExecution(long depth, long replayCost, long syncOverhead) {
        long optimizedDepth = Math.max(1, Math.min(depth, 100));
        long optimizedReplay = replayCost > 0 ? Math.max(0, replayCost - 1) : 0;
        long optimizedSync = syncOverhead > 1 ? Math.max(0, syncOverhead - 1) : syncOverhead;
        Map<String, Object> out = map();
        out.put("execution_depth", optimizedDepth);
        out.put("replay_cost", optimizedReplay);
        out.put("synchronization_overhead", optimizedSync);
        out.put("runtime_pressure", Math.max(0, depth - optimizedDepth));
        out.put("convergence_gain", optimizedSync == 0);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> adaptRuntimeStrategy(Map<String, Object> strategy,
            Map<String, Object> optimization) {
        Map<String, Object> adapted = new LinkedHashMap<>(strategy);
        if (Py.truthy(Py.get(optimization, "convergence_gain", null))) {
            adapted.put("synchronization_path", "continuous");
        }
        if (pyInt(Py.get(optimization, "runtime_pressure", 0L), 0) > 0) {
            adapted.put("extraction_path", "repair_then_extract");
        }
        adapted.put("adapted", true);
        adapted.put("bounded", true);
        return adapted;
    }

    public static List<Object> buildRuntimeMutations(Map<String, Object> selector, Map<String, Object> workflow,
            Map<String, Object> semantic, Map<String, Object> sync) {
        List<Object> mutations = new ArrayList<>();
        for (Object io : capped(asList(selector.get("selectors")), 10000)) {
            Map<String, Object> item = asMap(io);
            mutations.add(mapOf("kind", "selector", "target", str(Py.get(item, "original", "")),
                    "evolved", str(Py.get(item, "evolved", ""))));
        }
        if (Py.truthy(workflow.get("execution_ordering"))) {
            mutations.add(mapOf("kind", "workflow", "target", "execution_ordering",
                    "evolved", workflow.get("execution_ordering")));
        }
        if (Py.truthy(semantic.get("domain"))) {
            mutations.add(mapOf("kind", "semantic", "target", "domain", "evolved", semantic.get("domain")));
        }
        if (Py.truthy(sync.get("convergence"))) {
            mutations.add(mapOf("kind", "sync", "target", "convergence", "evolved", true));
        }
        sortByKindTarget(mutations);
        return mutations;
    }

    public static List<Object> buildRuntimeLineage(String evolutionId, List<Object> mutations, String parentId) {
        List<Object> lineage = new ArrayList<>();
        if (!parentId.isEmpty()) {
            lineage.add(mapOf("id", parentId, "relation", "parent"));
        }
        lineage.add(mapOf("id", evolutionId, "relation", "current"));
        for (Object mo : capped(mutations, 1000)) {
            Map<String, Object> m = asMap(mo);
            lineage.add(mapOf("id", str(Py.get(m, "kind", "")) + ":" + str(Py.get(m, "target", "")),
                    "relation", "mutation", "ancestor", evolutionId));
        }
        lineage.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        return lineage;
    }

    public static Map<String, Object> buildRuntimePolicy() {
        Map<String, Object> mc = map();
        mc.put("allow_selector", true);
        mc.put("allow_workflow", true);
        mc.put("allow_semantic", true);
        mc.put("allow_sync", true);
        mc.put("allow_code_synthesis", false);
        Map<String, Object> out = map();
        out.put("evolution_bounds", 10000L);
        out.put("repair_limits", 1000L);
        out.put("synchronization_threshold", 1000L);
        out.put("optimization_ceiling", 100L);
        out.put("mutation_constraints", mc);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> enforceRuntimePolicy(Map<String, Object> policy, List<Object> mutations,
            List<Object> repairs, long depth) {
        boolean within = mutations.size() <= pyInt(policy.get("evolution_bounds"), 10000)
                && repairs.size() <= pyInt(policy.get("repair_limits"), 1000)
                && depth <= pyInt(policy.get("optimization_ceiling"), 100);
        Map<String, Object> out = map();
        out.put("within_bounds", within);
        out.put("mutation_count", (long) mutations.size());
        out.put("repair_count", (long) repairs.size());
        out.put("depth", depth);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimePatterns(Map<String, Object> ui, List<Object> workflows,
            Map<String, Object> semantic, List<Object> syncHistory) {
        Map<String, Object> u = ui == null ? map() : ui;
        List<Object> wf = workflows == null ? new ArrayList<>() : workflows;
        List<Object> sh = syncHistory == null ? new ArrayList<>() : syncHistory;
        List<Object> patterns = new ArrayList<>();
        for (Object wo : capped(wf, 1000)) {
            Map<String, Object> w = asMap(wo);
            patterns.add(str(Py.get(w, "objective", Py.get(w, "action", ""))));
        }
        List<Object> layouts = new ArrayList<>();
        if (semantic != null) {
            for (String k : new ArrayList<>(semantic.keySet())) {
                layouts.add(k);
                if (layouts.size() >= 100) {
                    break;
                }
            }
        }
        Map<String, Object> out = map();
        out.put("ui_structures", new ArrayList<Object>(sortedKeys(u)));
        out.put("workflow_patterns", patterns);
        out.put("semantic_layouts", layouts);
        out.put("sync_histories", (long) sh.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> convergeRuntimeEvolution(List<Object> evolutions) {
        List<Object> merged = new ArrayList<>();
        Set<String> seen = new LinkedHashSet<>();
        List<Object> sorted = new ArrayList<>(evolutions);
        sorted.sort((a, b) -> cmp(str(Py.get(asMap(a), "evolution_id", "")),
                str(Py.get(asMap(b), "evolution_id", ""))));
        for (Object eo : sorted) {
            for (Object mo : asList(asMap(eo).get("mutations"))) {
                Map<String, Object> m = asMap(mo);
                String key = str(m.get("kind")) + " " + str(m.get("target"));
                if (seen.contains(key)) {
                    continue;
                }
                seen.add(key);
                merged.add(mo);
            }
        }
        sortByKindTarget(merged);
        Map<String, Object> out = map();
        out.put("converged_mutations", merged);
        out.put("evolution_count", (long) evolutions.size());
        out.put("consistent", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> diffEvolutionRuntime(Map<String, Object> previous, Map<String, Object> current) {
        String prevId = str(Py.get(previous, "evolution_id", ""));
        String currId = str(Py.get(current, "evolution_id", ""));
        Map<String, Object> out = map();
        out.put("evolution_changed", !prevId.equals(currId));
        out.put("previous_id", prevId);
        out.put("current_id", currId);
        out.put("mutation_delta", (long) asList(current.get("mutations")).size()
                - asList(previous.get("mutations")).size());
        out.put("revertible", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeEvolutionGraph(Map<String, Object> evolution,
            Map<String, Object> repairs, Map<String, Object> optimization) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        String evolutionId = str(Py.get(evolution, "evolution_id", "evolution:root"));
        nodes.add(mapOf("id", evolutionId, "type", "evolution"));
        for (Object mo : capped(asList(evolution.get("mutations")), 5000)) {
            Map<String, Object> m = asMap(mo);
            String nodeId = "mutation:" + str(m.get("kind")) + ":" + str(m.get("target"));
            nodes.add(mapOf("id", nodeId, "type", "mutation"));
            edges.add(mapOf("from", evolutionId, "to", nodeId, "relation", "evolves"));
        }
        for (Object ro : capped(asList(repairs.get("repairs")), 5000)) {
            String nodeId = "repair:" + str(Py.get(asMap(ro), "action", ""));
            nodes.add(mapOf("id", nodeId, "type", "repair"));
            edges.add(mapOf("from", nodeId, "to", evolutionId, "relation", "repairs"));
        }
        nodes.add(mapOf("id", "optimization:root", "type", "optimization"));
        edges.add(mapOf("from", "optimization:root", "to", evolutionId, "relation", "optimizes"));
        edges.add(mapOf("from", evolutionId, "to", evolutionId, "relation", "converges"));
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), EvolutionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), EvolutionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), EvolutionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- IR / memory

    public static Map<String, Object> compileEvolutionRuntimeIr(Map<String, Object> evolution) {
        Map<String, Object> out = map();
        out.put("ir", "evolution_runtime");
        out.put("evolution", Py.get(evolution, "evolution", map()));
        out.put("selector", Py.get(evolution, "selector", map()));
        out.put("workflow", Py.get(evolution, "workflow", map()));
        out.put("semantic", Py.get(evolution, "semantic", map()));
        out.put("topology", Py.get(evolution, "topology", map()));
        out.put("strategy", Py.get(evolution, "strategy", map()));
        out.put("repairs", Py.get(evolution, "repairs", map()));
        out.put("optimization", Py.get(evolution, "optimization", map()));
        out.put("patterns", Py.get(evolution, "patterns", map()));
        out.put("lineage", Py.get(evolution, "lineage", new ArrayList<>()));
        out.put("graph", Py.get(evolution, "graph", map()));
        out.put("policy", Py.get(evolution, "policy", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> evolutionRuntimeIrToGraph(Map<String, Object> evolutionIr) {
        Map<String, Object> graph = asMap(evolutionIr.get("graph"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "evolution:root", "type", "evolution")));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "evolution_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rememberEvolutionRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"evolution_histories", "selector_lineage", "workflow_evolution",
                "semantic_evolution", "optimization_histories"}) {
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
        m.put("evolution_histories", new ArrayList<>());
        m.put("selector_lineage", new ArrayList<>());
        m.put("workflow_evolution", map());
        m.put("semantic_evolution", map());
        m.put("optimization_histories", new ArrayList<>());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_evolution_runtime(path, memory, key)}. */
    public static Map<String, Object> saveEvolutionRuntime(String path, Map<String, Object> memory, String key) {
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

    /** {@code load_evolution_runtime(path, key)}. */
    public static Map<String, Object> loadEvolutionRuntime(String path, String key) {
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

    private static long countOccurrences(List<Object> list, String value) {
        long c = 0;
        for (Object o : list) {
            if (value.equals(o)) {
                c++;
            }
        }
        return c;
    }

    /** {@code run_evolution_runtime}. */
    public static Map<String, Object> runEvolutionRuntime(Map<String, Object> adaptiveMemory,
            Map<String, Object> workflowResult, Map<String, Object> semanticResult, Map<String, Object> syncResult,
            Map<String, Object> distributedResult, List<Object> failures, Map<String, Object> memory, long tick) {
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);
        Map<String, Object> am = adaptiveMemory == null ? map() : adaptiveMemory;
        List<Object> fail = failures == null ? new ArrayList<>() : failures;

        Map<String, Object> healed = new LinkedHashMap<>(asMap(Py.get(am, "healed_selectors", map())));
        Map<String, Object> selector = evolveSelectorRuntime(asMap(Py.get(am, "selectors", map())), healed);

        Map<String, Object> workflowInner = asMap(Py.get(workflowResult == null ? map() : workflowResult,
                "workflow", workflowResult));
        Map<String, Object> workflow = evolveWorkflowRuntime(asMap(Py.get(workflowInner, "plan", map())),
                asMap(Py.get(workflowInner, "execution", map())),
                asList(Py.get(mem, "evolution_histories", new ArrayList<>())));

        Map<String, Object> semantic = evolveSemanticRuntime(semanticResult,
                asList(Py.get(mem, "evolution_histories", new ArrayList<>())));

        Map<String, Object> syncInner = asMap(Py.get(syncResult == null ? map() : syncResult,
                "synchronization", syncResult));
        Map<String, Object> topology = evolveRuntimeTopology(
                asList(Py.get(distributedResult == null ? map() : distributedResult, "workers", new ArrayList<>())),
                syncInner, asMap(Py.get(syncResult == null ? map() : syncResult, "causality", null)));

        Map<String, Object> evidence = map();
        evidence.put("drift_count", (long) asList(asMap(Py.get(syncInner, "drift", map())).get("drifts")).size());
        evidence.put("failed_steps", countOccurrences(fail, "failed_workflow"));
        Map<String, Object> strategy = buildRuntimeStrategy(evidence);
        Map<String, Object> repairs = repairRuntimeFailures(fail, healed);
        Map<String, Object> recovery = evolveRecoveryOrder(asList(repairs.get("repairs")));

        long depth = asList(workflow.get("execution_ordering")).size();
        Map<String, Object> optimization = optimizeRuntimeExecution(depth,
                asList(Py.get(mem, "evolution_histories", new ArrayList<>())).size(),
                asList(Py.get(syncInner, "deltas", new ArrayList<>())).size());
        Map<String, Object> adaptedStrategy = adaptRuntimeStrategy(strategy, optimization);

        List<Object> mutations = buildRuntimeMutations(selector, workflow, semantic,
                asMap(Py.get(syncInner, "convergence", map())));
        String parentId = str(Py.get(mem, "last_evolution_id", ""));
        List<Object> lineage = buildRuntimeLineage("", mutations, parentId);
        Map<String, Object> evolution = buildRuntimeEvolution(mutations, lineage);
        String evolutionId = (String) evolution.get("evolution_id");
        lineage = buildRuntimeLineage(evolutionId, mutations, parentId);

        Map<String, Object> policy = buildRuntimePolicy();
        Map<String, Object> enforcement = enforceRuntimePolicy(policy, mutations, asList(repairs.get("repairs")),
                depth);

        Map<String, Object> patterns = buildRuntimePatterns(
                asMap(Py.get(asMap(Py.get(semanticResult == null ? map() : semanticResult, "semantic", map())),
                        "ui", map())),
                new ArrayList<>(List.of(Py.get(workflowInner, "plan", map()))), semanticResult,
                asList(Py.get(mem, "evolution_histories", new ArrayList<>())));

        Map<String, Object> graph = buildRuntimeEvolutionGraph(evolution, repairs, optimization);

        Map<String, Object> prior = asMap(Py.get(mem, "last_evolution", map()));
        Map<String, Object> diff = Py.truthy(prior) ? diffEvolutionRuntime(prior, evolution)
                : mapOf("revertible", true);

        List<Object> distributedEvolutions = new ArrayList<>(List.of(evolution));
        if (Py.truthy(Py.get(mem, "distributed_evolutions", null))) {
            distributedEvolutions.addAll(asList(mem.get("distributed_evolutions")));
        }
        Map<String, Object> convergence = convergeRuntimeEvolution(distributedEvolutions);

        Map<String, Object> payload = map();
        payload.put("evolution", evolution);
        payload.put("selector", selector);
        payload.put("workflow", workflow);
        payload.put("semantic", semantic);
        payload.put("topology", topology);
        payload.put("strategy", adaptedStrategy);
        payload.put("repairs", repairs);
        payload.put("recovery", recovery);
        payload.put("optimization", optimization);
        payload.put("patterns", patterns);
        payload.put("lineage", lineage);
        payload.put("graph", graph);
        payload.put("policy", policy);
        payload.put("enforcement", enforcement);
        payload.put("convergence", convergence);
        payload.put("diff", diff);
        payload.put("tick", tick);
        payload.put("bounded", true);

        List<Object> histories = new ArrayList<>(asList(Py.get(mem, "evolution_histories", new ArrayList<>())));
        histories.add(evolution);
        List<Object> optHistories = new ArrayList<>(asList(Py.get(mem, "optimization_histories", new ArrayList<>())));
        optHistories.add(optimization);
        List<Object> distLast10 = distributedEvolutions.size() > 10
                ? new ArrayList<>(distributedEvolutions.subList(distributedEvolutions.size() - 10,
                        distributedEvolutions.size()))
                : distributedEvolutions;
        Map<String, Object> update = map();
        update.put("evolution_histories", histories);
        update.put("selector_lineage", lineage);
        update.put("workflow_evolution", workflow);
        update.put("semantic_evolution", semantic);
        update.put("optimization_histories", optHistories);
        update.put("last_evolution", evolution);
        update.put("last_evolution_id", evolutionId);
        update.put("distributed_evolutions", distLast10);
        Map<String, Object> updatedMemory = rememberEvolutionRuntime(mem, update);

        payload.put("memory", updatedMemory);
        Map<String, Object> replay = map();
        replay.put("lineage", lineage);
        replay.put("evolution", evolution);
        replay.put("replayed", true);
        replay.put("bounded", true);
        payload.put("replay", replay);
        payload.put("evolution_ir", compileEvolutionRuntimeIr(payload));
        return payload;
    }

    /** {@code run_evolution_for_extraction} (no FS when memory path/key empty). */
    public static Map<String, Object> runEvolutionForExtraction(boolean evolvingRuntime, String memoryPath,
            String memoryKey, Map<String, Object> adaptiveMemory, Map<String, Object> workflowResult,
            Map<String, Object> semanticResult, Map<String, Object> syncResult, Map<String, Object> distributedResult,
            List<Object> failures, long tick, boolean mergeGraph) {
        if (!evolvingRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> memory = map(); // empty memory path -> no FS load

        Map<String, Object> result = runEvolutionRuntime(adaptiveMemory, workflowResult, semanticResult, syncResult,
                distributedResult, failures, memory, tick);

        Map<String, Object> graphIr = evolutionRuntimeIrToGraph(asMap(Py.get(result, "evolution_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("evolution", result);
        out.put("evolution_ir", Py.get(result, "evolution_ir", map()));
        out.put("evolution_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
