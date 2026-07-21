# WebWeaveX Dart SDK — Architecture

## System Architecture

```mermaid
graph TB
    subgraph Input
        A[HTML/JSON/Markdown/URL]
    end
    
    subgraph Canonical Pipeline
        B[extractWeb / runCanonicalPipeline]
        C[Normalization + Kaalka v5]
        D[Runtime Graph Construction]
    end
    
    subgraph Cognition Layers
        E[Memory Fabric]
        F[Replay Equivalence]
        G[Reconstruction]
        H[Workflow Execution]
    end
    
    subgraph Output
        I[Fingerprinted Runtime Graph]
        J[Replay-Safe Artifacts]
        K[Knowledge Graph]
    end
    
    A --> B --> C --> D
    D --> E & F & G & H
    E & F & G & H --> I & J & K
```

## Deterministic Runtime Flow

```mermaid
graph LR
    A[normalizeRuntimeValue] --> B[stableSerialize]
    B --> C[UTF-8]
    C --> D[deriveKaalkaTimeKey]
    D --> E[kaalka._proc]
    E --> F[base64]
```

## Replay Pipeline

```mermaid
graph LR
    A[Original Envelope] --> C[validateReplayEquivalence]
    B[Replayed Envelope] --> C
    C --> D{equivalent?}
    D -->|Yes| E[Replay Valid]
    D -->|No| F[Replay Failed]
```

## Memory Lineage

```mermaid
graph TB
    A[buildRuntimeMemoryFabric] --> B[Runtime Graph]
    A --> C[Stable Hash]
    B --> D[queryRuntimeMemoryFabric]
    C --> D
    D --> E[Query Results]
    
    F[buildRuntimeMemory] --> G[History]
    F --> H[Lineage]
    F --> I[Semantic Relations]
    G & H & I --> J[queryRuntimeMemory]
```

## Kaalka Runtime

```mermaid
graph LR
    A[Plaintext] --> B[UTF-8]
    B --> C[deriveKaalkaTimeKey]
    C --> D[kaalka._proc]
    D --> E[base64 Ciphertext]
    
    E --> F[decryptValue]
    F --> G[Plaintext]
```

## Cross-Language Architecture

```mermaid
graph TB
    subgraph Shared Contract
        S1[Normalization]
        S2[Stable Serialization]
        S3[Fingerprint Algorithm]
        S4[Kaalka v5]
    end
    
    subgraph Python
        P[PyPI: webweavex]
    end
    
    subgraph JavaScript
        JS[npm: webweavex]
    end
    
    subgraph Dart
        D[pub.dev: webweavex]
    end
    
    P & JS & D --> S1 & S2 & S3 & S4
```

## Workflow Execution

```mermaid
graph TB
    A[buildWorkflowPlan] --> B[runAutonomousWorkflow]
    B --> C[Execute Steps]
    C --> D[replayWorkflowRuntime]
    D --> E[Validated Output]
```

## Module Dependencies

```mermaid
graph TB
    subgraph Core
        K[kernel] --> D[determinism]
        K --> G[graph]
        K --> M[memory]
        K --> R[replay]
    end
    
    subgraph Extraction
        B[browser] --> K
        EX[extraction] --> K
    end
    
    subgraph Cognition
        C[causality] --> K
        SE[semantic] --> K
        SY[synchronization] --> K
        EV[evolution] --> K
        W[workflows] --> K
        EXE[execution] --> K
    end
    
    subgraph Infrastructure
        CR[crypto] --> D
        P[persistence] --> K
        CO[connectors] --> K
    end
```
