# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.12** — ReliableAgent with planning, recovery & self-correction.

## ReliableAgent (New in v0.12)

Designed to be more robust than typical LangChain agents:

- Explicit multi-step planning
- Step-by-step execution with state
- Automatic **replanning** when a step fails
- Self-reflection + answer correction
- Better tool error recovery
- Verbose mode for full transparency

```python
from powerchain import ChatOpenAI, tool, ReliableAgent

@tool
def calculate(expression: str) -> str:
    return str(eval(expression))

agent = ReliableAgent(llm=ChatOpenAI(), tools=[calculate], reflect=True)
print(agent.run("Complex multi-step task here..."))
```

## Feature Overview

| Area | Capabilities |
|------|--------------|
| **Reliable Agents** | `ReliableAgent` (plan → execute → replan → reflect → correct) |
| **Other Agents** | Agent, PlanningAgent, ReflectiveAgent |
| **Models** | OpenAI, Anthropic, Groq, Ollama + Retry/Fallback |
| **Memory** | Conversation, Summary, Vector |
| **RAG** | FAISS, Chroma, InMemory + loaders |
| **Multi-Agent** | Crew + Graph |
| **Output Parsing** | Pydantic, JSON, List |
| **CLI + Tests** | Yes |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
