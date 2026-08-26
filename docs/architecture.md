# Architecture

## Design principles

1. **Evidence is a first-class object.** Evidence IDs and provenance exist independently of generated prose.
2. **Generation is not validation.** Model output is parsed and validated by application code.
3. **Prompts and schemas are versioned independently.** A behavioral change can therefore be traced to the prompt, schema, model, retrieval, or tool layer.
4. **The model proposes; the engineer decides.** Root-cause confirmation remains outside the LLM.
5. **Failure should become abstention, not fabricated certainty.** Invalid output is converted into a structured human-review record.

## v0.1 components

- FastAPI interface;
- diagnostic service;
- versioned prompt registry;
- deterministic mock LLM adapter;
- optional OpenAI Responses API adapter;
- Pydantic contracts;
- evidence-reference validation;
- safety-sensitive input detection;
- trace events to stdout;
- synthetic engineering knowledge examples;
- automated contract tests.

## Evolution

Retrieval, tool calling, expanded escalation logic, and richer observability are deliberately introduced in later releases so each capability can be evaluated independently.
