package com.webweavex

data class GraphNode(
    val id: String,
    val type: String,
    val value: String
)

data class GraphEdge(
    val source: String,
    val target: String,
    val weight: Int = 1
) {
    fun toMap(): Map<String, Any> = mapOf("source" to source, "target" to target, "weight" to weight)
}

data class GraphData(
    val nodes: List<GraphNode>,
    val edges: List<GraphEdge>
)

class Graph {
    fun build(entities: List<Entity>): GraphData {
        if (entities.isEmpty()) {
            return GraphData(emptyList(), emptyList())
        }

        val uniqueEntities = entities.distinct()

        val sortedEntities = uniqueEntities.sortedWith(
            compareBy<Entity> { it.type }.thenBy { it.value }
        )

        val nodes = sortedEntities.map { entity ->
            val id = "${entity.type}:${entity.value}"
            GraphNode(id, entity.type, entity.value)
        }.sortedBy { it.id }

        val edges = mutableListOf<GraphEdge>()
        for (i in sortedEntities.indices) {
            for (j in i + 1 until sortedEntities.size) {
                val source = "${sortedEntities[i].type}:${sortedEntities[i].value}"
                val target = "${sortedEntities[j].type}:${sortedEntities[j].value}"
                edges.add(GraphEdge(source, target, 1))
            }
        }

        val sortedEdges = edges.sortedWith(
            compareBy<GraphEdge> { it.source }.thenBy { it.target }
        )

        return GraphData(nodes, sortedEdges)
    }
}
