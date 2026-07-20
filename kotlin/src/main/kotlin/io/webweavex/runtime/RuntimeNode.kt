package io.webweavex.runtime

data class RuntimeNode(
    val id: String,
    val type: String = "default",
    val data: Map<String, Any> = emptyMap(),
    val metadata: Map<String, Any> = emptyMap()
) {
    fun toMap(): Map<String, Any> = mapOf(
        "id" to id, "type" to type, "data" to data, "metadata" to metadata
    )
}
