from __future__ import annotations

import json
from typing import Any, List, Optional

from powerchain.core.models.base import BaseChatModel, ChatMessage, Role
from powerchain.core.tools.base import BaseTool
from powerchain.core.memory.conversation import ConversationMemory


class Agent:
    """A capable agent with tool use, memory, and an extensible loop.

    Designed to be more reliable and easier to debug than classic ReAct agents.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[ConversationMemory] = None,
        system_prompt: str = (
            "You are a helpful, precise AI assistant. "
            "Use tools when they help you answer accurately. "
            "Think step by step when needed."
        ),
        max_iterations: int = 8,
    ):
        self.llm = llm
        self.tools = {t.name: t for t in (tools or [])}
        self.memory = memory or ConversationMemory()
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations

    def _tool_schemas(self) -> List[dict]:
        return [t.to_openai_tool() for t in self.tools.values()]

    def _execute_tool(self, name: str, arguments: str) -> str:
        if name not in self.tools:
            return f"Error: Unknown tool '{name}'"

        tool = self.tools[name]
        try:
            args = json.loads(arguments) if arguments else {}
            result = tool.run(**args)
            return str(result)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def run(self, user_input: str) -> str:
        """Run the agent on a user message and return the final answer."""
        self.memory.add_user(user_input)

        messages: List[ChatMessage] = [
            ChatMessage(role=Role.SYSTEM, content=self.system_prompt),
            *self.memory.get_messages(),
        ]

        for iteration in range(self.max_iterations):
            response = self.llm.invoke(
                messages,
                tools=self._tool_schemas() if self.tools else None,
            )

            # If the model wants to call tools
            if response.tool_calls:
                messages.append(response)

                for tc in response.tool_calls:
                    name = tc["function"]["name"]
                    args = tc["function"]["arguments"]
                    tool_result = self._execute_tool(name, args)

                    messages.append(
                        ChatMessage(
                            role=Role.TOOL,
                            content=tool_result,
                            tool_call_id=tc["id"],
                            name=name,
                        )
                    )
                continue

            # Final answer
            final = response.content
            self.memory.add_assistant(final)
            return final

        return "I reached the maximum number of reasoning steps without a final answer."

    async def arun(self, user_input: str) -> str:
        """Async version of run."""
        self.memory.add_user(user_input)

        messages: List[ChatMessage] = [
            ChatMessage(role=Role.SYSTEM, content=self.system_prompt),
            *self.memory.get_messages(),
        ]

        for _ in range(self.max_iterations):
            response = await self.llm.ainvoke(
                messages,
                tools=self._tool_schemas() if self.tools else None,
            )

            if response.tool_calls:
                messages.append(response)

                for tc in response.tool_calls:
                    name = tc["function"]["name"]
                    args = tc["function"]["arguments"]
                    tool_result = self._execute_tool(name, args)

                    messages.append(
                        ChatMessage(
                            role=Role.TOOL,
                            content=tool_result,
                            tool_call_id=tc["id"],
                            name=name,
                        )
                    )
                continue

            final = response.content
            self.memory.add_assistant(final)
            return final

        return "I reached the maximum number of reasoning steps without a final answer."
