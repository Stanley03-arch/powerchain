"""
Simple RAG example with PowerChain.

Requires OPENAI_API_KEY.
"""

from powerchain import (
    ChatOpenAI,
    Document,
    RecursiveCharacterTextSplitter,
    OpenAIEmbeddings,
    InMemoryVectorStore,
    RAGChain,
)


def main():
    # 1. Sample documents (in real use you would load from files)
    raw_docs = [
        Document(
            page_content=(
                "PowerChain is a modern Python framework for building LLM applications. "
                "It focuses on clean architecture, strong typing, and powerful agents. "
                "It was created as a cleaner alternative to LangChain."
            ),
            metadata={"source": "intro"},
        ),
        Document(
            page_content=(
                "The core features of PowerChain include agents with tool calling, "
                "conversation memory, prompt templates, runnable composition, "
                "and a full RAG pipeline with embeddings and vector stores."
            ),
            metadata={"source": "features"},
        ),
        Document(
            page_content=(
                "Nairobi is the capital city of Kenya. It is known for its national park "
                "and vibrant tech scene. The weather is often mild."
            ),
            metadata={"source": "geo"},
        ),
    ]

    # 2. Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splitter.split_documents(raw_docs)

    # 3. Embed + store
    embeddings = OpenAIEmbeddings()
    vectorstore = InMemoryVectorStore(embedding=embeddings)
    vectorstore.add_documents(docs)

    # 4. Create RAG chain
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    rag = RAGChain(llm=llm, retriever=retriever)

    # 5. Ask questions
    questions = [
        "What is PowerChain?",
        "What features does it have?",
        "What is the capital of Kenya?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        answer = rag.invoke(q)
        print(f"A: {answer}")


if __name__ == "__main__":
    main()
