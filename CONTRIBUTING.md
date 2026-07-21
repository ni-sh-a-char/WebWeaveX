# Contributing to WebWeaveX Kotlin SDK

Thank you for your interest in contributing to WebWeaveX!

## Development Setup

```bash
git clone https://github.com/ni-sh-a-char/WebWeaveX.git -b kotlin
cd WebWeaveX/kotlin
gradle build
gradle test
```

## Rules

| Rule | Requirement |
|------|-------------|
| Determinism | No `System.currentTimeMillis()`, `Math.random()`, `UUID.randomUUID()` in runtime paths |
| Replay safety | Preserve graph normalization semantics |
| Canonical pipeline | Single execution path, no parallel orchestrators |
| Persistence | Kaalka-compatible checkpoints |
| Tests | `gradle test` must pass; 133+ tests required |
| Kotlin style | Kotlin idioms, data classes, minimal mutation |
| API stability | No breaking changes to frozen public APIs |

## Pull Request Process

1. Fork the repository
2. Create a feature branch from `kotlin`
3. Write tests for any new functionality
4. Ensure `gradle clean test` passes
5. Follow the naming conventions below
6. Submit a pull request with a clear description

## Naming Conventions

- Classes: `PascalCase` (e.g., `SearchIndex`, `QuerySession`)
- Functions: `camelCase` (e.g., `searchWithIndex`, `buildRuntimeGraph`)
- Constants: `UPPER_SNAKE_CASE` for truly constant values
- Packages: `io.webweavex.<module>` (e.g., `io.webweavex.repository`)

## Code Quality

- No TODO/FIXME in production code
- No deprecated API usage
- No unused parameters or imports
- Immutable data classes preferred
- Deterministic output ordering

## Running Tests

```bash
gradle clean test
```

## Reporting Issues

Open a GitHub issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Kotlin version and OS

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
