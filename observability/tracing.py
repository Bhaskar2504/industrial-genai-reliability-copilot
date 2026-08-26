import json
from datetime import datetime, timezone


def trace(event: str, request_id: str, payload: dict | None = None, enabled: bool = True) -> None:
    if not enabled:
        return
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "request_id": request_id,
        "payload": payload or {},
    }
    print(json.dumps(record, sort_keys=True))
