package io.webweavex.determinism;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * JDK-only {@code json.loads} — parses a JSON document into the native value tree used by the
 * runtime layers ({@code LinkedHashMap}/{@code List}/{@code String}/{@code Long}/{@code BigInteger}/
 * {@code Double}/{@code Boolean}/{@code null}), matching CPython {@code json.loads} semantics:
 *
 * <ul>
 *   <li>objects preserve insertion order (LinkedHashMap);</li>
 *   <li>integer literals (no {@code .}/{@code e}/{@code E}) become {@code Long}, or
 *       {@code BigInteger} on overflow — CPython {@code int} is unbounded;</li>
 *   <li>everything else numeric becomes {@code Double};</li>
 *   <li>{@code NaN}/{@code Infinity}/{@code -Infinity} are accepted (CPython default);</li>
 *   <li>{@code \\uXXXX} escapes (incl. surrogate pairs) and standard string escapes.</li>
 * </ul>
 *
 * <p>This is the inverse of {@link PyJson}; it is the substrate every {@code decrypt_*}/
 * {@code load_*} round-trip API needs.
 */
public final class PyJsonParse {

    private PyJsonParse() {
    }

    /** {@code json.loads(text)}. */
    public static Object loads(String text) {
        Parser p = new Parser(text);
        p.skipWs();
        Object v = p.parseValue();
        p.skipWs();
        if (!p.atEnd()) {
            throw new IllegalArgumentException("Extra data at position " + p.pos);
        }
        return v;
    }

    private static final class Parser {
        private final String s;
        private int pos;

        Parser(String s) {
            this.s = s;
        }

        boolean atEnd() {
            return pos >= s.length();
        }

        void skipWs() {
            while (pos < s.length()) {
                char c = s.charAt(pos);
                if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                    pos++;
                } else {
                    break;
                }
            }
        }

        private IllegalArgumentException err(String msg) {
            return new IllegalArgumentException(msg + " at position " + pos);
        }

        Object parseValue() {
            if (atEnd()) {
                throw err("Expecting value");
            }
            char c = s.charAt(pos);
            switch (c) {
                case '{':
                    return parseObject();
                case '[':
                    return parseArray();
                case '"':
                    return parseString();
                case 't':
                    return parseLiteral("true", Boolean.TRUE);
                case 'f':
                    return parseLiteral("false", Boolean.FALSE);
                case 'n':
                    return parseLiteral("null", null);
                case 'N':
                    return parseLiteral("NaN", Double.NaN);
                case 'I':
                    return parseLiteral("Infinity", Double.POSITIVE_INFINITY);
                default:
                    if (c == '-' || (c >= '0' && c <= '9')) {
                        return parseNumber();
                    }
                    throw err("Expecting value");
            }
        }

        private Object parseLiteral(String word, Object value) {
            if (s.regionMatches(pos, word, 0, word.length())) {
                pos += word.length();
                return value;
            }
            throw err("Expecting value");
        }

        private Map<String, Object> parseObject() {
            Map<String, Object> map = new LinkedHashMap<>();
            pos++; // {
            skipWs();
            if (!atEnd() && s.charAt(pos) == '}') {
                pos++;
                return map;
            }
            while (true) {
                skipWs();
                if (atEnd() || s.charAt(pos) != '"') {
                    throw err("Expecting property name enclosed in double quotes");
                }
                String key = parseString();
                skipWs();
                if (atEnd() || s.charAt(pos) != ':') {
                    throw err("Expecting ':' delimiter");
                }
                pos++; // :
                skipWs();
                map.put(key, parseValue());
                skipWs();
                if (atEnd()) {
                    throw err("Expecting ',' delimiter");
                }
                char c = s.charAt(pos++);
                if (c == '}') {
                    return map;
                }
                if (c != ',') {
                    throw err("Expecting ',' delimiter");
                }
            }
        }

        private List<Object> parseArray() {
            List<Object> list = new ArrayList<>();
            pos++; // [
            skipWs();
            if (!atEnd() && s.charAt(pos) == ']') {
                pos++;
                return list;
            }
            while (true) {
                skipWs();
                list.add(parseValue());
                skipWs();
                if (atEnd()) {
                    throw err("Expecting ',' delimiter");
                }
                char c = s.charAt(pos++);
                if (c == ']') {
                    return list;
                }
                if (c != ',') {
                    throw err("Expecting ',' delimiter");
                }
            }
        }

        private String parseString() {
            StringBuilder sb = new StringBuilder();
            pos++; // opening "
            while (true) {
                if (atEnd()) {
                    throw err("Unterminated string");
                }
                char c = s.charAt(pos++);
                if (c == '"') {
                    return sb.toString();
                }
                if (c == '\\') {
                    if (atEnd()) {
                        throw err("Unterminated string");
                    }
                    char e = s.charAt(pos++);
                    switch (e) {
                        case '"': sb.append('"'); break;
                        case '\\': sb.append('\\'); break;
                        case '/': sb.append('/'); break;
                        case 'b': sb.append('\b'); break;
                        case 'f': sb.append('\f'); break;
                        case 'n': sb.append('\n'); break;
                        case 'r': sb.append('\r'); break;
                        case 't': sb.append('\t'); break;
                        case 'u': sb.append(parseUnicodeEscape()); break;
                        default: throw err("Invalid \\escape");
                    }
                } else {
                    sb.append(c);
                }
            }
        }

        private char parseUnicodeEscape() {
            if (pos + 4 > s.length()) {
                throw err("Invalid \\uXXXX escape");
            }
            int cp = Integer.parseInt(s.substring(pos, pos + 4), 16);
            pos += 4;
            return (char) cp;
        }

        private Object parseNumber() {
            int start = pos;
            if (s.charAt(pos) == '-') {
                pos++;
                if (!atEnd() && s.charAt(pos) == 'I') {
                    parseLiteral("Infinity", null);
                    return Double.NEGATIVE_INFINITY;
                }
            }
            boolean isFloat = false;
            while (pos < s.length()) {
                char c = s.charAt(pos);
                if (c >= '0' && c <= '9') {
                    pos++;
                } else if (c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') {
                    isFloat = isFloat || c == '.' || c == 'e' || c == 'E';
                    pos++;
                } else {
                    break;
                }
            }
            String num = s.substring(start, pos);
            if (isFloat) {
                return Double.parseDouble(num);
            }
            try {
                return Long.parseLong(num);
            } catch (NumberFormatException ex) {
                return new BigInteger(num);
            }
        }
    }
}
