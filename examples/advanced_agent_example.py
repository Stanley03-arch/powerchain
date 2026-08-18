"""
Advanced agents: PlanningAgent and ReflectiveAgent.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, tool
from powerchain.core.agents import PlanningAgent, ReflectiveAgent


@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


def demo_planning():
    print("=== PlanningAgent ===\n")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    agent = PlanningAgent(llm=llm, tools=[calculate])

    result = agent.run(
        "I have 3 boxes. Each box contains 4 smaller boxes. "
        "Each smaller box contains 5 chocolates. How many chocolates do I have in total?"
    )
    print(f"\nFinal answer:\n{result}")


def demo_reflective():
    print("\n\n=== ReflectiveAgent ===\n")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    agent = ReflectiveAgent(llm=llm)

    result = agent.run(
        "Explain the main advantages of PowerChain over traditional LangChain in 3 clear points."
    )
    print(f"\nImproved answer:\n{result}")


if __name__ == "__main__":
    demo_planning()
    demo_reflective()
