# Python 学习项目

本仓库包含 Python 基础与 Pydantic 学习资料：

- `sample.ipynb` 与 `seq.ipynb`：字典与序列的示例与练习。
- `pydantic_lab/`：使用 Pydantic 进行数据验证的示例（CLI、FastAPI、环境配置）。
- `requirements.txt`：安装依赖以运行示例与测试。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

FastAPI 示例运行：

```bash
uvicorn pydantic_lab.api:app --reload --host 0.0.0.0 --port 8000
```
