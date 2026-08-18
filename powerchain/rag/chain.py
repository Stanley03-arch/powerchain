from __future__ import annotations

from typing import List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.prompts.template import PromptTemplate
from powerchain.rag.documents import Document
from powerchain.rag.retrievers.base import BaseRetriever


DEFAULT_RAG_PROMPT = PromptTemplate(
    """Use the following pieces of context to answer the question.
If you don't know the answer based on the context, say so clearly.

Context:
{context}

Question: {question}

Answer:"""
)


class RAGChain:
    """Simple and effective Retrieval-Augmented Generation chain."""

    def __init__(
        self,
        llm: BaseChatModel,
        retriever: BaseRetriever,
        prompt: Optional[PromptTemplate] = None,
    ):
        self.llm = llm
        self.retriever = retriever
        self.prompt = prompt or DEFAULT_RAG_PROMPT

    def _format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def invoke(self, question: str) -> str:
        docs = self.retriever.get_relevant_documents(question)
        context = self._format_docs(docs)

        prompt_text = self.prompt.format(context=context, question=question)

        messages = [
            ChatMessage(role=Role.USER, content=prompt_text),
        ]
        response = self.llm.invoke(messages)
        return response.content

    async def ainvoke(self, question: str) -> str:
        docs = await self.retriever.aget_relevant_documents(question)
        context = self._format_docs(docs)

        prompt_text = self.prompt.format(context=context, question=question)

        messages = [
            ChatMessage(role=Role.USER, content=prompt_text),
        ]
        response = await self.llm.ainvoke(messages)
        return response.content
