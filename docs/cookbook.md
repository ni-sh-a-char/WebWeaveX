# WebWeaveX — Cookbook & Code Recipes

Practical recipes for common runtime cognition tasks.

---

## Recipe 1: Authenticated Session Continuation (Python)

```python
from webweavex import UniversalInput, run_canonical_pipeline

# Authenticated session with user-supplied authorization cookies
session_tokens = {
    "sessionid": "auth_cookie_998127391823",
    "csrf_token": "csrf_val_881923891"
}

input_data = UniversalInput(
    source="https://app.enterprise.com/dashboard",
    source_type="web",
    session=session_tokens
)

result = run_canonical_pipeline(input_data)
print(f"Authenticated Graph Hash: {result.pipeline_hash}")
print(f"Kaalka Sealed Session : {result.encrypted_session}")
```

---

## Recipe 2: Node.js / TypeScript Web Extraction (JavaScript)

```typescript
import { UniversalInput, runCanonicalPipeline } from 'webweavex';

async function extractWebSurface() {
  const input = new UniversalInput({
    source: 'https://news.ycombinator.com',
    sourceType: 'web'
  });

  const result = await runCanonicalPipeline(input);
  console.log(`Extracted Nodes: ${result.graph.nodes.length}`);
  console.log(`Stable DOM Hash: ${result.fingerprint.domHash}`);
}

extractWebSurface();
```

---

## Recipe 3: Federated Memory Merge Across Ticks (Python)

```python
from webweavex import UniversalInput, run_canonical_pipeline

# Tick 1
tick1 = run_canonical_pipeline(UniversalInput(source="https://example.com/step1", source_type="web"))

# Tick 2
tick2 = run_canonical_pipeline(UniversalInput(source="https://example.com/step2", source_type="web"))

# Memory merge verification
print(f"Tick 1 Hash: {tick1.pipeline_hash}")
print(f"Tick 2 Hash: {tick2.pipeline_hash}")
```
