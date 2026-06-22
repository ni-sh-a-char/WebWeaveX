package io.webweavex.repository;

import io.webweavex.determinism.Py;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.agents.repository_query_engine.query_repository}. Dependency-clean
 * (0 forbidden, importable). Pure accessor: {@code result['content']['repository']}, optionally a
 * single key within it. Zero new substrate.
 */
public final class RepositoryQuery {

    private RepositoryQuery() {
    }

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    /** {@code query_repository(result, key='')}. */
    public static Object queryRepository(Map<String, Object> result, String key) {
        Map<String, Object> res = result == null ? map() : result;
        Map<String, Object> repo = asMap(Py.get(asMap(Py.get(res, "content", map())), "repository", map()));
        if (key == null || key.isEmpty()) {
            return repo;
        }
        return repo.get(key);
    }
}
