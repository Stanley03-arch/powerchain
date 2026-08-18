"""
Reliability features: Retry + Fallback + Streaming.

Requires OPENAI_API_KEY.
"""

from powerchain import ChatOpenAI, ChatMessage, Role
from powerchain.core.models import RetryChatModel, FallbackChatModel


def demo_retry():
    print("=== RetryChatModel ===")
    base = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    reliable = RetryChatModel(base, max_attempts=3)

    msg = [ChatMessage(role=Role.USER, content="Say hello in one short sentence.")]
    response = reliable.invoke(msg)
    print(response.content)


def demo_fallback():
    print("\n=== FallbackChatModel ===")
    # Primary + backup (both same here for demo; in real life use different providers)
    primary = ChatOpenAI(model="gpt-4o-mini")
    backup = ChatOpenAI(model="gpt-4o-mini")

    fallback = FallbackChatModel([primary, backup])
    msg = [ChatMessage(role=Role.USER, content="What is 2 + 2?")]
    print(fallback.invoke(msg).content)


def demo_streaming():
    print("\n=== Streaming ===")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    messages = [ChatMessage(role=Role.USER, content="Write a very short poem about coding.")]

    print("Streamed output:")
    for chunk in llm.stream(messages):
        print(chunk, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    demo_retry()
    demo_fallback()
    demo_streaming()
