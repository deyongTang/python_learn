from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):
    """A small task item tracked by the CLI."""

    id: str = Field(default_factory=lambda: uuid4().hex, description="Unique identifier")
    title: str = Field(..., min_length=1, description="Task summary")
    completed: bool = Field(False, description="Whether the task is done")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")


class TaskList(BaseModel):
    """Container for persisting a collection of tasks."""

    tasks: list[Task] = Field(default_factory=list)

    def add(self, title: str) -> Task:
        task = Task(title=title)
        self.tasks.append(task)
        return task

    def mark_complete(self, task_id: str) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                return task
        return None

    def remove_completed(self) -> None:
        self.tasks = [task for task in self.tasks if not task.completed]
