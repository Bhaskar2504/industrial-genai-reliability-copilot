# Evaluation Strategy

Evaluation is treated as part of the product, not as a final demo step.

## v0.2 baseline

The first quantitative baseline uses eight synthetic cases and the deterministic mock backend so the result is reproducible without an API key. It deliberately includes a failing contradictory-evidence case.

Current baseline result:

- 8 cases total;
- 7 passed;
- 1 failed;
- 87.5% case pass rate;
- 100% structured-output validity;
- 100% evidence citation-ID accuracy;
- 100% repeated-run consistency;
- 87.5% abstention accuracy;
- 87.5% human-escalation accuracy.

These are workflow-level synthetic metrics, not real-world diagnostic accuracy. The unsupported-claim metric is currently a structural proxy: it verifies that diagnostic hypotheses carry supplied evidence IDs, not that every cited passage semantically proves the claim.

See [`../evaluation/reports/v0.2-baseline.md`](../evaluation/reports/v0.2-baseline.md). Running the evaluator also creates a local machine-readable `evaluation/reports/v0.2_results.json`; that generated file is intentionally ignored to avoid noisy request-level artifacts in Git history.

## Evaluation layers

### 1. Contract evaluation

Can the system produce valid, parseable, versioned engineering records?

### 2. Grounding evaluation

Do evidence citations exist, and do they support the associated claim? v0.2 validates citation IDs structurally; semantic support evaluation is still planned.

### 3. Diagnostic evaluation

Does the answer include relevant plausible mechanisms, useful contradicting evidence, and appropriate checks?

### 4. Retrieval evaluation

From v0.3, did retrieval return the right evidence before generation even started?

### 5. Tool evaluation

From v0.4, did the system choose and call deterministic tools correctly?

### 6. Safety and escalation evaluation

Did the system abstain and escalate when the evidence or risk profile required it?

## Why failed cases stay public

Failed examples are retained with an explanation of whether the failure came from retrieval, prompt behavior, schema compliance, tool choice, contradiction handling, or policy/escalation logic. A visible limitation is more useful than an artificially perfect benchmark.
