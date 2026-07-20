package io.webweavex.extract

import io.webweavex.determinism.StableSerialize
import io.webweavex.fingerprint.Fingerprint

object ExtractionPipeline {
    fun extract(request: ExtractionRequest): ExtractionResult {
        val inputType = request.detectInputType()
        val content = when (inputType) {
            "html" -> HtmlExtractor.extract(request.source)
            "markdown" -> MarkdownExtractor.extract(request.source)
            "json" -> JsonExtractor.extract(request.source)
            else -> mapOf("content" to mapOf("text" to request.source), "metadata" to mapOf("format" to inputType))
        }
        val rawText = (content["content"] as? Map<*, *>)?.get("text")?.toString() ?: request.source
        val fp = Fingerprint.compute(content)
        return ExtractionResult(
            content = content["content"] as? Map<String, Any> ?: emptyMap(),
            code = content["code"] as? Map<String, Any> ?: emptyMap(),
            metadata = (content["metadata"] as? Map<String, Any> ?: emptyMap()) + mapOf("input_type" to inputType),
            rawText = rawText,
            sourceUrl = request.sourceUrl,
            fingerprint = fp
        )
    }

    fun extractText(text: String, sourceUrl: String = ""): ExtractionResult {
        return extract(ExtractionRequest(source = text, sourceUrl = sourceUrl))
    }
}
