# Industrial GenAI Reliability Copilot

A production-informed GenAI application demonstrating how industrial reliability and Asset Performance Management expertise can be translated into evidence-grounded engineering workflows using structured prompting, automated evaluation, guardrails, citations, traceability and human-review controls.

> **Current capability: v0.2 — Evaluation Baseline.** v0.1 established structured prompting and output contracts. v0.2 adds a reproducible synthetic evaluation dataset, scoring harness, repeated-run checks, and a public report that deliberately includes a failing case.

## 1. The industrial reliability problem

Industrial troubleshooting is not a generic question-answering problem. Engineers need answers that distinguish observations from hypotheses, show the evidence behind each claim, respect equipment operating context, expose uncertainty, and escalate when evidence is insufficient.

A useful reliability copilot therefore needs more than an LLM call. It needs explicit engineering contracts, evidence handling, testable behavior and clear limits on what the system is allowed to claim.

## 2. Intended users and use cases

**Intended users**

- reliability and maintenance engineers;
- condition-monitoring engineers;
- plant performance engineers;
- Industrial AI / APM practitioners;
- technical consultants translating engineering requirements into AI workflows.

**Example use cases**

- structure an initial diagnostic assessment from observed symptoms;
- compare plausible failure mechanisms rather than jump to one root cause;
- connect hypotheses to explicit evidence IDs;
- identify missing checks before a maintenance decision;
- abstain or escalate when evidence is insufficient or the request is safety-sensitive.

## 3. What the system does — and does not do

### It does

- use a versioned diagnostic prompt;
- return a structured diagnostic record;
- separate hypotheses from confirmed facts;
- require traceable evidence identifiers;
- validate output structure and evidence references;
- abstain when no evidence is available;
- route safety-sensitive requests to qualified human review;
- support deterministic mock execution for reproducible testing;
- optionally use an LLM provider behind the same validation layer;
- publish successful **and failed** evaluation cases.

### It does not

- replace qualified engineering judgement;
- bypass plant procedures, OEM requirements, interlocks or protection systems;
- provide autonomous control actions;
- claim a root cause solely because a model produced a plausible explanation;
- use employer, customer or proprietary plant information;
- claim real-world diagnostic accuracy from synthetic tests.

## 4. Architecture and data flow

```text
Engineering question
        |
        v
Input validation
        |
        v
Asset context + evidence records
        |
        v
Versioned diagnostic prompt
        |
        v
LLM adapter / deterministic mock
        |
        v
Structured JSON response
        |
        v
Schema + evidence validation
        |
        +---- insufficient / unsafe ----> human escalation
        |
        v
Trace record + engineering response
```

See [`docs/architecture.md`](docs/architecture.md).

## 5. Diagnostic workflow

The reasoning pattern is deliberately engineering-led:

**Context → Observations → Relationships → Plausible mechanisms → Contradicting evidence → Confidence → Next checks → Escalation if needed**

The prompt explicitly treats an anomaly as evidence, not automatically as a confirmed failure mode.

The structured response includes:

- problem summary;
- asset context;
- diagnostic hypotheses;
- supporting and contradicting evidence IDs;
- confidence;
- recommended checks;
- safety notes;
- abstention state;
- escalation record;
- prompt/schema version information.

## 6. RAG and citation approach

**Status: RAG is planned for v0.3 and is not yet implemented.**

v0.2 still receives evidence records explicitly. This is intentional: prompt behavior, output contracts, evaluation and safety controls are being tested before retrieval is introduced.

The v0.3 design will:

- ingest only synthetic or clearly licensed public sources;
- preserve source provenance and stable evidence IDs;
- retrieve candidate evidence independently of generation;
- validate that cited evidence exists in the retrieved set;
- measure retrieval precision separately from answer quality.

See [`knowledge/sources.md`](knowledge/sources.md).

## 7. Structured outputs and engineering tools

The machine-readable contracts are defined in:

- [`schemas/diagnostic_output.json`](schemas/diagnostic_output.json)
- [`schemas/evidence_record.json`](schemas/evidence_record.json)
- [`schemas/escalation_record.json`](schemas/escalation_record.json)

Pydantic models provide the runtime validation layer.

**Engineering tool calling is planned for v0.4.** Reserved modules exist for trend analysis, alarm/event analysis and failure-mode lookup, but they are not presented as implemented capability yet.

## 8. Evaluation methodology and current results

Evaluation is treated as part of the application, not as a final demo step.

v0.2 introduces an 8-case deterministic synthetic baseline covering:

- diagnostic relevance / failure-mode coverage;
- evidence citation-ID accuracy;
- structured-output validity;
- unsupported-claim structural proxy;
- abstention behavior;
- repeated-run consistency;
- safety-sensitive human escalation;
- an adversarial evidence-text case;
- a deliberately conflicting-evidence case.

