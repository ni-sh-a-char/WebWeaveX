package io.webweavex.repository

data class QueryResult(
    val matches: List<Map<String, Any>>,
    val totalMatches: Int,
    val fingerprint: String
)

object QueryEngine {
    fun search(graph: KnowledgeGraph, query: String): QueryResult {
        val matches = graph.nodes.filter { it.data.values.any { v -> v.toString().contains(query, ignoreCase = true) } }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint())
    }
}
