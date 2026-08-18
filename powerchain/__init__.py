"""
PowerChain — A cleaner, more powerful alternative to LangChain.
"""

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.models.openai import ChatOpenAI
from powerchain.core.tools.base import tool, Tool, BaseTool
from powerchain.core.agents.agent import Agent
from powerchain.core.memory.conversation import ConversationMemory
from powerchain.core.prompts.template import PromptTemplate
from powerchain.core.runnables.base import Runnable, Sequential, Parallel

__version__ = "0.1.0"

__all__ = [
    "BaseChatModel",
    "ChatMessage",
    "Role",
    "ChatOpenAI",
    "tool",
    "Tool",
    "BaseTool",
    "Agent",
    "ConversationMemory",
    "PromptTemplate",
    "Runnable",
    "Sequential",
    "Parallel",
]
