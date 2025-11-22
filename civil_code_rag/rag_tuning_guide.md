# 企业级 RAG 系统调优指南

在企业环境中，RAG 系统的效果往往取决于细节的打磨。以下是常见的调优方向。

## 1. 数据质量 (Data Quality) - "Garbage In, Garbage Out"

*   **清洗**：去除页眉、页脚、乱码、无意义的符号。
*   **结构化**：尽可能解析表格、标题层级，保留文档的结构信息。
*   **元数据**：为文档添加元数据（如发布时间、部门、文档类型），以便在检索时进行过滤（Pre-filtering）。

## 2. 切分策略 (Chunking Strategy)

*   **语义切分**：不要只按字符数切分。尽量按段落、句子或语义完整性切分。
*   **重叠 (Overlap)**：保持一定的重叠（如 10%-20%），防止上下文在切分处丢失。
*   **父子索引 (Parent-Child Indexing)**：
    *   检索时使用“小块”（Small Chunk）以提高匹配精准度。
    *   生成时使用该小块所属的“大块”（Parent Chunk）以提供更完整的上下文。

## 3. 检索优化 (Retrieval Optimization)

*   **混合检索 (Hybrid Search)**：
    *   **关键词检索 (BM25)**：擅长匹配精确名词（如人名、产品型号）。
    *   **向量检索 (Dense Vector)**：擅长匹配语义（如“合同违约怎么办”）。
    *   **加权融合**：将两者结果结合（Reciprocal Rank Fusion, RRF）。
*   **重排序 (Re-ranking)**：
    *   先检索出 Top-50 个文档（粗排）。
    *   使用高精度的 Cross-Encoder 模型（如 BGE-Reranker）对这 50 个文档进行精细打分。
    *   取 Top-5 给大模型。
    *   *这是提升 RAG 效果最立竿见影的方法。*

## 4. 提示词工程 (Prompt Engineering)

*   **角色设定**：明确设定 AI 的角色和限制（如“只根据上下文回答”）。
*   **少样本学习 (Few-Shot Learning)**：在 Prompt 中提供 1-2 个理想的问答范例。
*   **思维链 (Chain-of-Thought)**：引导模型先分析检索到的内容，再得出结论。

## 5. 流程优化 (Flow Optimization) - LangGraph 的用武之地

*   **查询改写 (Query Rewriting)**：用户的问题往往不完整。先用 LLM 将用户问题改写为更适合检索的形式。
*   **多路召回 (Multi-Query)**：将一个问题拆解为 3 个不同角度的子问题，分别检索，然后汇总结果。
*   **自我修正 (Self-Correction)**：
    *   检索后，让 LLM 判断检索结果是否相关（我们项目中已经实现了 `grade_documents`）。
    *   生成后，让 LLM 检查答案是否出现幻觉（Hallucination）。

## 6. 评估体系 (Evaluation)

*   **RAGAS / TruLens**：使用自动化框架评估 RAG 的各项指标：
    *   **Context Precision**：检索到的上下文是否包含答案？
    *   **Context Recall**：是否漏掉了关键信息？
    *   **Faithfulness**：回答是否忠实于上下文（无幻觉）？
    *   **Answer Relevance**：回答是否解决了用户问题？

---

### 调优路线图建议
1.  **基线**：先跑通流程（当前状态）。
2.  **数据**：优化 PDF/Word 解析效果。
3.  **检索**：加入 Re-ranker（重排序模型）。
4.  **流程**：加入 Query Rewrite（查询改写）。
