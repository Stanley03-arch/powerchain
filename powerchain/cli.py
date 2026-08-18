"""
Simple PowerChain CLI.

Usage:
  python -m powerchain.cli chat
  python -m powerchain.cli version
"""

from __future__ import annotations

import argparse
import os
import sys


def cmd_version(_: argparse.Namespace) -> None:
    from powerchain import __version__
    print(f"PowerChain v{__version__}")


def cmd_chat(args: argparse.Namespace) -> None:
    from powerchain import ChatOpenAI, Agent, ConversationMemory, tool

    @tool
    def get_time() -> str:
        """Return the current time."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    model = args.model or "gpt-4o-mini"
    llm = ChatOpenAI(model=model, temperature=0.4)
    agent = Agent(llm=llm, tools=[get_time], memory=ConversationMemory())

    print(f"PowerChain Chat (model={model})")
    print("Type 'quit' or 'exit' to leave.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Bye!")
            break

        try:
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="powerchain", description="PowerChain CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("version", help="Show version")

    chat_parser = sub.add_parser("chat", help="Interactive chat with an agent")
    chat_parser.add_argument("--model", default=None, help="Model name (default: gpt-4o-mini)")

    args = parser.parse_args(argv)

    if args.command == "version":
        cmd_version(args)
    elif args.command == "chat":
        if not os.getenv("OPENAI_API_KEY"):
            print("Warning: OPENAI_API_KEY not set. Chat may fail.")
        cmd_chat(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
