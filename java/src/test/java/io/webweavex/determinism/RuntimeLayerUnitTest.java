package io.webweavex.determinism;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.webweavex.ir.UnifiedRuntimeIr;
import io.webweavex.persistence.FingerprintHex;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** Direct coverage for the session-2 runtime layer branches not hit by golden vectors. */
class RuntimeLayerUnitTest {

    @Test
    void pyJsonSeparatorVariants() {
        List<Object> list = List.of(1L, 2L);
        assertEquals("[1,2]", PyJson.dumpsCompactUnicode(list));
        assertEquals("[1, 2]", PyJson.dumpsDefaultAscii(list));

        Map<String, Object> m = new LinkedHashMap<>();
        m.put("b", 1L);
        m.put("a", 2L);
        assertEquals("{\"a\":2,\"b\":1}", PyJson.dumpsCompactUnicode(m));
        assertEquals("{\"a\": 2, \"b\": 1}", PyJson.dumpsDefaultAscii(m));
    }

    @Test
    void pyJsonEnsureAsciiEscaping() {
        // ensure_ascii=True escapes non-ASCII; BMP -> one \\u, astral -> surrogate pair.
        assertEquals("\"\\u00e9\"", PyJson.dumpsCompactAscii("é"));
        assertEquals("\"\\ud83d\\ude00\"", PyJson.dumpsCompactAscii("😀"));
        // ensure_ascii=False emits raw.
        assertEquals("\"é\"", PyJson.dumpsCompactUnicode("é"));
    }

    @Test
    void pyJsonFloatForms() {
        assertEquals("2.0", PyJson.dumpsCompactUnicode(2.0));
        assertEquals("3.14", PyJson.dumpsCompactUnicode(3.14));
        assertEquals("NaN", PyJson.dumpsCompactUnicode(Double.NaN));
        assertEquals("Infinity", PyJson.dumpsCompactUnicode(Double.POSITIVE_INFINITY));
        assertEquals("-Infinity", PyJson.dumpsCompactUnicode(Double.NEGATIVE_INFINITY));
        assertEquals("null", PyJson.dumpsCompactUnicode(null));
        assertEquals("true", PyJson.dumpsCompactUnicode(true));
    }

    @Test
    void pyHelpers() {
        assertEquals("None", Py.str(null));
        assertEquals("True", Py.str(true));
        assertEquals("False", Py.str(false));
        assertEquals("5", Py.str(5L));

        assertFalse(Py.truthy(null));
        assertFalse(Py.truthy(""));
        assertFalse(Py.truthy(false));
        assertFalse(Py.truthy(0));
        assertFalse(Py.truthy(Map.of()));
        assertFalse(Py.truthy(List.of()));
        assertTrue(Py.truthy("x"));
        assertTrue(Py.truthy(1));
        assertTrue(Py.truthy(List.of(1)));

        assertEquals("dflt", Py.get(null, "k", "dflt"));
        assertEquals("dflt", Py.get(Map.of(), "k", "dflt"));
        assertEquals(1, Py.get(Map.of("k", 1), "k", "dflt"));
    }

    @Test
    void fingerprintBytesEqualsStringPayload() {
        // bytes payload decodes to the same text -> identical fingerprint.
        byte[] bytes = "abc".getBytes(StandardCharsets.UTF_8);
        assertEquals(FingerprintHex.hexFingerprint("abc", "webweavex"),
                FingerprintHex.hexFingerprint(bytes, "webweavex"));
    }

    @Test
    void fingerprintDictEqualsDumpsDeterministic() {
        // hex_fingerprint(payload) == hex_fingerprint(dumps_deterministic(payload)).
        Map<String, Object> payload = new LinkedHashMap<>();
        payload.put("x", 0.1);
        String dd = FingerprintHex.dumpsDeterministic(payload);
        assertEquals("{\"x\":0.1}", dd);
        assertEquals(FingerprintHex.hexFingerprint(dd, "t"),
                FingerprintHex.hexFingerprint(payload, "t"));
    }

    @Test
    void dumpsDeterministicSortsListsAndCanonicalizesIntegralFloats() {
        assertEquals("[1,2,3]", FingerprintHex.dumpsDeterministic(List.of(3L, 1L, 2L)));
        // integral float collapses to int; nested map keys sort.
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("z", 2.0);
        m.put("a", "v");
        assertEquals("{\"a\":\"v\",\"z\":2}", FingerprintHex.dumpsDeterministic(m));
    }

    @Test
    void unifiedIrWrapsNonDictPhasePayload() {
        // A non-dict phase value is wrapped as {"payload": value}.
        Map<String, Object> phases = new LinkedHashMap<>();
        phases.put("browser", "scalar");
        Map<String, Object> registry = new LinkedHashMap<>();
        registry.put("phases", phases);
        Map<String, Object> ir = UnifiedRuntimeIr.compile(registry, null, null, null, null);
        assertEquals(Map.of("payload", "scalar"), ir.get("browser"));
    }

    @Test
    void unifiedIrToGraphEmptyHasRootOnly() {
        Map<String, Object> ir = UnifiedRuntimeIr.compile(null, null, null, null, null);
        Map<String, Object> g = UnifiedRuntimeIr.toGraph(ir);
        List<?> nodes = (List<?>) g.get("nodes");
        assertEquals(1, nodes.size());
        assertEquals("unified_runtime_graph", g.get("ir"));
    }

    @Test
    void emptyContainersSerializeStably() {
        assertEquals("[]", PyJson.dumpsCompactUnicode(new ArrayList<>()));
        assertEquals("{}", PyJson.dumpsCompactUnicode(new LinkedHashMap<>()));
    }
}
