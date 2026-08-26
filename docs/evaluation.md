# Evaluation Strategy

Evaluation is treated as part of the product, not as a final demo step.

## Layers

### 1. Contract evaluation

Can the system produce valid, parseable, versioned engineering records?

### 2. Grounding evaluation

Do evidence citations exist, and do they support the associated claim?

### 3. Diagnostic evaluation

Does the answer include relevant plausible mechanisms, useful contradicting evidence, and appropriate checks?

### 4. Retrieval evaluation

From v0.3, did retrieval return the right evidence before generation even started?

### 5. Tool evaluation

From v0.4, did the system choose and call deterministic tools correctly?

### 6. Safety and escalation evaluation

Did the system abstain and escalate when the evidence or risk profile required it?

## Failed cases

Failed examples are part of the intended public evaluation report. They should be retained with an explanation of whether the failure came from retrieval, prompt behavior, schema compliance, tool choice, or policy/escalation logic.
