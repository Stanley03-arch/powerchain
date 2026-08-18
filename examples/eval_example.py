"""
Simple evaluation example using QAEvaluator.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, RAGChain, Document, OpenAIEmbeddings, InMemoryVectorStore
from powerchain.eval import QAEvaluator


def main():
    # Tiny knowledge base
    docs = [
        Document(page_content="PowerChain is a modern Python framework for building LLM applications."),
        Document(page_content="It supports agents, tools, RAG, multi-agent crews, and graph orchestration."),
        Document(page_content="Nairobi is the capital of Kenya."),
    ]

    embeddings = OpenAIEmbeddings()
    store = InMemoryVectorStore(embedding=embeddings)
    store.add_documents(docs)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    rag = RAGChain(llm=llm, retriever=store.as_retriever())

    # Test cases
    questions = [
        "What is PowerChain?",
        "What features does PowerChain have?",
        "What is the capital of Kenya?",
    ]
    references = [
        "PowerChain is a modern Python framework for building LLM applications.",
        "Agents, tools, RAG, multi-agent crews, and graph orchestration.",
        "Nairobi",
    ]

    predictions = [rag.invoke(q) for q in questions]

    evaluator = QAEvaluator(llm=llm, pass_threshold=0.7)
    results = evaluator.evaluate_batch(questions, predictions, references)

    print("Evaluation Results:\n")
    for r in results:
        print(f"Q: {r.input}")
        print(f"Pred: {r.prediction[:100]}...")
        print(f"Score: {r.score:.2f} | {'PASS' if r.passed else 'FAIL'}\n")

    summary = evaluator.summary(results)
    print("Summary:", summary)


if __name__ == "__main__":
    main()
