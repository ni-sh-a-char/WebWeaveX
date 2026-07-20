package io.webweavex.fetch

interface HttpTransport {
    suspend fun fetch(url: String): Map<String, Any>
    companion object { fun default(): HttpTransport = JavaNetTransport() }
}
