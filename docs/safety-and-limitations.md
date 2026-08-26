# Safety and Limitations

## Safety boundary

This application is engineering decision support. It is not a control system, safety instrumented system, protection system, operating procedure, maintenance instruction, or OEM substitute.

## Required human role

A qualified engineer must review material conclusions before operating or maintenance action.

## Key limitations

- LLM outputs can be incorrect even when fluent.
- Confidence fields are not calibrated probabilities.
- Synthetic data cannot establish plant performance.
- Missing or poor evidence can make a plausible explanation wrong.
- Failure mechanisms can share similar signal patterns.
- Instrument faults and process changes can imitate equipment degradation.
- Later RAG quality will depend on source quality and retrieval behavior.

## Safe behavior

When evidence is insufficient, contradictory, invalid, or safety-sensitive, the preferred output is abstention plus a clear request for human review.
