# PowerChain

**A cleaner, more powerful alternative to LangChain.**

PowerChain is designed from the ground up to fix the main pain points of LangChain while delivering stronger agent capabilities, better composition, first-class streaming, and excellent observability.

> Status: **v0.1 Core** — solid foundation ready for rapid expansion.

## Why PowerChain?

| Area              | LangChain pain point              | PowerChain approach                          |
|-------------------|-----------------------------------|----------------------------------------------|
| Composition       | LCEL can feel heavy / magical     | Explicit, typed, easy-to-debug Runnables     |
| Agents            | Often brittle                     | First-class agent loop + planning + reflection |
| Tools             | Schema + execution mixed          | Clean schema + robust execution + retries    |
| Memory            | Many overlapping classes          | Simple hierarchical memory from day one      |
| Observability     | Bolted on                         | Built-in tracing & callbacks                 |
| Typing            | Inconsistent                      | Strong Pydantic + modern type hints          |
| Streaming         | Uneven support                    | First-class everywhere                       |

## Features in v0.1

- Unified LLM / ChatModel interface (streaming + tool calling ready)
- Strong typed Tool system
- Modern Agent loop with hooks for planning & reflection
- Composition primitives (`Runnable`, `Sequential`, `Parallel`)
- Conversation + summary memory
- Prompt templates
- Built-in tracing hooks
- Clean package structure ready for RAG, multi-agent, and integrations

## Quick Start

```bash
pip install -e .
```

```python
from powerchain import ChatOpenAI, tool, Agent, ConversationMemory

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Sunny and 24°C in {city}"

llm = ChatOpenAI(model="gpt-4o-mini")  # or any compatible model
agent = Agent(llm=llm, tools=[get_weather], memory=ConversationMemory())

response = agent.run("What's the weather in Nairobi?")
print(response)
```

## Project Structure

```
powerchain/
├── core/
│   ├── models/          # LLM interfaces
│   ├── prompts/         # Prompt templates
│   ├── tools/           # Tool system
│   ├── agents/          # Agent runtime
│   ├── memory/          # Memory systems
│   ├── runnables/       # Composition
│   └── tracing/         # Observability
├── rag/                 # (coming soon)
├── integrations/        # (coming soon)
└── eval/                 # (coming soon)
```

## Roadmap

### v0.2 — RAG & Retrieval
- Document loaders & splitters
- Vector store interface
- Hybrid retrievers
- Agentic RAG patterns

### v0.3 — Multi-Agent & Graphs
- Native multi-agent orchestration
- Graph-based workflows (LangGraph-style but cleaner)
- Human-in-the-loop

### v0.4+ — Production Power
- More LLM providers
- Advanced memory (vector + hierarchical)
- Evaluation harness
- Better streaming & parallelism
- Guardrails & reliability features

## Contributing

This is early-stage. Issues, ideas, and PRs are very welcome.

## License

MIT
