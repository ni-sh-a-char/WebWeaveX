package io.webweavex.determinism

/**
 * Small Python-semantics helpers shared by the higher runtime layers —
 * faithful to CPython's `str()` coercion and truthiness so ported
 * dictionary/list logic stays byte-exact. Mirrors
 * `io.webweavex.determinism.Py` (Java).
 */
object Py {

    /** CPython `str(obj)` for the value shapes that occur in runtime dicts. */
    @JvmStatic
    fun str(o: Any?): String {
        if (o == null) return "None"
        if (o is Boolean) return if (o) "True" else "False"
        return o.toString()
    }

    /** CPython truthiness: None, "", False, 0, empty containers are falsy. */
    @JvmStatic
    fun truthy(o: Any?): Boolean {
        if (o == null || o == false) return false
        return when (o) {
            is String -> o.isNotEmpty()
            is Number -> o.toDouble() != 0.0
            is Map<*, *> -> o.isNotEmpty()
            is List<*> -> o.isNotEmpty()
            else -> true
        }
    }

    @Suppress("UNCHECKED_CAST")
    @JvmStatic
    fun asMap(o: Any?): Map<String, Any?>? = if (o is Map<*, *>) o as Map<String, Any?> else null

    @Suppress("UNCHECKED_CAST")
    @JvmStatic
    fun asList(o: Any?): List<Any?>? = if (o is List<*>) o as List<Any?> else null

    /** `container.get(key, default)` where container may be null or non-dict. */
    @JvmStatic
    fun get(container: Any?, key: String, dflt: Any?): Any? {
        val m = asMap(container) ?: return dflt
        if (!m.containsKey(key)) return dflt
        return m[key]
    }
}
