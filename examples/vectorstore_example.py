"""
Example using different vector stores with PowerChain.

InMemory works out of the box.
FAISS requires: pip install faiss-cpu
Chroma requires: pip install chromadb
"""

from powerchain import (
    Document,
    OpenAIEmbeddings,
    InMemoryVectorStore,
    FAISSVectorStore,
    ChromaVectorStore,
    RAGChain,
    ChatOpenAI,
)


def demo_store(name: str, store):
    print(f"\n=== {name} ===")
    docs = [
        Document(page_content="PowerChain is a modern LLM framework."),
        Document(page_content="It supports agents, RAG, and multi-agent systems."),
        Document(page_content="Nairobi is the capital city of Kenya."),
    ]
    store.add_documents(docs)

    results = store.similarity_search("What is PowerChain?", k=2)
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")


def main():
    embeddings = OpenAIEmbeddings()

    # 1. In-memory (always available)
    demo_store("InMemoryVectorStore", InMemoryVectorStore(embedding=embeddings))

    # 2. FAISS
    try:
        demo_store("FAISSVectorStore", FAISSVectorStore(embedding=embeddings))
    except ImportError as e:
        print(f"\nFAISS skipped: {e}")

    # 3. Chroma
    try:
        demo_store("ChromaVectorStore", ChromaVectorStore(embedding=embeddings))
    except ImportError as e:
        print(f"\nChroma skipped: {e}")


if __name__ == "__main__":
    main()
