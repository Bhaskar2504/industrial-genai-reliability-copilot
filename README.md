# Industrial GenAI Reliability Copilot

A production-informed GenAI application showing how industrial reliability and Asset Performance Management expertise can be translated into evidence-grounded engineering troubleshooting workflows with structured outputs, retrieval, citations, evaluation, guardrails and human review.

> **Current capability: v0.3 — RAG and Citations.** The repository is built in genuine capability stages. Later features are not presented as complete before they are implemented and tested.

## Why this project exists

Industrial troubleshooting is not a generic question-answering problem. Engineers need answers that distinguish observations from hypotheses, show the evidence behind each claim, respect operating context, expose uncertainty, and escalate when evidence is insufficient.

The project therefore treats **engineering usefulness, evidence quality, evaluation and governance** as first-class requirements rather than wrapping a chat interface around an LLM.

## Current capability

v0.3 adds a deterministic local Retrieval-Augmented Generation path over synthetic engineering notes:

- markdown knowledge ingestion;
- stable chunk-level evidence IDs;
- provenance and source locators;
- deterministic TF-IDF cosine retrieval;
- `/retrieve` API for retrieval inspection;
- `/diagnose/rag` API for retrieval-grounded diagnosis;
- versioned `diagnostic-v0.3` prompt;
- validation that generated citation IDs came from the retrieved evidence set;
- retrieval evaluation with a visible failed case;
- no API key required for the reproducible mock demonstration.

Existing v0.1/v0.2 controls remain in place: structured outputs, schemas, abstention, safety escalation, prompt injection treatment, trace events and automated tests.

## Intended users and use cases

Designed for reliability, maintenance, condition-monitoring, plant-performance and Industrial AI practitioners who need decision support for questions such as:

- What evidence is relevant to this equipment symptom?
- Which failure mechanisms are plausible rather than merely statistically unusual?
- What evidence supports or contradicts a hypothesis?
- What engineering checks should reduce uncertainty?
- When should the system abstain and escalate to a qualified engineer?

## What the system does — and does not do

The copilot can retrieve relevant engineering notes, construct traceable evidence records, produce structured diagnostic hypotheses, cite the evidence IDs supplied to generation, recommend engineering checks, abstain when evidence is absent, and escalate safety-sensitive requests.

It does **not** confirm root cause autonomously, replace qualified engineering judgement, bypass plant procedures or OEM requirements, issue control actions, or use employer/customer information.

## Architecture and data flow

```text
Engineering question
        |
        v
Input validation
        |
        v
Knowledge ingestion -> chunk IDs + provenance
        |
        v
Deterministic retrieval -----> /retrieve inspection
        |
        v
Retrieved evidence records
        |
        v
Versioned diagnostic prompt
        |
        v
LLM / deterministic mock
        |
        v
Structured JSON output
        |
        v
Schema + citation validation
        |
        +---- insufficient / unsafe ----> human escalation
        |
        v
Trace record + engineering response
```

See [`docs/architecture.md`](docs/architecture.md).

## Diagnostic workflow

The reasoning frame is deliberately engineering-led:

**Context → Evidence quality → Observations → Relationships → Plausible mechanisms → Contradicting evidence → Confidence → Next checks → Escalation if needed**

An anomaly is evidence, not a confirmed failure mode.

## RAG and citation approach

The v0.3 knowledge base contains only synthetic engineering notes. Each markdown document is split into stable paragraph-level chunks. Every chunk carries an evidence ID, source title, source type, excerpt, source locator and document path.

Retrieval uses a deterministic TF-IDF cosine scorer. This is intentionally simple and inspectable; it provides a measurable baseline before semantic retrieval or reranking is introduced.

The generation layer is allowed to cite only evidence IDs in the retrieved set. Output validation rejects unsupported citation IDs. This is **structural grounding**, not a claim that every generated sentence has been semantically entailed by its citation.

## Structured outputs and engineering tools

The main diagnostic contract is defined in [`schemas/diagnostic_output.json`](schemas/diagnostic_output.json). Supporting evidence and escalation schemas live alongside it.

