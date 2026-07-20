package io.webweavex.runtime

data class RuntimeConfig(
    val deterministic: Boolean = true,
    val stableOrdering: Boolean = true,
    val canonicalSerialization: Boolean = true,
    val validationEnabled: Boolean = true,
    val maxGraphSize: Int = 10000,
    val timeoutMs: Long = 30000L
) {
    companion object {
        fun default() = RuntimeConfig()
    }
}
