package io.webweavex.runtime

data class RuntimeEdge(
    val source: String,
    val target: String,
    val type: String = "default",
    val data: Map<String, Any> = emptyMap()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "source" to source, "target" to target, "type" to type, "data" to data
    )
}
