# Pydantic 是什么？

Pydantic 是一个基于 Python 类型注解的**数据验证与设置管理**库，可以在模型创建时自动校验字段类型、约束并给出可读的错误信息。它常用于：

- **API/表单/CLI 请求体验证**：保证输入数据符合预期类型与范围。
- **配置加载**：从环境变量或 `.env` 文件中读取设置并验证。
- **数据序列化/反序列化**：将模型安全地转换为字典或 JSON。

本仓库的 `pydantic_lab/` 目录包含完整示例（CLI、FastAPI、环境配置），所有注释均为中文，适合自学。

## 核心特性速览
- **基于类型提示**：用标准注解声明字段类型，自动校验并转换。
- **字段约束**：通过 `Field` 设置最小/最大长度、默认值、描述等。
- **自定义校验器**：使用 `@field_validator` 或 `@model_validator` 处理复杂规则。
- **配置灵活**：`BaseSettings` 可读取环境变量并支持 `.env` 文件。
- **友好的错误信息**：返回结构化错误，便于定位问题。

## 快速上手示例
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    """用户模型：演示必填字段、默认值和约束。"""
    id: int
    name: str = Field(..., min_length=1, description="用户名不能为空")
    email: str = Field(..., pattern=r".+@.+", description="必须是邮箱格式")

# 创建并自动校验
user = User.model_validate({"id": 1, "name": "Alice", "email": "a@example.com"})

# 序列化
as_dict = user.model_dump()       # 转换为字典
as_json = user.model_dump_json()  # 转换为 JSON 字符串
```

## 常用模式
### 字段约束与默认值
```python
from pydantic import Field
from pydantic import BaseModel

class Article(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, description="标题长度 3-50")
    tags: list[str] = Field(default_factory=list, description="标签列表，默认空")
```

### 自定义字段校验
```python
from pydantic import BaseModel, field_validator

class Login(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def check_strength(cls, value: str) -> str:
        """确保密码至少 8 位且包含数字。"""
        if len(value) < 8 or not any(ch.isdigit() for ch in value):
            raise ValueError("密码需要至少 8 位并包含数字")
        return value
```

### 模型组合与嵌套
```python
from pydantic import BaseModel

class Profile(BaseModel):
    bio: str | None = None
    city: str | None = None

class UserWithProfile(User):
    profile: Profile | None = None
```

### 配置与环境变量
```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    db_url: str
    debug: bool = False

    class Config:
        env_file = ".env"  # 支持从 .env 读取

settings = AppSettings()  # 自动读取环境变量并校验
```

## 本仓库如何实践
- **模型示例**：阅读 `pydantic_lab/models.py`，包含基本字段约束、嵌套模型与 `RootModel` 的中文注释。
- **配置加载**：`pydantic_lab/settings.py` 展示如何通过 `BaseSettings` 读取 `.env` 并在代码中复用。
- **命令行校验**：运行 `python -m pydantic_lab.cli -j '{"id":1,"name":"Alice","email":"alice@example.com"}'`，或使用 `-f data.json` 从文件读取。`-f` 与 `-j` 互斥，路径错误会输出中文提示。
- **FastAPI 示例**：启动 `uvicorn pydantic_lab.api:app --reload --host 0.0.0.0 --port 8000`，通过 `POST /users` 与 `GET /users/{id}` 体验请求体验证。
- **测试练习**：`pydantic_lab/tests/test_pydantic_lab.py` 覆盖了模型验证、CLI 参数冲突等场景，可据此添加更多边界测试。

## 进一步学习建议
1. 在 Notebook 中编写自己的 `BaseModel`，尝试不同的字段约束与校验器。
2. 扩充 FastAPI 示例：增加分页、查询参数或自定义错误响应。
3. 结合 `pydantic` 与 `typing` 高级用法（如 `Annotated`、`Literal`）实现更严格的接口契约。