Deterministic engineering tool calling is the next capability stage, **v0.4**. Planned tools include trend analysis, alarm/event-window analysis and failure-mode lookup. They are not represented as implemented yet.

## Evaluation methodology and results

Evaluation is part of the repository, not a final presentation layer.

### v0.2 — workflow baseline

- 8 synthetic cases;
- 7 passed, 1 deliberately retained failure;
- 100% structured-output validity;
- 100% evidence citation-ID accuracy;
- 87.5% abstention accuracy;
- 87.5% human-escalation accuracy.

### v0.3 — retrieval and citations

- 7 retrieval cases;
- 6 passed, 1 deliberately retained ambiguous-query failure;
- **85.7% retrieval precision@1**;
- **100% citation-ID accuracy**;
- **100% source-locator completeness**;
- **100% repeated retrieval consistency**.

The failed v0.3 case is a useful limitation: a simple lexical retriever can overweight overlapping pump/flow terms and miss the intended motor-current context.

See [`evaluation/reports/v0.3-rag-and-citations.md`](evaluation/reports/v0.3-rag-and-citations.md) and [`docs/evaluation.md`](docs/evaluation.md).

## Guardrails and human review

Controls include malformed/empty input rejection, evidence-ID validation, schema validation, unsupported-citation detection, insufficient-evidence abstention, safety-sensitive escalation, explicit prohibition on bypassing protections or procedures, and treating retrieved text as untrusted evidence rather than executable instructions.

See [`docs/safety-and-limitations.md`](docs/safety-and-limitations.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Installation and demonstration

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env
pytest -q
python evaluation/run_retrieval_v03.py
uvicorn app.api.main:app --reload
```

The default deterministic mock mode requires no API key.

Useful endpoints: `GET /health`, `POST /retrieve`, `POST /diagnose`, and `POST /diagnose/rag`.

Open `/docs` on the local FastAPI server for the interactive API schema.

## Repository map

```text
app/             API, orchestration, configuration and provider adapter
prompts/         versioned diagnostic prompts
schemas/         machine-validatable engineering contracts
knowledge/       synthetic/public-safe source material and provenance register
rag/             ingestion, retrieval and citation components
tools/           deterministic engineering tools (v0.4 target)
evaluation/      datasets, metrics, cases and public reports
guardrails/      input, output and escalation controls
observability/   trace model and later instrumentation
tests/           automated tests
docs/            architecture, evaluation, safety and decisions
examples/        runnable demonstrations
screenshots/     future demonstration media
```

## Release evolution

| Release | Capability | Status |
|---|---|---|
| v0.1 | Structured Prompting | complete |
| v0.2 | Evaluation Baseline | complete |
| **v0.3** | **RAG and Citations** | **current** |
| v0.4 | Engineering Tool Calling | planned |
| v0.5 | Guardrails and Human Escalation | planned expansion |
| v0.6 | Observability and Traceability | planned expansion |
| v1.0 | Integrated Demonstration | planned |

Releases are advanced only after the corresponding capability exists and is reproducible.

## Limitations and planned improvements

Current limitations include a small synthetic knowledge base, lexical rather than semantic retrieval, no reranker, no semantic entailment evaluator for citation support, deliberately simple deterministic mock reasoning, no production vector store, and no deterministic engineering tool calling yet.

These limitations are visible by design. The project is intended to demonstrate disciplined evolution, not an artificially complete production claim.

## Data provenance and confidentiality

This is an independent personal project. It is not affiliated with, sponsored by, or endorsed by any employer, customer, plant operator or software vendor.

Only synthetic, generated, or clearly licensed public engineering information may be committed. Employer/customer documents, plant tag data, alert histories, functional-design documents, internal SOPs, proprietary failure-mode libraries, credentials and identifiable operational information are prohibited.

See [`knowledge/sources.md`](knowledge/sources.md), [`SECURITY.md`](SECURITY.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Safety statement

This application supports engineering analysis. It does not replace qualified engineering judgement, approved safety procedures, OEM guidance, plant operating procedures or formal maintenance decision processes.

## License

See [`LICENSE`](LICENSE).
