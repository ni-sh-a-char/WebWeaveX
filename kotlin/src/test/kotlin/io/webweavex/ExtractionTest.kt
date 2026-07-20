package io.webweavex

import io.webweavex.extract.*
import io.webweavex.fingerprint.Fingerprint
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ExtractionTest {
    @Test
    fun `HTML extraction extracts title and text`() {
        val html = "<html><head><title>Test</title></head><body><h1>Hello</h1><p>World</p></body></html>"
        val result = ExtractionPipeline.extractText(html)
        assertTrue(result.content.isNotEmpty())
        assertEquals("Test", result.metadata["title"])
    }

    @Test
    fun `HTML extraction extracts links`() {
        val html = "<html><body><a href=\"https://example.com\">Link</a></body></html>"
        val result = ExtractionPipeline.extractText(html)
        assertTrue(result.content.containsKey("text"))
    }

    @Test
    fun `Markdown extraction extracts headings`() {
        val md = "# Title\n## Section\n### Sub"
        val result = ExtractionPipeline.extractText(md)
        assertTrue(result.content.containsKey("hierarchy"))
    }

    @Test
    fun `JSON extraction parses valid JSON`() {
        val json = "{\"key\": \"value\", \"number\": 42}"
        val result = ExtractionPipeline.extractText(json)
        assertEquals("json", result.metadata["input_type"])
    }

    @Test
    fun `ExtractionRequest detects input types`() {
        assertEquals("html", ExtractionRequest("<div>test</div>").detectInputType())
        assertEquals("json", ExtractionRequest("{\"a\":1}").detectInputType())
        assertEquals("markdown", ExtractionRequest("# Title").detectInputType())
        assertEquals("url", ExtractionRequest("https://example.com").detectInputType())
        assertEquals("text", ExtractionRequest("plain text").detectInputType())
    }

    @Test
    fun `extraction produces fingerprint`() {
        val result = ExtractionPipeline.extractText("<html><body>test</body></html>")
        assertTrue(result.fingerprint.isNotEmpty())
        assertEquals(64, result.fingerprint.length)
    }

    @Test
    fun `extraction is deterministic`() {
        val html = "<html><body>test content</body></html>"
        val r1 = ExtractionPipeline.extractText(html)
        val r2 = ExtractionPipeline.extractText(html)
        assertEquals(r1.fingerprint, r2.fingerprint)
    }

    @Test
    fun `HTML strips scripts and styles`() {
        val html = "<html><body><script>alert('xss')</script><style>.red{}</style><p>Safe</p></body></html>"
        val result = ExtractionPipeline.extractText(html)
        val text = result.rawText
        assertTrue(!text.contains("alert"))
        assertTrue(!text.contains("red"))
        assertTrue(text.contains("Safe"))
    }

    @Test
    fun `extraction result is serializable`() {
        val result = ExtractionPipeline.extractText("<html><body>test</body></html>")
        val map = result.toMap()
        assertTrue(map.containsKey("content"))
        assertTrue(map.containsKey("metadata"))
        assertTrue(map.containsKey("fingerprint"))
    }
}
