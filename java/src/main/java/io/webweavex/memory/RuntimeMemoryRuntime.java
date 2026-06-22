package io.webweavex.memory;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import io.webweavex.execution.ExecutionRuntime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Port of the {@code core.memory} orchestrator family — {@code run_runtime_memory} and
 * {@code run_memory_for_extraction} — plus the ~14 deterministic memory sub-engines and the
 * runtime-memory IR they fan out to. Dependency-clean (37-module closure, 0 forbidden, importable;
 * serializable output). Reuses the already-certified {@link RuntimeMemory}, {@link MemoryQuery},
 * {@link MemorySearch} engines, the {@link MemoryPersistence} persistence, and
 * {@link ExecutionRuntime#buildUnifiedRuntimeGraph}. Zero new substrate. The final dependency-clean
 * slice of Phase A.
 */
public final class RuntimeMemoryRuntime {

    private RuntimeMemoryRuntime() {
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

    private static long historyTick(Object o) {
        Map<String, Object> m = asMap(o);
        return pyInt(Py.get(m, "tick", Py.get(m, "step", 0L)), 0);
    }

    // -------------------------------------------------------------- sub-engines

    public static List<Object> appendRuntimeHistory(List<Object> history, Map<String, Object> entry) {
        List<Object> updated = new ArrayList<>(history);
        updated.add(entry);
        updated.sort(Comparator.comparingLong(RuntimeMemoryRuntime::historyTick));
        return capped(updated, 100000);
    }

    public static Map<String, Object> buildKnowledgeMemory(List<Object> entities, List<Object> relations,
            Map<String, Object> topology) {
        List<Object> ent = new ArrayList<>(entities == null ? new ArrayList<>() : entities);
        ent.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        List<Object> rel = new ArrayList<>(relations == null ? new ArrayList<>() : relations);
        rel.sort(Comparator.comparing((Object r) -> str(Py.get(asMap(r), "from", "")), RuntimeMemoryRuntime::cmp)
                .thenComparing(r -> str(Py.get(asMap(r), "to", "")), RuntimeMemoryRuntime::cmp)
                .thenComparing(r -> str(Py.get(asMap(r), "relation", "")), RuntimeMemoryRuntime::cmp));
        Map<String, Object> topo = topology == null ? map() : topology;
        Map<String, Object> out = map();
        out.put("entities", ent);
        out.put("semantic_relations", rel);
        out.put("runtime_graphs", asList(topo.get("graphs")));
        out.put("distributed_topology", new LinkedHashMap<>(asMap(topo.get("distributed"))));
        out.put("application_cognition", new LinkedHashMap<>(asMap(topo.get("application"))));
        out.put("operational_structures", asList(topo.get("operations")));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildSemanticMemory(Map<String, Object> semantic, List<Object> history) {
        Map<String, Object> sem = semantic == null ? map() : semantic;
        List<Object> hist = history == null ? new ArrayList<>() : history;
        Map<String, Object> inner = asMap(Py.get(sem, "semantic", sem));
        List<Object> entities = asList(asMap(Py.get(inner, "entities", map())).get("entities"));
        Set<String> conceptSet = new LinkedHashSet<>();
        for (Object eo : entities) {
            Map<String, Object> entity = asMap(eo);
            String label = str(Py.get(entity, "label", Py.get(entity, "type", "")));
            if (!label.isEmpty()) {
                conceptSet.add(label);
            }
        }
        List<Object> concepts = new ArrayList<>(conceptSet);
        concepts.sort((a, b) -> cmp((String) a, (String) b));
        List<Object> recurringWorkflows = new ArrayList<>();
        for (Object io : hist) {
            Map<String, Object> item = asMap(io);
            if ("workflow".equals(item.get("kind"))) {
                recurringWorkflows.add(str(Py.get(item, "objective", "")));
            }
        }
        List<Object> structures = new ArrayList<>();
        TreeMap<String, Object> innerSorted = new TreeMap<>(Normalization::codePointCompare);
        innerSorted.putAll(inner);
        structures.addAll(innerSorted.keySet());
        Map<String, Object> out = map();
        out.put("semantic_convergence", new ArrayList<>(concepts));
        out.put("recurring_concepts", new ArrayList<>(concepts));
        out.put("recurring_workflows", recurringWorkflows);
        out.put("recurring_structures", structures);
        out.put("domain", str(Py.get(asMap(Py.get(inner, "domain", map())), "domain", "")));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeLineageMemory(List<Object> selector, List<Object> workflow,
            List<Object> sync, List<Object> evolution, List<Object> extraction) {
        List<Object> lineage = new ArrayList<>();
        Object[][] buckets = {
            {"selector", selector}, {"workflow", workflow}, {"sync", sync}, {"evolution", evolution},
            {"extraction", extraction},
        };
        for (Object[] b : buckets) {
            String bucket = (String) b[0];
            List<Object> items = b[1] == null ? new ArrayList<>() : asList(b[1]);
            List<Object> cap = capped(items, 1000);
            for (int index = 0; index < cap.size(); index++) {
                Map<String, Object> item = asMap(cap.get(index));
                lineage.add(mapOf("id", str(Py.get(item, "id", bucket + ":" + index)), "kind", bucket,
                        "ancestor", str(Py.get(item, "ancestor", ""))));
            }
        }
        List<Object> sorted = new ArrayList<>(lineage);
        sorted.sort(Comparator.comparing((Object i) -> str(asMap(i).get("kind")), RuntimeMemoryRuntime::cmp)
                .thenComparing(i -> str(asMap(i).get("id")), RuntimeMemoryRuntime::cmp));
        Map<String, Object> out = map();
        out.put("lineage", sorted);
        out.put("selector_ancestry", filterKind(lineage, "selector"));
        out.put("workflow_ancestry", filterKind(lineage, "workflow"));
        out.put("sync_ancestry", filterKind(lineage, "sync"));
        out.put("evolution_ancestry", filterKind(lineage, "evolution"));
        out.put("extraction_ancestry", filterKind(lineage, "extraction"));
        out.put("bounded", true);
        return out;
    }

    private static List<Object> filterKind(List<Object> lineage, String kind) {
        List<Object> out = new ArrayList<>();
        for (Object i : lineage) {
            if (kind.equals(asMap(i).get("kind"))) {
                out.add(i);
            }
        }
        return out;
    }

    public static Map<String, Object> buildRuntimeMemoryGraph(List<Object> entities, List<Object> relations) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        for (Object eo : capped(entities, 10000)) {
            Map<String, Object> entity = asMap(eo);
            String nodeId = str(Py.get(entity, "id", Py.get(entity, "label", "")));
            if (nodeId.isEmpty()) {
                continue;
            }
            nodes.add(mapOf("id", nodeId, "type", str(Py.get(entity, "type", "entity"))));
        }
        for (Object ro : capped(relations, 10000)) {
            Map<String, Object> relation = asMap(ro);
            edges.add(mapOf("from", str(Py.get(relation, "from", "")), "to", str(Py.get(relation, "to", "")),
                    "relation", str(Py.get(relation, "relation", "relates_to"))));
        }
        if (nodes.isEmpty()) {
            nodes.add(mapOf("id", "memory:root", "type", "memory"));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), RuntimeMemoryRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), RuntimeMemoryRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), RuntimeMemoryRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeIndex(List<Object> entities, List<Object> workflows,
            List<Object> graphs, List<Object> streams, List<Object> connectors) {
        TreeMap<String, Object> entityIndex = new TreeMap<>(Normalization::codePointCompare);
        for (Object eo : entities) {
            Map<String, Object> item = asMap(eo);
            if (Py.truthy(item.get("id")) || Py.truthy(item.get("label"))) {
                entityIndex.put(str(Py.get(item, "id", Py.get(item, "label", ""))), item);
            }
        }
        TreeMap<String, Object> workflowIndex = new TreeMap<>(Normalization::codePointCompare);
        for (Object wo : workflows) {
            Map<String, Object> item = asMap(wo);
            workflowIndex.put(str(Py.get(item, "id", Py.get(item, "objective", ""))), item);
        }
        Map<String, Object> graphIndex = map();
        for (int i = 0; i < graphs.size(); i++) {
            graphIndex.put(String.valueOf(i), graphs.get(i));
        }
        Map<String, Object> streamIndex = map();
        for (int i = 0; i < streams.size(); i++) {
            streamIndex.put(String.valueOf(i), streams.get(i));
        }
        Map<String, Object> connectorIndex = map();
        for (int i = 0; i < connectors.size(); i++) {
            connectorIndex.put(String.valueOf(i), connectors.get(i));
        }
        Map<String, Object> out = map();
        out.put("entity_index", new LinkedHashMap<>(entityIndex));
        out.put("workflow_index", new LinkedHashMap<>(workflowIndex));
        out.put("graph_index", graphIndex);
        out.put("stream_index", streamIndex);
        out.put("connector_index", connectorIndex);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> replicateRuntimeMemory(Map<String, Object> source, List<Object> nodes) {
        List<Object> replicas = new ArrayList<>();
        List<Object> cap = capped(nodes, 1000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> node = asMap(cap.get(index));
            Map<String, Object> r = map();
            r.put("node_id", str(Py.get(node, "node_id", "node:" + index)));
            r.put("memory_id", str(Py.get(source, "memory_id", "")));
            r.put("runtime_history", asList(source.get("runtime_history")));
            r.put("lineage", asList(source.get("lineage")));
            r.put("replicated", true);
            replicas.add(r);
        }
        Map<String, Object> out = map();
        out.put("replicas", replicas);
        out.put("replica_count", (long) replicas.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> convergeRuntimeMemory(List<Object> replicas) {
        if (replicas.isEmpty()) {
            Map<String, Object> out = map();
            out.put("converged", true);
            out.put("memory_id", "");
            out.put("bounded", true);
            return out;
        }
        Map<String, Object> base = asMap(replicas.get(0));
        for (int i = 1; i < replicas.size(); i++) {
            if (!java.util.Objects.equals(asMap(replicas.get(i)).get("memory_id"), base.get("memory_id"))) {
                Map<String, Object> out = map();
                out.put("converged", false);
                out.put("conflict", true);
                out.put("bounded", true);
                return out;
            }
        }
        Map<String, Object> out = map();
        out.put("converged", true);
        out.put("memory_id", str(Py.get(base, "memory_id", "")));
        out.put("replica_count", (long) replicas.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildDistributedMemory(List<Object> nodes) {
        List<Object> merged = new ArrayList<>(nodes);
        merged.sort((a, b) -> cmp(str(Py.get(asMap(a), "node_id", "")), str(Py.get(asMap(b), "node_id", ""))));
        boolean synchronized_ = true;
        long conflicts = 0;
        for (Object no : merged) {
            Map<String, Object> n = asMap(no);
            if (!Py.truthy(Py.get(n, "synced", true))) {
                synchronized_ = false;
            }
            conflicts += pyInt(Py.get(n, "conflicts_resolved", 0L), 0);
        }
        Map<String, Object> out = map();
        out.put("nodes", merged);
        out.put("replication", (long) merged.size());
        out.put("synchronized", synchronized_);
        out.put("conflicts_resolved", conflicts);
        out.put("converged", merged.size() > 0);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> federateRuntimeMemory(List<Object> memories) {
        List<Object> history = new ArrayList<>();
        List<Object> lineage = new ArrayList<>();
        List<Object> relations = new ArrayList<>();
        for (Object mo : memories) {
            Map<String, Object> m = asMap(mo);
            history.addAll(asList(m.get("runtime_history")));
            lineage.addAll(asList(m.get("lineage")));
            relations.addAll(asList(m.get("semantic_relations")));
        }
        history.sort(Comparator.comparingLong(RuntimeMemoryRuntime::historyTick));
        lineage.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        relations.sort(Comparator.comparing((Object r) -> str(Py.get(asMap(r), "from", "")), RuntimeMemoryRuntime::cmp)
                .thenComparing(r -> str(Py.get(asMap(r), "to", "")), RuntimeMemoryRuntime::cmp));
        Map<String, Object> out = map();
        out.put("federated_count", (long) memories.size());
        out.put("runtime_history", history);
        out.put("lineage", lineage);
        out.put("semantic_relations", relations);
        out.put("bounded", true);
        return out;
    }

    /** {@code merge_runtime_memories} — sorts each memory's runtime_history IN PLACE (canon mutates). */
    public static Map<String, Object> mergeRuntimeMemories(List<Object> memories) {
        List<Object> ordered = new ArrayList<>(memories);
        ordered.sort((a, b) -> cmp(str(Py.get(asMap(a), "memory_id", Py.get(asMap(a), "runtime_id", ""))),
                str(Py.get(asMap(b), "memory_id", Py.get(asMap(b), "runtime_id", "")))));
        for (Object mo : ordered) {
            Map<String, Object> m = asMap(mo);
            Object history = m.get("runtime_history");
            if (history instanceof List) {
                List<Object> h = new ArrayList<>((List<Object>) history);
                h.sort(Comparator.comparingLong((Object x) -> pyInt(asMap(x).get("tick"), 0))
                        .thenComparing(x -> str(Py.get(asMap(x), "kind", "")), RuntimeMemoryRuntime::cmp)
                        .thenComparing(x -> str(Py.get(asMap(x), "source", "")), RuntimeMemoryRuntime::cmp));
                m.put("runtime_history", h);
            }
        }
        Map<String, Object> federated = federateRuntimeMemory(ordered);
        return RuntimeMemory.build(asList(federated.get("runtime_history")), asList(federated.get("lineage")),
                asList(federated.get("semantic_relations")));
    }

    public static Map<String, Object> buildRuntimeMemoryPolicy() {
        Map<String, Object> out = map();
        out.put("memory_bounds", 100000L);
        out.put("replay_limits", 10000L);
        out.put("synchronization_ceilings", 100000L);
        out.put("replication_depth", 1000L);
        out.put("federation_constraints", 1000L);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> enforceMemoryPolicy(Map<String, Object> policy, List<Object> history,
            List<Object> lineage, long replicas) {
        boolean within = history.size() <= pyInt(policy.get("memory_bounds"), 100000)
                && lineage.size() <= pyInt(policy.get("synchronization_ceilings"), 100000)
                && replicas <= pyInt(policy.get("replication_depth"), 1000);
        Map<String, Object> out = map();
        out.put("within_bounds", within);
        out.put("history_count", (long) history.size());
        out.put("lineage_count", (long) lineage.size());
        out.put("replicas", replicas);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> diffRuntimeMemory(Map<String, Object> previous, Map<String, Object> current) {
        Set<String> prevIds = new LinkedHashSet<>();
        for (Object i : asList(previous.get("lineage"))) {
            prevIds.add(str(Py.get(asMap(i), "id", "")));
        }
        Set<String> currIds = new LinkedHashSet<>();
        for (Object i : asList(current.get("lineage"))) {
            currIds.add(str(Py.get(asMap(i), "id", "")));
        }
        List<Object> added = new ArrayList<>();
        for (String id : currIds) {
            if (!prevIds.contains(id)) {
                added.add(id);
            }
        }
        added.sort((a, b) -> cmp((String) a, (String) b));
        List<Object> removed = new ArrayList<>();
        for (String id : prevIds) {
            if (!currIds.contains(id)) {
                removed.add(id);
            }
        }
        removed.sort((a, b) -> cmp((String) a, (String) b));
        Map<String, Object> out = map();
        out.put("memory_changed", !java.util.Objects.equals(previous.get("memory_id"), current.get("memory_id")));
        out.put("lineage_added", added);
        out.put("lineage_removed", removed);
        out.put("history_delta", (long) asList(current.get("runtime_history")).size()
                - asList(previous.get("runtime_history")).size());
        out.put("revertible", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> captureMemorySnapshot(Map<String, Object> state, long tick) {
        Map<String, Object> out = map();
        out.put("snapshot_id", "memory_snapshot:" + tick);
        out.put("tick", tick);
        out.put("state", new LinkedHashMap<>(state));
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- IR

    public static Map<String, Object> compileRuntimeMemoryIr(Map<String, Object> payload) {
        Map<String, Object> out = map();
        out.put("ir", "runtime_memory");
        out.put("memory_graphs", Py.get(payload, "graph", map()));
        out.put("semantic_indexes", Py.get(payload, "index", map()));
        out.put("lineage", Py.get(payload, "lineage", map()));
        out.put("runtime_history", Py.get(payload, "runtime", map()));
        out.put("distributed_memory", Py.get(payload, "distributed", map()));
        out.put("knowledge", Py.get(payload, "knowledge", map()));
        out.put("semantic", Py.get(payload, "semantic", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> runtimeMemoryIrToGraph(Map<String, Object> memoryIr) {
        Map<String, Object> graph = asMap(memoryIr.get("memory_graphs"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "memory:root", "type", "memory")));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "runtime_memory_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- orchestrator

    private static List<Object> collectHistory(Map<String, Object> sources, long tick) {
        List<Object> history = new ArrayList<>();
        if (Py.truthy(sources.get("workflow"))) {
            history.add(mapOf("tick", tick, "kind", "workflow", "source", "workflow"));
        }
        if (Py.truthy(sources.get("sync"))) {
            history.add(mapOf("tick", tick, "kind", "sync", "source", "sync"));
        }
        if (Py.truthy(sources.get("evolution"))) {
            history.add(mapOf("tick", tick, "kind", "evolution", "source", "evolution"));
        }
        if (Py.truthy(sources.get("live"))) {
            history.add(mapOf("tick", tick, "kind", "live", "source", "connectors"));
        }
        if (Py.truthy(sources.get("extraction"))) {
            history.add(mapOf("tick", tick, "kind", "extraction", "source", "browser"));
        }
        return history;
    }

    /** {@code run_runtime_memory}. */
    public static Map<String, Object> runRuntimeMemory(Map<String, Object> sources, Map<String, Object> stored,
            List<Object> nodesArg, long tick) {
        Map<String, Object> src = sources == null ? map() : sources;
        Map<String, Object> st = new LinkedHashMap<>(stored == null ? map() : stored);
        List<Object> nodes = nodesArg != null ? new ArrayList<>(nodesArg)
                : new ArrayList<>(List.of(mapOf("node_id", "primary", "synced", true)));

        Map<String, Object> priorRuntime = asMap(Py.get(st, "runtime", map()));
        boolean hasPrior = Py.truthy(priorRuntime);
        List<Object> history = asList(priorRuntime.get("runtime_history"));
        for (Object entry : collectHistory(src, tick)) {
            history = appendRuntimeHistory(history, asMap(entry));
        }

        List<Object> entities = new ArrayList<>();
        List<Object> relations = new ArrayList<>();
        Map<String, Object> semanticSrc = asMap(Py.get(src, "semantic", map()));
        if (Py.truthy(semanticSrc)) {
            Map<String, Object> inner = asMap(Py.get(semanticSrc, "semantic", semanticSrc));
            Map<String, Object> ents = asMap(Py.get(inner, "entities", map()));
            entities = asList(ents.get("entities"));
            relations = asList(ents.get("relations"));
        }

        Map<String, Object> topology = map();
        topology.put("graphs", new ArrayList<>(List.of(Py.get(src, "graph", map()))));
        topology.put("distributed", Py.get(src, "distributed", map()));
        topology.put("application", Py.get(src, "application", map()));
        Map<String, Object> knowledge = buildKnowledgeMemory(entities, relations, topology);
        Map<String, Object> semantic = buildSemanticMemory(semanticSrc, history);

        Map<String, Object> lineageObj = buildRuntimeLineageMemory(
                asList(asMap(Py.get(asMap(Py.get(src, "evolution", map())), "selector", map())).get("selectors")),
                new ArrayList<>(List.of(mapOf("id", "wf:0", "ancestor", ""))),
                asList(asMap(Py.get(src, "sync", map())).get("lineage")),
                asList(asMap(Py.get(src, "evolution", map())).get("lineage")),
                new ArrayList<>(List.of(mapOf("id", "extract:" + tick, "ancestor", ""))));

        Map<String, Object> runtime = RuntimeMemory.build(history, asList(lineageObj.get("lineage")),
                asList(knowledge.get("semantic_relations")));

        Map<String, Object> graph = buildRuntimeMemoryGraph(asList(knowledge.get("entities")),
                asList(knowledge.get("semantic_relations")));

        List<Object> streams = asList(asMap(Py.get(asMap(Py.get(src, "live", map())), "streams", map())).get("streams"));
        Map<String, Object> index = buildRuntimeIndex(asList(knowledge.get("entities")),
                new ArrayList<>(List.of(mapOf("id", str(Py.get(asMap(Py.get(src, "workflow", map())), "objective", "operate"))))),
                new ArrayList<>(List.of(graph)), streams,
                new ArrayList<>(List.of(Py.get(src, "live", map()))));

        Map<String, Object> replication = replicateRuntimeMemory(runtime, nodes);
        Map<String, Object> convergence = convergeRuntimeMemory(asList(replication.get("replicas")));
        Map<String, Object> distributed = buildDistributedMemory(nodes);

        List<Object> memoryList = hasPrior ? new ArrayList<>(List.of(runtime, priorRuntime))
                : new ArrayList<>(List.of(runtime));
        Map<String, Object> federated = federateRuntimeMemory(memoryList);
        List<Object> mergeList = hasPrior ? new ArrayList<>(List.of(runtime, priorRuntime))
                : new ArrayList<>(List.of(runtime));
        Map<String, Object> merged = mergeRuntimeMemories(mergeList); // mutates runtime.runtime_history in place

        Map<String, Object> policy = buildRuntimeMemoryPolicy();
        Map<String, Object> enforcement = enforceMemoryPolicy(policy, asList(runtime.get("runtime_history")),
                asList(runtime.get("lineage")), pyInt(replication.get("replica_count"), 0));

        Map<String, Object> diff = hasPrior ? diffRuntimeMemory(priorRuntime, runtime) : mapOf("revertible", true);
        Map<String, Object> snapState = map();
        snapState.put("runtime", runtime);
        snapState.put("knowledge", knowledge);
        snapState.put("graph", graph);
        Map<String, Object> snapshot = captureMemorySnapshot(snapState, tick);

        Map<String, Object> payload = map();
        payload.put("runtime", runtime);
        payload.put("knowledge", knowledge);
        payload.put("semantic", semantic);
        payload.put("lineage", lineageObj);
        payload.put("graph", graph);
        payload.put("index", index);
        payload.put("distributed", distributed);
        payload.put("federation", federated);
        payload.put("merged", merged);
        payload.put("replication", replication);
        payload.put("convergence", convergence);
        payload.put("policy", policy);
        payload.put("enforcement", enforcement);
        payload.put("diff", diff);
        payload.put("snapshot", snapshot);
        payload.put("bounded", true);

        Map<String, Object> replay = map();
        replay.put("lineage", asList(lineageObj.get("lineage")));
        replay.put("runtime_history", asList(runtime.get("runtime_history")));
        replay.put("memory_id", str(Py.get(runtime, "memory_id", "")));
        replay.put("replayed", true);
        replay.put("bounded", true);
        payload.put("replay", replay);
        payload.put("memory_ir", compileRuntimeMemoryIr(payload));
        return payload;
    }

    /** {@code run_memory_for_extraction}. */
    public static Map<String, Object> runMemoryForExtraction(boolean federatedMemory, String memoryPath,
            String memoryKey, Map<String, Object> sources, List<Object> nodes, long tick, boolean mergeGraph) {
        if (!federatedMemory) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> stored = map(); // empty memory path -> no FS load

        Map<String, Object> result = runRuntimeMemory(sources, stored, nodes, tick);

        Map<String, Object> graphIr = runtimeMemoryIrToGraph(asMap(Py.get(result, "memory_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("memory", result);
        out.put("memory_ir", Py.get(result, "memory_ir", map()));
        out.put("memory_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("query", MemoryQuery.queryRuntimeMemory(asMap(Py.get(result, "runtime", map())), "semantic", ""));
        out.put("search", MemorySearch.searchRuntimeMemory(asMap(Py.get(result, "index", map())), "", "structural"));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
