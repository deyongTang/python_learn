# Todo Manager（独立目录示例）

这个小项目展示了如何在仓库中将脚本功能放在独立目录中进行隔离。它提供了一个基于命令行的待办事项管理器，使用 Pydantic 进行数据校验，并通过 JSON 文件持久化。

## 功能与特点

- `add`：新增待办事项，自动生成唯一 ID 和时间戳。
- `list`：以 ✅ / ⏳ 符号展示当前任务列表。
- `complete`：根据任务 ID 将事项标记为完成。
- `clear`：清理所有已完成的任务，保持列表整洁。
- 支持 `--storage` 参数自定义存储位置，默认使用本目录下的 `data/todos.json`。

## 快速开始

```bash
# 添加任务
python -m projects.todo_manager.cli add "阅读 Pydantic 文档"

# 查看列表
python -m projects.todo_manager.cli list

# 标记完成（将 <ID> 替换为 list 输出中的值）
python -m projects.todo_manager.cli complete <ID>

# 清理已完成任务
python -m projects.todo_manager.cli clear
```

## 运行测试

```bash
pytest projects/todo_manager/tests
```

## 目录结构

```
projects/
  todo_manager/
    cli.py          # 命令行入口
    models.py       # Pydantic 数据模型
    storage.py      # 文件读写逻辑
    data/           # 默认存储目录（包含 .gitkeep 以确保目录存在）
    tests/          # 单元测试
```

使用时请保持该目录与仓库其他脚本隔离，便于独立维护与演示。
