"""
Example using different LLM providers with PowerChain.

Set the appropriate API keys / run Ollama locally as needed.
"""

from powerchain import ChatMessage, Role
from powerchain.core.models import ChatOpenAI, ChatAnthropic, ChatGroq, ChatOllama


def try_model(name: str, model):
    print(f"\n=== {name} ===")
    try:
        messages = [ChatMessage(role=Role.USER, content="Say hello in one short sentence.")]
        response = model.invoke(messages)
        print(response.content)
    except Exception as e:
        print(f"Skipped / Error: {e}")


def main():
    # OpenAI (or compatible)
    try_model("OpenAI", ChatOpenAI(model="gpt-4o-mini"))

    # Groq (very fast)
    try_model("Groq", ChatGroq(model="llama-3.3-70b-versatile"))

    # Anthropic
    try_model("Anthropic", ChatAnthropic(model="claude-3-5-haiku-20241022"))

    # Ollama (local)
    try_model("Ollama", ChatOllama(model="llama3.2"))


if __name__ == "__main__":
    main()
