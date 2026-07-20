package io.webweavex.extract

data class ExtractionResult(
    val content: Map<String, Any>,
    val code: Map<String, Any> = emptyMap(),
    val dependencies: Map<String, Any> = emptyMap(),
    val metadata: Map<String, Any> = emptyMap(),
    val relationships: Map<String, Any> = emptyMap(),
    val rawText: String = "",
    val sourceUrl: String = "",
    val fingerprint: String = ""
) {
    fun toMap(): Map<String, Any> = mapOf(
        "content" to content, "code" to code, "dependencies" to dependencies,
        "metadata" to metadata, "relationships" to relationships,
        "raw_text" to rawText, "source_url" to sourceUrl, "fingerprint" to fingerprint
    )
}
