package io.webweavex

import io.webweavex.runtime.*
import io.webweavex.repository.*
import io.webweavex.extract.ExtractionPipeline
import io.webweavex.extract.ExtractionRequest
import io.webweavex.memory.MemoryEngine
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import io.webweavex.replay.ReplayEngine
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.serialization.CanonicalSerialization
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ReleaseCandidateTest {
    private val sampleGraph = KnowledgeGraph(
        listOf(
            KnowledgeNode("n1", "file", mapOf("name" to "Main.kt", "lang" to "kotlin")),
            KnowledgeNode("n2", "module", mapOf("name" to "core", "lang" to "kotlin")),
            KnowledgeNode("n3", "file", mapOf("name" to "Utils.java", "lang" to "java")),
            KnowledgeNode("n4", "config", mapOf("name" to "build.gradle.kts", "lang" to "kotlin"))
        ),
        listOf(
            KnowledgeEdge("n1", "n2", "imports"),
            KnowledgeEdge("n3", "n2", "imports"),
            KnowledgeEdge("n4", "n1", "configures")
        )
    )

    @Test
    fun `1 - API freeze - all data classes immutable`() {
        val node = KnowledgeNode("id", "type", mapOf("k" to "v"))
        val edge = KnowledgeEdge("s", "t", "r")
        val graph = KnowledgeGraph(listOf(node), listOf(edge))
        assertEquals("id", node.id)
        assertEquals("s", edge.source)
        assertEquals(1, graph.nodes.size)
    }

    @Test
    fun `2 - API freeze - deterministic fingerprint`() {
        val a = Fingerprint.compute(mapOf("x" to 1))
        val b = Fingerprint.compute(mapOf("x" to 1))
        assertEquals(a, b)
        assertEquals(64, a.length)
    }

    @Test
    fun `3 - API freeze - deterministic serialization`() {
        val data = mapOf("z" to 1, "a" to 2, "m" to mapOf("b" to 3))
        assertEquals(CanonicalSerialization.serialize(data), CanonicalSerialization.serialize(data))
    }

    @Test
    fun `4 - index lifecycle - build produces consistent index`() {
        val i1 = SearchIndex.build(sampleGraph)
        val i2 = SearchIndex.build(sampleGraph)
        assertEquals(i1.fingerprint, i2.fingerprint)
        assertEquals(i1.size, i2.size)
        assertEquals(i1.size, 4)
    }

    @Test
    fun `5 - prepared execution - session reuses index`() {
        val session = QuerySession(sampleGraph)
        val r1 = session.search("kotlin")
        val r2 = session.search("kotlin")
        assertEquals(r1.totalMatches, r2.totalMatches)
        assertTrue(session.metrics().totalQueries == 2)
    }

    @Test
    fun `6 - indexed vs fallback equivalence`() {
        val indexed = QueryEngine.search(sampleGraph, "kotlin", useIndex = true)
        val fallback = QueryEngine.search(sampleGraph, "kotlin", useIndex = false)
        assertEquals(indexed.totalMatches, fallback.totalMatches)
        assertEquals(indexed.indexed, true)
        assertEquals(fallback.indexed, false)
    }

    @Test
    fun `7 - type filtering`() {
        val r = QueryEngine.filterByType(sampleGraph, "file")
        assertEquals(2, r.totalMatches)
    }

    @Test
    fun `8 - relationship queries`() {
        val r = QueryEngine.findByRelationship(sampleGraph, "imports")
        assertEquals(2, r.totalMatches)
    }

    @Test
    fun `9 - boolean queries`() {
        val r = QueryEngine.booleanQuery(sampleGraph, must = listOf("kotlin"), mustNot = listOf("java"))
        assertTrue(r.totalMatches >= 1)
    }

    @Test
    fun `10 - query planner diagnostics`() {
        val plan = QueryPlanner.plan("kotlin", sampleGraph)
        assertTrue(plan.diagnostics.isNotEmpty())
        assertTrue(plan.strategy.isNotEmpty())
    }

    @Test
    fun `11 - node lookup O1 access`() {
        val lookup = NodeLookup.build(sampleGraph)
        assertEquals("n1", lookup.get("n1")?.id)
        assertTrue(lookup.contains("n1"))
        assertEquals(4, lookup.size())
    }

    @Test
    fun `12 - memory engine`() {
        var store = MemoryEngine.create()
        store = store.put("k1", "v1")
        store = store.put("k2", 42)
        assertEquals("v1", store.get("k1"))
        assertEquals(42, store.get("k2"))
    }

    @Test
    fun `13 - workflow engine`() {
        val steps = listOf(
            WorkflowStep("s1", { mapOf("out" to 1) }),
            WorkflowStep("s2", { mapOf("out" to 2) })
        )
        val result = WorkflowEngine.execute(steps, emptyMap())
        assertTrue(result.success)
    }

    @Test
    fun `14 - replay engine`() {
        val state = mapOf("key" to "value")
        val snap = ReplayEngine.createSnapshot(state, 0)
        assertTrue(snap.fingerprint.isNotEmpty())
        assertEquals(state, snap.state)
    }

    @Test
    fun `15 - extraction pipeline`() {
        val result = ExtractionPipeline.extract(ExtractionRequest("<html><h1>Test</h1></html>"))
        assertTrue(result.content.isNotEmpty())
    }

    @Test
    fun `16 - runtime kernel`() {
        val kernel = RuntimeKernel.create()
        val output = kernel.extract(UniversalInput("<html>test</html>"))
        assertTrue(output.isValid())
        assertEquals("3.0.0", output.version)
    }

    @Test
    fun `17 - large graph performance`() {
        val nodes = (1..1000).map { KnowledgeNode("n$it", "type${it % 10}", mapOf("data" to "item_$it")) }
        val edges = (1..999).map { KnowledgeEdge("n$it", "n${it + 1}", "link") }
        val graph = KnowledgeGraph(nodes, edges)
        val session = QuerySession(graph)
        val start = System.nanoTime()
        repeat(100) { session.search("item_${it * 10}") }
        val elapsed = (System.nanoTime() - start) / 1_000_000
        assertEquals(100, session.metrics().totalQueries)
        assertTrue(elapsed < 5000)
    }

    @Test
    fun `18 - tokenizer determinism`() {
        val t1 = DeterministicTokenizer.tokenize("Hello World 123")
        val t2 = DeterministicTokenizer.tokenize("Hello World 123")
        assertEquals(t1, t2)
        assertTrue(t1.contains("hello"))
        assertTrue(t1.contains("world"))
        assertTrue(t1.contains("123"))
    }

    @Test
    fun `19 - search index statistics`() {
        val index = SearchIndex.build(sampleGraph)
        val stats = index.statistics()
        assertEquals(4, stats["totalNodes"])
        assertTrue((stats["uniqueTokens"] as Int) > 0)
        assertTrue((stats["uniqueTypes"] as Int) > 0)
    }

    @Test
    fun `20 - language detection`() {
        assertEquals("Kotlin", LanguageDetector.detect(java.io.File("test.kt")))
        assertEquals("Java", LanguageDetector.detect(java.io.File("Main.java")))
        assertEquals("Python", LanguageDetector.detect(java.io.File("app.py")))
    }

    @Test
    fun `21 - cross-SDK fingerprint consistency`() {
        val data = mapOf("version" to "3.0.0", "type" to "test")
        val fp1 = Fingerprint.compute(data)
        val fp2 = Fingerprint.compute(data)
        assertEquals(fp1, fp2)
        assertEquals(64, fp1.length)
        assertTrue(fp1.all { it in '0'..'9' || it in 'a'..'f' })
    }

    @Test
    fun `22 - search field index`() {
        val index = SearchIndex.build(sampleGraph)
        val results = index.searchByField("lang", "kotlin")
        assertTrue(results.isNotEmpty())
        assertTrue(results.contains("n1"))
    }

    @Test
    fun `23 - search type index`() {
        val index = SearchIndex.build(sampleGraph)
        val files = index.searchByType("file")
        assertEquals(2, files.size)
        assertTrue(files.contains("n1"))
        assertTrue(files.contains("n3"))
    }

    @Test
    fun `24 - session index statistics`() {
        val session = QuerySession(sampleGraph)
        val stats = session.indexStatistics()
        assertEquals(4, stats["totalNodes"])
    }

    @Test
    fun `25 - empty graph handling`() {
        val graph = KnowledgeGraph(emptyList(), emptyList())
        val session = QuerySession(graph)
        val r = session.search("anything")
        assertEquals(0, r.totalMatches)
    }
}
