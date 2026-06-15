package io.webweavex.determinism;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Cross-language proof for the {@link PyRepr} / {@link PyRound} helpers: every
 * expected value is the exact output of the corresponding CPython
 * {@code repr()} / {@code round()} call, so these assert Java == Python (not
 * Java == Java).
 */
class PyHelpersS3Test {

    @Test
    void pyReprScalars() {
        assertEquals("None", PyRepr.repr(null));          // repr(None)
        assertEquals("True", PyRepr.repr(true));          // repr(True)
        assertEquals("False", PyRepr.repr(false));        // repr(False)
        assertEquals("5", PyRepr.repr(5L));               // repr(5)
        assertEquals("1.5", PyRepr.repr(1.5));            // repr(1.5)
        assertEquals("2.0", PyRepr.repr(2.0));            // repr(2.0)
        assertEquals("'a'", PyRepr.repr("a"));            // repr("a")
    }

    @Test
    void pyReprStringQuoting() {
        assertEquals("'plain'", PyRepr.repr("plain"));       // repr("plain")
        assertEquals("\"it's\"", PyRepr.repr("it's"));       // repr("it's") -> double quotes
        assertEquals("'a\"b'", PyRepr.repr("a\"b"));         // repr('a"b') -> single quotes
        assertEquals("'a\\'b\"c'", PyRepr.repr("a'b\"c"));   // both -> single, escape '
        assertEquals("'a\\\\b'", PyRepr.repr("a\\b"));       // backslash
        assertEquals("'a\\nb'", PyRepr.repr("a\nb"));        // newline
        assertEquals("'a\\tb'", PyRepr.repr("a\tb"));        // tab
        assertEquals("'\\x00'", PyRepr.repr(new String(new int[] {0x00}, 0, 1)));  // repr("\x00")
    }

    @Test
    void pyReprContainers() {
        assertEquals("[1, 2, 3]", PyRepr.repr(List.of(1L, 2L, 3L)));      // repr([1,2,3])
        assertEquals("[]", PyRepr.repr(new ArrayList<>()));               // repr([])
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("from", "a");
        m.put("to", "b");
        assertEquals("{'from': 'a', 'to': 'b'}", PyRepr.repr(m));         // repr({...}) insertion order
        Map<String, Object> mixed = new LinkedHashMap<>();
        mixed.put("n", 1L);
        mixed.put("ok", true);
        mixed.put("none", null);
        mixed.put("nested", List.of("x"));
        assertEquals("{'n': 1, 'ok': True, 'none': None, 'nested': ['x']}", PyRepr.repr(mixed));
    }

    @Test
    void pyReprStrIdentityForStrings() {
        // str("x") == "x" (no quotes), but str(dict) == repr(dict).
        assertEquals("x", PyRepr.str("x"));
        assertEquals("{'a': 1}", PyRepr.str(Map.of("a", 1L)));
    }

    @Test
    void pyRoundHalfEven() {
        assertEquals(0.2, PyRound.round(0.2, 3));          // round(0.2, 3)
        assertEquals(0.25, PyRound.round(0.25, 3));        // round(0.25, 3)
        assertEquals(2.0, PyRound.round(2.0, 4));          // round(2.0, 4)
        assertEquals(0.12, PyRound.round(0.123, 2));       // round(0.123, 2)
        assertEquals(0.12, PyRound.round(0.125, 2));       // round(0.125, 2) -> banker's -> 0.12
        assertEquals(Double.NaN, PyRound.round(Double.NaN, 2));
    }
}
