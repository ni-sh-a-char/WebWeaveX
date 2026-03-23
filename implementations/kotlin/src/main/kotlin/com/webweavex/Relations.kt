package com.webweavex

data class Relation(
    val source: String,
    val target: String,
    val type: String = "cooccurrence"
) {
    fun toMap(): Map<String, String> = mapOf("source" to source, "target" to target, "type" to type)
}

class Relations {
    fun extract(entities: List<Entity>): List<Relation> {
        if (entities.isEmpty()) return emptyList()

        val uniqueEntities = entities.distinct()

        val sortedEntities = uniqueEntities.sortedWith(
            compareBy<Entity> { it.type }.thenBy { it.value }
        )

        val relations = mutableListOf<Relation>()
        for (i in sortedEntities.indices) {
            for (j in i + 1 until sortedEntities.size) {
                val source = "${sortedEntities[i].type}:${sortedEntities[i].value}"
                val target = "${sortedEntities[j].type}:${sortedEntities[j].value}"
                relations.add(Relation(source, target, "cooccurrence"))
            }
        }

        return relations.sortedWith(
            compareBy<Relation> { it.source }.thenBy { it.target }
        )
    }
}
