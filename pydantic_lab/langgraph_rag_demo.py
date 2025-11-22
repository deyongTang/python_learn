"""LangGraph + Pydantic: minimal offline RAG flow.

特点：
- 全离线：用内置小语料和关键词打分做“检索”，无需外部模型或网络。
- 强类型状态：用 Pydantic 定义状态与文档结构，extra="forbid" 防漏字段。
- 节点返回增量：依靠 Annotated + operator.add 累积 steps、retrieved。

运行：
    python -m pydantic_lab.langgraph_rag_demo
"""

import operator
from typing import Annotated, List, Optional

from langgraph.graph import END, StateGraph
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class Doc(BaseModel):
    title: str
    content: str


class RagState(BaseModel):
    """RAG 状态：查询、检索结果、合成答案。"""

    model_config = ConfigDict(extra="forbid")

    steps: Annotated[List[str], operator.add] = Field(default_factory=list)
    user_query: str
    top_k: int = Field(default=2, ge=1, le=5)
    retrieved: Annotated[List[Doc], operator.add] = Field(default_factory=list)
    answer: Optional[str] = None

    @field_validator("user_query", mode="before")
    @classmethod
    def coerce_query(cls, v):
        return v if isinstance(v, str) else str(v)


CORPUS = [
    Doc(
        title="LangGraph 简介",
        content="LangGraph 是一个构建有状态图式代理的库，支持节点、边与状态合并策略。",
    ),
    Doc(
        title="Pydantic 核心",
        content="Pydantic 使用类型注解进行数据验证与转换，BaseModel 负责结构化校验。",
    ),
    Doc(
        title="RAG 定义",
        content="RAG 通过检索相关文档，再结合生成模型返回答案，常见步骤包含查询、检索、重排与合成。",
    ),
    Doc(
        title="向量检索与关键词",
        content="真实系统常用向量检索，示例中用简单关键词计数来模拟相似度。",
    ),
]


def retrieve(state: RagState) -> dict:
    """基于关键词计数的简易检索，返回 top_k 文档。"""
    query_tokens: List[str] = []
    for token in state.user_query.lower().split():
        clean = token.strip()
        if clean:
            query_tokens.append(clean)

    if not query_tokens:
        # 如果查询为空，返回空检索
        return {"retrieved": [], "steps": ["retrieve"]}

    def score(doc: Doc) -> int:
        text = (doc.title + " " + doc.content).lower()
        total = 0
        for tok in query_tokens:
            total += text.count(tok)
        return total

    # 计算每个文档的得分
    scored_docs: List[tuple[Doc, int]] = []
    for doc in CORPUS:
        scored_docs.append((doc, score(doc)))

    # 按得分降序排序
    scored_sorted = sorted(scored_docs, key=lambda item: item[1], reverse=True)

    # 取前 top_k 个文档
    top_docs: List[Doc] = []
    for doc, _score in scored_sorted[: state.top_k]:
        top_docs.append(doc)

    return {"retrieved": top_docs, "steps": ["retrieve"]}


def synthesize(state: RagState) -> dict:
    """合成回答：拼接检索到的文档摘要并给出引用。"""
    if not state.retrieved:
        return {"answer": "没有找到相关信息，请提供更具体的描述。", "steps": ["synthesize"]}

    snippets: List[str] = []
    for doc in state.retrieved:
        snippets.append(f"- {doc.title}: {doc.content}")

    answer = "根据检索结果，我找到以下信息：\n" + "\n".join(snippets)
    return {"answer": answer, "steps": ["synthesize"]}


def build_graph():
    graph = StateGraph(RagState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("synthesize", synthesize)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()


def run_demo() -> None:
    app = build_graph()
    examples = [
        {"user_query": "什么是 RAG LangGraph"},
        {"user_query": "Pydantic 用途"},
        {"user_query": 123},  # 展示数字查询被转换为字符串
    ]

    for payload in examples:
        print(f"\n=== 查询: {payload!r}")
        try:
            raw_state = app.invoke(payload)
            state = RagState.model_validate(raw_state)
        except ValidationError as exc:
            print("验证失败：", exc)
            continue

        print("步骤:", state.steps)
        print("检索到的文档标题:", [doc.title for doc in state.retrieved])
        print("答案:\n", state.answer)


if __name__ == "__main__":
    run_demo()
