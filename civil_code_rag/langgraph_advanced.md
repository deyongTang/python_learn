# LangGraph 高阶使用指南

LangGraph 不仅仅是一个简单的状态机，它旨在构建复杂的、有状态的、多角色的 Agent 系统。以下是一些高阶使用模式。

## 1. 条件分支 (Conditional Branching)

在工作流中根据上一步的结果动态决定下一步的走向。

```python
from langgraph.graph import StateGraph, END

def router(state):
    # 根据评分决定下一步
    if state["grade"] == "relevant":
        return "generate"
    else:
        return "rewrite_query"

workflow = StateGraph(GraphState)
# ... 添加节点 ...

# 添加条件边
workflow.add_conditional_edges(
    "grade_documents",  # 起始节点
    router,             # 路由函数
    {                   # 映射关系
        "generate": "generate",
        "rewrite_query": "rewrite_query"
    }
)
```

## 2. 循环与反思 (Cycles & Reflection)

Agent 的核心能力之一是自我纠错。通过在图中创建“环”，可以让 Agent 反复尝试直到满足条件。

**场景**：代码生成 -> 运行测试 -> 失败则修改代码 -> 再次运行测试。

```python
# 简单的循环结构
workflow.add_edge("run_tests", "check_results")

def check_results_router(state):
    if state["test_passed"]:
        return END
    elif state["attempts"] > 3:
        return END  # 避免死循环
    else:
        return "fix_code" # 回到修复节点

workflow.add_conditional_edges("check_results", check_results_router)
workflow.add_edge("fix_code", "run_tests") # 闭环
```

## 3. 人在回路 (Human-in-the-loop)

在关键步骤暂停执行，等待人工审批或修改状态，然后再继续。

```python
# 编译时开启中断
app = workflow.compile(interrupt_before=["deploy_node"])

# 运行到 deploy_node 前会暂停
thread = {"configurable": {"thread_id": "1"}}
app.invoke(inputs, config=thread)

# 人工检查 state，甚至可以修改 state
current_state = app.get_state(thread)
# ... 人工确认 ...

# 继续执行
app.invoke(None, config=thread)
```

## 4. 子图 (Subgraphs)

将复杂的流程拆分为多个子图，每个子图可以独立开发和测试，然后在主图中像调用普通节点一样调用子图。

```python
# 定义子图
sub_workflow = StateGraph(SubState)
# ... 构建子图 ...
sub_app = sub_workflow.compile()

# 在主图中使用
main_workflow.add_node("research_team", sub_app)
```

## 5. 多 Agent 协作 (Multi-Agent Collaboration)

构建多个拥有不同 Prompt 和工具的 Agent 节点，让它们互相传递消息。

*   **Supervisor 模式**：一个监管者 Agent 决定下一个由哪个专家 Agent 工作。
*   **Hierarchical Teams**：层级化的 Agent 团队。

---

### 总结
LangGraph 的强大之处在于其**对状态的精细控制**和**图结构的灵活性**。通过组合上述模式，可以构建出非常强大的企业级 Agent 应用。
