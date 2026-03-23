package com.webweavex

import com.google.gson.GsonBuilder

class Pipeline {
    private val cleaner = Cleaner()
    private val chunker = Chunker()
    private val entities = Entities()
    private val relations = Relations()
    private val graph = Graph()
    private val insights = Insights()

    private val gson = GsonBuilder().setPrettyPrinting().create()

    fun extractFromText(text: String): Map<String, Any> {
        val cleanedText = cleaner.clean(text)
        val chunkList = chunker.chunk(cleanedText)
        val entityList = entities.extract(cleanedText)
        val relationList = relations.extract(entityList)
        val graphData = graph.build(entityList)
        val insightsData = insights.compute(entityList, chunkList, cleanedText)

        return buildResult("", "", cleanedText, chunkList, entityList, relationList, graphData, insightsData)
    }

    private fun buildResult(
        url: String,
        title: String,
        text: String,
        chunks: List<Chunk>,
        entityList: List<Entity>,
        relationList: List<Relation>,
        graphData: GraphData,
        insightsData: InsightsData
    ): Map<String, Any> {
        val sortedChunks = chunks.sortedBy { it.index }

        val sortedEntities = entityList.distinct().sortedWith(
            compareBy<Entity> { it.type }.thenBy { it.value }
        )

        val sortedRelations = relationList.sortedWith(
            compareBy<Relation> { it.source }.thenBy { it.target }
        )

        val sortedNodes = graphData.nodes.sortedBy { it.id }
        val sortedEdges = graphData.edges.sortedWith(
            compareBy<GraphEdge> { it.source }.thenBy { it.target }
        )

        val meta = linkedMapOf(
            "title" to title,
            "url" to url
        )

        val content = linkedMapOf(
            "text" to text
        )

        val chunksList = sortedChunks.map { chunk ->
            linkedMapOf(
                "text" to chunk.text,
                "index" to chunk.index,
                "start" to chunk.start,
                "end" to chunk.end
            )
        }

        val entitiesList = sortedEntities.map { entity ->
            linkedMapOf(
                "type" to entity.type,
                "value" to entity.value
            )
        }

        val relationsList = sortedRelations.map { relation ->
            linkedMapOf(
                "source" to relation.source,
                "target" to relation.target,
                "type" to relation.type
            )
        }

        val graphMap = linkedMapOf(
            "nodes" to sortedNodes.map { node ->
                linkedMapOf(
                    "id" to node.id,
                    "type" to node.type,
                    "value" to node.value
                )
            },
            "edges" to sortedEdges.map { edge ->
                linkedMapOf(
                    "source" to edge.source,
                    "target" to edge.target,
                    "weight" to edge.weight
                )
            }
        )

        val insightsMap = linkedMapOf(
            "top_entities" to insightsData.top_entities,
            "stats" to insightsData.stats,
            "entity_counts" to insightsData.entity_counts
        )

        return linkedMapOf(
            "meta" to meta,
            "content" to content,
            "chunks" to chunksList,
            "entities" to entitiesList,
            "relations" to relationsList,
            "graph" to graphMap,
            "insights" to insightsMap
        )
    }

    fun toJson(map: Map<String, Any>): String {
        return gson.toJson(map)
    }
}
