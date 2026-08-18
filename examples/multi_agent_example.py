"""
Multi-agent example with PowerChain Crew.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, tool
from powerchain.multiagent import AgentNode, Crew


@tool
def search_web(query: str) -> str:
    """Simulate a web search (demo only)."""
    return f"Search results for '{query}': PowerChain is a modern LLM framework focused on clean design and powerful agents."


@tool
def write_summary(text: str) -> str:
    """Create a short summary of the given text."""
    return f"Summary: {text[:120]}..."


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    researcher = AgentNode(
        name="Researcher",
        llm=llm,
        role="Senior Research Analyst",
        goal="Find accurate and relevant information",
        tools=[search_web],
    )

    writer = AgentNode(
        name="Writer",
        llm=llm,
        role="Technical Writer",
        goal="Turn research into clear, well-structured text",
        tools=[write_summary],
    )

    critic = AgentNode(
        name="Critic",
        llm=llm,
        role="Quality Critic",
        goal="Improve clarity, accuracy and usefulness of the content",
    )

    crew = Crew(agents=[researcher, writer, critic], verbose=True)

    task = "Explain what PowerChain is and why someone might choose it over LangChain."

    print("Running sequential multi-agent crew...\n")
    final = crew.run_sequential(task)

    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print(final)


if __name__ == "__main__":
    main()
