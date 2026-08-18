"""
PowerChain — A cleaner, more powerful alternative to LangChain.
"""

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.models.openai import ChatOpenAI
from powerchain.core.tools.base import tool, Tool, BaseTool
from powerchain.core.agents.agent import Agent
from powerchain.core.memory.conversation import ConversationMemory
from powerchain.core.memory.summary import SummaryMemory
from powerchain.core.memory.vector import VectorMemory
from powerchain.core.prompts.template import PromptTemplate
from powerchain.core.runnables.base import Runnable, Sequential, Parallel

# RAG
from powerchain.rag.documents import Document
from powerchain.rag.loaders.text import TextLoader
from powerchain.rag.splitters.recursive import RecursiveCharacterTextSplitter
from powerchain.rag.embeddings.openai import OpenAIEmbeddings
from powerchain.rag.vectorstores.memory import InMemoryVectorStore
from powerchain.rag.retrievers.vector import VectorStoreRetriever
from powerchain.rag.chain import RAGChain

# Multi-agent
from powerchain.multiagent.agent_node import AgentNode
from powerchain.multiagent.crew import Crew
from powerchain.multiagent.graph import Graph, Node, Edge

__version__ = "0.4.0"

__all__ = [
    # Core
    "BaseChatModel",
    "ChatMessage",
    "Role",
    "ChatOpenAI",
    "tool",
    "Tool",
    "BaseTool",
    "Agent",
    "ConversationMemory",
    "SummaryMemory",
    "VectorMemory",
    "PromptTemplate",
    "Runnable",
    "Sequential",
    "Parallel",
    # RAG
    "Document",
    "TextLoader",
    "RecursiveCharacterTextSplitter",
    "OpenAIEmbeddings",
    "InMemoryVectorStore",
    "VectorStoreRetriever",
    "RAGChain",
    # Multi-agent
    "AgentNode",
    "Crew",
    "Graph",
    "Node",
    "Edge",
]
