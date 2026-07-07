package io.webweavex.determinism

/**
 * Canonical string serialization used for hashing, encryption, and
 * fingerprints — byte-identical to Python `stable_serialize`
 * (`core/determinism/normalization.py`) and the Java/Dart/JS ports.
 *
 * - [String] -> [Normalization.normalizeRuntimeValue]
 * - [Map] -> canonical JSON of its key-stabilized form
 * - [List] -> canonical JSON of the array re-keyed as an object
 *   (`{"0": ..., "1": ...}`), matching the JavaScript runtime's
 *   `fast-json-stable-stringify` array handling
 * - any scalar -> canonical JSON of its canonicalized number form
 *
 * Mirrors `io.webweavex.determinism.StableSerialize` (Java) line for line.
 */
object StableSerialize {

    @JvmStatic
    fun stableSerialize(value: Any?): String {
        if (value is String) {
            return Normalization.normalizeRuntimeValue(value)
        }
        if (value is Map<*, *>) {
            return CanonicalJson.canonicalJsonEncode(Normalization.stableSortKeys(value))
        }
        if (value is List<*>) {
            val asMap = LinkedHashMap<String, Any?>()
            for ((i, item) in value.withIndex()) {
                asMap[i.toString()] = if (item is Map<*, *>) {
                    Normalization.stableSortKeys(item)
                } else {
                    Normalization.canonicalizeNumber(item)
                }
            }
            return CanonicalJson.canonicalJsonEncode(asMap)
        }
        return CanonicalJson.canonicalJsonEncode(value)
    }
}
