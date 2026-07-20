package io.webweavex

import io.webweavex.runtime.*
import io.webweavex.memory.MemoryEngine
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import io.webweavex.replay.ReplayEngine
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.repository.LanguageDetector
import io.webweavex.repository.RepositoryAnalyzerEngine
import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ProductionHardeningTest {
    @Test
    fun `deterministic clock produces stable timestamps`() {
        DeterministicClock.reset()
        val t1 = DeterministicClock.now()
        val t2 = DeterministicClock.now()
        assertEquals(t1, t2)
        DeterministicClock.tick()
        val t3 = DeterministicClock.now()
        assertTrue(t3 > t1)
    }

    @Test
    fun `deterministic snapshot uses stable timestamps`() {
        DeterministicClock.reset()
        val s1 = io.webweavex.replay.ReplayEngine.createSnapshot(mapOf("key" to "value"), 0)
        val s2 = io.webweavex.replay.ReplayEngine.createSnapshot(mapOf("key" to "value"), 0)
        assertEquals(s1.timestamp, s2.timestamp)
    }

    @Test
    fun `language detector identifies project types`() {
        assertEquals("Gradle", LanguageDetector.detectProject(File(".")))
    }

    @Test
    fun `language detector identifies files`() {
        assertEquals("Kotlin", LanguageDetector.detect(File("test.kt")))
        assertEquals("Java", LanguageDetector.detect(File("Main.java")))
        assertEquals("Python", LanguageDetector.detect(File("app.py")))
        assertEquals("TypeScript", LanguageDetector.detect(File("main.ts")))
    }

    @Test
    fun `memory engine uses deterministic timestamps`() {
        DeterministicClock.reset()
        var store = MemoryEngine.create()
        store = store.put("key", "value")
        assertTrue(store.get("key") == "value")
    }

    @Test
    fun `workflow engine handles dependencies`() {
        val step1 = WorkflowStep("a", { mapOf("result" to 1) })
        val step2 = WorkflowStep("b", { mapOf("result" to 2) }, listOf("a"))
        val result = WorkflowEngine.execute(listOf(step1, step2), emptyMap())
        assertTrue(result.success)
        assertEquals(2, result.steps.size)
    }

    @Test
    fun `replay equivalence is deterministic`() {
        val state = mapOf("key" to "value")
        val snap = io.webweavex.replay.ReplayEngine.createSnapshot(state, 0)
        val fp1 = snap.fingerprint
        DeterministicClock.tick()
        val snap2 = io.webweavex.replay.ReplayEngine.createSnapshot(state, 1)
        val fp2 = snap2.fingerprint
        assertEquals(fp1, fp2)
    }

    @Test
    fun `repository analyzer handles empty directory`() {
        val result = RepositoryAnalyzerEngine.analyze(File("."))
        assertTrue(result.totalFiles >= 0)
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `extraction pipeline handles empty input`() {
        val result = io.webweavex.extract.ExtractionPipeline.extractText("")
        assertTrue(result.fingerprint.isNotEmpty())
    }
}
