package io.webweavex.runtime

data class UniversalInput(
    val source: String,
    val config: Map<String, Any> = emptyMap(),
    val options: Map<String, Any> = emptyMap()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "source" to source,
        "config" to config,
        "options" to options
    )
}
