from pathlib import Path

PROMPT_VERSION = "diagnostic-v0.1"
PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "diagnostic" / "v0.1.txt"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "diagnostic_output.json"


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def load_schema_text() -> str:
    return SCHEMA_PATH.read_text(encoding="utf-8")
