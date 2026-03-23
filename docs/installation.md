# WebWeaveX Installation Guide

This guide provides detailed installation instructions for each supported language.

---

## Python

### Requirements
- Python 3.9+
- pip

### Installation

```bash
pip install webweavex
```

### Development Installation

```bash
cd implementations/python/webweavex
pip install -e .
```

### Usage

```python
from webweavex import WebWeaveX

wx = WebWeaveX()
result = wx.extract("Contact test@example.com")
```

---

## Node.js

### Requirements
- Node.js 18+
- npm or yarn

### Installation

```bash
npm install webweavex
```

Or using yarn:

```bash
yarn add webweavex
```

### Usage

```javascript
import { WebWeaveX } from 'webweavex';

const wx = new WebWeaveX();
const result = wx.extract("Contact test@example.com");
```

### TypeScript Support

TypeScript types are included. For custom types:

```typescript
import { WebWeaveX, WXPResult } from 'webweavex';

const wx = new WebWeaveX();
const result: WXPResult = wx.extract("Contact test@example.com");
```

---

## Java

### Requirements
- Java 11+
- Maven

### Installation

Add to your `pom.xml`:

```xml
<dependency>
    <groupId>com.webweavex</groupId>
    <artifactId>webweavex</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Gradle Installation

```groovy
implementation 'com.webweavex:webweavex:1.0.0'
```

### Usage

```java
import com.webweavex.WebWeaveX;

public class Main {
    public static void main(String[] args) {
        WebWeaveX wx = new WebWeaveX();
        Map<String, Object> result = wx.extract("Contact test@example.com");
    }
}
```

---

## Kotlin

### Requirements
- Kotlin 1.9+
- Gradle or Maven

### Gradle Installation

```kotlin
implementation("com.webweavex:webweavex:1.0.0")
```

### Maven Installation

```xml
<dependency>
    <groupId>com.webweavex</groupId>
    <artifactId>webweavex</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Usage

```kotlin
import com.webweavex.WebWeaveX

fun main() {
    val wx = WebWeaveX()
    val result = wx.extract("Contact test@example.com")
}
```

---

## Dart

### Requirements
- Dart 3.0+
- pub

### Installation

```bash
dart pub add webweavex
```

### Usage

```dart
import 'package:webweavex/webweavex.dart';

void main() {
  final wx = WebWeaveX();
  final result = wx.extract('Contact test@example.com');
}
```

---

## Verify Installation

Run validation to verify installation:

```bash
python core/test_runner/validate_full_system.py
```

Expected output: 35/35 tests passing.

---

## Platform-Specific Notes

### Python
- Works on Windows, macOS, Linux
- Supports PyPy

### Node.js
- Works on Windows, macOS, Linux
- Native ESM modules

### Java
- Works on any JVM 11+
- Compatible with Android (API 24+)

### Kotlin
- Works on JVM 11+
- Interop with Java

### Dart
- Works on Windows, macOS, Linux
- Flutter compatible
