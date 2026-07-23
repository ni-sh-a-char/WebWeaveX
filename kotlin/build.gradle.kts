plugins {
    kotlin("jvm") version "1.9.22"
    `java-library`
    `maven-publish`
}

group = "io.webweavex"
version = "3.0.0"
description = "Deterministic runtime cognition infrastructure for humans and AI agents"

repositories { mavenCentral() }

dependencies {
    testImplementation(kotlin("test-junit5"))
}

kotlin { jvmToolchain(17) }

tasks.test { useJUnitPlatform() }

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            pom {
                name.set("WebWeaveX Kotlin SDK")
                description.set("Deterministic runtime cognition infrastructure for humans and AI agents")
                url.set("https://github.com/ni-sh-a-char/WebWeaveX")
                licenses {
                    license {
                        name.set("The Apache License, Version 2.0")
                        url.set("https://www.apache.org/licenses/LICENSE-2.0.txt")
                    }
                }
                developers {
                    developer {
                        id.set("piyushmishra")
                        name.set("Piyush Mishra")
                        email.set("piyushmishra.professional@gmail.com")
                    }
                }
                scm {
                    connection.set("scm:git:https://github.com/ni-sh-a-char/WebWeaveX.git")
                    developerConnection.set("scm:git:ssh://github.com/ni-sh-a-char/WebWeaveX.git")
                    url.set("https://github.com/ni-sh-a-char/WebWeaveX")
                }
            }
        }
    }
}
