"""
ReliableAgent example — stronger planning, recovery, and self-correction.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, tool
from powerchain.core.agents import ReliableAgent


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


@tool
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    agent = ReliableAgent(
        llm=llm,
        tools=[calculate, reverse_text],
        max_steps=6,
        max_replans=2,
        reflect=True,
        verbose=True,
    )

    task = (
        "I have the numbers 15, 7 and 3. "
        "First multiply 15 by 7, then add 3 to the result. "
        "Finally reverse the digits of the final number and tell me what you get."
    )

    answer = agent.run(task)
    print("\nFINAL ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()
