# Implementation Interfaces

## Purpose

This document defines the core data structures and interfaces
for implementing the Sovereign Intelligence Core.

---

## Knowledge State Enum

```
enum KnowledgeState {
    KNOWN,
    INFERRED,
    AMBIGUOUS,
    UNKNOWN
}
```

---

## Signal Structure

```
struct Signal {
    id: string
    source: string
    timestamp: datetime
    content: any
    quality: SignalQuality
    provenance: ProvenanceChain
}

enum SignalQuality {
    VERIFIED,
    UNVERIFIED,
    DEGRADED
}

struct ProvenanceChain {
    origin: string
    transformations: list<Transformation>
    integrity_verified: boolean
}
```

---

## Intelligence Output Structure

```
struct IntelligenceOutput {
    signals: list<Signal>
    interpretation: string
    knowledge_state: KnowledgeState
    epistemic_status: EpistemicStatus
    collapse_justification: optional<CollapseJustification>
}

struct EpistemicStatus {
    what_is_known: list<string>
    what_is_not_known: list<string>
    what_cannot_be_concluded: list<string>
    requirements_for_certainty: list<string>
}

struct CollapseJustification {
    prior_state: KnowledgeState
    new_evidence: list<Signal>
    collapse_timestamp: datetime
    irreversibility_acknowledged: boolean
}
```

---

## Core Operations

### 1. Process Signal

```
function processSignal(signal: Signal) -> IntelligenceOutput {
    // Classify signal
    quality = assessQuality(signal)
    
    // Determine knowledge state
    state = mapSignalToKnowledgeState(signal, quality)
    
    // Build output
    return IntelligenceOutput {
        signals: [signal],
        interpretation: interpretSignal(signal),
        knowledge_state: state,
        epistemic_status: buildEpistemicStatus(signal, state)
    }
}
```

### 2. Handle Conflict

```
function handleConflict(signals: list<Signal>) -> IntelligenceOutput {
    // Verify conflict exists
    if not hasConflict(signals) {
        return processNormally(signals)
    }
    
    // Preserve all conflicting signals
    return IntelligenceOutput {
        signals: signals,
        interpretation: "Conflicting signals detected",
        knowledge_state: AMBIGUOUS,
        epistemic_status: buildConflictStatus(signals)
    }
}
```

### 3. Attempt Collapse

```
function attemptCollapse(
    current: IntelligenceOutput,
    new_evidence: Signal
) -> IntelligenceOutput {
    
    // Check collapse conditions
    if not canCollapse(current, new_evidence) {
        return current  // No collapse
    }
    
    // Perform justified collapse
    return IntelligenceOutput {
        signals: current.signals + [new_evidence],
        interpretation: deriveNewInterpretation(current, new_evidence),
        knowledge_state: KNOWN,
        epistemic_status: buildCollapsedStatus(current, new_evidence),
        collapse_justification: CollapseJustification {
            prior_state: current.knowledge_state,
            new_evidence: [new_evidence],
            collapse_timestamp: now(),
            irreversibility_acknowledged: true
        }
    }
}
```

### 4. Refuse

```
function refuse(reason: string) -> IntelligenceOutput {
    return IntelligenceOutput {
        signals: [],
        interpretation: "Refusal",
        knowledge_state: UNKNOWN,
        epistemic_status: EpistemicStatus {
            what_is_known: [],
            what_is_not_known: ["All required information"],
            what_cannot_be_concluded: ["Any assertion"],
            requirements_for_certainty: [reason]
        }
    }
}
```

---

## Validation Rules

```
function validateOutput(output: IntelligenceOutput) -> boolean {
    // Rule 1: Knowledge state must be explicit
    if output.knowledge_state == null {
        return false
    }
    
    // Rule 2: Epistemic status must be complete
    if output.epistemic_status == null {
        return false
    }
    
    // Rule 3: Collapse requires justification
    if output.knowledge_state == KNOWN 
       and output.collapse_justification == null 
       and hasPriorAmbiguity(output) {
        return false
    }
    
    // Rule 4: Ambiguous state requires multiple signals or conflict
    if output.knowledge_state == AMBIGUOUS 
       and output.signals.length < 2 {
        return false
    }
    
    return true
}
```

---

## API Contract Example

### Request
```json
{
  "operation": "process_signals",
  "signals": [
    {
      "id": "sig_001",
      "source": "sensor_alpha",
      "timestamp": "2024-01-15T10:00:00Z",
      "content": {"temperature": 22},
      "quality": "VERIFIED"
    }
  ]
}
```

### Response
```json
{
  "signals": [...],
  "interpretation": "Temperature reading received",
  "knowledge_state": "KNOWN",
  "epistemic_status": {
    "what_is_known": ["Temperature at sensor_alpha is 22°C at 10:00:00Z"],
    "what_is_not_known": ["Temperature at other locations", "Temperature trend"],
    "what_cannot_be_concluded": ["Future temperature", "System health"],
    "requirements_for_certainty": []
  },
  "collapse_justification": null
}
```

---

## Closure

These interfaces enforce epistemic boundaries at the implementation level.
Any implementation violating these contracts is invalid.
