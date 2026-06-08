# FINAL PY2TS CORRECTNESS REPORT

**Measured:** 2026-05-29T13:40:58.501432+00:00

**Status:** PASS

| Sample transforms | 8 |
| Invalid samples | 0 |

## Transform audit

| Transform | Python | Valid | Reason |
|-----------|--------|-------|--------|
| dict_get | `x = d.get('k', {}).get('c', [])` | PASS | ok |
| append | `items = [] items.append({'a': 1})` | PASS | ok |
| fstring | `s = f'fallback_{index}'` | PASS | ok |
| comprehension | `xs = [str(x) for x in items]` | PASS | ok |
| enumerate | `for i, v in enumerate(items):     pass` | PASS | ok |
| len_sorted | `n = len(items) xs = sorted(items)` | PASS | ok |
| dict_literal | `return {'bounded': True, 'nodes': nodes}` | PASS | ok |
| call_name | `return recover_modal_runtime(page, html)` | PASS | ok |

## Generated tree scan (non-protected)

- No known invalid patterns detected in generated tree.

## Sample outputs

### dict_get

```python
x = d.get('k', {}).get('c', [])
```

```typescript
export function probe(): void {
  let x = ((((d as Record<string, unknown>)["k"] ?? {}) as Record<string, unknown>)["c"] ?? []);
  return null;
}
```

### append

```python
items = []
items.append({'a': 1})
```

```typescript
export function probe(): void {
  let items = [];
  items.push({"a": 1});
  return null;
}
```

### fstring

```python
s = f'fallback_{index}'
```

```typescript
export function probe(): void {
  let s = `fallback_${index}`;
  return null;
}
```

### comprehension

```python
xs = [str(x) for x in items]
```

```typescript
export function probe(): void {
  let xs = items.map((x) => String(x));
  return null;
}
```

### enumerate

```python
for i, v in enumerate(items):
    pass
```

```typescript
export function probe(): void {
  items.forEach((v, i) => {
    // pass
  });
  return null;
}
```

### len_sorted

```python
n = len(items)
xs = sorted(items)
```

```typescript
export function probe(): void {
  let n = (Array.isArray(items) ? items.length : Object.keys(items as object).length);
  let xs = [...items].slice().sort();
  return null;
}
```

### dict_literal

```python
return {'bounded': True, 'nodes': nodes}
```

```typescript
export function probe(): void {
  return {"bounded": true, "nodes": nodes};
  return null;
}
```

### call_name

```python
return recover_modal_runtime(page, html)
```

```typescript
export function probe(): void {
  return recoverModalRuntime(page, html);
  return null;
}
```
