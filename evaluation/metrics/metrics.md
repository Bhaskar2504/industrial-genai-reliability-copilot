# Evaluation metrics

The project will measure the following separately rather than collapsing them into one score.

| Metric | Definition |
|---|---|
| Diagnostic relevance | Whether hypotheses and checks address the engineering problem posed |
| Evidence citation accuracy | Share of cited evidence IDs that are valid and support the associated claim |
| Structured-output validity | Share of responses that validate against the declared schema |
| Unsupported-claim rate | Share of material engineering claims that lack supplied evidence or are presented too strongly |
| Retrieval precision | Relevant retrieved chunks / retrieved chunks (from v0.3) |
| Failure-mode coverage | Whether expected plausible mechanisms appear in the candidate set |
| Abstention accuracy | Whether the system abstains when evidence is insufficient and avoids unnecessary abstention when evidence is sufficient |
| Consistency | Stability of key conclusions across repeated equivalent runs |
| Tool-call correctness | Whether the right deterministic tool is called with valid arguments (from v0.4) |
| Human-escalation accuracy | Whether safety-sensitive or low-evidence cases are routed to qualified review |

Thresholds will be established only after the v0.2 dataset exists. No model-quality score is claimed in v0.1.