### Current v0.2 baseline

| Metric | Result |
|---|---:|
| Cases | 8 |
| Passed | 7 |
| Failed | 1 |
| Case pass rate | **87.5%** |
| Structured-output validity | **100%** |
| Evidence citation-ID accuracy | **100%** |
| Required citation coverage | **100%** |
| Unsupported-claim rate — structural proxy | **0%** |
| Failure-mode coverage | **100%** |
| Abstention accuracy | **87.5%** |
| Repeated-run consistency | **100%** |
| Human-escalation accuracy | **87.5%** |
| Retrieval precision | N/A until v0.3 |
| Tool-call correctness | N/A until v0.4 |

The failed case is intentionally public: conflicting pump-restriction and sensor-quality evidence should cause more uncertainty, but the current deterministic baseline prioritizes the pump keyword and does not abstain. That limitation is documented rather than hidden.

The unsupported-claim metric is currently only a **structural proxy**. It checks whether hypotheses carry supplied evidence IDs; it does not yet prove semantic entailment between each claim and cited passage.

See [`evaluation/reports/v0.2-baseline.md`](evaluation/reports/v0.2-baseline.md), [`evaluation/datasets/v0.2_baseline.json`](evaluation/datasets/v0.2_baseline.json) and [`docs/evaluation.md`](docs/evaluation.md).

## 9. Guardrails and human-review requirements

Current controls include:

- request validation;
- safety-sensitive phrase detection;
- structured-output validation;
- rejection of unknown evidence IDs;
- abstention when evidence is absent;
- fallback escalation when model output cannot be validated;
- urgent human review for requests involving protection/interlock bypass behavior;
- trace metadata without logging full engineering evidence text.

A qualified engineer remains responsible for material operating or maintenance decisions.

See [`docs/safety-and-limitations.md`](docs/safety-and-limitations.md) and [`docs/threat-model.md`](docs/threat-model.md).

## 10. Installation and demonstration

### Requirements

- Python 3.11+
- no API key required for the deterministic mock path

### Install

```bash
git clone https://github.com/Bhaskar2504/industrial-genai-reliability-copilot.git
cd industrial-genai-reliability-copilot
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env
```

### Run tests

```bash
pytest -q
```

### Run the diagnostic demonstration

```bash
python -m examples.demo_v01
```

### Run the v0.2 evaluation baseline

```bash
python evaluation/run_baseline.py
```

This regenerates the human-readable report and a local machine-readable result file.

### Run the API

```bash
uvicorn app.api.main:app --reload
```

Then open the local FastAPI `/docs` endpoint.

### Optional OpenAI backend

The default backend is deterministic `mock`. An optional adapter uses the OpenAI Responses API. Configure it through `.env`; model output still passes through the same application-level validation and escalation controls.

## 11. Screenshots or short demonstration

Demonstration media will be added only after the UI/API workflow is stable. Guidance is kept in [`screenshots/README.md`](screenshots/README.md).

## 12. Limitations and planned improvements

Current limitations include:

- synthetic rather than field data;
- deterministic heuristic mock behavior is not a real diagnostic model;
- contradiction-aware reasoning is weak and is exposed by the failed v0.2 case;
- semantic claim-support evaluation is not yet implemented;
- retrieval is not implemented yet;
- engineering tools are not implemented yet;
- confidence values are not calibrated probabilities;
- production authentication, persistent tracing and RBAC are outside the current scope.

## 13. Data provenance and confidentiality

This is an independent personal project. It is not affiliated with, sponsored by, or endorsed by any employer, customer, plant operator or software vendor.

Only synthetic, generated, or clearly licensed public engineering information may be committed. Employer/customer documents, plant tag data, alert histories, internal FDS/SOP material, proprietary failure-mode libraries, credentials, customer names and identifiable operational information are prohibited.

See [`knowledge/sources.md`](knowledge/sources.md), [`SECURITY.md`](SECURITY.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Release evolution

| Release | Capability | Status |
|---|---|---|
| v0.1 | Structured Prompting | implemented |
| **v0.2** | Evaluation Baseline | **current** |
| v0.3 | RAG and Citations | planned |
| v0.4 | Engineering Tool Calling | planned |
| v0.5 | Guardrails and Human Escalation | planned |
| v0.6 | Observability and Traceability | planned |
| v1.0 | Integrated Demonstration | planned |

The Git history is intended to reflect real capability changes. Later versions will be marked only after the corresponding capability is implemented and reproducible.

## Safety statement

This application supports engineering analysis. It does not replace qualified engineering judgement, approved safety procedures, OEM guidance, plant operating procedures or formal maintenance decision processes.

## License

MIT — see [`LICENSE`](LICENSE).
