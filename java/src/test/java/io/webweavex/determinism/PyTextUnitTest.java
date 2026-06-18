package io.webweavex.determinism;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * Unit coverage for {@link PyText} - asserts CPython {@code str.splitlines()} /
 * {@code str.strip()} / {@code str.lstrip()} semantics against concrete expected
 * values (not self-consistency). Covers the full line-boundary and whitespace sets.
 *
 * <p>Strings carrying control / exotic-whitespace code points are built with
 * {@link #cp} so the source stays pure ASCII and unambiguous.
 */
class PyTextUnitTest {

    /** Build a string from literal fragments and integer code points. */
    private static String cp(Object... parts) {
        StringBuilder sb = new StringBuilder();
        for (Object p : parts) {
            if (p instanceof Integer) {
                sb.appendCodePoint((Integer) p);
            } else {
                sb.append((String) p);
            }
        }
        return sb.toString();
    }

    @Test
    void splitlinesBoundarySet() {
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x0A, "b"))); // LF
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x0B, "b"))); // VT
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x0C, "b"))); // FF
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x0D, "b"))); // CR
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x1C, "b"))); // FS
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x1D, "b"))); // GS
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x1E, "b"))); // RS
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x85, "b"))); // NEL
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x2028, "b"))); // LS
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x2029, "b"))); // PS
        assertEquals(List.of("a", "b"), PyText.splitlines(cp("a", 0x0D, 0x0A, "b"))); // CRLF=1
    }

    @Test
    void splitlinesNoTrailingEmpty() {
        assertEquals(List.of("a"), PyText.splitlines(cp("a", 0x0A)));
        assertEquals(List.of(), PyText.splitlines(""));
        assertEquals(List.of("abc"), PyText.splitlines("abc"));
        assertEquals(List.of("", "x"), PyText.splitlines(cp(0x0A, "x")));
    }

    @Test
    void stripWhitespaceSet() {
        assertEquals("x", PyText.strip("  x  "));
        assertEquals("x", PyText.strip(cp(0x09, "x", 0x0A)));
        assertEquals("x", PyText.strip(cp(0xA0, "x", 0xA0)));   // NBSP - JDK strip would keep
        assertEquals("x", PyText.strip(cp(0x3000, "x", 0x3000))); // ideographic space
        assertEquals("x", PyText.strip(cp(0x202F, "x", 0x205F))); // narrow-NBSP / med-math
        assertEquals("x", PyText.strip(cp(0x1680, "x", 0x2000))); // ogham / en-quad
        assertEquals("", PyText.strip("   "));
        assertEquals("mid x", PyText.strip("mid x"));
    }

    @Test
    void lstripChars() {
        assertEquals("foo", PyText.lstrip("###foo", "#"));
        assertEquals("foo", PyText.lstrip("foo", "#"));
        assertEquals("", PyText.lstrip("###", "#"));
        assertEquals(" Title ##", PyText.lstrip("## Title ##", "#"));
    }

    @Test
    void isPyWhitespacePredicate() {
        for (int c : new int[] {0x09, 0x0A, 0x0D, 0x1C, 0x1F, 0x20, 0x85, 0xA0,
                0x1680, 0x2000, 0x200A, 0x2028, 0x2029, 0x202F, 0x205F, 0x3000}) {
            assertTrue(PyText.isPyWhitespace(c), "ws U+" + Integer.toHexString(c));
        }
        assertFalse(PyText.isPyWhitespace('a'));
        assertFalse(PyText.isPyWhitespace(0x200B)); // zero-width space not Python ws
        assertFalse(PyText.isPyWhitespace(0x2060));
    }
}
