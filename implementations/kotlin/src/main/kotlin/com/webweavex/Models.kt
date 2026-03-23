package com.webweavex

data class GraphResult(
    val nodes: List<Entity>,
    val edges: List<GraphEdge>
) {
    fun toMap(): Map<String, Any> = linkedMapOf(
        "nodes" to nodes.map { it.toMap() },
        "edges" to edges.map { it.toMap() }
    )
}

data class CrawlResult(
    val url: String,
    val text: String,
    val chunks: List<Chunk> = emptyList(),
    val entities: List<Entity> = emptyList(),
    val graph: GraphResult? = null,
    val metadata: Map<String, String>? = null
) {
    fun toMap(): Map<String, Any> = buildMap {
        put("url", url)
        put("text", text)
        if (chunks.isNotEmpty()) put("chunks", chunks.map { it.toMap() })
        if (entities.isNotEmpty()) put("entities", entities.map { it.toMap() })
        if (graph != null) put("graph", graph!!.toMap())
        if (metadata != null) put("metadata", metadata!!)
    }
}
