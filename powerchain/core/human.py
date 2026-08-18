from __future__ import annotations

from typing import Any, Callable, Optional


class HumanInput:
    """Simple human-in-the-loop helper.

    By default uses input() in the terminal.
    You can pass a custom callback for web UIs, Slack, etc.
    """

    def __init__(self, callback: Optional[Callable[[str], str]] = None):
        self.callback = callback or _default_terminal_input

    def ask(self, prompt: str, default: Optional[str] = None) -> str:
        full_prompt = prompt
        if default is not None:
            full_prompt += f" [{default}]"
        full_prompt += ": "

        response = self.callback(full_prompt).strip()
        if not response and default is not None:
            return default
        return response

    def confirm(self, prompt: str, default: bool = True) -> bool:
        suffix = " [Y/n]" if default else " [y/N]"
        response = self.ask(prompt + suffix).lower()
        if not response:
            return default
        return response in ("y", "yes", "true", "1")

    def choose(self, prompt: str, options: list[str]) -> str:
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            raw = self.ask("Enter number")
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            except ValueError:
                pass
            print("Invalid choice, try again.")


def _default_terminal_input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""
