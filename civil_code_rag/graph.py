import os
from typing import Dict, List, TypedDict

from langchain_chroma import Chroma
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph

from config import DB_PATH, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, MAX_RETRIES

# --- Configuration ---
EMBEDDING_MODEL = DashScopeEmbeddings(model=EMBEDDING_MODEL_NAME)
LLM_MODEL = LLM_MODEL_NAME # or qwen-plus, qwen-max

# --- State ---
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
        retry_count: number of retries for query rewriting
    """
    question: str
    generation: str
    documents: List[str]
    retry_count: int

# --- Nodes ---

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    retry_count = state.get("retry_count", 0)

    # Initialize Vector Store
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=EMBEDDING_MODEL)
    retriever = vectorstore.as_retriever()
    
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question, "retry_count": retry_count}

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """
    print("---CHECK DOCUMENT RELEVANCE---")
    question = state["question"]
    documents = state["documents"]

    # Data model for grading
    class GradeDocuments(BaseModel):
        """Binary score for relevance check on retrieved documents."""
        binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

    # LLM with structured output
    llm = ChatTongyi(model=LLM_MODEL, temperature=0)
    structured_llm_grader = llm.with_structured_output(GradeDocuments)

    # Prompt
    system = """你是一名评分员，负责评估检索到的文档与用户问题的相关性。\n
    如果文档包含与用户问题相关的关键词或语义含义，请将其评为相关。\n
    这不需要非常严格的测试。目标是过滤掉错误的检索结果。\n
    请给出二元评分 'yes' 或 'no' 来表明文档是否与问题相关。"""
    grade_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "检索到的文档: \n\n {document} \n\n 用户问题: {question}"),
        ]
    )

    grader = grade_prompt | structured_llm_grader
    
    filtered_docs = []
    for d in documents:
        score = grader.invoke({"question": question, "document": d.page_content})
        
        if not score:
            print("---GRADE: LLM RETURNED NONE (SKIPPING)---")
            continue
            
        grade = score.binary_score
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
            
    return {"documents": filtered_docs, "question": question}

def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    # LLM
    llm = ChatTongyi(model=LLM_MODEL, temperature=0)

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """你是一个基于《中华人民共和国民法典》回答问题的助手。
        请使用以下检索到的上下文来回答问题。
        如果你不知道答案，就直接说不知道，不要试图编造答案。
        回答要尽量简洁，控制在三句话以内。
        
        问题: {question} 
        上下文: {context} 
        回答:"""
    )

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}

def rewrite_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """
    print("---REWRITE QUERY---")
    question = state["question"]
    retry_count = state.get("retry_count", 0)

    llm = ChatTongyi(model=LLM_MODEL, temperature=0)

    # Prompt
    msg = [
        ("system", """你是一个问题改写助手。你的任务是将输入的问题改写为更适合向量检索的形式。
        请分析问题的核心意图，并尝试用更专业或更准确的法律术语进行表达。
        只输出改写后的问题，不要包含任何解释。"""),
        ("human", f"初始问题: {question}"),
    ]
    
    better_question = llm.invoke(msg).content
    print(f"---QUERY REWRITTEN: {better_question}---")
    
    return {"question": better_question, "retry_count": retry_count + 1}

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    print("---ASSESS GRADED DOCUMENTS---")
    filtered_documents = state["documents"]
    retry_count = state.get("retry_count", 0)

    if not filtered_documents:
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        if retry_count < MAX_RETRIES:
            print(f"---DECISION: ALL DOCUMENTS ARE NOT RELEVANT, REWRITING QUERY (Attempt {retry_count + 1}/{MAX_RETRIES})---")
            return "rewrite_query"
        else:
            print("---DECISION: MAX RETRIES REACHED, STOPPING---")
            # In a real app, you might want to return a fallback answer here
            # For now, we proceed to generate (which will likely say "I don't know")
            return "generate"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"

# --- Graph Build ---
def build_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("rewrite_query", rewrite_query)

    # Build graph
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    
    # Conditional edge
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "rewrite_query": "rewrite_query",
            "generate": "generate",
        },
    )
    
    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("generate", END)

    # Compile
    app = workflow.compile()
    return app
