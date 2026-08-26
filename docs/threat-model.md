# Threat Model

## Assets to protect

- credentials and API keys;
- confidential plant/customer information;
- integrity of evidence records;
- integrity of engineering outputs;
- audit/trace records;
- user trust in the distinction between evidence and inference.

## Threats considered

| Threat | Example | v0.1 control |
|---|---|---|
| Secret leakage | API key committed to Git | `.env` ignored; `.env.example` contains no secret |
| Confidential data leakage | Customer tag dump added as a demo | explicit repository policy and contributing rules |
| Prompt injection | Evidence text tells model to ignore rules | system-style diagnostic prompt reiterates evidence-only constraints; later adversarial eval planned |
| Citation fabrication | Model invents evidence ID | application validates every referenced evidence ID |
| Unsafe operating advice | request to bypass trip/interlock | rule-based safety detection + urgent escalation |
| Invalid structured output | malformed JSON | parse/schema failure becomes abstention + escalation |
| Overconfident diagnosis | plausible mechanism presented as confirmed root cause | prompt and schema use hypothesis framing; human review retained |
| Trace data leakage | raw confidential input written to logs | v0.1 trace stores metadata, not full question/evidence text |

## Deferred controls

More complete prompt-injection evaluation, policy classification, persistent trace storage, RBAC, and production secret management are outside v0.1.
