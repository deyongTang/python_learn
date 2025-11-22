# LangGraph 学习指南

面向：已经了解 Pydantic，并想快速上手 LangGraph 构建有状态的流程/代理。

## 安装与准备
- 依赖已写入 `requirements.txt`：`langgraph>=0.2.30`。
- 建议使用 Python 3.9+；如在 3.9，联合类型用 `Optional[...]`/`List[...]`。
- 本仓库已有最小示例：`python -m pydantic_lab.langgraph_pydantic_demo`。

## 核心概念速览
- **StateGraph**：声明式有向图，节点是可调用，边决定执行顺序。
- **状态模型**：推荐用 `BaseModel` 定义全局状态结构，`extra="forbid"` 防止漏字段。
- **合并策略**：用 `Annotated[<type>, operator.add|or|...]` 控制节点返回的“增量”如何与当前状态合并。
- **入口/出口**：`set_entry_point("node")` 定义开始；`langgraph.graph.END` 表示结束。
- **编译与调用**：`graph.compile()` 得到可调用的 `app`，可 `invoke()`、`astream_events()` 等。

## 最小模板
```python
import operator
from typing import Annotated, List, Optional
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, ConfigDict, Field


class FlowState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    steps: Annotated[List[str], operator.add] = Field(default_factory=list)
    user_input: str
    intent: Optional[str] = None
    reply: Optional[str] = None


def classify(state: FlowState) -> dict:
    intent = "order" if "买" in state.user_input else "chat"
    return {"intent": intent, "steps": ["classify"]}


def respond(state: FlowState) -> dict:
    text = "下单请提供商品与预算" if state.intent == "order" else "好的，我们聊聊！"
    return {"reply": text, "steps": ["respond"]}


def build_app():
    graph = StateGraph(FlowState)
    graph.add_node("classify", classify)
    graph.add_node("respond", respond)
    graph.set_entry_point("classify")
    graph.add_edge("classify", "respond")
    graph.add_edge("respond", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_app()
    result = app.invoke({"user_input": "我想买键盘"})
    print(result)
```

## RAG 示范（纯本地）
- 路径：`python -m pydantic_lab.langgraph_rag_demo`
- 特点：使用内置小语料 + 关键词计数模拟检索，完全离线；Pydantic 负责状态与文档验证；节点返回增量字典。
- 状态字段：`user_query`、`top_k`、`retrieved`、`answer`、`steps`（`Annotated[..., operator.add]` 用于累积）。

## 学习路径
1) 跑通最小示例，理解“节点返回增量 + 状态合并”。
2) 使用 `Field` 约束、`field_validator` 做输入清洗。
3) 引入分支：根据状态字段动态路由到不同节点。
4) 尝试流式调用：`astream_events()` 观察每步状态。
5) 加入外部 I/O（文件/HTTP/DB）和错误处理，验证健壮性。

## 练习项目（可逐步完成）
### 1) 意图路由 + 追踪
- 基于 `pydantic_lab/langgraph_pydantic_demo.py`。
- 需求：支持意图 `order`/`support`/`chitchat`，新增一个 `logger` 节点写入 `steps` 或打印当前状态摘要。
- 要点：使用 `Annotated[List[str], operator.add]` 追踪节点执行；对 `user_input` 做前置清洗。

### 2) CSV 数据清洗流水线
- 状态字段：`path`（输入文件）、`rows_valid`、`rows_invalid`、`stats`。
- 节点：
  - `load_file`：读取 CSV。
  - `validate_rows`：用 `BaseModel` 定义行模式，分类 valid/invalid。
  - `enrich`：对合法行做简单转换（如标准化大小写、计算派生列）。
  - `report`：输出统计信息并写回文件（或打印摘要）。
- 练习点：节点返回局部更新，合并列表与统计字典；对文件错误做异常捕获并填充错误信息到状态。

### 3) 表单收集对话（多轮填槽）
- 状态字段：`slots`（需要收集的键）、`filled`（已收集）、`pending`、`messages`。
- 节点：
  - `analyze_message`：根据用户输入填充槽位。
  - `next_question`：根据 `pending` 生成下一句话。
  - 结束条件：`pending` 为空或达到轮次上限。
- 练习点：用 `operator.or_` 合并字典、`operator.add` 合并消息列表；编写跨字段校验确保槽位完整。

### 4) 异常与重试（选做）
- 为某个节点故意加入可能失败的 I/O（如随机抛异常），在状态中记录错误并走重试分支。
- 练习点：在节点里捕获异常，返回 `{"error": "...", "steps": [...]}`，图中用条件边根据 `error` 决定下一步。

## 调试与测试建议
- 采用小输入快速迭代：`app.invoke` 并打印状态。
- 对关键节点写单元测试：给定状态 -> 期望增量。
- 使用 `extra="forbid"` 尽早发现漏字段；对外部输入加 `field_validator` 清洗。
- 需要了解状态合并策略时，可在节点里打印 `state` 和返回的增量，观察合并后的结果。

## 参考
- 官方文档与示例：https://github.com/langchain-ai/langgraph
- 本仓库示例：`pydantic_lab/langgraph_pydantic_demo.py`（含 Pydantic 校验与合并策略）。
