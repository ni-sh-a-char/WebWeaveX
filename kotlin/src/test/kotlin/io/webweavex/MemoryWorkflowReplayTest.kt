package io.webweavex

import io.webweavex.memory.*
import io.webweavex.workflow.*
import io.webweavex.replay.*
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.repository.RepositoryAnalyzer
import io.webweavex.extract.ExtractionPipeline
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class MemoryWorkflowReplayTest {
    @Test
    fun `memory store put and get`() {
        var store = MemoryEngine.create()
        store = store.put("key1", "value1")
        store = store.put("key2", 42)
        assertEquals("value1", store.get("key1"))
        assertEquals(42, store.get("key2"))
        assertEquals(2, store.size())
    }

    @Test
    fun `memory store is deterministic`() {
        var store = MemoryEngine.create()
        store = store.put("key1", "value1")
        val fp1 = store.fingerprint()
        val fp2 = store.fingerprint()
        assertEquals(fp1, fp2)
    }

    @Test
    fun `memory snapshot captures state`() {
        var store = MemoryEngine.create()
        store = store.put("key1", "value1")
        val snapshot = store.snapshot()
        assertEquals(1, snapshot.entries.size)
        assertTrue(snapshot.fingerprint.isNotEmpty())
    }

    @Test
    fun `memory merge combines stores`() {
        var a = MemoryEngine.create()
        a = a.put("a", 1)
        var b = MemoryEngine.create()
        b = b.put("b", 2)
        val merged = MemoryEngine.merge(a, b)
        assertEquals(2, merged.size())
        assertEquals(1, merged.get("a"))
        assertEquals(2, merged.get("b"))
    }

    @Test
    fun `workflow executes steps`() {
        val step1 = WorkflowStep("normalize", { mapOf("normalized" to true) })
        val step2 = WorkflowStep("extract", { mapOf("extracted" to true) }, listOf("normalize"))
        val steps = listOf(step1, step2)
        val result = WorkflowEngine.execute(steps, mapOf("input" to "data"))
        assertTrue(result.success)
        assertEquals(2, result.steps.size)
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `workflow is deterministic`() {
        val steps = listOf(WorkflowStep("step1", { mapOf("output" to "value") }))
        val r1 = WorkflowEngine.execute(steps, emptyMap())
        val r2 = WorkflowEngine.execute(steps, emptyMap())
        assertEquals(r1.fingerprint, r2.fingerprint)
    }

    @Test
    fun `replay snapshot creation`() {
        val state = mapOf("key" to "value")
        val snapshot = ReplayEngine.createSnapshot(state, 0)
        assertTrue(snapshot.fingerprint.isNotEmpty())
        assertEquals(0, snapshot.stepIndex)
    }

    @Test
    fun `replay equivalence validation`() {
        val state = mapOf("key" to "value")
        val a = ReplayEngine.createSnapshot(state, 0)
        val b = ReplayEngine.createSnapshot(state, 1)
        assertTrue(ReplayEngine.validateEquivalence(a, b))
    }

    @Test
    fun `replay execution`() {
        val snapshots = listOf(
            ReplayEngine.createSnapshot(mapOf("step" to "1"), 0),
            ReplayEngine.createSnapshot(mapOf("step" to "1"), 1)
        )
        val result = ReplayEngine.replay(snapshots)
        assertTrue(result.equivalent)
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `extraction pipeline produces fingerprint`() {
        val result = ExtractionPipeline.extractText("<html><body>test</body></html>")
        assertTrue(result.fingerprint.isNotEmpty())
        assertEquals(64, result.fingerprint.length)
    }

    @Test
    fun `repository analysis produces fingerprint`() {
        val result = RepositoryAnalyzer.analyze("test input")
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `complete workflow with memory`() {
        var store = MemoryEngine.create()
        store = store.put("extraction_result", "data")
        val result = ExtractionPipeline.extractText("<html><body>workflow test</body></html>")
        store = store.put("fingerprint", result.fingerprint)
        assertTrue(store.get("extraction_result") == "data")
        assertTrue(store.fingerprint().isNotEmpty())
    }
}
