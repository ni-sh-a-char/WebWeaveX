package io.webweavex.determinism

/**
 * Faithful Python `json.dumps` for the native value tree — configurable
 * separators and `ensure_ascii`, always `sort_keys=True`.
 *
 * Unlike [CanonicalJson] this does *not* canonicalize numbers or strip
 * volatile keys; it reproduces `json.dumps` verbatim. Mirrors
 * `io.webweavex.determinism.PyJson` (Java) line for line.
 */
object PyJson {

    /** `json.dumps(v, sort_keys=True, separators=(",",":"))` (ensure_ascii default True). */
    @JvmStatic
    fun dumpsCompactAscii(v: Any?): String = dumps(v, ",", ":", true)

    /** `json.dumps(v, sort_keys=True)` — default separators `(", ", ": ")`, ascii. */
    @JvmStatic
    fun dumpsDefaultAscii(v: Any?): String = dumps(v, ", ", ": ", true)

    /** `json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",",":"))`. */
    @JvmStatic
    fun dumpsCompactUnicode(v: Any?): String = dumps(v, ",", ":", false)

    @JvmStatic
    fun dumps(value: Any?, itemSep: String, kvSep: String, ensureAscii: Boolean): String {
        val sb = StringBuilder()
        encode(value, sb, itemSep, kvSep, ensureAscii)
        return sb.toString()
    }

    private fun encode(v: Any?, sb: StringBuilder, itemSep: String, kvSep: String, ensureAscii: Boolean) {
        when (v) {
            null -> sb.append("null")
            is Boolean -> sb.append(if (v) "true" else "false")
            is Double -> sb.append(floatRepr(v))
            is Float -> sb.append(floatRepr(v.toDouble()))
            is Number -> sb.append(v.toString())
            is String -> escape(v, sb, ensureAscii)
            is List<*> -> {
                sb.append('[')
                for ((i, item) in v.withIndex()) {
                    if (i > 0) sb.append(itemSep)
                    encode(item, sb, itemSep, kvSep, ensureAscii)
                }
                sb.append(']')
            }
            is Map<*, *> -> {
                val keys = v.keys.map { it.toString() }.sortedWith { a, b -> Normalization.codePointCompare(a, b) }
                sb.append('{')
                var first = true
                for (k in keys) {
                    if (!first) sb.append(itemSep)
                    first = false
                    escape(k, sb, ensureAscii)
                    sb.append(kvSep)
                    encode(lookup(v, k), sb, itemSep, kvSep, ensureAscii)
                }
                sb.append('}')
            }
            else -> escape(v.toString(), sb, ensureAscii)
        }
    }

    /** Python `json` float form: `repr` for finite, `NaN`/`Infinity` otherwise. */
    private fun floatRepr(d: Double): String {
        if (d.isNaN()) return "NaN"
        if (d == Double.POSITIVE_INFINITY) return "Infinity"
        if (d == Double.NEGATIVE_INFINITY) return "-Infinity"
        return PyFloat.pyFloatRepr(d)
    }

    private fun lookup(map: Map<*, *>, key: String): Any? {
        if (map.containsKey(key)) return map[key]
        for ((k, v) in map) {
            if (k.toString() == key) return v
        }
        return null
    }

    private fun escape(s: String, sb: StringBuilder, ensureAscii: Boolean) {
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
                    if (c.code < 0x20 || (ensureAscii && c.code > 0x7E)) {
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
