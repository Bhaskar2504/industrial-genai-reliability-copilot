# Industrial GenAI Reliability Copilot

A production-informed GenAI application demonstrating how industrial reliability and Asset Performance Management expertise can be translated into evidence-grounded engineering workflows using structured prompting, Retrieval-Augmented Generation, engineering tool calling, automated evaluation, guardrails, citations, observability and human-review controls.

> **Current release target: v0.1 — Structured Prompting.** The repository is intentionally being built in genuine capability stages. Features planned for later releases are clearly marked and are not presented as already complete.

## Why this project exists

Industrial troubleshooting is not a generic question-answering problem. Engineers need answers that distinguish observations from hypotheses, show the evidence behind each claim, respect equipment operating context, expose uncertainty, and escalate when the evidence is insufficient.

This project is designed to demonstrate how those requirements can be built into a GenAI workflow rather than added as an afterthought.

## v0.1 scope

The initial baseline focuses on:

- versioned diagnostic prompts;
- structured engineering output contracts;
- synthetic evidence records;
- deterministic mock execution for repeatable tests;
- optional LLM adapter behind the same contract;
- input and output validation;
- unsupported-citation detection;
- insufficient-evidence abstention;
- human-escalation logic;
- lightweight trace records;
- contract and guardrail tests.

RAG, engineering tool calling, full evaluation benchmarking, production observability and an integrated demonstration are planned for later releases.

## Intended users

- reliability engineers;
- maintenance and condition-monitoring engineers;
- plant performance engineers;
- Industrial AI / APM practitioners;
- technical consultants translating engineering workflows into AI systems.

## What the system does

Given an engineering question and a set of evidence records, the diagnostic workflow produces a structured response containing:

1. problem framing;
2. observations supported by evidence;
3. plausible failure-mode hypotheses;
4. evidence supporting or contradicting each hypothesis;
5. confidence and uncertainty;
6. recommended engineering checks;
7. cited evidence identifiers;
8. abstention or escalation status when appropriate.

## What it does not do

The application does **not**:

- replace qualified engineering judgement;
- bypass plant safety procedures, OEM requirements or maintenance procedures;
- claim a root cause when evidence is insufficient;
- provide autonomous control actions;
- use employer, customer or proprietary plant information.

## Architecture

```text
Engineering question
        |
        v
Input validation
        |
        v
Prompt registry + version
        |
        v
Evidence records ---------> evidence provenance
        |
        v
LLM / deterministic mock
        |
        v
Structured JSON response
        |
        v
Schema + citation validation
        |
        +---- insufficient / unsafe ----> human escalation
        |
        v
Trace record + engineering response
```

See [`docs/architecture.md`](docs/architecture.md) for the architecture and planned evolution.

## Diagnostic workflow

The core reasoning pattern is deliberately engineering-led:

**Context → Observations → Relationships → Plausible mechanisms → Contradicting evidence → Confidence → Next checks → Escalation if needed**

The prompt explicitly separates an anomaly from a confirmed failure mode. A statistically unusual condition is treated as evidence, not automatically as a diagnosis.

## Structured outputs

The main contract is defined in [`schemas/diagnostic_output.json`](schemas/diagnostic_output.json). Supporting evidence and escalation schemas live in the same directory.

Structured output is important because it makes the application testable. Claims, citations, confidence, escalation state and recommended checks can be validated independently instead of judging only whether prose sounds convincing.

## RAG and citations

**Status in v0.1: interface prepared; retrieval implementation planned for v0.3.**

The intended RAG design will retrieve only from synthetic or clearly licensed public engineering material. Retrieved chunks will carry stable evidence IDs and provenance metadata. Diagnostic claims will be allowed to cite only evidence IDs supplied to the generation step.

The v0.1 baseline already validates that returned citations exist in the supplied evidence set, which establishes the contract needed before retrieval is added.

## Engineering tools

**Status in v0.1: planned interfaces only; implementation planned for v0.4.**

Planned deterministic tools include:

- trend analysis;
- alarm/event-window analysis;
- failure-mode lookup.

The design principle is that arithmetic, lookup and deterministic engineering logic should be executed by tools where possible rather than improvised by a language model.

## Evaluation

Evaluation is treated as part of the product, not a final demo step.

Planned measurable dimensions include:

- diagnostic relevance;
- evidence citation accuracy;
- structured-output validity;
- unsupported-claim rate;
- retrieval precision;
- failure-mode coverage;
- abstention when evidence is insufficient;
- repeated-run consistency;
- tool-call correctness;
- human-escalation accuracy.

v0.1 contains contract-level tests and synthetic test cases. A quantitative evaluation baseline is the goal of v0.2. Successful and failed test cases will both be retained.

See [`docs/evaluation.md`](docs/evaluation.md).

## Guardrails and human review

The system is designed to fail safely when possible. Examples include:

- rejecting empty or malformed requests;
- requiring traceable evidence identifiers;
- checking output schema validity;
- detecting citations that were never provided to the model;
- escalating safety-critical or insufficient-evidence situations;
- preventing a generated answer from being represented as an autonomous maintenance instruction.

See [`docs/safety-and-limitations.md`](docs/safety-and-limitations.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate       # Windows
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
```

The deterministic mock mode does not require an API key.

### 4. Run tests

```bash
pytest
```

### 5. Run the v0.1 example

```bash
python -m examples.demo_v01
```

### 6. Run the API

```bash
uvicorn app.api.main:app --reload
```

Open `/docs` on the local FastAPI server for the interactive API schema.

## Repository map

```text
app/             API, orchestration, configuration and optional UI
prompts/         versioned prompt assets
schemas/         machine-validatable engineering contracts
knowledge/       synthetic and future public-source material
rag/             ingestion, retrieval and citation components
 tools/           deterministic engineering tool interfaces
 evaluation/      datasets, metrics, cases and reports
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
| **v0.1** | Structured Prompting | **current** |
| v0.2 | Evaluation Baseline | planned |
| v0.3 | RAG and Citations | planned |
| v0.4 | Engineering Tool Calling | planned |
| v0.5 | Guardrails and Human Escalation | planned |
| v0.6 | Observability and Traceability | planned |
| v1.0 | Integrated Demonstration | planned |

Releases will be created only when the corresponding capability is implemented and reproducible. The Git history will reflect actual development work rather than artificial milestone commits.

## Data provenance and confidentiality

This is an independent personal project. It is not affiliated with, sponsored by, or endorsed by any employer, customer, plant operator or software vendor.

Only synthetic, generated, or clearly licensed public engineering information may be committed. The repository must not contain employer/customer documents, plant tag data, alert histories, functional-design documents, internal SOPs, source code, proprietary failure-mode libraries, credentials, customer names or identifiable operational information.

See [`knowledge/sources.md`](knowledge/sources.md), [`SECURITY.md`](SECURITY.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Safety statement

This application supports engineering analysis. It does not replace qualified engineering judgement, approved safety procedures, OEM guidance, plant operating procedures or formal maintenance decision processes.

## License

See [`LICENSE`](LICENSE).
