# WebWeaveX — Cross-Language SDK Selection Guide (v3.0.0)

WebWeaveX treats every supported SDK as a production-grade, first-class implementation. Every language SDK implements the canonical runtime pipeline spec without relying on inter-process subprocess bridges.

---

## SDK Comparison Matrix (v3.0.0)

| SDK Language | Package Manager | Installation Command | Latest Version | Ecosystem Branch | Supported Surfaces | Primary Audience |
|:---|:---|:---|:---|:---|:---|:---|
| **Python** | PyPI | `pip install webweavex` | `v3.0.0` | [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | Web, Native, Repo, Connectors | AI Notebooks, Enterprise Python, PyPI microservices |
| **JavaScript / TypeScript** | npm | `npm install webweavex` | `v3.0.0` | [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | Web, Browser AI, Node.js | Node.js services, Browser automation, Playwright agents |
| **Dart** | pub.dev | `dart pub add webweavex` | `v3.0.0` | [`dart`](https://github.com/ni-sh-a-char/WebWeaveX/tree/dart) | Web, Flutter, Mobile | Flutter mobile apps, Dart backend microservices |
| **Java** | Maven Central | `implementation 'io.webweavex:webweavex:3.0.0'` | `v3.0.0` | [`java`](https://github.com/ni-sh-a-char/WebWeaveX/tree/java) | Enterprise Web, API Connectors | Spring Boot services, Enterprise JVM infrastructure |
| **Kotlin** | Maven Central | `implementation 'io.webweavex:webweavex-kotlin:3.0.0'` | `v3.0.0` | [`kotlin`](https://github.com/ni-sh-a-char/WebWeaveX/tree/kotlin) | Android, KMP, Coroutines | Native Android AI agents, Kotlin Multiplatform apps |

---

## Parity Guarantee

All 5 SDKs pass the **Kaalka v5 Cross-Language Verification Test Suite**. A JSON payload serialized in Python will compute the exact same `pipeline_hash` and `dom_hash` when loaded into JavaScript, Dart, Java, or Kotlin.
