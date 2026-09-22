import json
from pathlib import Path


def read_mock_emails(filename=None):
    path = Path(filename) if filename else Path(__file__).resolve().parent / "data/mock_emails.json"
    return json.loads(path.read_text(encoding="utf-8"))
