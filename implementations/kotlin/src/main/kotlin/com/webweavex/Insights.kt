package com.webweavex

data class InsightsData(
    val top_entities: List<Map<String, Any>>,
    val stats: Map<String, Any>,
    val entity_counts: Map<String, Int>
)

class Insights {
    fun compute(entities: List<Entity>, chunks: List<Chunk>, text: String): InsightsData {
        val entityCounts = mutableMapOf<String, Int>()
        val entityTypes = mutableSetOf<String>()

        for (entity in entities) {
            val key = "${entity.type}:${entity.value}"
            entityCounts[key] = entityCounts.getOrDefault(key, 0) + 1
            entityTypes.add(entity.type)
        }

        val sortedCounts = entityCounts.entries.sortedWith(
            compareByDescending<Map.Entry<String, Int>> { it.value }.thenBy { it.key }
        )

        val topEntities = sortedCounts.take(10).map { (key, count) ->
            val parts = key.split(":", limit = 2)
            mapOf(
                "type" to parts[0],
                "value" to (if (parts.size > 1) parts[1] else ""),
                "count" to count
            )
        }

        val stats = mutableMapOf<String, Any>(
            "total_entities" to entities.size,
            "unique_entities" to entityCounts.size,
            "entity_types" to entityTypes.size,
            "total_relations" to 0
        )

        if (chunks.isNotEmpty()) {
            stats["total_chunks"] = chunks.size
        }

        if (text.isNotEmpty()) {
            stats["text_length"] = text.length
            stats["word_count"] = text.trim().split("\\s+".toRegex()).size
        }

        val sortedEntityCounts = entityCounts.entries
            .sortedBy { it.key }
            .associate { it.key to it.value }

        return InsightsData(topEntities, stats, sortedEntityCounts)
    }
}
