package io.webweavex.extract

object MarkdownExtractor {
    fun extract(text: String): Map<String, Any> {
        val headings = Regex("^#{1,6}\\s+(.+)$", RegexOption.MULTILINE).findAll(text)
            .map { mapOf("level" to it.groupValues[0].takeWhile { c -> c == '#' }.length, "title" to it.groupValues[1].trim()) }
            .toList()

        val codeBlocks = Regex("```[\\w-]*\\n(.*?)```", RegexOption.DOT_MATCHES_ALL)
            .findAll(text).map { it.groupValues[1].trim() }.filter { it.isNotEmpty() }.toSortedSet().toList()

        val urls = Regex("https?://[^\\s)]+").findAll(text)
            .map { it.value }.toSortedSet().toList()

        return mapOf(
            "content" to mapOf("hierarchy" to headings, "urls" to urls),
            "code" to mapOf("blocks" to codeBlocks),
            "metadata" to mapOf("header_count" to headings.size.toString())
        )
    }
}
