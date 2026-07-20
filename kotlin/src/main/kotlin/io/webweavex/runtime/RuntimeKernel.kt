package io.webweavex.runtime

import io.webweavex.fingerprint.Fingerprint

data class RuntimeKernel(
    val version: String = "3.0.0",
    val capabilities: Set<String> = setOf(
        "extraction", "fingerprinting", "serialization",
        "repository_intelligence", "replay", "workflow"
    )
) {
    companion object {
        fun create(): RuntimeKernel = RuntimeKernel()
    }

    fun extract(input: UniversalInput): UniversalOutput {
        return UniversalOutput(
            data = input.toMap(),
            fingerprint = Fingerprint.compute(input.toMap()),
            version = version
        )
    }
}
