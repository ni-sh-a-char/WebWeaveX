package io.webweavex.connectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Unit coverage for the {@link Connectors} Python-semantics helpers — the
 * reachable coercion/copy/sort/slice branches that the cross-language vectors do
 * not all exercise directly. These assert CPython-faithful behaviour, not parity
 * hashes.
 */
class ConnectorsUnitTest {

    @Test
    void pyIntCoercesTowardZero() {
        assertEquals(5L, Connectors.pyInt(5L));
        assertEquals(5L, Connectors.pyInt(Integer.valueOf(5)));
        assertEquals(2L, Connectors.pyInt(2.9));
        assertEquals(-2L, Connectors.pyInt(-2.9));
        assertEquals(1L, Connectors.pyInt(Boolean.TRUE));
        assertEquals(0L, Connectors.pyInt(Boolean.FALSE));
        assertEquals(7L, Connectors.pyInt(" 7 "));
        assertEquals(0L, Connectors.pyInt(new Object()));
    }

    @Test
    void getListDefaultsOnAbsentAndNonList() {
        Map<String, Object> s = new LinkedHashMap<>();
        s.put("nonlist", "scalar");
        List<Object> dflt = Connectors.list("d");
        assertEquals(dflt, Connectors.getList(s, "missing", dflt));   // absent -> default copy
        assertEquals(dflt, Connectors.getList(s, "nonlist", dflt));   // present non-list -> default copy
        List<Object> present = Connectors.list("a", "b");
        s.put("xs", present);
        List<Object> copy = Connectors.getList(s, "xs", dflt);
        assertEquals(present, copy);
        assertTrue(copy != present);                                  // is a copy
    }

    @Test
    void getMapDefaultsToEmptyOnAbsentAndNonMap() {
        Map<String, Object> s = new LinkedHashMap<>();
        s.put("nonmap", 1L);
        assertTrue(Connectors.getMap(s, "missing").isEmpty());
        assertTrue(Connectors.getMap(s, "nonmap").isEmpty());
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("k", "v");
        s.put("m", m);
        Map<String, Object> copy = Connectors.getMap(s, "m");
        assertEquals(m, copy);
        assertTrue(copy != m);
    }

    @Test
    void orDefaultTreatsNullAndEmptyAsFalsy() {
        List<Object> dflt = Connectors.list("x");
        assertEquals(dflt, Connectors.orDefault(null, dflt));
        assertEquals(dflt, Connectors.orDefault(new ArrayList<>(), dflt));
        List<Object> nonEmpty = Connectors.list("y");
        assertEquals(nonEmpty, Connectors.orDefault(nonEmpty, dflt));
    }

    @Test
    void sliceAndSortByStrAndSnap() {
        assertEquals(Connectors.list("a", "b"),
                Connectors.slice(Connectors.list("a", "b", "c"), 2));
        assertEquals(Connectors.list("a", "b"),
                Connectors.slice(Connectors.list("a", "b"), 10));   // n > size
        // code-point order: uppercase 'M' (77) sorts before lowercase 'a' (97)
        assertEquals(Connectors.list("Mu", "alpha", "zeta"),
                Connectors.sortedByStr(Connectors.list("zeta", "alpha", "Mu")));
        assertTrue(Connectors.snap(null).isEmpty());
    }

    @Test
    void streamDegradedFallbackOnSubEngineFailure() {
        // A snapshot whose "kafka" value is a non-map, non-null shape that makes the
        // sub-engine path raise is coerced to null by Py.asMap, so exercise the
        // generic unknown/degraded structure via an empty-but-present stream list.
        Map<String, Object> out = StreamConnectors.extractRuntimeStreams(
                Connectors.list("queue"), null);
        @SuppressWarnings("unchecked")
        List<Object> streams = (List<Object>) out.get("streams");
        assertEquals(1L, out.get("count"));
        @SuppressWarnings("unchecked")
        Map<String, Object> entry = (Map<String, Object>) streams.get(0);
        assertEquals("queue", entry.get("stream_type"));
        assertTrue(((List<?>) entry.get("topics")).isEmpty());
    }
}
