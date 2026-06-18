package io.webweavex.determinism;

import java.util.ArrayList;
import java.util.List;

/**
 * Faithful CPython {@code str} text operations needed by the extraction layer so
 * ported parsing stays byte-exact: {@code str.splitlines()}, {@code str.strip()},
 * and {@code str.lstrip(chars)}.
 *
 * <p>These differ from the JDK defaults: {@link String#lines} omits the line-boundary
 * set CPython uses (it splits only on {@code \n}/{@code \r}/{@code \r\n}), and
 * {@link String#strip} uses {@link Character#isWhitespace} which excludes
 * {@code U+00A0}/{@code U+2007}/{@code U+202F} that CPython's whitespace set includes.
 */
public final class PyText {

    private PyText() {
    }

    /** True for the code-point set CPython {@code str.isspace()} / regex {@code \s} treats as
     * whitespace (used by {@code str.strip()} with no argument). */
    public static boolean isPyWhitespace(int cp) {
        return (cp >= 0x09 && cp <= 0x0D)     // \t \n \v \f \r
                || (cp >= 0x1C && cp <= 0x1F) // FS GS RS US
                || cp == 0x20
                || cp == 0x85
                || cp == 0xA0
                || cp == 0x1680
                || (cp >= 0x2000 && cp <= 0x200A)
                || cp == 0x2028
                || cp == 0x2029
                || cp == 0x202F
                || cp == 0x205F
                || cp == 0x3000;
    }

    /** True for the code points CPython {@code str.splitlines()} treats as line boundaries
     * (a strict subset of the whitespace set — e.g. {@code \t} and {@code space} are NOT
     * boundaries; {@code \v}/{@code \f}/{@code U+0085}/{@code U+2028}/{@code U+2029} are). */
    private static boolean isLineBoundary(int cp) {
        return cp == 0x0A || cp == 0x0B || cp == 0x0C || cp == 0x0D
                || cp == 0x1C || cp == 0x1D || cp == 0x1E
                || cp == 0x85 || cp == 0x2028 || cp == 0x2029;
    }

    /** CPython {@code text.splitlines()} — no {@code keepends}; no trailing empty element when
     * the text ends with a boundary; {@code \r\n} counts as a single boundary. */
    public static List<String> splitlines(String text) {
        List<String> out = new ArrayList<>();
        int n = text.length();
        int start = 0;
        int i = 0;
        while (i < n) {
            char c = text.charAt(i); // every boundary code point is in the BMP
            if (isLineBoundary(c)) {
                out.add(text.substring(start, i));
                if (c == '\r' && i + 1 < n && text.charAt(i + 1) == '\n') {
                    i += 1; // consume the \n of a \r\n pair
                }
                i += 1;
                start = i;
            } else {
                i += 1;
            }
        }
        if (start < n) {
            out.add(text.substring(start));
        }
        return out;
    }

    /** CPython {@code str.strip()} (no argument) — strip leading/trailing whitespace. */
    public static String strip(String s) {
        int start = 0;
        int end = s.length();
        while (start < end) {
            int cp = s.codePointAt(start);
            if (!isPyWhitespace(cp)) {
                break;
            }
            start += Character.charCount(cp);
        }
        while (end > start) {
            int cp = s.codePointBefore(end);
            if (!isPyWhitespace(cp)) {
                break;
            }
            end -= Character.charCount(cp);
        }
        return s.substring(start, end);
    }

    /** CPython {@code s.lstrip(chars)} — strip any leading code point contained in {@code chars}. */
    public static String lstrip(String s, String chars) {
        int start = 0;
        int n = s.length();
        while (start < n) {
            int cp = s.codePointAt(start);
            if (chars.indexOf(cp) < 0) {
                break;
            }
            start += Character.charCount(cp);
        }
        return s.substring(start);
    }
}
