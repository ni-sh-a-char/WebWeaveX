package io.webweavex.runtime

data class RuntimeMetadata(
    val source: String = "",
    val version: String = "3.0.0",
    val tags: Map<String, String> = emptyMap(),
    val properties: Map<String, Any> = emptyMap()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "source" to source, "version" to version,
        "tags" to tags, "properties" to properties
    )
}
