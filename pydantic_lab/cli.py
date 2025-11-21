"""Command-line interface that validates user JSON input."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Optional

from .models import User
from .settings import get_settings


def read_json_source(path: Optional[Path], inline_json: Optional[str]) -> str:
    """Return JSON text from a file, inline string, or stdin."""

    if inline_json:
        return inline_json
    if path:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def validate_user(json_text: str) -> User:
    """Parse and validate JSON into a User model."""

    return User.model_validate_json(json_text)


def format_user(user: User) -> str:
    """Pretty-print user data along with the active settings."""

    settings = get_settings()
    payload = {
        "settings": settings.model_dump(),
        "user": user.model_dump(mode="json"),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a user payload with Pydantic")
    parser.add_argument("-f", "--file", type=Path, help="Path to a JSON file containing a user")
    parser.add_argument("-j", "--json", help="Inline JSON string to validate")
    args = parser.parse_args(args=argv)

    try:
        json_text = read_json_source(args.file, args.json)
        user = validate_user(json_text)
        print(format_user(user))
    except Exception as exc:  # noqa: BLE001
        parser.exit(status=1, message=f"Validation failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
