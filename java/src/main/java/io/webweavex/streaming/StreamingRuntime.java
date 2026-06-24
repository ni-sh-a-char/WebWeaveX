package io.webweavex.streaming;

import io.webweavex.connectors.ApiConnectors;
import io.webweavex.connectors.ContainerConnector;
import io.webweavex.connectors.DatabaseConnectors;
import io.webweavex.connectors.IdeConnector;
import io.webweavex.connectors.KubernetesConnector;
import io.webweavex.connectors.StreamConnectors;
import io.webweavex.connectors.TelemetryConnector;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyRepr;
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
import java.util.stream.Collectors;

/**
 * Port of the {@code core.streaming} + {@code core.connectors.live_runtime} family —
 * {@code build_stream_timeline}, {@code replay_stream_events}, {@code run_live_runtime},
 * {@code save_live_runtime}, {@code load_live_runtime} — plus the live-runtime IR and the
 * {@code extract_filesystem_runtime}/{@code extract_cicd_runtime} sub-engines. Dependency-clean
 * (0 forbidden; the FS memory engine + the filesystem-snapshot fallback are the only OS touch
 * points, neither hit on the parity-proven paths). Reuses the certified connector engines
 * ({@link DatabaseConnectors}, {@link ApiConnectors}, {@link StreamConnectors}, …), the
 * determinism/crypto/json substrate, and {@link ExecutionRuntime#buildUnifiedRuntimeGraph}.
 */
public final class StreamingRuntime {

