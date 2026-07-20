package io.webweavex.repository

import io.webweavex.fingerprint.Fingerprint

data class QueryResult(
    val matches: List<Map<String, Any>>,
    val totalMatches: Int,
    val fingerprint: String,
    val ranking: List<String> = emptyList(),
    val scoring: List<Map<String, Any>> = emptyList(),
    val indexed: Boolean = false
)

object QueryEngine {
    fun search(graph: KnowledgeGraph, query: String, exact: Boolean = false, useIndex: Boolean = true): QueryResult {
        if (useIndex && query.isNotBlank()) {
            val index = SearchIndex.build(graph)
            val indexedIds = index.search(query)
            if (indexedIds.isNotEmpty()) {
                return indexedSearch(graph, query, indexedIds)
            }
        }
        return linearSearch(graph, query, exact)
    }

    private fun indexedSearch(graph: KnowledgeGraph, query: String, ids: List<String>): QueryResult {
        val idSet = ids.toSet()
        val matches: List<Map<String, Any>> = graph.nodes
            .filter { it.id in idSet }
            .map { node -> mapOf("id" to node.id, "type" to node.type, "data" to node.data, "score" to computeScore(node, query)) }
            .sortedByDescending { (it["score"] as Double) }
        val ranking = matches.map { it["id"] as String }
        val scoring = matches.map { run { val m = java.util.HashMap<String, Any>(); m["id"] = it["id"] ?: ""; m["score"] = it["score"] ?: 0.0; m } }
        return QueryResult(matches, matches.size, graph.fingerprint(), ranking, scoring, true)
    }

    private fun linearSearch(graph: KnowledgeGraph, query: String, exact: Boolean): QueryResult {
        val matches: List<Map<String, Any>> = graph.nodes
            .filter { node ->
                if (exact) node.id == query || node.type == query || node.data.values.any { it.toString() == query }
                else node.id.contains(query, ignoreCase = true) || node.type.contains(query, ignoreCase = true) || node.data.values.any { it.toString().contains(query, ignoreCase = true) }
            }
            .map { node -> mapOf("id" to node.id, "type" to node.type, "data" to node.data, "score" to computeScore(node, query)) }
            .sortedByDescending { (it["score"] as Double) }
        val ranking = matches.map { it["id"] as String }
        val scoring = matches.map { run { val m = java.util.HashMap<String, Any>(); m["id"] = it["id"] ?: ""; m["score"] = it["score"] ?: 0.0; m } }
        return QueryResult(matches, matches.size, graph.fingerprint(), ranking, scoring, false)
    }

    fun filterByType(graph: KnowledgeGraph, type: String): QueryResult {
        val matches: List<Map<String, Any>> = graph.nodes.filter { it.type.equals(type, ignoreCase = true) }
            .sortedBy { it.id }.map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    fun findByRelationship(graph: KnowledgeGraph, relation: String): QueryResult {
        val nodeIds = mutableSetOf<String>()
        for (edge in graph.edges) if (edge.type.equals(relation, ignoreCase = true)) nodeIds.add(edge.source)
        val matches: List<Map<String, Any>> = graph.nodes.filter { it.id in nodeIds }
            .sortedBy { it.id }.map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    fun booleanQuery(graph: KnowledgeGraph, must: List<String> = emptyList(), should: List<String> = emptyList(), mustNot: List<String> = emptyList()): QueryResult {
        val mustMatch = mutableSetOf<String>()
        val shouldMatch = mutableSetOf<String>()
        val mustNotMatch = mutableSetOf<String>()
        for (node in graph.nodes) {
            if (must.all { q -> node.data.values.any { it.toString().contains(q, ignoreCase = true) } }) mustMatch.add(node.id)
            if (should.isEmpty() || should.any { q -> node.data.values.any { it.toString().contains(q, ignoreCase = true) } }) shouldMatch.add(node.id)
            if (mustNot.any { q -> node.data.values.any { it.toString().contains(q, ignoreCase = true) } }) mustNotMatch.add(node.id)
        }
        val matchedIds = (mustMatch intersect shouldMatch) - mustNotMatch
        val matches: List<Map<String, Any>> = graph.nodes.filter { it.id in matchedIds }
            .sortedBy { it.id }.map { mapOf("id" to it.id, "type" to it.type, "data" to it.data) }
        return QueryResult(matches, matches.size, graph.fingerprint(), matches.map { it["id"] as String })
    }

    private fun computeScore(node: KnowledgeNode, query: String): Double {
        var score = 0.0
        if (node.id.contains(query, ignoreCase = true)) score += 10.0
        if (node.type.contains(query, ignoreCase = true)) score += 5.0
        for (v in node.data.values) {
            val vs = v.toString()
            if (vs.contains(query, ignoreCase = true)) score += if (vs.equals(query, ignoreCase = true)) 8.0 else 3.0
        }
        return score
    }
}
