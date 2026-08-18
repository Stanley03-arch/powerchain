"""
Demonstrates SummaryMemory and VectorMemory.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, Agent, OpenAIEmbeddings
from powerchain.core.memory import SummaryMemory, VectorMemory


def demo_summary_memory():
    print("=== SummaryMemory Demo ===\n")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    memory = SummaryMemory(llm=llm, max_messages=6, summarize_threshold=4)

    agent = Agent(llm=llm, memory=memory, system_prompt="You are a helpful assistant.")

    conversations = [
        "My name is Stanley and I live in Nairobi.",
        "I am building a framework called PowerChain.",
        "It is meant to be better than LangChain.",
        "What is my name and what am I building?",
    ]

    for msg in conversations:
        print(f"User: {msg}")
        reply = agent.run(msg)
        print(f"Agent: {reply}\n")


def demo_vector_memory():
    print("\n=== VectorMemory Demo ===\n")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    embeddings = OpenAIEmbeddings()

    memory = VectorMemory(embedding=embeddings, max_recent=4, k_long_term=3)

    # Manually add some history
    memory.add_user("I love hiking in the mountains.")
    memory.add_assistant("That sounds great! Mountains are beautiful.")
    memory.add_user("My favorite place is Mount Kenya.")
    memory.add_assistant("Mount Kenya is an amazing destination.")

    # Now query with something that should retrieve past context
    messages = memory.get_messages(query="What outdoor activity do I enjoy?")
    print("Retrieved context messages:")
    for m in messages:
        print(f"  [{m.role.value}] {m.content[:100]}...")


if __name__ == "__main__":
    demo_summary_memory()
    demo_vector_memory()
