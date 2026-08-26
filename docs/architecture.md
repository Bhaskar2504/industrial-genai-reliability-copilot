# Architecture

## Design principles

1. **Evidence is a first-class object.** Evidence IDs and provenance exist independently of generated prose.
2. **Retrieval is inspectable.** The evidence selected before generation can be examined through `/retrieve`.
3. **Generation is not validation.** Model output is parsed and validated by application code.
4. **Prompts, schemas, retrieval and tools evolve independently.** Behavioural changes can be traced to the layer that changed.
5. **The model proposes; the engineer decides.** Root-cause confirmation remains outside the LLM.
6. **Failure should become abstention or escalation, not fabricated certainty.**

## v0.3 components

```text
Question
  |
  +--> input validation
  |
  +--> markdown knowledge loader
          |
          +--> stable chunk ID
          +--> source title/type
          +--> source locator
  |
  +--> deterministic lexical retriever
          |
          +--> ranked evidence chunks
  |
  +--> versioned diagnostic prompt
  |
  +--> mock / optional provider adapter
  |
  +--> Pydantic diagnostic contract
  |
  +--> evidence-ID grounding validation
  |
  +--> abstention / safety escalation
  |
  +--> trace event
```

## Why deterministic retrieval first

v0.3 deliberately uses a small TF-IDF cosine retriever implemented with the Python standard library. This creates a transparent baseline whose ranking can be reproduced and evaluated without a hosted embedding model or vector database.

The trade-off is visible in the published evaluation: lexical overlap can mis-rank ambiguous queries. Semantic embeddings, hybrid retrieval and reranking are future improvements rather than hidden dependencies in the baseline.

## Citation boundary

Retrieved chunks become `EvidenceRecord` objects before generation. The output validator checks that every cited evidence ID exists in the evidence carried by the output. Source locators bind those IDs back to the exact knowledge document and chunk.

This establishes citation traceability. Semantic claim-to-passage entailment is not yet asserted.

## Evolution

- **v0.1:** structured prompting and contracts;
- **v0.2:** reproducible evaluation baseline;
- **v0.3:** deterministic RAG and citation traceability;
- **v0.4:** deterministic engineering tool calling;
- **v0.5:** stronger guardrail and escalation policies;
- **v0.6:** richer observability and traceability;
- **v1.0:** integrated demonstration.
