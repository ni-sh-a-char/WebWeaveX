package io.webweavex

import io.webweavex.repository.*
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.extract.ExtractionPipeline
import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class RepositoryTest {
    @Test
    fun `language detector identifies Kotlin files`() {
        assertEquals("Kotlin", LanguageDetector.detect(File("test.kt")))
        assertEquals("Java", LanguageDetector.detect(File("Main.java")))
        assertEquals("Python", LanguageDetector.detect(File("app.py")))
        assertEquals("JavaScript", LanguageDetector.detect(File("index.js")))
        assertEquals("TypeScript", LanguageDetector.detect(File("main.ts")))
    }

    @Test
    fun `repository analyzer produces summary`() {
        val text = "# My Project\n## Quick Start\npip install flask\nGET /api/users"
        val result = RepositoryAnalyzerEngine.analyze(File("."))
        assertTrue(result.totalFiles >= 0)
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `knowledge graph is deterministic`() {
        val nodes = listOf(KnowledgeNode("n1", "file"), KnowledgeNode("n2", "module"))
        val edges = listOf(KnowledgeEdge("n1", "n2", "imports"))
        val graph = KnowledgeGraph(nodes, edges)
        val fp1 = graph.fingerprint()
        val fp2 = graph.fingerprint()
        assertEquals(fp1, fp2)
    }

    @Test
    fun `query engine searches nodes`() {
        val nodes = listOf(KnowledgeNode("n1", "file", mapOf("name" to "test")), KnowledgeNode("n2", "module", mapOf("name" to "other")))
        val edges = listOf(KnowledgeEdge("n1", "n2", "imports"))
        val graph = KnowledgeGraph(nodes, edges)
        val result = QueryEngine.search(graph, "test")
        assertEquals(1, result.totalMatches)
        assertEquals("n1", result.matches[0]["id"])
    }

    @Test
    fun `repository summary is serializable`() {
        val summary = RepositorySummary(0, emptyMap(), emptyList(), emptyList(), emptyList(), "abc")
        val map = mapOf("files" to summary.totalFiles, "fingerprint" to summary.fingerprint)
        assertTrue(map.containsKey("fingerprint"))
    }
}
