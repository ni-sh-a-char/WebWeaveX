package io.webweavex.repository

import io.webweavex.fingerprint.Fingerprint

data class QueryResult(
    val matches: List<Map<String, Any>>,
    val totalMatches: Int,
    val fingerprint: String,
    val ranking: List<String> = emptyList(),
    val scoring: List<Map<String, Any>> = emptyList()
)

object QueryEngine {
    fun search(graph: KnowledgeGraph, query: String, exact: Boolean = false): QueryResult {
        val matches = graph.nodes
            .filter { node ->
                if (exact) {
                    node.id == query || node.type == query ||
                    node.data.values.any { it.toString() == query }
                } else {
                    node.id.contains(query, ignoreCase = true) ||
                    node.type.contains(query, ignoreCase = true) ||
                    node.data.values.any { it.toString().contains(query, ignoreCase = true) }
                }
            }
            .sortedBy { it.id }
            .map { node ->
                val score = computeScore(node, query)
                mapOf("id" to node.id, "type" to node.type, "data" to node.data, "score" to score)
            }
            .sortedByDescending { it["score"] as Double }
        return QueryResult(
            matches, matches.size, graph.fingerprint(),
            matches.map { it["id"] as String },
            matches.map { mapOf("id" to (it["id"] ?: ""), "score" to (it["score"] ?: 0.0)) }
        )
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
            .map { it.source }.toSet()
        val matches = graph.nodes
            .filter { it.id in nodeIds }
            .sortedBy { it.id }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    fun booleanQuery(graph: KnowledgeGraph, must: List<String> = emptyList(), should: List<String> = emptyList(), mustNot: List<String> = emptyList()): QueryResult {
        val mustMatch = graph.nodes.filter { n -> must.all { q -> n.data.values.any { it.toString().contains(q, ignoreCase = true) } } }
        val shouldMatch = graph.nodes.filter { n -> should.isEmpty() || should.any { q -> n.data.values.any { it.toString().contains(q, ignoreCase = true) } } }
        val mustNotMatch = graph.nodes.filter { n -> mustNot.any { q -> n.data.values.any { it.toString().contains(q, ignoreCase = true) } } }
        val matchedIds = (mustMatch.map { it.id }.toSet() intersect shouldMatch.map { it.id }.toSet()) - mustNotMatch.map { it.id }.toSet()
        val matches = graph.nodes.filter { it.id in matchedIds }.sortedBy { it.id }
            .map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    private fun computeScore(node: KnowledgeNode, query: String): Double {
        var score = 0.0
        if (node.id.contains(query, ignoreCase = true)) score += 10.0
        if (node.type.contains(query, ignoreCase = true)) score += 5.0
        node.data.forEach { (_, v) ->
            val vs = v.toString()
            if (vs.contains(query, ignoreCase = true)) {
                score += if (vs.equals(query, ignoreCase = true)) 8.0 else 3.0
            }
        }
        return score
    }
}
