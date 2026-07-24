# WebWeaveX Kotlin SDK v3.0.0

## Quick Start

### 1. Add the JAR to your project

**Gradle (manual JAR):**
`kotlin
dependencies {
    implementation(files("webweavex-kotlin-3.0.0.jar"))
}
`

**Maven:**
`xml
<dependency>
    <groupId>io.webweavex</groupId>
    <artifactId>webweavex-kotlin</artifactId>
    <version>3.0.0</version>
</dependency>
`

### 2. Usage

`kotlin
import io.webweavex.WebWeaveX

fun main() {
    // Extract runtime cognition from a URL
    val result = WebWeaveX.extract("https://example.com")
    
    // Access the pipeline hash (deterministic)
    println("Hash: ")
    
    // Access runtime graph nodes
    println("Nodes: ")
}
`

## What is WebWeaveX?

Deterministic runtime cognition infrastructure for humans and AI agents.
Same Kaalka v5 encryption, replay equivalence, and cross-language parity
as the Python, JavaScript, and Dart SDKs.

## License

Apache 2.0
