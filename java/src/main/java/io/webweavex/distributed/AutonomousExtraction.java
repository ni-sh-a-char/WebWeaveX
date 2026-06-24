package io.webweavex.distributed;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.streaming.StreamingRuntime;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.TreeSet;

/**
 * Port of {@code run_autonomous_extraction} ({@code core.distributed_extraction.
 * autonomous_extraction_engine}) and its pure distributed scheduler {@code run_distributed_extraction}
 * plus the distributed sub-engines (worker/queue/scheduler/load-balancer/session/identity/adaptive/
 * stream/federation/runtime-graph/monitoring/cluster). Deterministic task-dict scheduler — operates on
 * task descriptors (URL strings, priorities), never fetches or parses page content. Certified for the
 * portable flag contract (the optional {@code native_extraction} branch — the only blocked sub-path —
 * is excluded). See {@code java/JAVA_PENDING_API_AUDIT.md}.
 */
public final class AutonomousExtraction {

    private AutonomousExtraction() {
    }

    private static final int MAX_QUEUE_SIZE = 10000;
    private static final int MAX_SCHEDULED = 5000;
    private static final int DEFAULT_COOLDOWN = 5;
    private static final int MAX_WORKERS = 1000;
    private static final int MAX_GRAPH = 1_000_000;

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
        return Py.str(o);
    }

    private static int cmp(String a, String b) {
        return Normalization.codePointCompare(a, b);
    }

    private static Object gd(Map<String, Object> m, String k, Object dflt) {
        return m.containsKey(k) ? m.get(k) : dflt;
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
            try {
                return Long.parseLong(((String) v).trim());
            } catch (NumberFormatException e) {
                return dflt;
            }
        }
        return dflt;
    }

    // -------------------------------------------------------------- worker / queue / scheduler
    private static Map<String, Object> createExtractionWorker(String workerId, Map<String, Object> identity,
            Map<String, Object> adaptiveRuntime, Map<String, Object> streamRuntime) {
        Map<String, Object> w = map();
        w.put("worker_id", str(workerId));
        w.put("runtime_state", map());
        w.put("identity", identity == null ? map() : new LinkedHashMap<>(identity));
        w.put("adaptive_runtime", adaptiveRuntime == null ? map() : new LinkedHashMap<>(adaptiveRuntime));
        w.put("stream_runtime", streamRuntime == null ? map() : new LinkedHashMap<>(streamRuntime));
        w.put("status", "idle");
        w.put("bounded", true);
        return w;
    }

    private static List<Object> enqueueExtraction(List<Object> queue, Map<String, Object> task) {
        List<Object> bounded = new ArrayList<>(queue.subList(0, Math.min(queue.size(), MAX_QUEUE_SIZE)));
        String taskId = str(gd(task, "task_id", "task_" + bounded.size()));
        Map<String, Object> entry = map();
        entry.put("task_id", taskId);
        entry.put("url", str(gd(task, "url", "")));
        entry.put("priority", pyInt(gd(task, "priority", 0L), 0));
        entry.put("order", (long) bounded.size());
        entry.put("bounded", true);
        bounded.add(entry);
        bounded.sort(AutonomousExtraction::queueOrder);
        if (bounded.size() > MAX_QUEUE_SIZE) {
            bounded = new ArrayList<>(bounded.subList(0, MAX_QUEUE_SIZE));
        }
        return bounded;
    }

    private static int queueOrder(Object a, Object b) {
        Map<String, Object> ma = asMap(a);
        Map<String, Object> mb = asMap(b);
        int c = Long.compare(-pyInt(ma.get("priority"), 0), -pyInt(mb.get("priority"), 0));
        if (c != 0) {
            return c;
        }
        c = Long.compare(pyInt(ma.get("order"), 0), pyInt(mb.get("order"), 0));
        return c != 0 ? c : cmp(str(ma.get("task_id")), str(mb.get("task_id")));
    }

    private static Map<String, Object> scheduleExtractionRuntime(List<Object> tasks, long tick) {
        List<Object> scheduled = new ArrayList<>();
        int limit = Math.min(tasks.size(), MAX_SCHEDULED);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> task = asMap(tasks.get(index));
            long priority = pyInt(gd(task, "priority", 0L), 0);
            long retries = pyInt(gd(task, "retries", 0L), 0);
            long cooldown = pyInt(gd(task, "cooldown", (long) DEFAULT_COOLDOWN), DEFAULT_COOLDOWN);
            long pacing = pyInt(gd(task, "pacing", 1L), 1);
            long runAt = tick + (cooldown * retries) + (pacing * index);
            Map<String, Object> e = map();
            e.put("task_id", str(gd(task, "task_id", "task_" + index)));
            e.put("url", str(gd(task, "url", "")));
            e.put("priority", priority);
            e.put("run_at", runAt);
            e.put("retries", retries);
            e.put("bounded", true);
            scheduled.add(e);
        }
        scheduled.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int c = Long.compare(pyInt(ma.get("run_at"), 0), pyInt(mb.get("run_at"), 0));
            if (c != 0) {
                return c;
            }
            c = Long.compare(-pyInt(ma.get("priority"), 0), -pyInt(mb.get("priority"), 0));
            return c != 0 ? c : cmp(str(ma.get("task_id")), str(mb.get("task_id")));
        });
        Map<String, Object> out = map();
        out.put("scheduled", scheduled);
        out.put("tick", tick);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> balanceExtractionWorkloads(List<Object> workers, List<Object> tasks) {
        if (workers.isEmpty()) {
            Map<String, Object> out = map();
            out.put("assignments", new ArrayList<>());
            out.put("bounded", true);
            return out;
        }
        List<Object> active = new ArrayList<>(workers.subList(0, Math.min(workers.size(), MAX_WORKERS)));
        active.sort((a, b) -> cmp(str(asMap(a).get("worker_id")), str(asMap(b).get("worker_id"))));
        List<Object> assignments = new ArrayList<>();
        for (int index = 0; index < tasks.size(); index++) {
            Map<String, Object> task = asMap(tasks.get(index));
            Map<String, Object> worker = asMap(active.get(index % active.size()));
            Map<String, Object> a = map();
            a.put("task_id", str(gd(task, "task_id", "task_" + index)));
            a.put("worker_id", str(gd(worker, "worker_id", "")));
            a.put("partition", (long) (index % active.size()));
            assignments.add(a);
        }
        assignments.sort((x, y) -> {
            Map<String, Object> mx = asMap(x);
            Map<String, Object> my = asMap(y);
            int c = cmp(str(mx.get("worker_id")), str(my.get("worker_id")));
            return c != 0 ? c : cmp(str(mx.get("task_id")), str(my.get("task_id")));
        });
        Map<String, Object> out = map();
        out.put("assignments", assignments);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> routeAuthenticatedSessions(List<Object> workers) {
        List<Object> routes = new ArrayList<>();
        for (Object wObj : workers) {
            Map<String, Object> worker = asMap(wObj);
            String workerId = str(gd(worker, "worker_id", ""));
            Map<String, Object> session = asMap(gd(asMap(gd(worker, "runtime_state", map())), "session", map()));
            Map<String, Object> r = map();
            r.put("worker_id", workerId);
            r.put("session_fingerprint", str(gd(session, "session_fingerprint", workerId)));
            r.put("isolated", true);
            routes.add(r);
        }
        routes.sort((a, b) -> cmp(str(asMap(a).get("worker_id")), str(asMap(b).get("worker_id"))));
        Map<String, Object> out = map();
        out.put("routes", routes);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> routeBrowserIdentity(List<Object> workers) {
        List<Object> routes = new ArrayList<>();
        for (Object wObj : workers) {
            Map<String, Object> worker = asMap(wObj);
            Map<String, Object> identity = asMap(gd(worker, "identity", map()));
            Map<String, Object> r = map();
            r.put("worker_id", str(gd(worker, "worker_id", "")));
            r.put("profile_id", str(gd(identity, "profile_id", "default")));
            r.put("fingerprint_hash", str(gd(identity, "fingerprint_hash", "")));
            routes.add(r);
        }
        routes.sort((a, b) -> cmp(str(asMap(a).get("worker_id")), str(asMap(b).get("worker_id"))));
        Map<String, Object> out = map();
        out.put("routes", routes);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> synchronizeAdaptiveRuntime(List<Object> adaptiveStates) {
        Map<String, Object> healed = new TreeMap<>();
        TreeSet<String> pagination = new TreeSet<>(Normalization::codePointCompare);
        List<Object> modals = new ArrayList<>();
        TreeSet<String> stableFields = new TreeSet<>(Normalization::codePointCompare);
        for (Object sObj : adaptiveStates) {
            Map<String, Object> state = asMap(sObj);
            Map<String, Object> memory = state.containsKey("memory")
                    ? asMap(state.get("memory")) : asMap(gd(state, "adaptive_runtime", map()));
            healed.putAll(asMap(gd(memory, "healed_selectors", map())));
            for (Object p : asList(gd(memory, "pagination_patterns", new ArrayList<>()))) {
                pagination.add(str(p));
            }
            modals.addAll(asList(gd(memory, "modal_solutions", new ArrayList<>())));
            Map<String, Object> schema = asMap(gd(state, "schema", map()));
            for (Object f : asList(gd(schema, "fields", new ArrayList<>()))) {
                stableFields.add(str(f));
            }
        }
        Map<String, Object> out = map();
        out.put("healed_selectors", new LinkedHashMap<>(healed));
        out.put("pagination_patterns", new ArrayList<>(pagination));
        out.put("modal_solutions", modals.subList(0, Math.min(modals.size(), 1000)));
        out.put("stable_schema_fields", new ArrayList<>(stableFields));
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> mergeStreamRuntimes(List<Object> streams) {
        List<Object> merged = new ArrayList<>();
        int limit = Math.min(streams.size(), 1000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> stream = asMap(streams.get(index));
            String source = str(gd(stream, "source", "stream_" + index));
            List<Object> events = StreamingRuntime.normalizeStreamEvents(asList(gd(stream, "events", new ArrayList<>())));
            for (Object eObj : events) {
                Map<String, Object> enriched = new LinkedHashMap<>(asMap(eObj));
                enriched.put("stream_source", source);
                merged.add(enriched);
            }
        }
        merged.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int c = Long.compare(pyInt(ma.get("timestamp"), 0), pyInt(mb.get("timestamp"), 0));
            if (c != 0) {
                return c;
            }
            c = cmp(str(ma.get("stream_source")), str(mb.get("stream_source")));
            return c != 0 ? c : cmp(str(ma.get("id")), str(mb.get("id")));
        });
        Map<String, Object> out = map();
        out.put("events", merged);
        out.put("stream_count", (long) Math.min(streams.size(), 1000));
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> federateStreamRuntimes(List<Object> streams) {
        List<Object> payloads = new ArrayList<>();
        for (int index = 0; index < streams.size(); index++) {
            Map<String, Object> stream = asMap(streams.get(index));
            List<Object> events = asList(gd(stream, "events", new ArrayList<>()));
            if (events.isEmpty() && stream.get("stream_runtime") != null) {
                events = asList(gd(asMap(stream.get("stream_runtime")), "events", new ArrayList<>()));
            }
            Map<String, Object> p = map();
            p.put("source", str(gd(stream, "worker_id", "worker_" + index)));
            p.put("events", new ArrayList<>(events));
            payloads.add(p);
        }
        Map<String, Object> merged = mergeStreamRuntimes(payloads);
        Map<String, Object> out = map();
        out.put("events", merged.get("events"));
        out.put("stream_count", merged.get("stream_count"));
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> buildRuntimeGraphList(List<Object> runtimeIrs) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        java.util.Set<String> seenNodes = new java.util.HashSet<>();
        java.util.Set<String> seenEdges = new java.util.HashSet<>();
        int limit = Math.min(runtimeIrs.size(), 10000);
        for (int i = 0; i < limit; i++) {
            Map<String, Object> runtime = asMap(runtimeIrs.get(i));
            String rt = str(gd(runtime, "ir", "unknown"));
            for (Object nObj : asList(runtime.get("nodes"))) {
                Map<String, Object> node = asMap(nObj);
                String id = str(gd(node, "id", "")).strip();
                if (id.isEmpty() || seenNodes.contains(id)) {
                    continue;
                }
                seenNodes.add(id);
                Map<String, Object> en = new LinkedHashMap<>(node);
                en.put("runtime_type", rt);
                nodes.add(en);
                if (nodes.size() >= MAX_GRAPH) {
                    break;
                }
            }
            for (Object eObj : asList(runtime.get("edges"))) {
                Map<String, Object> edge = asMap(eObj);
                String src = str(gd(edge, "from", "")).strip();
                String dst = str(gd(edge, "to", "")).strip();
                String rel = str(gd(edge, "relation", "related_to")).strip();
                if (src.isEmpty() || dst.isEmpty()) {
                    continue;
                }
                String key = src + " " + dst + " " + rel;
                if (seenEdges.contains(key)) {
                    continue;
                }
                seenEdges.add(key);
                Map<String, Object> en = new LinkedHashMap<>(edge);
                en.put("runtime_type", rt);
                edges.add(en);
                if (edges.size() >= MAX_GRAPH) {
                    break;
                }
            }
        }
        nodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        edges.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int c = cmp(str(ma.get("from")), str(mb.get("from")));
            if (c != 0) {
                return c;
            }
            c = cmp(str(ma.get("to")), str(mb.get("to")));
            return c != 0 ? c : cmp(str(ma.get("relation")), str(mb.get("relation")));
        });
        Map<String, Object> out = map();
        out.put("ir", "unified_runtime_graph");
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> emptyGraph() {
        Map<String, Object> g = map();
        g.put("ir", "unified_runtime_graph");
        g.put("nodes", new ArrayList<>());
        g.put("edges", new ArrayList<>());
        g.put("bounded", true);
        return g;
    }

    private static Map<String, Object> federateExtractionRuntimes(List<Object> runtimes) {
        List<Object> graphs = new ArrayList<>();
        int limit = Math.min(runtimes.size(), MAX_WORKERS);
        for (int i = 0; i < limit; i++) {
            Map<String, Object> runtime = asMap(runtimes.get(i));
            if (Py.truthy(runtime.get("nodes")) || Py.truthy(runtime.get("edges"))) {
                graphs.add(runtime);
            }
        }
        Map<String, Object> merged = graphs.isEmpty() ? emptyGraph() : buildRuntimeGraphList(graphs);
        Map<String, Object> out = map();
        out.put("topology", merged);
        out.put("runtime_count", (long) Math.min(runtimes.size(), MAX_WORKERS));
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> buildDistributedRuntimeGraph(List<Object> workers, Map<String, Object> topology) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        for (Object wObj : workers) {
            Map<String, Object> worker = asMap(wObj);
            Map<String, Object> n = map();
            n.put("id", str(gd(worker, "worker_id", "")));
            n.put("type", "worker");
            n.put("status", gd(worker, "status", "idle"));
            nodes.add(n);
        }
        for (Object nObj : asList(gd(topology, "nodes", new ArrayList<>()))) {
            Map<String, Object> node = asMap(nObj);
            Map<String, Object> n = map();
            n.put("id", str(gd(node, "id", "")));
            n.put("type", gd(node, "type", "runtime"));
            nodes.add(n);
        }
        for (int index = 0; index < workers.size() - 1; index++) {
            Map<String, Object> e = map();
            e.put("from", str(gd(asMap(workers.get(index)), "worker_id", "")));
            e.put("to", str(gd(asMap(workers.get(index + 1)), "worker_id", "")));
            e.put("relation", "worker_next");
            edges.add(e);
        }
        nodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        Map<String, Object> out = map();
        out.put("ir", "distributed_runtime_graph");
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> monitorExtractionCluster(List<Object> workers, List<Object> queue) {
        Map<String, Long> statuses = new TreeMap<>();
        for (Object wObj : workers) {
            String status = str(gd(asMap(wObj), "status", "unknown"));
            statuses.merge(status, 1L, Long::sum);
        }
        long active = statuses.getOrDefault("idle", 0L) + statuses.getOrDefault("running", 0L);
        Map<String, Object> out = map();
        out.put("worker_statuses", new LinkedHashMap<>(statuses));
        out.put("queue_depth", (long) queue.size());
        out.put("active_workers", active);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> buildClusterState(List<Object> workers, List<Object> queue) {
        TreeSet<String> workerIds = new TreeSet<>(Normalization::codePointCompare);
        for (Object wObj : workers) {
            workerIds.add(str(gd(asMap(wObj), "worker_id", "")));
        }
        Map<String, Object> out = map();
        out.put("worker_count", (long) workers.size());
        out.put("queue_depth", (long) queue.size());
        out.put("worker_ids", new ArrayList<>(workerIds));
        out.put("bounded", true);
        return out;
    }

    private static final Map<String, List<String>> OBJECTIVES = new LinkedHashMap<>();

    static {
        OBJECTIVES.put("login", List.of("open_login", "fill_credentials", "submit"));
        OBJECTIVES.put("extract_dashboard", List.of("navigate_dashboard", "capture_widgets", "capture_tables"));
        OBJECTIVES.put("export_report", List.of("open_reports", "select_report", "export"));
        OBJECTIVES.put("extract_invoices", List.of("open_invoices", "paginate", "extract_rows"));
        OBJECTIVES.put("monitor_metrics", List.of("open_dashboard", "observe_metrics", "checkpoint"));
    }

    private static Map<String, Object> buildRuntimeGoal(String objective) {
        List<String> steps = OBJECTIVES.getOrDefault(objective, List.of("observe", "extract"));
        Map<String, Object> out = map();
        out.put("objective", objective);
        out.put("steps", new ArrayList<>(steps));
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- run_distributed_extraction
    private static Map<String, Object> runDistributedExtraction(List<Object> tasks, List<Object> workers, long tick) {
        List<Object> queue = new ArrayList<>();
        List<Object> workerList = workers != null ? new ArrayList<>(workers) : new ArrayList<>();
        if (workerList.isEmpty()) {
            Map<String, Object> identity = map();
            identity.put("profile_id", "default");
            identity.put("fingerprint_hash", "fp0");
            Map<String, Object> healedMem = map();
            healedMem.put("healed_selectors", map());
            Map<String, Object> adaptive = map();
            adaptive.put("memory", healedMem);
            Map<String, Object> streamRt = map();
            streamRt.put("events", new ArrayList<>());
            workerList.add(createExtractionWorker("worker_0", identity, adaptive, streamRt));
        }
        for (Object t : tasks) {
            queue = enqueueExtraction(queue, asMap(t));
        }
        Map<String, Object> schedule = scheduleExtractionRuntime(tasks, tick);
        Map<String, Object> assignments = balanceExtractionWorkloads(workerList, tasks);
        Map<String, Object> sessionRoutes = routeAuthenticatedSessions(workerList);
        Map<String, Object> identityRoutes = routeBrowserIdentity(workerList);

        List<Object> adaptiveStates = new ArrayList<>();
        for (Object w : workerList) {
            adaptiveStates.add(gd(asMap(w), "adaptive_runtime", map()));
        }
        Map<String, Object> adaptiveSync = synchronizeAdaptiveRuntime(adaptiveStates);

        List<Object> streamInputs = new ArrayList<>();
        for (Object w : workerList) {
            Map<String, Object> worker = asMap(w);
            Map<String, Object> s = map();
            s.put("worker_id", worker.get("worker_id"));
            s.put("events", asList(gd(asMap(gd(worker, "stream_runtime", map())), "events", new ArrayList<>())));
            streamInputs.add(s);
        }
        Map<String, Object> streamFederation = federateStreamRuntimes(streamInputs);

        Map<String, Object> federation = federateExtractionRuntimes(new ArrayList<>());
        Map<String, Object> distributedGraph = buildDistributedRuntimeGraph(workerList, asMap(gd(federation, "topology", map())));
        Map<String, Object> monitoring = monitorExtractionCluster(workerList, queue);
        Map<String, Object> cluster = buildClusterState(workerList, queue);

        Map<String, Object> nextCheckpoint = map();
        nextCheckpoint.put("queue", queue);
        nextCheckpoint.put("workers", workerList);
        nextCheckpoint.put("runtime_graph", distributedGraph);
        nextCheckpoint.put("identities", gd(identityRoutes, "routes", new ArrayList<>()));
        nextCheckpoint.put("adaptive_memory", adaptiveSync);
        nextCheckpoint.put("stream_runtime", streamFederation);
        nextCheckpoint.put("tick", tick + 1);
        nextCheckpoint.put("assignments", gd(assignments, "assignments", new ArrayList<>()));
        nextCheckpoint.put("bounded", true);

        Map<String, Object> out = map();
        out.put("workers", workerList);
        out.put("queue", queue);
        out.put("schedule", schedule);
        out.put("assignments", assignments);
        out.put("session_routes", sessionRoutes);
        out.put("identity_routes", identityRoutes);
        out.put("adaptive_sync", adaptiveSync);
        out.put("stream_federation", streamFederation);
        out.put("topology", federation);
        out.put("distributed_graph", distributedGraph);
        out.put("monitoring", monitoring);
        out.put("cluster", cluster);
        out.put("checkpoint", nextCheckpoint);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- run_autonomous_extraction (portable contract)
    /** {@code run_autonomous_extraction(tasks, workers, tick, objective_execution, objective_name)} —
     * portable flag contract (native_extraction and other live-runtime flags excluded). */
    public static Map<String, Object> runAutonomousExtraction(List<Object> tasks, List<Object> workers, long tick,
            boolean objectiveExecution, String objectiveName) {
        List<Object> taskList = tasks == null ? new ArrayList<>() : tasks;
        Map<String, Object> result = runDistributedExtraction(taskList, workers, tick);
        Map<String, Object> payload = new LinkedHashMap<>(result);
        payload.put("autonomous", true);
        payload.put("bounded", true);
        if (objectiveExecution) {
            Map<String, Object> oe = map();
            oe.put("enabled", true);
            oe.put("objective", objectiveName);
            oe.put("goal", buildRuntimeGoal(objectiveName));
            oe.put("bounded", true);
            payload.put("objective_execution", oe);
        }
        return payload;
    }
}
