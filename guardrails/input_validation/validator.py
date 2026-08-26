from dataclasses import dataclass


SAFETY_TERMS = (
    "bypass interlock",
    "disable protection",
    "override trip",
    "force open",
    "force close",
    "operate valve",
    "trip the",
    "start the pump",
    "stop the pump",
)


@dataclass(frozen=True)
class InputAssessment:
    safety_sensitive: bool
    reasons: tuple[str, ...]


def assess_input(question: str) -> InputAssessment:
    q = question.lower()
    matches = tuple(term for term in SAFETY_TERMS if term in q)
    return InputAssessment(
        safety_sensitive=bool(matches),
        reasons=matches,
    )
