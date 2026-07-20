package io.webweavex.serialization

import io.webweavex.determinism.StableSerialize

object CanonicalSerialization {
    fun serialize(value: Any?): String = StableSerialize.stableSerialize(value)
    
    fun hash(value: Any?): String = io.webweavex.fingerprint.Fingerprint.compute(value)
}
