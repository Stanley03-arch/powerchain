"""
PowerChain — A cleaner, more powerful alternative to LangChain.
"""

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.models.openai import ChatOpenAI
from powerchain.core.models.retry import RetryChatModel
from powerchain.core.models.fallback import FallbackChatModel
from powerchain.core.models.anthropic import ChatAnthropic
from powerchain.core.models.groq import ChatGroq
from powerchain.core.models.ollama import ChatOllama
from powerchain.core.tools.base import tool, Tool, BaseTool
from powerchain.core.agents.agent import Agent
from powerchain.core.agents.planner import Planner
from powerchain.core.agents.reflector import Reflector
from powerchain.core.agents.advanced import PlanningAgent, ReflectiveAgent
from powerchain.core.agents.reliable import ReliableAgent
from powerchain.core.memory.conversation import ConversationMemory
from powerchain.core.memory.summary import SummaryMemory
from powerchain.core.memory.vector import VectorMemory
from powerchain.core.prompts.template import PromptTemplate
from powerchain.core.runnables.base import Runnable, Sequential, Parallel
from powerchain.core.output_parsers import (
    BaseOutputParser,
    JsonOutputParser,
    PydanticOutputParser,
    ListOutputParser,
)

# RAG
from powerchain.rag.documents import Document
from powerchain.rag.loaders.text import TextLoader
from powerchain.rag.loaders.web import WebLoader
from powerchain.rag.loaders.directory import DirectoryLoader
from powerchain.rag.splitters.recursive import RecursiveCharacterTextSplitter
from powerchain.rag.embeddings.openai import OpenAIEmbeddings
from powerchain.rag.vectorstores.memory import InMemoryVectorStore
from powerchain.rag.vectorstores.faiss_store import FAISSVectorStore
from powerchain.rag.vectorstores.chroma_store import ChromaVectorStore
from powerchain.rag.retrievers.vector import VectorStoreRetriever
from powerchain.rag.chain import RAGChain

# Multi-agent
from powerchain.multiagent.agent_node import AgentNode
from powerchain.multiagent.crew import Crew
from powerchain.multiagent.graph import Graph, Node, Edge
from powerchain.multiagent.shared_memory import SharedMemory

# Eval
from powerchain.eval.evaluator import Evaluator, EvalResult
from powerchain.eval.qa_eval import QAEvaluator

__version__ = "0.14.0"

__all__ = [
    # Core / Models
    "BaseChatModel",
    "ChatMessage",
    "Role",
    "ChatOpenAI",
    "ChatAnthropic",
    "ChatGroq",
    "ChatOllama",
    "RetryChatModel",
    "FallbackChatModel",
    "tool",
    "Tool",
    "BaseTool",
    "Agent",
    "Planner",
    "Reflector",
    "PlanningAgent",
    "ReflectiveAgent",
    "ReliableAgent",
    "ConversationMemory",
    "SummaryMemory",
    "VectorMemory",
    "PromptTemplate",
    "Runnable",
    "Sequential",
    "Parallel",
    # Output parsers
    "BaseOutputParser",
    "JsonOutputParser",
    "PydanticOutputParser",
    "ListOutputParser",
    # RAG
    "Document",
    "TextLoader",
    "WebLoader",
    "DirectoryLoader",
    "RecursiveCharacterTextSplitter",
    "OpenAIEmbeddings",
    "InMemoryVectorStore",
    "FAISSVectorStore",
    "ChromaVectorStore",
    "VectorStoreRetriever",
    "RAGChain",
    # Multi-agent
    "AgentNode",
    "Crew",
    "Graph",
    "Node",
    "Edge",
    "SharedMemory",
    # Eval
    "Evaluator",
    "EvalResult",
    "QAEvaluator",
]
