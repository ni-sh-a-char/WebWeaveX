package io.webweavex.interaction;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Port of {@code core.interaction.interaction_graph_engine.build_interaction_graph} — build a
 * deterministic interaction state graph (root → per-interaction nodes, typed edges) and embed a
 * {@code graph_hash}. Verified free of BeautifulSoup, lxml, browser, OCR, PDF, DOCX, network and
 * LLM dependencies (5-module closure; see {@code java/JAVA_SESSION_6_ANALYSIS.md}).
 *
 * <p>{@code compute_kaalka_hash_payload} is {@code compute_deterministic_hash} is
 * {@code sha256(stable_serialize(value))} — exactly {@link Kaalka#computeKaalkaHash}.
 */
public final class InteractionGraph {

    private InteractionGraph() {
    }

    private static final int MAX_GRAPH_NODES = 10000;
    private static final int MAX_GRAPH_EDGES = 50000;

    /** {@code build_interaction_graph(interactions)}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> buildInteractionGraph(List<Object> interactions) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();

        String previousId = "state_root";
        Map<String, Object> root = new LinkedHashMap<>();
        root.put("id", previousId);
        root.put("type", "state");
        root.put("name", "root");
        nodes.add(root);

        int count = interactions == null ? 0 : Math.min(interactions.size(), MAX_GRAPH_NODES);
        for (int index = 0; index < count; index++) {
            Map<String, Object> interaction = (Map<String, Object>) interactions.get(index);

            String nodeId = Py.str(Py.get(interaction, "id", "interaction_" + index));
            String action = Py.str(Py.get(interaction, "action", ""));
            String selector = Py.str(Py.get(interaction, "selector", ""));

            String nodeType = action.equals("fill") ? "form" : "page";
            String selLower = selector.toLowerCase(Locale.ROOT);
            if (selLower.contains("modal")) {
                nodeType = "modal";
            }
            if (selLower.contains("tab")) {
                nodeType = "tab";
            }

            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", nodeId);
            node.put("type", nodeType);
            node.put("action", action);
            node.put("selector", selector);
            nodes.add(node);

            String relation = action.isEmpty() ? "transition" : action;
            if (action.equals("click")) {
                relation = "click";
            } else if (action.equals("fill") || action.equals("select")) {
                relation = "submission";
            } else if (action.equals("wait")) {
                relation = "navigation";
            }

            Map<String, Object> edge = new LinkedHashMap<>();
            edge.put("from", previousId);
            edge.put("to", nodeId);
            edge.put("relation", relation);
            edges.add(edge);

            previousId = nodeId;
        }

        List<Object> nodesSliced = slice(nodes, MAX_GRAPH_NODES);
        List<Object> edgesSliced = slice(edges, MAX_GRAPH_EDGES);

        Map<String, Object> payload = new LinkedHashMap<>();
        payload.put("nodes", nodesSliced);
        payload.put("edges", edgesSliced);

        Map<String, Object> graph = new LinkedHashMap<>();
        graph.put("ir", "interaction_graph");
        graph.put("nodes", nodesSliced);
        graph.put("edges", edgesSliced);
        graph.put("graph_hash", Kaalka.computeKaalkaHash(payload));
        graph.put("bounded", true);
        return graph;
    }

    private static List<Object> slice(List<Object> xs, int n) {
        return new ArrayList<>(xs.subList(0, Math.min(n, xs.size())));
    }
}
