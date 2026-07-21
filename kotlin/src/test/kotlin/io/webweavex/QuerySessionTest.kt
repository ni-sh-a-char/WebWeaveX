package io.webweavex

import io.webweavex.repository.*
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class QuerySessionTest {
    @Test
    fun `query session reuses index`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "other"))),
            listOf(KnowledgeEdge("n1", "n2", "imports"))
        )
        val session = QuerySession(graph)
        val r1 = session.search("test")
        val r2 = session.search("test")
        assertEquals(r1.totalMatches, r2.totalMatches)
    }

    @Test
    fun `query session tracks metrics`() {
        val graph = KnowledgeGraph(listOf(KnowledgeNode("n1", "file", mapOf("name" to "test"))), emptyList())
        val session = QuerySession(graph)
        session.search("test")
        session.search("other")
        val m = session.metrics()
        assertEquals(2, m.totalQueries)
        assertTrue(m.totalLatencyMs >= 0)
    }

    @Test
    fun `query session filter by type`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "a")), KnowledgeNode("n2", "module", mapOf("name" to "b"))),
            emptyList()
        )
        val session = QuerySession(graph)
        val r = session.filterByType("file")
        assertEquals(1, r.totalMatches)
    }

    @Test
    fun `query session statistics`() {
        val graph = KnowledgeGraph(listOf(KnowledgeNode("n1", "file", mapOf("name" to "test"))), emptyList())
        val session = QuerySession(graph)
        val stats = session.indexStatistics()
        assertTrue(stats.containsKey("totalNodes"))
        assertTrue(stats.containsKey("uniqueTokens"))
    }
}
