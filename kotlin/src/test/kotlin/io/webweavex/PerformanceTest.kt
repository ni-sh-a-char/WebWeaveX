package io.webweavex

import io.webweavex.repository.*
import io.webweavex.extract.ExtractionPipeline
import io.webweavex.memory.MemoryEngine
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import io.webweavex.replay.ReplayEngine
import io.webweavex.fingerprint.Fingerprint
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class PerformanceTest {
    @Test
    fun `search index builds from knowledge graph`() {
        val nodes = listOf(
            KnowledgeNode("n1", "file", mapOf("name" to "test")),
            KnowledgeNode("n2", "module", mapOf("name" to "production")),
            KnowledgeNode("n3", "file", mapOf("name" to "test"))
        )
        val edges = listOf(KnowledgeEdge("n1", "n2", "imports"), KnowledgeEdge("n2", "n3", "uses"))
        val graph = KnowledgeGraph(nodes, edges)
        val index = SearchIndex.build(graph)
        assertTrue(index.fingerprint.isNotEmpty())
    }

    @Test
    fun `search index finds tokens`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "hello world")), KnowledgeNode("n2", "module", mapOf("name" to "other"))),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        val results = index.search("hello")
        assertEquals(1, results.size)
        assertEquals("n1", results[0])
    }

    @Test
    fun `search index multi-word query`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "hello world")),
                KnowledgeNode("n2", "file", mapOf("name" to "hello there"))
            ),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        val results = index.search("hello world")
        assertEquals(1, results.size)
        assertEquals("n1", results[0])
    }

    @Test
    fun `query engine with scoring`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "test"))),
            emptyList()
        )
        val result = QueryEngine.search(graph, "test")
        assertEquals(2, result.totalMatches)
        assertTrue(result.scoring.isNotEmpty())
        assertTrue(result.ranking.isNotEmpty())
    }

    @Test
    fun `boolean query with must and mustNot`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "test")),
                KnowledgeNode("n2", "module", mapOf("name" to "other"))
            ),
            emptyList()
        )
        val result = QueryEngine.booleanQuery(graph, must = listOf("test"), mustNot = listOf("other"))
        assertEquals(1, result.totalMatches)
        assertEquals("n1", result.matches[0]["id"])
    }

    @Test
    fun `large workflow execution`() {
        val steps = (1..100).map { i ->
            WorkflowStep("step_$i", { mapOf("step" to i) }, if (i > 1) listOf("step_${i - 1}") else emptyList())
        }
        val result = WorkflowEngine.execute(steps, emptyMap())
        assertTrue(result.success)
        assertEquals(100, result.executionOrder.size)
    }

    @Test
    fun `memory store scales`() {
        var store = MemoryEngine.create()
        repeat(1000) { store = store.put("key_$it", "value_$it") }
        assertEquals(1000, store.size())
        assertTrue(store.fingerprint().isNotEmpty())
    }

    @Test
    fun `replay with many snapshots`() {
        val state = mapOf("key" to "value"); val snapshots = (0..99).map { io.webweavex.replay.ReplayEngine.createSnapshot(state, it) }
        val result = io.webweavex.replay.ReplayEngine.replay(snapshots)
        assertTrue(result.equivalent)
        assertEquals(100, result.snapshots.size)
    }
}
