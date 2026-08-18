"""
Upgraded multi-agent example with shared memory and different execution modes.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI
from powerchain.multiagent import AgentNode, Crew, SharedMemory


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    researcher = AgentNode(
        name="Researcher",
        llm=llm,
        role="Senior Research Analyst",
        goal="Find accurate facts and key insights",
    )

    writer = AgentNode(
        name="Writer",
        llm=llm,
        role="Technical Writer",
        goal="Turn information into clear, structured text",
    )

    critic = AgentNode(
        name="Critic",
        llm=llm,
        role="Quality Critic",
        goal="Improve accuracy, clarity and usefulness",
    )

    memory = SharedMemory()
    crew = Crew(agents=[researcher, writer, critic], shared_memory=memory, verbose=True)

    task = "Explain what makes PowerChain different from LangChain in simple terms."

    print("\n" + "=" * 60)
    print("MODE: Coordinated (with shared memory)")
    print("=" * 60)
    result = crew.run_coordinated(task)

    print("\n" + "=" * 60)
    print("FINAL RESULT:")
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()
