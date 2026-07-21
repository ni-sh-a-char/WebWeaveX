package io.webweavex.repository

data class QueryPlan(
    val strategy: String,
    val indexed: Boolean,
    val diagnostics: List<String>
)

object QueryPlanner {
    fun plan(query: String, graph: KnowledgeGraph, useIndex: Boolean = true): QueryPlan {
        val diagnostics = mutableListOf<String>()
        
        if (!useIndex) {
            diagnostics.add("Index disabled, using linear scan")
            return QueryPlan("linear_scan", false, diagnostics)
        }
        
        if (query.isBlank()) {
            diagnostics.add("Empty query, using linear scan")
            return QueryPlan("linear_scan", false, diagnostics)
        }
        
        if (graph.nodes.isEmpty()) {
            diagnostics.add("Empty graph, returning empty result")
            return QueryPlan("empty_graph", false, diagnostics)
        }
        
        // Check if query looks like a type filter
        val tokens = DeterministicTokenizer.tokenize(query)
        if (tokens.size == 1 && graph.nodes.any { it.type.equals(tokens[0], ignoreCase = true) }) {
            diagnostics.add("Single-token type match, using type index")
            return QueryPlan("type_index", true, diagnostics)
        }
        
        diagnostics.add("Using token index for multi-token query")
        return QueryPlan("token_index", true, diagnostics)
    }
}
