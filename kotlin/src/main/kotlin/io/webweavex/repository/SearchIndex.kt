package io.webweavex.repository

import io.webweavex.fingerprint.Fingerprint

class SearchIndex(
    val tokenIndex: Map<String, List<String>>,
    val typeIndex: Map<String, List<String>>,
    val fingerprint: String
) {
    companion object {
        fun build(graph: KnowledgeGraph): SearchIndex {
            val tokenIndex = mutableMapOf<String, MutableList<String>>()
            val typeIndex = mutableMapOf<String, MutableList<String>>()

            for (node in graph.nodes) {
                val tokens = mutableSetOf(node.id.lowercase(), node.type.lowercase())
                node.data.values.forEach { tokens.addAll(it.toString().lowercase().split(Regex("\\s+")).filter { it.isNotEmpty() }) }
                tokens.forEach { token ->
                    tokenIndex.getOrPut(token) { mutableListOf() }.add(node.id)
                }
                typeIndex.getOrPut(node.type.lowercase()) { mutableListOf() }.add(node.id)
            }

            val fp = Fingerprint.compute(mapOf(
                "tokens" to tokenIndex.keys.sorted(),
                "types" to typeIndex.keys.sorted()
            ))

            return SearchIndex(
                tokenIndex = tokenIndex.mapValues { it.value.distinct().sorted() },
                typeIndex = typeIndex.mapValues { it.value.distinct().sorted() },
                fingerprint = fp
            )
        }
    }

    fun search(query: String): List<String> {
        val tokens = query.lowercase().split(Regex("\\s+")).filter { it.isNotEmpty() }
        if (tokens.isEmpty()) return emptyList()
        var result = (tokenIndex[tokens[0]] ?: emptyList()).toMutableSet()
        for (token in tokens.drop(1)) {
            result = result.intersect(tokenIndex[token] ?: emptySet()).toMutableSet()
        }
        return result.sorted()
    }
}
