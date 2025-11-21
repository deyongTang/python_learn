"""命令行工具：读取 JSON 并使用 Pydantic 校验。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Optional

from .models import User
from .settings import get_settings


def read_json_source(path: Optional[Path], inline_json: Optional[str]) -> str:
    """读取 JSON 文本，可来自文件、内联字符串或标准输入。

    - 如果同时传入 `-f` 与 `-j`，视为用户误操作，直接提示冲突。
    - 当给定文件路径时，提前检查文件是否存在，给出中文错误信息。
    """

    if path and inline_json:
        raise ValueError("请仅选择文件(-f)或内联 JSON(-j) 之一，避免参数冲突")
    if inline_json:
        return inline_json
    if path:
        if not path.exists():
            raise FileNotFoundError(f"未找到指定的 JSON 文件：{path}")
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def validate_user(json_text: str) -> User:
    """解析并校验 JSON，返回 `User` 模型实例。"""

    return User.model_validate_json(json_text)


def format_user(user: User) -> str:
    """将用户数据与当前配置一起美化输出，方便学习观察。"""

    settings = get_settings()
    payload = {
        "settings": settings.model_dump(),
        "user": user.model_dump(mode="json"),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main(argv: Optional[Iterable[str]] = None) -> int:
    """命令行入口：演示 Pydantic 校验流程。"""

    parser = argparse.ArgumentParser(description="用 Pydantic 校验用户数据的示例 CLI")
    parser.add_argument("-f", "--file", type=Path, help="包含用户数据的 JSON 文件路径")
    parser.add_argument("-j", "--json", help="直接传入的内联 JSON 字符串")
    args = parser.parse_args(args=argv)

    try:
        json_text = read_json_source(args.file, args.json)
        user = validate_user(json_text)
        print(format_user(user))
    except Exception as exc:  # noqa: BLE001
        parser.exit(status=1, message=f"校验失败：{exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
