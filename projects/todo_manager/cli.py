from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .models import TaskList
from .storage import TaskStorage

DEFAULT_STORAGE = Path(__file__).resolve().parent / "data" / "todos.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="轻量级待办事项管理器（使用 Pydantic 校验与 JSON 持久化）",
    )
    parser.add_argument(
        "--storage",
        type=Path,
        default=DEFAULT_STORAGE,
        help="自定义存储文件路径，默认使用项目 data 目录下的 todos.json",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="添加一条待办事项")
    add_parser.add_argument("title", help="待办事项的标题")

    subparsers.add_parser("list", help="列出所有待办事项")

    complete_parser = subparsers.add_parser("complete", help="将事项标记为完成")
    complete_parser.add_argument("task_id", help="任务 ID，可从 list 输出中获取")

    subparsers.add_parser("clear", help="删除所有已完成的事项")

    return parser


def add_task(args: argparse.Namespace) -> None:
    storage = TaskStorage(args.storage)
    task_list = storage.load()
    task = task_list.add(args.title)
    storage.save(task_list)
    print(f"已添加: {task.title} (ID: {task.id})")


def list_tasks(args: argparse.Namespace) -> None:
    storage = TaskStorage(args.storage)
    task_list = storage.load()
    if not task_list.tasks:
        print("暂无待办事项，试试添加一条吧！")
        return

    for task in task_list.tasks:
        status = "✅" if task.completed else "⏳"
        print(f"{status} {task.title} (ID: {task.id})")


def complete_task(args: argparse.Namespace) -> None:
    storage = TaskStorage(args.storage)
    task_list = storage.load()
    task = task_list.mark_complete(args.task_id)
    if task:
        storage.save(task_list)
        print(f"已完成: {task.title}")
    else:
        print("未找到对应 ID 的任务，请检查后重试。")


def clear_completed(args: argparse.Namespace) -> None:
    storage = TaskStorage(args.storage)
    task_list = storage.load()
    before = len(task_list.tasks)
    task_list.remove_completed()
    after = len(task_list.tasks)
    storage.save(task_list)
    print(f"已清理 {before - after} 条已完成的任务，剩余 {after} 条待办。")


def dispatch(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    handlers = {
        "add": add_task,
        "list": list_tasks,
        "complete": complete_task,
        "clear": clear_completed,
    }
    handler = handlers[args.command]
    handler(args)


def main() -> None:
    dispatch()


if __name__ == "__main__":
    main()
