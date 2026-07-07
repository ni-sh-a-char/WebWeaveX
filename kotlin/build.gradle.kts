plugins {
    kotlin("jvm") version "2.0.20"
    `java-library`
    `maven-publish`
}

group = "io.webweavex"
version = "2.1.0" // synchronized with python/javascript/java/dart

repositories { mavenCentral() }

dependencies {
    testImplementation(kotlin("test-junit5"))
}

kotlin { jvmToolchain(17) }

tasks.test { useJUnitPlatform() }

publishing {
    publications { create<MavenPublication>("maven") { from(components["java"]) } }
}
