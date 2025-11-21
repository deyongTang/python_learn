from __future__ import annotations

import json
from pathlib import Path

from pydantic_lab.cli import format_user, read_json_source, validate_user
from pydantic_lab.models import TagList, User
from pydantic_lab.settings import AppSettings


def test_user_validation_strips_whitespace():
    payload = json.dumps({"id": 1, "name": " Alice ", "email": "alice@example.com"})
    user = validate_user(payload)
    assert user.name == "Alice"


def test_taglist_normalizes_to_lowercase():
    tags = TagList.model_validate(["PyCon", "PYTHON"])
    assert tags.root == ["pycon", "python"]


def test_cli_format_includes_settings(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("APP_DB_URL", "sqlite:///demo.db")
    monkeypatch.setenv("APP_DEBUG", "true")
    user_json = tmp_path / "user.json"
    user_json.write_text(json.dumps({"id": 2, "name": "Bob", "email": "bob@example.com"}), encoding="utf-8")

    raw_json = read_json_source(path=user_json, inline_json=None)
    user = validate_user(raw_json)
    formatted = json.loads(format_user(user))

    assert formatted["settings"]["db_url"] == "sqlite:///demo.db"
    assert formatted["settings"]["debug"] is True
    assert formatted["user"]["email"] == "bob@example.com"


def test_settings_read_from_env(monkeypatch):
    monkeypatch.setenv("APP_DB_URL", "postgresql://localhost:5432/app")
    settings = AppSettings()
    assert settings.db_url.startswith("postgresql://")


def test_read_json_source_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin.read", lambda: "{\"id\":3,\"name\":\"Cara\",\"email\":\"c@example.com\"}")
    text = read_json_source(path=None, inline_json=None)
    assert "Cara" in text
    assert validate_user(text).id == 3
