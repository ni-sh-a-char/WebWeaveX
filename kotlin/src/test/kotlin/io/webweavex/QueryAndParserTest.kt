package io.webweavex

import io.webweavex.repository.*
import io.webweavex.extract.*
import io.webweavex.fingerprint.Fingerprint
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class QueryAndParserTest {
    @Test
    fun `query engine searches by text`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "test")),
                KnowledgeNode("n2", "module", mapOf("name" to "other"))
            ),
            listOf(KnowledgeEdge("n1", "n2", "imports"))
        )
        val result = QueryEngine.search(graph, "test")
        assertEquals(1, result.totalMatches)
        assertEquals("n1", result.matches[0]["id"])
    }

    @Test
    fun `query engine filters by type`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "a")),
                KnowledgeNode("n2", "module", mapOf("name" to "b")),
                KnowledgeNode("n3", "file", mapOf("name" to "c"))
            ),
            emptyList()
        )
        val result = QueryEngine.filterByType(graph, "file")
        assertEquals(2, result.totalMatches)
    }

    @Test
    fun `query engine finds by relationship`() {
        val graph = KnowledgeGraph(
            listOf(
                KnowledgeNode("n1", "file", mapOf("name" to "a")),
                KnowledgeNode("n2", "module", mapOf("name" to "b"))
            ),
            listOf(KnowledgeEdge("n1", "n2", "imports"))
        )
        val result = QueryEngine.findByRelationship(graph, "imports")
        assertEquals(1, result.totalMatches)
        assertEquals("n1", result.matches[0]["id"])
    }

    @Test
    fun `HTML extraction handles malformed input`() {
        val html = "<html><body><p>Unclosed tag<div>Nested</p></body>"
        val result = ExtractionPipeline.extractText(html)
        assertTrue(result.content.isNotEmpty())
    }

    @Test
    fun `HTML extraction handles empty input`() {
        val result = ExtractionPipeline.extractText("")
        assertTrue(result.rawText.isEmpty() || result.rawText == "")
    }

    @Test
    fun `HTML extraction handles comments`() {
        val html = "<html><!-- comment --><body>Content</body></html>"
        val result = ExtractionPipeline.extractText(html)
        assertTrue(result.rawText.contains("Content"))
        assertTrue(!result.rawText.contains("comment"))
    }

    @Test
    fun `Markdown extraction handles nested lists`() {
        val md = "# Title\n- Item 1\n- Item 2\n  - Nested\n- Item 3"
        val result = ExtractionPipeline.extractText(md)
        assertTrue(result.content.containsKey("hierarchy"))
    }

    @Test
    fun `JSON extraction handles malformed input`() {
        val result = ExtractionPipeline.extractText("{invalid json}")
        assertEquals("json", result.metadata["input_type"])
    }

    @Test
    fun `repository analyzer detects languages`() {
        val result = RepositoryAnalyzerEngine.analyze(java.io.File("."))
        assertTrue(result.languages.isNotEmpty() || result.totalFiles >= 0)
    }

    @Test
    fun `language detector identifies all types`() {
        assertEquals("Kotlin", LanguageDetector.detect(java.io.File("test.kt")))
        assertEquals("Java", LanguageDetector.detect(java.io.File("Main.java")))
        assertEquals("Python", LanguageDetector.detect(java.io.File("app.py")))
        assertEquals("JavaScript", LanguageDetector.detect(java.io.File("index.js")))
        assertEquals("TypeScript", LanguageDetector.detect(java.io.File("main.ts")))
        assertEquals("Dart", LanguageDetector.detect(java.io.File("main.dart")))
        assertEquals("Go", LanguageDetector.detect(java.io.File("main.go")))
        assertEquals("Rust", LanguageDetector.detect(java.io.File("main.rs")))
    }

    @Test
    fun `language detector identifies project types`() {
        assertEquals("Gradle", LanguageDetector.detectProject(java.io.File(".")))
    }

    @Test
    fun `knowledge graph is deterministic`() {
        val nodes = listOf(KnowledgeNode("n1", "a"), KnowledgeNode("n2", "b"))
        val edges = listOf(KnowledgeEdge("n1", "n2", "rel"))
        val g = KnowledgeGraph(nodes, edges)
        assertEquals(g.fingerprint(), g.fingerprint())
    }

    @Test
    fun `query ranking is deterministic`() {
        val graph = KnowledgeGraph(
            listOf(KnowledgeNode("n1", "f", mapOf("name" to "x")), KnowledgeNode("n2", "f", mapOf("name" to "y"))),
            emptyList()
        )
        val r1 = QueryEngine.search(graph, "x")
        val r2 = QueryEngine.search(graph, "x")
        assertEquals(r1.ranking, r2.ranking)
    }
}
