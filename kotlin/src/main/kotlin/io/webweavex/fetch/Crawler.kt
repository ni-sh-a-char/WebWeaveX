package io.webweavex.fetch

class Crawler(private val transport: HttpTransport = HttpTransport.default()) {
    private val visited = linkedSetOf<String>()
    private val discovered = mutableListOf<String>()

    suspend fun crawl(url: String, maxDepth: Int = 3): Map<String, Any> {
        crawlRecursive(url, 0, maxDepth)
        return mapOf("visited" to visited.toList(), "discovered" to discovered.toList())
    }

    private suspend fun crawlRecursive(url: String, depth: Int, maxDepth: Int) {
        if (depth > maxDepth || url in visited) return
        visited.add(url)
        val resp = transport.fetch(url)
        if (resp["ok"] != true) return
        val text = resp["text"] as? String ?: return
        Regex("href=\"([^\"]+)\"").findAll(text).forEach { m ->
            val link = m.groupValues[1]
            if (link !in visited) discovered.add(link)
        }
    }
}
