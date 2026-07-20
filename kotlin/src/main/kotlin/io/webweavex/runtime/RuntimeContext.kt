package io.webweavex.runtime

data class RuntimeContext(
    val kernel: RuntimeKernel = RuntimeKernel.create(),
    val metadata: RuntimeMetadata = RuntimeMetadata(),
    val config: RuntimeConfig = RuntimeConfig()
)
