# Python 学习项目

本仓库包含 Python 基础与 Pydantic 学习资料（中文注释与文档方便自学）：

- `sample.ipynb` 与 `seq.ipynb`：字典与序列的示例与练习，推荐通过 Jupyter Notebook 交互学习。
- `pydantic_lab/`：使用 Pydantic 进行数据验证的示例（CLI、FastAPI、环境配置）。
- `python -m pydantic_lab.langgraph_pydantic_demo`：LangGraph + Pydantic 状态机示例，展示类型校验与节点状态合并。
- `docs/学习指南.md`：快速了解如何使用 Notebook 与 Pydantic 示例的中文技术文档。
- `docs/LangGraph学习指南.md`：LangGraph 入门与练习项目指引（含最小模板与练习思路）。
- `docs/Pydantic介绍.md`：Pydantic 的概念、常用模式与本仓库示例的中文入门介绍。
- `requirements.txt`：安装依赖以运行示例与测试（包含 Jupyter）。
- `python -m pydantic_lab.cli`：命令行校验 JSON 的示例，`-f` 与 `-j` 参数二选一；路径不存在会给出中文提示。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

如需以交互方式查看 Notebook，建议运行：

```bash
jupyter notebook
```

> 国内或受限网络环境可为 `pip` 指定镜像源（如清华）：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

FastAPI 示例运行：

```bash
uvicorn pydantic_lab.api:app --reload --host 0.0.0.0 --port 8000
```
