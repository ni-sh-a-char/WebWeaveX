package io.webweavex.graph;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.List;

/** Shared graph-access helpers mirroring Python {@code graph.get(key, []) or []}. */
final class GraphUtil {

    private GraphUtil() {
    }

    /** {@code dict.get(key, []) or []} — list value or empty. */
    static List<Object> list(Object container, String key) {
        List<Object> l = Py.asList(Py.get(container, key, null));
        return l == null ? new ArrayList<>() : l;
    }
}
