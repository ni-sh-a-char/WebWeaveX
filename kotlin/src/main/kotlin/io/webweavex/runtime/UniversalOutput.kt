package io.webweavex.runtime

data class UniversalOutput(
    val data: Map<String, Any>,
    val fingerprint: String,
    val version: String = "3.0.0",
    val metadata: Map<String, Any> = emptyMap()
) {
    fun isValid(): Boolean = data.isNotEmpty() && fingerprint.isNotEmpty()
}
