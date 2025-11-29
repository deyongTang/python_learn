from pathlib import Path

from .. import cli
from ..storage import TaskStorage


def test_storage_round_trip(tmp_path: Path) -> None:
    storage_file = tmp_path / "todos.json"
    storage = TaskStorage(storage_file)

    # Start empty
    task_list = storage.load()
    assert task_list.tasks == []

    # Add and persist
    task = task_list.add("写测试")
    storage.save(task_list)

    # Reload and validate
    reloaded = storage.load()
    assert len(reloaded.tasks) == 1
    assert reloaded.tasks[0].title == "写测试"
    assert not reloaded.tasks[0].completed

    # Mark complete and persist
    reloaded.mark_complete(task.id)
    storage.save(reloaded)
    completed = storage.load()
    assert completed.tasks[0].completed is True


def test_cli_end_to_end(tmp_path: Path, capsys) -> None:
    storage_path = tmp_path / "todos.json"

    cli.dispatch(["--storage", str(storage_path), "add", "阅读仓库文档"])
    output = capsys.readouterr().out
    assert "已添加" in output

    cli.dispatch(["--storage", str(storage_path), "list"])
    output = capsys.readouterr().out
    assert "阅读仓库文档" in output
    assert "⏳" in output

    # Capture ID from storage to complete the task
    storage = TaskStorage(storage_path)
    task_id = storage.load().tasks[0].id

    cli.dispatch(["--storage", str(storage_path), "complete", task_id])
    output = capsys.readouterr().out
    assert "已完成" in output

    cli.dispatch(["--storage", str(storage_path), "clear"])
    output = capsys.readouterr().out
    assert "已清理" in output
    # After clearing completed tasks, list should be empty
    task_list = storage.load()
    assert task_list.tasks == []
