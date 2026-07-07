package io.webweavex.determinism

/**
 * Compact canonical JSON encoder — byte-identical to Python
 * `json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)`
 * and the aligned JavaScript, Dart, and Java runtimes.
 *
 * Mirrors `io.webweavex.determinism.CanonicalJson` (Java) line for line.
 */
object CanonicalJson {

    @JvmStatic
    fun canonicalJsonEncode(value: Any?): String {
        val sb = StringBuilder()
        encode(value, sb)
        return sb.toString()
    }

    private fun encode(raw: Any?, sb: StringBuilder) {
        val v = Normalization.canonicalizeNumber(raw)
        when (v) {
            null -> sb.append("null")
            is Boolean -> sb.append(if (v) "true" else "false")
            is Double -> sb.append(PyFloat.pyFloatRepr(v))
            is Number -> sb.append(v.toString())
            is String -> escapeJsonString(v, sb)
            is List<*> -> {
                sb.append('[')
                for ((i, item) in v.withIndex()) {
                    if (i > 0) sb.append(',')
                    encode(item, sb)
                }
                sb.append(']')
            }
            is Map<*, *> -> {
                val keys = v.keys.map { it.toString() }.sortedWith { a, b -> Normalization.codePointCompare(a, b) }
                sb.append('{')
                var first = true
                for (k in keys) {
                    if (!first) sb.append(',')
                    first = false
                    escapeJsonString(k, sb)
                    sb.append(':')
                    encode(lookup(v, k), sb)
                }
                sb.append('}')
            }
            else -> escapeJsonString(v.toString(), sb)
        }
    }

    private fun lookup(map: Map<*, *>, key: String): Any? {
        if (map.containsKey(key)) return map[key]
        for ((k, v) in map) {
            if (k.toString() == key) return v
        }
        return null
    }

    /**
     * JSON string escaping identical to Python `json.dumps` with
     * `ensure_ascii=False`: quote/backslash/backspace/tab/newline/formfeed/CR
     * use short escapes, other control characters below U+0020 use lowercase
     * `\uXXXX`, everything else (including all non-ASCII) is emitted verbatim.
     */
    fun escapeJsonString(s: String, sb: StringBuilder) {
        sb.append('"')
        for (c in s) {
            when (c) {
                '"' -> sb.append("\\\"")
                '\\' -> sb.append("\\\\")
                '\b' -> sb.append("\\b")
                '\t' -> sb.append("\\t")
                '\n' -> sb.append("\\n")
                '' -> sb.append("\\f")
                '\r' -> sb.append("\\r")
                else -> {
                    if (c.code < 0x20) {
                        sb.append(String.format("\\u%04x", c.code))
                    } else {
                        sb.append(c)
                    }
                }
            }
        }
        sb.append('"')
    }
}
