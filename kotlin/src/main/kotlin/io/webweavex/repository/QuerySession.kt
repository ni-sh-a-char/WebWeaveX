package io.webweavex.repository

data class QueryMetrics(
    val totalQueries: Int = 0,
    val indexedQueries: Int = 0,
    val fallbackQueries: Int = 0,
    val averageLatencyMs: Double = 0.0
)

class QuerySession(
    val graph: KnowledgeGraph,
    private val index: SearchIndex = SearchIndex.build(graph),
    private val nodeLookup: NodeLookup = NodeLookup.build(graph)
) {
    private var queryCount = 0
    private var indexedCount = 0
    private var totalLatencyMs = 0L

    fun search(query: String, exact: Boolean = false): QueryResult {
        val start = System.nanoTime()
        val result = QueryEngine.searchWithIndex(query, index, nodeLookup, exact)
        val elapsed = (System.nanoTime() - start) / 1_000_000
        queryCount++
        if (result.indexed) indexedCount++
        totalLatencyMs += elapsed
        return result
    }

    fun filterByType(type: String): QueryResult = QueryEngine.filterByType(graph, type)
    fun findByRelationship(relation: String): QueryResult = QueryEngine.findByRelationship(graph, relation)

    fun metrics(): QueryMetrics = QueryMetrics(
        queryCount, indexedCount, queryCount - indexedCount,
        if (queryCount > 0) totalLatencyMs.toDouble() / queryCount else 0.0
    )

    fun indexStatistics(): Map<String, Any> = index.statistics()
}
