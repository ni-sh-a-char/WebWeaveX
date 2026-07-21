package io.webweavex.repository

class NodeLookup(private val nodes: Map<String, KnowledgeNode>) {
    companion object {
        fun build(graph: KnowledgeGraph): NodeLookup {
            return NodeLookup(graph.nodes.associateBy { it.id })
        }
    }

    fun get(id: String): KnowledgeNode? = nodes[id]
    fun contains(id: String): Boolean = nodes.containsKey(id)
    fun size(): Int = nodes.size
    fun ids(): Set<String> = nodes.keys.toSortedSet()
}
