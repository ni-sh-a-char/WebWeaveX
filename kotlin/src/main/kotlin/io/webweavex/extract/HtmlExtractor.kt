package io.webweavex.extract

object HtmlExtractor {
    fun extract(text: String): Map<String, Any> {
        val cleaned = text
            .replace(Regex("<script[^>]*>.*?</script>", RegexOption.DOT_MATCHES_ALL), "")
            .replace(Regex("<style[^>]*>.*?</style>", RegexOption.DOT_MATCHES_ALL), "")
            .replace(Regex("<!--.*?-->", RegexOption.DOT_MATCHES_ALL), "")

        val title = Regex("<title[^>]*>(.*?)</title>", RegexOption.DOT_MATCHES_ALL)
            .find(cleaned)?.groupValues?.get(1)?.trim()?.let { stripTags(it).trim() } ?: ""

        val links = Regex("href=\"([^\"]+)\"").findAll(cleaned)
            .map { it.groupValues[1] }.filter { it.isNotEmpty() }.toSortedSet().toList()

        val codeBlocks = Regex("<(?:pre|code)[^>]*>(.*?)</(?:pre|code)>", RegexOption.DOT_MATCHES_ALL)
            .findAll(cleaned).map { stripTags(it.groupValues[1]).trim() }.filter { it.isNotEmpty() }.toSortedSet().toList()

        val bodyText = stripTags(cleaned).replace(Regex("\\s+"), " ").trim()

        return mapOf(
            "content" to mapOf("text" to bodyText, "links" to links),
            "code" to mapOf("blocks" to codeBlocks),
            "metadata" to mapOf("title" to title)
        )
    }

    private fun stripTags(html: String): String = html.replace(Regex("<[^>]*>"), "")
}
