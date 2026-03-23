package com.webweavex

import java.time.Instant

class WebWeaveX {
    private val pipeline = Pipeline()

    fun extract(textOrHtml: String): Map<String, Any> {
        return try {
            if (textOrHtml.isEmpty()) {
                pipeline.extractFromText("")
            } else if (textOrHtml.trim().startsWith("<") && textOrHtml.lowercase().contains("</html>")) {
                pipeline.extractFromText(textOrHtml)
            } else {
                pipeline.extractFromText(textOrHtml)
            }
        } catch (e: Exception) {
            createErrorResult()
        }
    }

    fun clean(text: String): String {
        return pipeline.extractFromText(text)["content"]?.let { 
            (it as? Map<*, *>)?.get("text") as? String ?: ""
        } ?: ""
    }

    fun chunk(text: String): List<Chunk> {
        return pipeline.extractFromText(text)["chunks"] as? List<Chunk> ?: emptyList()
    }

    fun entities(text: String): List<Entity> {
        return pipeline.extractFromText(text)["entities"] as? List<Entity> ?: emptyList()
    }

    fun graph(text: String): GraphData {
        return pipeline.extractFromText(text)["graph"] as? GraphData ?: GraphData(emptyList(), emptyList())
    }

    fun extractAgent(text: String): Map<String, Any> {
        return try {
            val result = extract(text)
            extractAgentFromResult(result, text)
        } catch (e: Exception) {
            linkedMapOf(
                "task" to "web_analysis",
                "input" to (if (text.length > 500) text.substring(0, 500) else text),
                "output" to linkedMapOf<String, Any>(),
                "summary" to "Error: ${e.message}",
                "actions" to emptyList<String>(),
                "confidence" to 0.0
            )
        }
    }

    @Suppress("UNCHECKED_CAST")
    private fun extractAgentFromResult(result: Map<String, Any>, inputText: String): Map<String, Any> {
        val content = result["content"] as? Map<*, *> ?: emptyMap<Any, Any>()
        val text = content["text"] as? String ?: ""
        val entities = result["entities"] as? List<Map<String, String>> ?: emptyList()
        val relations = result["relations"] as? List<Map<String, String>> ?: emptyList()

        val summary = if (entities.isEmpty()) {
            "No entities extracted from input text."
        } else {
            "Extracted ${entities.size} entities from text."
        }

        val actions = mutableListOf<String>()
        val types = entities.mapNotNull { it["type"] }.toSet()
        if ("url" in types) actions.add("crawl")
        if ("email" in types) actions.add("contact")
        if ("phone" in types) actions.add("call")
        if (entities.size > 5) actions.add("extract_more")
        if (actions.isEmpty()) actions.add("analyze")

        val confidence = if (text.isNotEmpty()) {
            minOf((entities.size + relations.size * 0.5) / text.length.toDouble() * 10, 1.0)
        } else {
            0.0
        }

        return linkedMapOf(
            "task" to "web_analysis",
            "input" to (if (text.length > 500) text.substring(0, 500) else text),
            "output" to result,
            "summary" to summary,
            "actions" to actions,
            "confidence" to (confidence * 100).toInt() / 100.0
        )
    }

    fun toMemoryBlock(result: Map<String, Any>): Map<String, Any> {
        return try {
            linkedMapOf(
                "type" to "webweavex_memory",
                "entities" to (result["entities"] ?: emptyList<Map<String, Any>>()),
                "relations" to (result["relations"] ?: emptyList<Map<String, Any>>()),
                "graph" to (result["graph"] ?: createEmptyGraph()),
                "timestamp" to Instant.now().toString(),
                "source" to "webweavex"
            )
        } catch (e: Exception) {
            linkedMapOf(
                "type" to "webweavex_memory",
                "entities" to emptyList<Map<String, Any>>(),
                "relations" to emptyList<Map<String, Any>>(),
                "graph" to createEmptyGraph(),
                "timestamp" to Instant.now().toString(),
                "source" to "webweavex"
            )
        }
    }

