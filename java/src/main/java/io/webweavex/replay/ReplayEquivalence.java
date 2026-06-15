package io.webweavex.replay;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.GlobalRuntimeFingerprint;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.graph.RuntimeGraph;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Port of {@code core.replay.replay_equivalence_engine.validate_replay_equivalence}
 * — verifies a replayed extraction restored equivalent runtime graphs,
 * fingerprints, and browser identity. Output is byte-identical to Python under
 * {@code compute_deterministic_hash}.
 */
public final class ReplayEquivalence {

    private ReplayEquivalence() {
    }

    public static Map<String, Object> validate(
            Map<String, Object> original, Map<String, Object> replayed) {

        Map<String, Object> origGraph = graphOf(original);
        Map<String, Object> replayGraph = graphOf(replayed);

        String origFp = GlobalRuntimeFingerprint.compute(
                original, origGraph, null, null, null, "");
        String replayFp = GlobalRuntimeFingerprint.compute(
                replayed, replayGraph, null, null, null, "");

        String ghOrig = graphHash(origGraph);
        String ghReplay = graphHash(replayGraph);

        List<Object> checks = new ArrayList<>();
        checks.add(check("graph_hash", ghOrig.equals(ghReplay),
                ghOrig.substring(0, 16), ghReplay.substring(0, 16)));
        checks.add(check("global_fingerprint", origFp.equals(replayFp),
                origFp.substring(0, 16), replayFp.substring(0, 16)));

        Map<String, Object> identityCheck = new LinkedHashMap<>();
        identityCheck.put("name", "browser_identity");
        identityCheck.put("ok", Objects.equals(
                identity(original), identity(replayed)));
        checks.add(identityCheck);

        boolean equivalent = true;
        for (Object c : checks) {
            if (!Boolean.TRUE.equals(((Map<?, ?>) c).get("ok"))) {
                equivalent = false;
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("equivalent", equivalent);
        out.put("checks", checks);
        out.put("bounded", true);
        return out;
    }

    /** Port of {@code _graph_hash}: contract-normalize then hash the spaced-JSON of nodes/edges. */
    public static String graphHash(Map<String, Object> graph) {
        Map<String, Object> normalized = RuntimeGraph.normalizeContract(graph);
        Map<String, Object> payload = new LinkedHashMap<>();
        payload.put("nodes", Py.get(normalized, "nodes", new ArrayList<>()));
        payload.put("edges", Py.get(normalized, "edges", new ArrayList<>()));
        return Kaalka.computeKaalkaHash(PyJson.dumpsDefaultAscii(payload));
    }

    private static Map<String, Object> graphOf(Map<String, Object> envelope) {
        Object g = Py.get(envelope, "unified_runtime_graph", Py.get(envelope, "graph", Map.of()));
        Map<String, Object> m = Py.asMap(g);
        return m == null ? new LinkedHashMap<>() : m;
    }

    private static Object identity(Map<String, Object> envelope) {
        Object browserIr = Py.get(envelope, "browser_ir", Map.of());
        return Py.get(browserIr, "runtime_identity", null);
    }

    private static Map<String, Object> check(String name, boolean ok, String orig, String replay) {
        Map<String, Object> c = new LinkedHashMap<>();
        c.put("name", name);
        c.put("ok", ok);
        c.put("original", orig);
        c.put("replay", replay);
        return c;
    }
}