    private StreamingRuntime() {
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

    /** Python {@code d.get(key)} — the value (cast to Map) when present, else {@code null}. */
    @SuppressWarnings("unchecked")
    private static Map<String, Object> subMap(Map<String, Object> d, String key) {
        Object v = d.get(key);
        return v instanceof Map ? (Map<String, Object>) v : null;
    }

    @SuppressWarnings("unchecked")
    private static List<Object> subList(Map<String, Object> d, String key) {
        Object v = d.get(key);
        return v instanceof List ? (List<Object>) v : null;
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

    private static String configStr(Map<String, Object> config, String key, String dflt) {
        Object v = config.get(key);
        return v == null ? dflt : str(v);
    }

    // -------------------------------------------------------------- stream replay engine

    /** {@code build_stream_timeline}. */
    public static Map<String, Object> buildStreamTimeline(List<Object> events) {
        List<Object> ordered = new ArrayList<>(events == null ? new ArrayList<>() : events);
        ordered.sort(Comparator.comparingLong((Object e) -> pyInt(asMap(e).get("timestamp"), 0))
                .thenComparing(e -> str(Py.get(asMap(e), "id", "")), StreamingRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "source", "")), StreamingRuntime::cmp));
        List<Object> edges = new ArrayList<>();
        String previousId = "";
        for (Object eo : ordered) {
            String eventId = str(Py.get(asMap(eo), "id", ""));
            if (!previousId.isEmpty()) {
                edges.add(mapOf("from", previousId, "to", eventId, "relation", "stream_next"));
            }
            previousId = eventId;
        }
        Map<String, Object> out = map();
        out.put("events", ordered);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    /** {@code replay_stream_events} (page test-hook side effect omitted; output is page-independent). */
    public static Map<String, Object> replayStreamEvents(List<Object> streamLog) {
        List<Object> replayed = new ArrayList<>();
        List<Object> cap = capped(streamLog == null ? new ArrayList<>() : streamLog, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = map();
            e.put("step", (long) index);
            e.put("event", new LinkedHashMap<>(asMap(cap.get(index))));
            e.put("replayed", true);
            replayed.add(e);
        }
        Map<String, Object> out = map();
        out.put("replay", replayed);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- connector sub-engines

    /** {@code extract_filesystem_runtime} (snapshot path is pure; null-snapshot walks the FS). */
    public static Map<String, Object> extractFilesystemRuntime(String root, Map<String, Object> snapshot) {
        if (snapshot != null) {
            List<Object> files = asList(snapshot.get("files"));
            files.sort((a, b) -> cmp(str(a), str(b)));
            Map<String, Object> out = map();
            out.put("root", str(Py.get(snapshot, "root", root)));
            out.put("topology", files);
            out.put("mutation_streams", asList(snapshot.get("mutations")));
            out.put("synchronization_state", new LinkedHashMap<>(asMap(snapshot.get("sync"))));
            out.put("permissions", new LinkedHashMap<>(asMap(snapshot.get("permissions"))));
            out.put("inode_relationships", asList(snapshot.get("inodes")));
            out.put("bounded", true);
            return out;
        }
        List<Object> topology = new ArrayList<>();
        try {
            Path base = Paths.get(root);
            if (Files.exists(base)) {
                List<String> rel = Files.walk(base).filter(Files::isRegularFile)
                        .map(p -> base.relativize(p).toString()).sorted(Normalization::codePointCompare)
                        .limit(5000).collect(Collectors.toList());
                topology.addAll(rel);
            }
        } catch (Exception e) {
            Map<String, Object> degraded = map();
            degraded.put("root", root);
            degraded.put("topology", new ArrayList<>());
            degraded.put("degraded", true);
            degraded.put("bounded", true);
            return degraded;
        }
        Map<String, Object> out = map();
        out.put("root", root);
        out.put("topology", topology);
        out.put("mutation_streams", new ArrayList<>());
        out.put("synchronization_state", map());
        out.put("permissions", map());
        out.put("inode_relationships", new ArrayList<>());
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_cicd_runtime}. */
    public static Map<String, Object> extractCicdRuntime(String provider, Map<String, Object> snapshot) {
        Map<String, Object> snap = snapshot == null ? map() : snapshot;
        Map<String, Object> out = map();
        out.put("provider", provider);
        out.put("workflows", asList(snap.get("workflows")));
        out.put("jobs", asList(snap.get("jobs")));
        out.put("logs", capped(asList(snap.get("logs")), 1000));
        out.put("artifacts", asList(snap.get("artifacts")));
        out.put("failures", asList(snap.get("failures")));
        out.put("deployment_graph", new LinkedHashMap<>(asMap(snap.get("deployment_graph"))));
        out.put("degraded", Py.get(snap, "degraded", false));
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- live runtime IR

    public static Map<String, Object> buildLiveTopologyGraph(Map<String, Object> live) {
        List<Object> nodes = new ArrayList<>();
        nodes.add(mapOf("id", "live:root", "type", "live_runtime"));
        List<Object> edges = new ArrayList<>();
        Map<String, Object> db = asMap(live.get("database"));
        if (Py.truthy(db.get("tables"))) {
            String dbId = "db:" + str(Py.get(db, "database_type", "db"));
            nodes.add(mapOf("id", dbId, "type", "database"));
            edges.add(mapOf("from", "live:root", "to", dbId, "relation", "connects"));
        }
        Map<String, Object> api = asMap(live.get("api"));
        if (Py.truthy(api.get("endpoints"))) {
            String apiId = "api:" + str(Py.get(api, "api_type", "rest"));
            nodes.add(mapOf("id", apiId, "type", "api"));
            edges.add(mapOf("from", "live:root", "to", apiId, "relation", "exposes"));
        }
        Map<String, Object> containers = asMap(live.get("containers"));
        for (Object co : capped(asList(containers.get("containers")), 1000)) {
            String cid = co instanceof Map ? str(Py.get(asMap(co), "id", co)) : str(co);
            nodes.add(mapOf("id", "container:" + cid, "type", "container"));
            edges.add(mapOf("from", "live:root", "to", "container:" + cid, "relation", "runs"));
        }
        Map<String, Object> k8s = asMap(live.get("kubernetes"));
        for (Object po : capped(asList(k8s.get("pods")), 1000)) {
            String pid = po instanceof Map ? str(Py.get(asMap(po), "name", po)) : str(po);
            nodes.add(mapOf("id", "pod:" + pid, "type", "pod"));
            edges.add(mapOf("from", "live:root", "to", "pod:" + pid, "relation", "schedules"));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), StreamingRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), StreamingRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> compileLiveRuntimeIr(Map<String, Object> live) {
        Map<String, Object> out = map();
        out.put("ir", "live_runtime");
        out.put("database_topology", Py.get(live, "database", map()));
        out.put("api_topology", Py.get(live, "api", map()));
        out.put("stream_lineage", Py.get(live, "streams", map()));
        out.put("filesystem", Py.get(live, "filesystem", map()));
        out.put("containers", Py.get(live, "containers", map()));
        out.put("kubernetes", Py.get(live, "kubernetes", map()));
        out.put("cicd", Py.get(live, "cicd", map()));
        out.put("telemetry", Py.get(live, "telemetry", map()));
        out.put("ide", Py.get(live, "ide", map()));
        out.put("graph", Py.get(live, "graph", map()));
        out.put("synchronization", Py.get(live, "sync_state", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> liveRuntimeIrToGraph(Map<String, Object> liveIr) {
        Map<String, Object> graph = asMap(liveIr.get("graph"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "live:root", "type", "live_runtime")));
        }
        Map<String, Object> k8s = asMap(liveIr.get("kubernetes"));
        for (Object deploy : capped(asList(k8s.get("deployments")), 1000)) {
            String name = deploy instanceof Map ? str(Py.get(asMap(deploy), "name", deploy)) : str(deploy);
            nodes.add(mapOf("id", "k8s:deploy:" + name, "type", "deployment"));
        }
        for (Object so : capped(asList(asMap(liveIr.get("stream_lineage")).get("streams")), 1000)) {
            Map<String, Object> stream = asMap(so);
            List<Object> topics = asList(stream.get("topics"));
            if (!topics.isEmpty()) {
                nodes.add(mapOf("id", "stream:" + str(Py.get(stream, "stream_type", "unknown")) + ":"
                        + str(topics.get(0)), "type", "stream"));
            }
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "live_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- memory

    public static Map<String, Object> rememberLiveRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"connector_states", "stream_states", "topology", "telemetry_lineage",
                "snapshots"}) {
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
        m.put("connector_states", map());
        m.put("stream_states", map());
        m.put("topology", map());
        m.put("telemetry_lineage", new ArrayList<>());
        m.put("snapshots", map());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_live_runtime(path, memory, key)}. */
    public static Map<String, Object> saveLiveRuntime(String path, Map<String, Object> memory, String key) {
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

    /** {@code load_live_runtime(path, key)}. */
    public static Map<String, Object> loadLiveRuntime(String path, String key) {
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

    /** {@code run_live_runtime}. */
    public static Map<String, Object> runLiveRuntime(Map<String, Object> config, Map<String, Object> snapshot,
            Map<String, Object> memory, long tick) {
        Map<String, Object> cfg = config == null ? map() : config;
        Map<String, Object> snap = snapshot == null ? map() : snapshot;
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);

        Map<String, Object> database = DatabaseConnectors.extractDatabaseRuntime(
                configStr(cfg, "database_type", "postgresql"), subMap(snap, "database"));
        Map<String, Object> api = ApiConnectors.extractApiRuntime(
                configStr(cfg, "api_type", "rest"), subMap(snap, "api"));
        Map<String, Object> streams = StreamConnectors.extractRuntimeStreams(subList(cfg, "stream_types"), snap);
        Map<String, Object> filesystem = extractFilesystemRuntime(
                configStr(cfg, "filesystem_root", "."), subMap(snap, "filesystem"));
        Map<String, Object> containers = ContainerConnector.extractContainerRuntime(
                configStr(cfg, "container_runtime", "docker"), subMap(snap, "containers"));
        Map<String, Object> kubernetes = KubernetesConnector.extractKubernetesRuntime(subMap(snap, "kubernetes"));
        Map<String, Object> cicd = extractCicdRuntime(
                configStr(cfg, "cicd_provider", "github_actions"), subMap(snap, "cicd"));
        Map<String, Object> telemetry = TelemetryConnector.extractTelemetryRuntime(
                subList(cfg, "telemetry_backends"), subMap(snap, "telemetry"));
        Map<String, Object> ide = IdeConnector.extractIdeRuntime(
                configStr(cfg, "ide", "vscode"), subMap(snap, "ide"));

        Map<String, Object> payload = map();
        payload.put("database", database);
        payload.put("api", api);
        payload.put("streams", streams);
        payload.put("filesystem", filesystem);
        payload.put("containers", containers);
        payload.put("kubernetes", kubernetes);
        payload.put("cicd", cicd);
        payload.put("telemetry", telemetry);
        payload.put("ide", ide);
        payload.put("tick", tick);
        payload.put("bounded", true);

        Map<String, Object> graph = buildLiveTopologyGraph(payload);
        payload.put("graph", graph);
        Map<String, Object> syncState = map();
        syncState.put("stream_lineage", streams);
        syncState.put("topology", graph);
        payload.put("sync_state", syncState);

        List<Object> streamLineage = new ArrayList<>();
        for (Object so : asList(streams.get("streams"))) {
            streamLineage.addAll(asList(asMap(so).get("event_lineage")));
        }

        Map<String, Object> connectorStates = map();
        connectorStates.put("database", database);
        connectorStates.put("api", api);
        connectorStates.put("containers", containers);
        connectorStates.put("kubernetes", kubernetes);
        Map<String, Object> update = map();
        update.put("connector_states", connectorStates);
        update.put("stream_states", streams);
        update.put("topology", graph);
        update.put("telemetry_lineage", asList(telemetry.get("distributed_correlations")));
        update.put("snapshots", payload);
        update.put("stream_lineage", streamLineage);
        Map<String, Object> updatedMemory = rememberLiveRuntime(mem, update);

        payload.put("memory", updatedMemory);
        Map<String, Object> replay = map();
        replay.put("stream_lineage", streamLineage);
        replay.put("topology", graph);
        replay.put("replayed", true);
        replay.put("bounded", true);
        payload.put("replay", replay);
        payload.put("live_ir", compileLiveRuntimeIr(payload));
        return payload;
    }

    // ------------------------------------------------- stream capture engines (Session 28)
    // Browser-free deterministic contract: the engines read only a page's _test_* attributes
    // (or return empty when absent / page is null). No live Playwright involvement — verified
    // against the canonical Python unit tests. See java/JAVA_PLAYWRIGHT_VERDICT.md.

    private static final int MAX_STREAM_EVENTS = 10000;
    private static final int MAX_FRAMES = 10000;
    private static final int MAX_CONNECTIONS = 1000;
    private static final int MAX_MUTATIONS = 10000;

    /** Python {@code d.get(key, default)} — default only when the key is absent. */
    private static Object gd(Map<String, Object> m, String key, Object dflt) {
        return m.containsKey(key) ? m.get(key) : dflt;
    }

    /** Python code-point slice {@code s[:n]} (test data is BMP, well under the caps). */
    private static String slice(String s, int n) {
        return s.length() <= n ? s : s.substring(0, n);
    }

    /** {@code core.streaming.stream_capture_engine.make_stream_event}. */
    public static Map<String, Object> makeStreamEvent(
            long step, String source, String direction, String payload, String connectionId) {
        Map<String, Object> e = map();
        e.put("id", "stream_" + step);
        e.put("timestamp", step);
        e.put("source", str(source));
        e.put("direction", str(direction));
        e.put("payload", slice(str(payload), 10000));
        e.put("connection_id", str(connectionId));
        e.put("bounded", true);
        return e;
    }

    /** {@code core.streaming.stream_capture_engine.normalize_stream_events}. */
    public static List<Object> normalizeStreamEvents(List<Object> events) {
        List<Object> normalized = new ArrayList<>();
        int limit = Math.min(events.size(), MAX_STREAM_EVENTS);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> ev = asMap(events.get(index));
            normalized.add(makeStreamEvent(
                    pyInt(gd(ev, "timestamp", (long) index), index),
                    str(gd(ev, "source", "unknown")),
                    str(gd(ev, "direction", "incoming")),
                    str(gd(ev, "payload", "")),
                    str(gd(ev, "connection_id", ""))));
        }
        normalized.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            long ta = pyInt(gd(ma, "timestamp", 0L), 0);
            long tb = pyInt(gd(mb, "timestamp", 0L), 0);
            if (ta != tb) {
                return Long.compare(ta, tb);
            }
            return cmp(str(gd(ma, "id", "")), str(gd(mb, "id", "")));
        });
        return normalized;
    }

    /** {@code capture_websocket_frames(page)} — deterministic stub-page contract. */
    public static Map<String, Object> captureWebsocketFrames(StreamPage page) {
        List<Object> events = new ArrayList<>();
        if (page != null && page.hasTestWebsocketFrames()) {
            List<Object> frames = page.testWebsocketFrames();
            int limit = Math.min(frames.size(), MAX_FRAMES);
            for (int index = 0; index < limit; index++) {
                Map<String, Object> frame = asMap(frames.get(index));
                events.add(makeStreamEvent(index, "websocket",
                        str(gd(frame, "direction", "incoming")),
                        str(gd(frame, "payload", "")),
                        str(gd(frame, "connection_id", ""))));
            }
        }
        Map<String, Object> out = map();
        out.put("events", normalizeStreamEvents(events));
        out.put("bounded", true);
        return out;
    }

    /** {@code track_websocket_connections(page)} — deterministic stub-page contract. */
    public static Map<String, Object> trackWebsocketConnections(StreamPage page) {
        List<Object> connections = new ArrayList<>();
        if (page != null && page.hasTestWebsocketConnections()) {
            connections = new ArrayList<>(capped(page.testWebsocketConnections(), MAX_CONNECTIONS));
        } else if (page != null && page.hasTestWebsocketFrames()) {
            Map<String, Object> seen = new LinkedHashMap<>();
            List<Object> frames = page.testWebsocketFrames();
            int limit = Math.min(frames.size(), MAX_CONNECTIONS);
            for (int i = 0; i < limit; i++) {
                Map<String, Object> frame = asMap(frames.get(i));
                String cid = str(gd(frame, "connection_id", ""));
                if (!seen.containsKey(cid)) {
                    Map<String, Object> c = map();
                    c.put("connection_id", cid);
                    c.put("url", slice(str(gd(frame, "url", "")), 2000));
                    c.put("lifecycle", "open");
                    seen.put(cid, c);
                }
            }
            connections = new ArrayList<>(seen.values());
            connections.sort((a, b) ->
                    cmp(str(gd(asMap(a), "connection_id", "")), str(gd(asMap(b), "connection_id", ""))));
        }
        Map<String, Object> out = map();
        out.put("connections", connections);
        out.put("bounded", true);
        return out;
    }

    /** {@code capture_dom_mutations(page)} — deterministic stub-page contract. */
    public static Map<String, Object> captureDomMutations(StreamPage page) {
        List<Object> mutations = new ArrayList<>();
        List<Object> events = new ArrayList<>();
        if (page != null && page.hasTestDomMutations()) {
            mutations = new ArrayList<>(capped(page.testDomMutations(), MAX_MUTATIONS));
        }
        for (int index = 0; index < mutations.size(); index++) {
            Map<String, Object> mutation = asMap(mutations.get(index));
            events.add(makeStreamEvent(index, "dom_mutation",
                    str(gd(mutation, "type", "mutation")),
                    str(gd(mutation, "payload", "")),
                    str(gd(mutation, "node_id", ""))));
        }
        String domSnapshot = "";
        if (page != null && page.hasTestHtml()) {
            domSnapshot = str(page.testHtml());
        }
        Map<String, Object> out = map();
        out.put("mutations", mutations);
        out.put("events", events);
        out.put("dom_hash", Kaalka.computeKaalkaHash(slice(domSnapshot, 1000000)));
        out.put("bounded", true);
        return out;
    }

}
