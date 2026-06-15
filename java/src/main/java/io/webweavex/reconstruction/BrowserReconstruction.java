package io.webweavex.reconstruction;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Port of {@code core.reconstruction.browser_reconstruction_engine.reconstruct_browser_runtime}. */
public final class BrowserReconstruction {

    private BrowserReconstruction() {
    }

    public static Map<String, Object> reconstructBrowserRuntime(
            Map<String, Object> browserIr, Map<String, Object> interactionIr,
            Map<String, Object> identity, Map<String, Object> session,
            Map<String, Object> streaming, Map<String, Object> dom) {
        Map<String, Object> bIr = orEmpty(browserIr);
        Map<String, Object> iIr = orEmpty(interactionIr);
        Map<String, Object> id = orEmpty(identity);
        Map<String, Object> sess = orEmpty(session);
        Map<String, Object> stream = orEmpty(streaming);
        Map<String, Object> domMap = orEmpty(dom);

        // tab source: interaction.tab_states.tabs OR browser.routes.history OR [{path: url}]
        List<Object> tabSource = firstTruthy(
                nestedList(iIr, "tab_states", "tabs"),
                nestedList(bIr, "routes", "history"),
                List.of(mapOf("path", Py.get(bIr, "url", "/"))));
        List<Object> tabs = new ArrayList<>();
        for (int i = 0; i < tabSource.size(); i++) {
            tabs.add(mapOf2("id", "tab:" + i, "path", Py.str(Py.get(tabSource.get(i), "path", ""))));
        }
        tabs.sort(Comparator.comparing(t -> (String) ((Map<?, ?>) t).get("id"),
                Normalization::codePointCompare));

        // navigation source: interaction.route_transitions.routes OR browser.navigation.history OR []
        List<Object> navSource = firstTruthy(
                nestedList(iIr, "route_transitions", "routes"),
                nestedList(bIr, "navigation", "history"),
                new ArrayList<>());
        List<Object> navigation = new ArrayList<>();
        for (int i = 0; i < navSource.size(); i++) {
            Object item = navSource.get(i);
            long order = toLong(Py.get(item, "order", (long) i));
            navigation.add(mapOf2("path", Py.str(Py.get(item, "path", "")), "order", order));
        }
        navigation.sort(Comparator.comparingLong(n -> (long) ((Map<?, ?>) n).get("order")));

        List<Object> interactions = listOf(Py.get(iIr, "interactions", new ArrayList<>()));
        List<Object> flows = new ArrayList<>(interactions.subList(0, Math.min(1000, interactions.size())));

        List<Object> cookies = new ArrayList<>(listOf(Py.get(sess, "cookies", new ArrayList<>())));
        cookies.sort(Comparator.comparing(c -> Py.str(Py.get(c, "name", "")),
                Normalization::codePointCompare));

        Map<String, Object> authState = new LinkedHashMap<>();
        authState.put("authenticated", Py.truthy(Py.get(sess, "authenticated", false)));
        authState.put("cookies", cookies);

        Map<String, Object> storage = new LinkedHashMap<>();
        storage.put("local", new LinkedHashMap<>(asMap(Py.get(sess, "local_storage", new LinkedHashMap<>()))));
        storage.put("session", new LinkedHashMap<>(asMap(Py.get(sess, "session_storage", new LinkedHashMap<>()))));

        Object domStructure = Py.get(domMap, "structure", Py.get(domMap, "nodes", new LinkedHashMap<>()));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("tabs", tabs);
        out.put("navigation_history", navigation);
        out.put("dom_structure", new LinkedHashMap<>(asMap(domStructure)));
        out.put("interaction_flows", flows);
        out.put("browser_identity", new LinkedHashMap<>(id));
        out.put("authenticated_state", authState);
        out.put("storage", storage);
        out.put("streaming_state", new LinkedHashMap<>(stream));
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    private static List<Object> nestedList(Map<String, Object> root, String k1, String k2) {
        return listOf(Py.get(asMap(Py.get(root, k1, new LinkedHashMap<>())), k2, new ArrayList<>()));
    }

    @SafeVarargs
    private static List<Object> firstTruthy(List<Object>... options) {
        for (List<Object> o : options) {
            if (Py.truthy(o)) {
                return o;
            }
        }
        return options[options.length - 1];
    }

    private static Map<String, Object> mapOf(String k, Object v) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put(k, v);
        return m;
    }

    private static Map<String, Object> mapOf2(String k1, Object v1, String k2, Object v2) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put(k1, v1);
        m.put(k2, v2);
        return m;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : new LinkedHashMap<>();
    }

    private static Map<String, Object> orEmpty(Map<String, Object> m) {
        return m == null ? new LinkedHashMap<>() : m;
    }

    private static List<Object> listOf(Object o) {
        List<Object> l = Py.asList(o);
        return l == null ? new ArrayList<>() : l;
    }

    private static long toLong(Object o) {
        return o instanceof Number ? ((Number) o).longValue() : 0L;
    }
}
