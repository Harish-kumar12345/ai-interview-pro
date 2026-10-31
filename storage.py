import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HISTORY_PATH = Path(__file__).parent / "data" / "interview_history.json"


def load_history(path: Path = HISTORY_PATH) -> list[dict[str, Any]]:
    try:
        if not path.exists():
            return []
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, list) else []
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Unable to read interview history.") from exc


def save_interview(record: dict[str, Any], path: Path = HISTORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    history = load_history(path)
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **record}
    temporary_path = path.with_suffix(".tmp")
    try:
        temporary_path.write_text(json.dumps([record, *history], indent=2), encoding="utf-8")
        temporary_path.replace(path)
    except OSError as exc:
        raise RuntimeError("Unable to save interview history.") from exc