package io.webweavex.determinism

import java.text.Normalizer

/**
 * Cross-language normalization primitives — byte-identical to the Python
 * canonical runtime (`core/determinism/normalization.py`) and the aligned
 * JavaScript, Dart, and Java runtimes.
 *
 * Mirrors `io.webweavex.determinism.Normalization` (Java) line for line so the
 * canonical bytes stay identical; only syntax is idiomatic Kotlin.
 */
object Normalization {

    /** Keys stripped from every dictionary level before canonicalization. */
    @JvmField
    val VOLATILE_RUNTIME_KEYS: Set<String> = setOf(
        "timestamp",
        "created_at",
        "updated_at",
        "nonce",
        "request_id",
        "csrf",
        "generated_at",
        "runtime_id",
        "random",
        "uuid",
    )

    /**
     * NFKC + CRLF->LF + trailing-whitespace strip, in that order. Matches Python
     * `normalize_runtime_value`.
     */
    @JvmStatic
    fun normalizeRuntimeValue(value: String): String {
        var s = Normalizer.normalize(value, Normalizer.Form.NFKC)
        s = s.replace("\r\n", "\n").replace("\r", "\n")
        return stripTrailingWhitespace(s)
    }

    /** True for the exact code-point set matched by Python str `\s`. */
    private fun isPyWhitespace(cp: Int): Boolean {
        return (cp in 0x09..0x0D) || // \t \n \v \f \r
            (cp in 0x1C..0x1F) || // FS GS RS US
            cp == 0x20 ||
            cp == 0x85 ||
            cp == 0xA0 ||
            cp == 0x1680 ||
            (cp in 0x2000..0x200A) ||
            cp == 0x2028 ||
            cp == 0x2029 ||
            cp == 0x202F ||
            cp == 0x205F ||
            cp == 0x3000
    }

    private fun stripTrailingWhitespace(s: String): String {
        var end = s.length
        while (end > 0) {
            val cp = s.codePointBefore(end)
            if (!isPyWhitespace(cp)) break
            end -= Character.charCount(cp)
        }
        return s.substring(0, end)
    }

    /**
     * Unicode code-point string comparison (Python `sorted()` semantics) —
     * `String.compareTo` orders by UTF-16 code unit, which inverts astral-plane
     * characters relative to U+E000-U+FFFF, so keys are compared code point by
     * code point instead.
     */
    @JvmStatic
    fun codePointCompare(a: String, b: String): Int {
        var i = 0
        var j = 0
        while (i < a.length && j < b.length) {
            val ca = a.codePointAt(i)
            val cb = b.codePointAt(j)
            if (ca != cb) return ca.compareTo(cb)
            i += Character.charCount(ca)
            j += Character.charCount(cb)
        }
        return (a.length - i).compareTo(b.length - j)
    }

    /**
     * Cross-language numeric canonicalization: integral doubles below 2^63
     * become integers (Long), non-finite doubles become null, everything else
     * is returned unchanged.
     */
    @JvmStatic
    fun canonicalizeNumber(v: Any?): Any? {
        val d: Double = when (v) {
            is Double -> v
            is Float -> v.toDouble()
            else -> return v
        }
        if (d.isNaN() || d.isInfinite()) return null
        if (d == Math.floor(d) && Math.abs(d) < 9223372036854775808.0) {
            return d.toLong()
        }
        return if (v is Float) d else v
    }

    /**
     * Recursively sort keys by code point, drop volatile keys at every dict
     * level, and canonicalize numbers — mirrors Python `stable_sort_keys`.
     */
    @JvmStatic
    fun stableSortKeys(obj: Map<*, *>): Map<String, Any?> {
        val keys = obj.keys.map { it.toString() }.sortedWith { a, b -> codePointCompare(a, b) }
        val sorted = LinkedHashMap<String, Any?>()
        for (k in keys) {
            if (k in VOLATILE_RUNTIME_KEYS) continue
            val value = get(obj, k)
            sorted[k] = when (value) {
                is Map<*, *> -> stableSortKeys(value)
                is List<*> -> value.map { item ->
                    if (item is Map<*, *>) stableSortKeys(item) else canonicalizeNumber(item)
                }
                else -> canonicalizeNumber(value)
            }
        }
        return sorted
    }

    /** Looks up a value whose original key may be a non-String (e.g. number). */
    private fun get(obj: Map<*, *>, key: String): Any? {
        if (obj.containsKey(key)) return obj[key]
        for ((k, v) in obj) {
            if (k.toString() == key) return v
        }
        return null
    }
}
