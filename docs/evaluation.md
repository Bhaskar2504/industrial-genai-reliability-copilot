# Evaluation Strategy

Evaluation is treated as part of the product, not as a final demo step.

## v0.2 workflow baseline

Eight synthetic cases exercise structured outputs, evidence-ID grounding, abstention, safety escalation and repeatability. Seven pass and one contradictory-evidence case is deliberately retained as a failure.

See [`../evaluation/reports/v0.2-baseline.md`](../evaluation/reports/v0.2-baseline.md).

## v0.3 RAG and citation baseline

Seven targeted retrieval cases exercise the synthetic knowledge base and deterministic lexical retriever.

Current result:

- 7 cases total;
- 6 passed;
- 1 deliberately retained ambiguous-query failure;
- 85.7% retrieval precision@1;
- 100% citation-ID accuracy;
- 100% source-locator completeness;
- 100% repeated retrieval consistency.

See [`../evaluation/reports/v0.3-rag-and-citations.md`](../evaluation/reports/v0.3-rag-and-citations.md).

These are portfolio-scale synthetic metrics, not real-world diagnostic accuracy.

## Evaluation layers

### 1. Contract evaluation
Can the system produce valid, parseable, versioned engineering records?

### 2. Grounding evaluation
Do evidence citations exist and come from the supplied/retrieved evidence set? Semantic entailment scoring remains a future improvement.

### 3. Diagnostic evaluation
Does the answer include plausible mechanisms, contradicting evidence and useful next checks without presenting hypotheses as confirmed root cause?

### 4. Retrieval evaluation
Did retrieval rank the intended engineering source before generation began?

### 5. Tool evaluation
From v0.4, did the system choose and call deterministic engineering tools correctly?

### 6. Safety and escalation evaluation
Did the system abstain and escalate when evidence or risk required it?

## Why failed cases stay public

Failed examples are retained with an explanation of whether the failure came from retrieval, prompt behaviour, schema compliance, tool choice, contradiction handling or escalation logic. A visible limitation is more informative than an artificially perfect benchmark.
