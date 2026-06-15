package io.webweavex.determinism;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** Direct unit coverage for determinism branches not exercised by golden vectors. */
class DeterminismUnitTest {

    @Test
    void pyFloatReprNonFinite() {
        assertEquals("nan", PyFloat.pyFloatRepr(Double.NaN));
        assertEquals("inf", PyFloat.pyFloatRepr(Double.POSITIVE_INFINITY));
        assertEquals("-inf", PyFloat.pyFloatRepr(Double.NEGATIVE_INFINITY));
    }

    @Test
    void pyFloatReprIntegralAndSigns() {
        // Direct integral path (canonicalization collapses these before the
        // encoder, but pyFloatRepr must still match Python repr()).
        assertEquals("100.0", PyFloat.pyFloatRepr(100.0));
        assertEquals("-3.0", PyFloat.pyFloatRepr(-3.0));
        assertEquals("-0.0", PyFloat.pyFloatRepr(-0.0));
        assertEquals("0.0", PyFloat.pyFloatRepr(0.0));
    }

    @Test
    void pyFloatReprScientificThresholds() {
        assertEquals("1e+16", PyFloat.pyFloatRepr(1e16));
        assertEquals("1e-05", PyFloat.pyFloatRepr(1e-5));
        assertEquals("0.0001", PyFloat.pyFloatRepr(1e-4));
        assertEquals("1.5e+20", PyFloat.pyFloatRepr(1.5e20));
        assertEquals("-2.5e-10", PyFloat.pyFloatRepr(-2.5e-10));
    }

    @Test
    void codePointCompareOrdersByCodePoint() {
        // Astral character sorts AFTER all BMP characters by code point.
        assertTrue(Normalization.codePointCompare("a", "é") < 0);
        assertTrue(Normalization.codePointCompare("é", "😀") < 0);
        assertTrue(Normalization.codePointCompare("ab", "a") > 0);
        assertEquals(0, Normalization.codePointCompare("same", "same"));
    }

    @Test
    void canonicalizeNumberRules() {
        assertEquals(2L, Normalization.canonicalizeNumber(2.0));
        assertEquals(2L, Normalization.canonicalizeNumber(2.0f));
        assertEquals(0.5, Normalization.canonicalizeNumber(0.5));
        assertEquals(null, Normalization.canonicalizeNumber(Double.NaN));
        assertEquals(null, Normalization.canonicalizeNumber(Double.POSITIVE_INFINITY));
        assertEquals(7L, Normalization.canonicalizeNumber(7L));
        assertEquals("x", Normalization.canonicalizeNumber("x"));
    }

    @Test
    void normalizeRuntimeValueOrder() {
        // NFKC fold, CRLF -> LF, trailing whitespace strip across the full set.
        assertEquals("fi", Normalization.normalizeRuntimeValue("ﬁ"));
        assertEquals("a\nb", Normalization.normalizeRuntimeValue("a\r\nb"));
        assertEquals("keep", Normalization.normalizeRuntimeValue("keep  \t  "));
    }

    @Test
    void stableSerializeNestedAndVolatile() {
        Map<String, Object> inner = new LinkedHashMap<>();
        inner.put("nonce", "drop");
        inner.put("z", 1);
        inner.put("a", 2.0);
        Map<String, Object> outer = new LinkedHashMap<>();
        outer.put("timestamp", 999);
        outer.put("nested", inner);
        assertEquals("{\"nested\":{\"a\":2,\"z\":1}}", StableSerialize.stableSerialize(outer));
    }

    @Test
    void stableSerializeListOfMixed() {
        List<Object> list = new ArrayList<>();
        list.add(Map.of("b", 1, "a", 2));
        list.add(2.0);
        list.add("s");
        assertEquals("{\"0\":{\"a\":2,\"b\":1},\"1\":2,\"2\":\"s\"}",
                StableSerialize.stableSerialize(list));
    }

    @Test
    void nonStringMapKeysAreStringified() {
        // Mirrors Python/Dart str(key) coercion; exercises the key-lookup
        // fallback in both stableSortKeys and the encoder.
        Map<Object, Object> m = new LinkedHashMap<>();
        m.put(10, "ten");
        m.put(2, "two");
        assertEquals("{\"10\":\"ten\",\"2\":\"two\"}", StableSerialize.stableSerialize(m));
        assertEquals("{\"10\":\"ten\",\"2\":\"two\"}", CanonicalJson.canonicalJsonEncode(m));
    }

    @Test
    void unknownObjectFallsBackToStringEncoding() {
        Object opaque = new Object() {
            @Override
            public String toString() {
                return "opaque-value";
            }
        };
        assertEquals("\"opaque-value\"", CanonicalJson.canonicalJsonEncode(opaque));
    }

    @Test
    void topLevelListEncodesAsJsonArray() {
        // canonicalJsonEncode keeps a raw List as a JSON array (the keyed-object
        // rewrite happens only in stableSerialize).
        assertEquals("[1,2,3]", CanonicalJson.canonicalJsonEncode(List.of(1, 2, 3)));
    }

    @Test
    void canonicalJsonControlCharEscaping() {
        // Control chars below 0x20 -> lowercase \\uXXXX; 0x7f (DEL) stays raw.
        String controls = new String(new int[] {0x01, 0x1F}, 0, 2);
        assertEquals("\"\\u0001\\u001f\"", CanonicalJson.canonicalJsonEncode(controls));
        assertEquals("\"a\\nb\\tc\"", CanonicalJson.canonicalJsonEncode("a\nb\tc"));

        String del = new String(new int[] {0x7F}, 0, 1);
        assertEquals("\"" + del + "\"", CanonicalJson.canonicalJsonEncode(del));
    }
}
