package io.webweavex.repository

import io.webweavex.fingerprint.Fingerprint

class SearchIndex(
    val tokenIndex: Map<String, List<String>>,
    val typeIndex: Map<String, List<String>>,
    val fieldIndex: Map<String, Map<String, List<String>>>,
    val fingerprint: String
) {
    companion object {
        fun build(graph: KnowledgeGraph): SearchIndex {
            val tokenIndex = mutableMapOf<String, MutableList<String>>()
            val typeIndex = mutableMapOf<String, MutableList<String>>()
            val fieldIndex = mutableMapOf<String, MutableMap<String, MutableList<String>>>()

            for (node in graph.nodes) {
                val tokens = mutableSetOf<String>()
                tokens.addAll(DeterministicTokenizer.tokenize(node.id))
                tokens.addAll(DeterministicTokenizer.tokenize(node.type))
                node.data.forEach { (field, value) ->
                    tokens.addAll(DeterministicTokenizer.tokenize(value.toString()))
                    fieldIndex.getOrPut(field) { mutableMapOf() }
                        .getOrPut(value.toString().lowercase()) { mutableListOf() }
                        .add(node.id)
                }
                tokens.forEach { token ->
                    tokenIndex.getOrPut(token) { mutableListOf() }.add(node.id)
                }
                typeIndex.getOrPut(node.type.lowercase()) { mutableListOf() }.add(node.id)
            }

            val fp = Fingerprint.compute(mapOf(
                "tokens" to tokenIndex.keys.sorted(),
                "types" to typeIndex.keys.sorted(),
                "fields" to fieldIndex.keys.sorted()
            ))

            return SearchIndex(
                tokenIndex = tokenIndex.mapValues { it.value.distinct().sorted() },
                typeIndex = typeIndex.mapValues { it.value.distinct().sorted() },
                fieldIndex = fieldIndex.mapValues { entry -> entry.value.mapValues { it.value.distinct().sorted() } },
                fingerprint = fp
            )
        }
    }

    fun search(query: String): List<String> {
        val tokens = DeterministicTokenizer.tokenize(query)
        if (tokens.isEmpty()) return emptyList()
        var result = (tokenIndex[tokens[0]] ?: emptyList()).toMutableSet()
        for (token in tokens.drop(1)) {
            result = result.intersect(tokenIndex[token] ?: emptySet()).toMutableSet()
        }
        return result.sorted()
    }

    fun searchByType(type: String): List<String> {
        return typeIndex[type.lowercase()]?.sorted() ?: emptyList()
    }

    fun searchByField(field: String, value: String): List<String> {
        return fieldIndex[field]?.get(value.lowercase())?.sorted() ?: emptyList()
    }
}
