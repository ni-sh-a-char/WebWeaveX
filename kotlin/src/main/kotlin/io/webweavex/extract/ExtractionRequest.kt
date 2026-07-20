package io.webweavex.extract

data class ExtractionRequest(
    val source: String,
    val sourceUrl: String = "",
    val inputType: String = "auto",
    val options: Map<String, Any> = emptyMap()
) {
    fun detectInputType(): String {
        if (inputType != "auto") return inputType
        if (source.startsWith("http://") || source.startsWith("https://")) return "url"
        if (source.trimStart().startsWith("<")) return "html"
        if (source.trimStart().startsWith("{") || source.trimStart().startsWith("[")) return "json"
        if (source.trimStart().startsWith("#")) return "markdown"
        if (source.trimStart().startsWith("<?xml") || source.trimStart().startsWith("<")) return "xml"
        return "text"
    }
}
