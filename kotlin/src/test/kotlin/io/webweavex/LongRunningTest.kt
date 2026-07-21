package io.webweavex

import io.webweavex.repository.*
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class LongRunningTest {
    @Test
    fun `session handles many repeated queries`() {
        val graph = KnowledgeGraph(
            (1..100).map { KnowledgeNode("n$it", "type${it % 5}", mapOf("name" to "item_$it")) },
            (1..99).map { KnowledgeEdge("n$it", "n${it + 1}", "depends_on") }
        )
        val session = QuerySession(graph)
        repeat(1000) { session.search("item_${it % 100}") }
        val m = session.metrics()
        assertEquals(1000, m.totalQueries)
        assertTrue(m.totalLatencyMs >= 0)
    }

    @Test
    fun `session handles mixed queries`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "other"))),
            listOf(KnowledgeEdge("n1", "n2", "imports"))
        )
        val session = QuerySession(graph)
        session.search("test")
        session.filterByType("file")
        session.findByRelationship("imports")
        assertEquals(2, session.metrics().totalQueries)
    }

    @Test
    fun `multiple independent sessions`() {
        val graph = KnowledgeGraph(listOf(KnowledgeNode("n1", "file", mapOf("name" to "test"))), emptyList())
        val s1 = QuerySession(graph)
        val s2 = QuerySession(graph)
        val r1 = s1.search("test")
        val r2 = s2.search("test")
        assertEquals(r1.totalMatches, r2.totalMatches)
        assertEquals(1, s1.metrics().totalQueries)
        assertEquals(1, s2.metrics().totalQueries)
    }

    @Test
    fun `index rebuild produces consistent results`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "other"))),
            emptyList()
        )
        val i1 = SearchIndex.build(graph)
        val i2 = SearchIndex.build(graph)
        assertEquals(i1.fingerprint, i2.fingerprint)
        assertEquals(i1.size, i2.size)
    }

    @Test
    fun `session metrics are accurate`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "other"))),
            emptyList()
        )
        val session = QuerySession(graph)
        session.search("test")
        session.search("nonexistent")
        session.filterByType("file")
        val m = session.metrics()
        assertEquals(3, m.totalQueries)
        assertTrue(m.indexedQueries >= 0)
    }
}
