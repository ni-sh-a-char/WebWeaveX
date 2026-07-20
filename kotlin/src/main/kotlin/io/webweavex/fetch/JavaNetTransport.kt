package io.webweavex.fetch

import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.time.Duration

class JavaNetTransport : HttpTransport {
    private val client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(30)).followRedirects(HttpClient.Redirect.NORMAL).build()

    override suspend fun fetch(url: String): Map<String, Any> {
        return try {
            val req = HttpRequest.newBuilder().uri(URI.create(url)).header("User-Agent", "WebWeaveX/3.0.0").timeout(Duration.ofSeconds(30)).GET().build()
            val resp = client.send(req, HttpResponse.BodyHandlers.ofString())
            mapOf("text" to resp.body(), "status" to resp.statusCode(), "contentType" to (resp.headers().firstValue("content-type").orElse("text/plain")), "ok" to (resp.statusCode() in 200..399), "error" to "")
        } catch (e: Exception) {
            mapOf("text" to "", "status" to 0, "contentType" to "text/plain", "ok" to false, "error" to (e.message ?: "unknown"))
        }
    }
}
