from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Task, TaskList


class TaskStorage:
    """Persistence layer for storing tasks in a JSON file."""

    def __init__(self, storage_file: Path):
        self.storage_file = storage_file
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> TaskList:
        if not self.storage_file.exists():
            return TaskList()

        content = self.storage_file.read_text(encoding="utf-8")
        if not content.strip():
            return TaskList()

        data = json.loads(content)
        return TaskList.model_validate(data)

    def save(self, task_list: TaskList) -> None:
        payload = task_list.model_dump(mode="json")
        self.storage_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def write_all(self, tasks: Iterable[Task]) -> None:
        task_list = TaskList(tasks=list(tasks))
        self.save(task_list)
