package io.webweavex

import io.webweavex.runtime.*
import io.webweavex.repository.*
import io.webweavex.extract.ExtractionPipeline
import io.webweavex.memory.MemoryEngine
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import io.webweavex.replay.ReplayEngine
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.serialization.CanonicalSerialization
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ReleaseValidationTest {
    @Test
    fun `API consistency - extract produces UniversalOutput`() {
        val kernel = RuntimeKernel.create()
        val input = UniversalInput(source = "<html>test</html>")
        val output = kernel.extract(input)
        assertTrue(output.isValid())
        assertEquals("3.0.0", output.version)
    }

    @Test
    fun `API consistency - fingerprint is deterministic`() {
        val data = mapOf("key" to "value")
        val h1 = Fingerprint.compute(data)
        val h2 = Fingerprint.compute(data)
        assertEquals(h1, h2)
        assertEquals(64, h1.length)
    }

    @Test
    fun `API consistency - serialization is deterministic`() {
        val data = mapOf("z" to 1, "a" to 2)
        val s1 = CanonicalSerialization.serialize(data)
        val s2 = CanonicalSerialization.serialize(data)
        assertEquals(s1, s2)
    }

    @Test
    fun `API consistency - query session uses prepared execution`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test"))),
            emptyList()
        )
        val session = QuerySession(graph)
        val r1 = session.search("test")
        val r2 = session.search("test")
        assertEquals(r1.totalMatches, r2.totalMatches)
        assertTrue(session.metrics().totalQueries >= 2)
    }

    @Test
    fun `API consistency - workflow execution`() {
        val steps = listOf(WorkflowStep("step1", { mapOf("result" to 1) }))
        val result = WorkflowEngine.execute(steps, emptyMap())
        assertTrue(result.success)
    }

    @Test
    fun `API consistency - memory operations`() {
        var store = MemoryEngine.create()
        store = store.put("key", "value")
        assertEquals("value", store.get("key"))
    }

    @Test
    fun `API consistency - replay equivalence`() {
        val state = mapOf("key" to "value")
        val snap = ReplayEngine.createSnapshot(state, 0)
        assertTrue(snap.fingerprint.isNotEmpty())
    }

    @Test
    fun `API consistency - extraction pipeline`() {
        val result = ExtractionPipeline.extractText("<html>test</html>")
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `API consistency - repository analysis`() {
        val result = RepositoryAnalyzerEngine.analyze(java.io.File("."))
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `API consistency - language detection`() {
        assertEquals("Kotlin", LanguageDetector.detect(java.io.File("test.kt")))
        assertEquals("Java", LanguageDetector.detect(java.io.File("Main.java")))
    }

    @Test
    fun `API consistency - search index`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "file", mapOf("name" to "test"))),
            emptyList()
        )
        val index = SearchIndex.build(graph)
        assertTrue(index.search("test").isNotEmpty())
    }
}
