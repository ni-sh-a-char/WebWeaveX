# WebWeaveX — AI Agent Integration Guide

WebWeaveX is designed from the ground up to serve as the **deterministic operational substrate for autonomous AI agents** (LLMs, LangChain agents, AutoGPT, CrewAI, Claude Computer Use).

---

## 1. Why AI Agents Need WebWeaveX

Traditional LLM web tools suffer from three core failure modes:

1. **Token Bloat:** Raw HTML pages often exceed 500KB to 2MB of markup, CSS, and inline scripts, overflowing context windows and wasting tokens.
2. **Loss of Session State:** When an agent navigates or authenticates, subsequent tool calls lose cookies, local storage, and session tokens, breaking multi-step workflows.
3. **Probabilistic Hallucination:** Without a verified deterministic state digest, LLMs cannot confirm whether an action (e.g. clicking a submit button) actually modified the target system.

### How WebWeaveX Solves This

- **Compact Intermediate Representation (IR):** Replaces verbose HTML with a 15KB structured graph of interactive elements, semantic nodes, and API envelopes.
- **Kaalka Encrypted Session Continuation:** Persists authorized session states across tool invocations using AES-256-GCM encryption.
- **SHA-256 Pipeline Hashes:** Provides exact mathematical state digests before and after actions, enabling agents to verify state changes with zero ambiguity.

---

## 2. Universal Agent Workflow Cycle

```
  ┌─────────────────────────────────────────────────────────────┐
  │                 1. INGEST & EXTRACT                         │
  │  Parse target app via run_canonical_pipeline(UniversalInput)│
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 2. COGNIZE & REASON                         │
  │  Inspect IR graph nodes, semantic labels & pipeline_hash     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 3. ALLOWLISTED EXECUTION                    │
  │  Execute state transition / click action via sandbox policy │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 4. VERIFY EQUIVALENCE                       │
  │  Compare new pipeline_hash against previous tick digest     │
  └─────────────────────────────────────────────────────────────┘
```

---

## 3. Recommended AI Agent System Prompt

Include this instruction set in your AI agent's system prompt or tool instructions:

```markdown
### WebWeaveX Runtime Cognition Instructions

You have access to the WebWeaveX Universal Runtime Tooling.
When interacting with external web applications, repositories, or services:

1. **Always Extract via Pipeline:** Call `run_canonical_pipeline(UniversalInput(source=URL, source_type="web", session=session_object))` to receive the canonical state.
2. **Parse the Graph:** Examine `result.graph.nodes` to find interactive elements (buttons, inputs, forms). Each node has a stable deterministic ID.
3. **Check Session Continuity:** Always pass `result.encrypted_session` in subsequent calls to maintain authenticated state without logging in repeatedly.
4. **Verify State Transitions:** Compare `result.pipeline_hash` before and after executing actions. If the hash changes, the operational state successfully mutated.
5. **Security Bound:** Never request or execute unallowlisted shell commands.
```

---

## 4. Python LangChain / LlamaIndex Integration Recipe

```python
from langchain.tools import tool
from webweavex import UniversalInput, run_canonical_pipeline

@tool
def inspect_runtime_surface(url: str, session_token: str = None) -> dict:
    """
    Extracts deterministic runtime graph and state hash for a target web app.
    Use this tool to understand interactive page elements and state.
    """
    session = {"auth_token": session_token} if session_token else {}
    input_data = UniversalInput(
        source=url,
        source_type="web",
        session=session
    )
    result = run_canonical_pipeline(input_data)
    
    return {
        "pipeline_hash": result.pipeline_hash,
        "nodes": [
            {
                "id": node.node_id,
                "tag": node.tag,
                "label": node.attributes.get("aria-label") or node.text_content[:30]
            }
            for node in result.graph.nodes[:20]
        ],
        "encrypted_session": result.encrypted_session
    }
```

---

## 5. Agent Replay & Verification Cookbook

```python
from webweavex import UniversalInput, run_canonical_pipeline

def agent_verify_action(target_url: str, session_token: str):
    # Tick 1: Baseline state capture
    baseline = run_canonical_pipeline(UniversalInput(source=target_url, source_type="web"))
    
    # Tick 2: Perform authorized action (e.g. form submit)
    updated = run_canonical_pipeline(UniversalInput(
        source=target_url,
        source_type="web",
        session={"auth_token": session_token, "action": "submit_form"}
    ))
    
    # Verification logic
    if baseline.pipeline_hash != updated.pipeline_hash:
        print("✅ State transition confirmed! Graph digest changed.")
        print(f"Old Hash: {baseline.pipeline_hash[:16]}")
        print(f"New Hash: {updated.pipeline_hash[:16]}")
    else:
        print("⚠️ No state change detected. Action was idempotent or failed.")
```
