package io.webweavex.repository

data class KnowledgeNode(val id: String, val type: String, val data: Map<String, Any> = emptyMap())
data class KnowledgeEdge(val source: String, val target: String, val type: String)

data class KnowledgeGraph(
    val nodes: List<KnowledgeNode>,
    val edges: List<KnowledgeEdge>
) {
    fun fingerprint(): String = io.webweavex.fingerprint.Fingerprint.compute(
        mapOf("nodes" to nodes.map { it.id }, "edges" to edges.map { "${it.source}->${it.target}" })
    )
}
