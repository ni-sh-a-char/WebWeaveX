package io.webweavex.graph

data class RuntimeGraph(
    val nodes: List<Map<String, Any>> = emptyList(),
    val edges: List<Map<String, Any>> = emptyList()
) {
    fun fingerprint(): String = io.webweavex.fingerprint.Fingerprint.computeGraph(nodes, edges)
    
    fun normalize(): RuntimeGraph {
        val sortedNodes = nodes.sortedBy { it["id"].toString() }
        val sortedEdges = edges.sortedBy { "${it["from"]}|${it["to"]}|${it["type"]}" }
        return RuntimeGraph(sortedNodes, sortedEdges)
    }
}
