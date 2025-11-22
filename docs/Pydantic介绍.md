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

## BaseModel 是什么、如何使用
`BaseModel` 是 Pydantic 的核心基类，用类型注解声明数据模型，并在实例化时自动完成**类型转换**与**校验**。它适合用来描述接口入参、配置、业务领域对象。

特性速览
- 类型驱动：根据注解尽力转换输入（如 `"1"` 转为 `int`），失败抛出 `ValidationError`。
- 默认值与必填：未提供默认值的字段必填；`Field` 可指定约束、别名、描述。
- 序列化：`model_dump()`/`model_dump_json()` 可控制包含/排除、按别名导出。
- 校验扩展：`@field_validator` 做字段校验，`@model_validator` 处理跨字段逻辑。
- 额外字段策略：`extra="forbid" | "ignore" | "allow"` 决定未声明字段的处理方式。
- 不可变模型：`ConfigDict(frozen=True)` 可使实例属性只读。
- 模型嵌套与集合：子模型、列表、字典会递归校验。
- 实用方法：`model_validate`/`model_validate_json` 从对象或 JSON 创建；`model_copy(update=...)` 基于现有实例复制并修改。

使用示例（Pydantic v2）
```python
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict

class Account(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: int
    name: str = "anonymous"
    email: str = Field(..., alias="e_mail")
    age: int | None = None

    @field_validator("email")
    @classmethod
    def must_be_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("邮箱格式错误")
        return v

try:
    acc = Account(id="1", e_mail="a@b.com", age="20")
    print(acc.id, type(acc.id))             # 自动转成 int
    print(acc.model_dump())                 # {'id': 1, 'name': 'anonymous', 'email': 'a@b.com', 'age': 20}
    print(acc.model_dump(by_alias=True))    # {'id': 1, 'name': 'anonymous', 'e_mail': 'a@b.com', 'age': 20}
except ValidationError as e:
    print(e)                                # 结构化的错误信息
```

使用建议
1. 在生产环境将 `extra` 设为 `forbid`，避免静默接受未声明字段。
2. 通过 `Field` 提前声明长度、范围等约束，错误更早暴露。
3. 使用校验器保持业务规则清晰明了，错误消息针对最终用户。
4. 若需要只读对象或值对象模式，启用 `frozen=True`。

## LangGraph + Pydantic 案例
- 位置：`pydantic_lab/langgraph_pydantic_demo.py`
- 运行：`python -m pydantic_lab.langgraph_pydantic_demo`
- 依赖：`pip install langgraph>=0.2.30`（已写入 `requirements.txt`）

案例说明
- 用 `ChatState(BaseModel)` 定义 LangGraph 的状态结构与约束，`steps` 字段通过 `Annotated[..., operator.add]` 让节点返回的步骤列表自动累加。
- `classify_intent` 节点根据输入文本标注意图；`craft_response` 节点根据意图生成回复，均返回部分状态更新。
- `StateGraph(ChatState)` 会在节点边界执行 Pydantic 校验与类型转换（例如传入整数会被转为字符串）。
- `app.invoke` 得到的原始字典可通过 `ChatState.model_validate(...)` 转为模型实例，便于 IDE 补全与后续逻辑。
- 如使用 Python 3.9，示例已用 `typing.Optional`/`List` 兼容；若使用 3.10+ 可改回 `str | None` 与 `list[str]`。
- `user_input` 字段增加了 `field_validator(mode="before")`，保证非字符串输入（如数字）被转换成字符串后再进入图。

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
