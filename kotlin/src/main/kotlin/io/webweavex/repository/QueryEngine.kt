package io.webweavex.repository

import io.webweavex.fingerprint.Fingerprint

data class QueryResult(
    val matches: List<Map<String, Any>>,
    val totalMatches: Int,
    val fingerprint: String,
    val ranking: List<String> = emptyList()
)

object QueryEngine {
    fun search(graph: KnowledgeGraph, query: String): QueryResult {
        val matches = graph.nodes
            .filter { node ->
                node.id.contains(query, ignoreCase = true) ||
                node.type.contains(query, ignoreCase = true) ||
                node.data.values.any { it.toString().contains(query, ignoreCase = true) }
            }
            .sortedBy { it.id }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    fun filterByType(graph: KnowledgeGraph, type: String): QueryResult {
        val matches = graph.nodes
            .filter { it.type.equals(type, ignoreCase = true) }
            .sortedBy { it.id }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    fun findByRelationship(graph: KnowledgeGraph, relation: String): QueryResult {
        val nodeIds = graph.edges
            .filter { it.type.equals(relation, ignoreCase = true) }
            .map { it.source }
            .toSet()
        val matches = graph.nodes
            .filter { it.id in nodeIds }
            .sortedBy { it.id }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }
}
