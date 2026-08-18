"""
Basic PowerChain agent example.

Make sure you have OPENAI_API_KEY set (or another compatible provider).
"""

from powerchain import ChatOpenAI, tool, Agent, ConversationMemory


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # Fake implementation for demo
    return f"The weather in {city} is sunny and 24°C."


@tool
def calculate(expression: str) -> str:
    """Evaluate a simple math expression."""
    try:
        # Very basic and safe eval for demo only
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    agent = Agent(
        llm=llm,
        tools=[get_weather, calculate],
        memory=ConversationMemory(),
        system_prompt=(
            "You are a helpful assistant. "
            "Use the available tools when they can help you give accurate answers."
        ),
    )

    print("PowerChain Agent ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            break

        response = agent.run(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