    @Suppress("UNCHECKED_CAST")
    fun toRagChunks(result: Map<String, Any>): List<Map<String, Any>> {
        return try {
            val chunks = result["chunks"] as? List<Map<String, Any>> ?: emptyList()
            val entities = result["entities"] as? List<Map<String, String>> ?: emptyList()
            val relations = result["relations"] as? List<Map<String, String>> ?: emptyList()

            chunks.map { chunk ->
                linkedMapOf(
                    "text" to (chunk["text"] ?: ""),
                    "metadata" to linkedMapOf(
                        "entities" to entities,
                        "relations" to relations.take(5),
                        "source" to "webweavex"
                    )
                )
            }
        } catch (e: Exception) {
            emptyList()
        }
    }

    fun extractStream(text: String): Sequence<String> {
        return sequenceOf("cleaning", "chunking", "entities", "relations", "graph", "insights")
    }

    fun prettyPrint(result: Map<String, Any>): String {
        val sb = StringBuilder()
        sb.appendLine("==================================================")
        sb.appendLine("WebWeaveX Analysis")
        sb.appendLine("==================================================")
        sb.appendLine()
        sb.appendLine("ENTITY SUMMARY:")
        sb.appendLine("------------------------------")

        val insights = result["insights"] as? Map<*, *>
        val entityCounts = insights?.get("entity_counts") as? Map<String, Int>
        entityCounts?.forEach { (key, count) ->
            sb.appendLine("  $key: $count")
        }

        val stats = insights?.get("stats") as? Map<String, Any>
        if (stats != null) {
            sb.appendLine()
            sb.appendLine("STATISTICS:")
            sb.appendLine("------------------------------")
            sb.appendLine("  Total Entities: ${stats["total_entities"] ?: 0}")
            sb.appendLine("  Unique Entities: ${stats["unique_entities"] ?: 0}")
            sb.appendLine("  Entity Types: ${stats["entity_types"] ?: 0}")
            sb.appendLine("  Total Relations: ${stats["total_relations"] ?: 0}")
            sb.appendLine("  Total Chunks: ${stats["total_chunks"] ?: 0}")
            sb.appendLine("  Text Length: ${stats["text_length"] ?: 0}")
            sb.appendLine("  Word Count: ${stats["word_count"] ?: 0}")
        }

        sb.appendLine()
        sb.appendLine("==================================================")
        return sb.toString()
    }

    companion object {
        fun getToolSchema(): Map<String, Any> {
            return linkedMapOf(
                "name" to "webweavex_extract",
                "description" to "Extract structured intelligence from text",
                "parameters" to linkedMapOf(
                    "type" to "object",
                    "properties" to linkedMapOf(
                        "input" to linkedMapOf("type" to "string")
                    ),
                    "required" to listOf("input")
                )
            )
        }

        fun getAllTools(): List<Map<String, Any>> {
            return listOf(
                getToolSchema(),
                linkedMapOf(
                    "name" to "webweavex_entities",
                    "description" to "Extract only entities from text",
                    "parameters" to linkedMapOf(
                        "type" to "object",
                        "properties" to linkedMapOf(
                            "input" to linkedMapOf("type" to "string")
                        ),
                        "required" to listOf("input")
                    )
                )
            )
        }

        fun getCapabilities(): List<String> {
            return listOf(
                "extract", "entities", "graph", "rag",
                "agent_mode", "memory_export", "streaming"
            )
        }

        private fun createEmptyGraph(): Map<String, Any> {
            return linkedMapOf(
                "nodes" to emptyList<Map<String, Any>>(),
                "edges" to emptyList<Map<String, Any>>()
            )
        }
    }

    private fun createErrorResult(): Map<String, Any> {
        return linkedMapOf(
            "meta" to linkedMapOf("title" to "", "url" to ""),
            "content" to linkedMapOf("text" to ""),
            "chunks" to emptyList<Map<String, Any>>(),
            "entities" to emptyList<Map<String, Any>>(),
            "relations" to emptyList<Map<String, Any>>(),
            "graph" to createEmptyGraph(),
            "insights" to linkedMapOf(
                "entity_counts" to emptyMap<String, Int>(),
                "stats" to emptyMap<String, Any>(),
                "top_entities" to emptyList<Map<String, Any>>()
            )
        )
    }
}
