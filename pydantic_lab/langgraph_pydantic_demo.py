"""Minimal LangGraph + Pydantic demo.

Run `python -m pydantic_lab.langgraph_pydantic_demo` to see how the state flows
through the graph with automatic type validation.
"""

import operator
from typing import Annotated, List, Optional

from langgraph.graph import END, StateGraph
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class ChatState(BaseModel):
    """Graph state validated by Pydantic."""

    model_config = ConfigDict(extra="forbid")

    # Annotated with operator.add so LangGraph merges lists across nodes.
    steps: Annotated[List[str], operator.add] = Field(default_factory=list)
    user_input: str
    intent: Optional[str] = None
    response: Optional[str] = None

    @field_validator("user_input", mode="before")
    @classmethod
    def coerce_to_str(cls, v):
        """Allow non-string input (e.g., numbers) and coerce to str for the graph."""
        return v if isinstance(v, str) else str(v)


def classify_intent(state: ChatState) -> dict:
    """Route to a lightweight intent label."""
    text = state.user_input.lower()
    is_order = any(keyword in text for keyword in ("buy", "购买", "下单"))
    intent = "order" if is_order else "chitchat"
    return {"intent": intent, "steps": ["classify_intent"]}


def craft_response(state: ChatState) -> dict:
    """Draft a reply based on the intent detected earlier."""
    if state.intent == "order":
        reply = f"订单助手：好的，关于“{state.user_input}”，请告诉我想买的型号或预算。"
    else:
        reply = f"闲聊助手：你说了“{state.user_input}”，我可以继续陪你聊。"
    return {"response": reply, "steps": ["craft_response"]}


def build_graph() -> StateGraph:
    """Assemble a directed graph with validation at each node boundary."""
    graph = StateGraph(ChatState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("craft_response", craft_response)

    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "craft_response")
    graph.add_edge("craft_response", END)

    return graph


def run_demo() -> None:
    app = build_graph().compile()
    examples = [
        "我想购买一把吉他，预算 2000 内",
        "今天天气不错，聊聊音乐吧",
        123,  # 展示 Pydantic 的类型转换，数字变成字符串
    ]

    for text in examples:
        print(f"\n=== 输入: {text!r}")
        try:
            raw_state = app.invoke({"user_input": text})
        except ValidationError as exc:
            print("验证失败：", exc)
            continue

        # app.invoke 返回符合状态模式的字典，转为 BaseModel 便于 IDE 补全与后续使用。
        state = ChatState.model_validate(raw_state)
        print("步骤执行顺序:", state.steps)
        print("意图标签:", state.intent)
        print("模型回复:", state.response)


if __name__ == "__main__":
    run_demo()
