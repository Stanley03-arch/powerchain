# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.9** — Now with Planning & Reflection agents.

## Advanced Agents (v0.9)

```python
from powerchain import ChatOpenAI, PlanningAgent, ReflectiveAgent

llm = ChatOpenAI()

# 1. Planning Agent — breaks task into steps, executes them, synthesizes answer
planner = PlanningAgent(llm=llm)
print(planner.run("Complex multi-step task here..."))

# 2. Reflective Agent — answers, critiques itself, then improves the answer
reflective = ReflectiveAgent(llm=llm)
print(reflective.run("Explain the benefits of PowerChain"))
```

## Full Feature Set

| Area | Capabilities |
|------|--------------|
| **Models** | OpenAI, Anthropic, Groq, Ollama + Retry + Fallback |
| **Agents** | Basic Agent, PlanningAgent, ReflectiveAgent |
| **Tools** | Typed `@tool` decorator |
| **Memory** | Conversation, Summary, Vector |
| **RAG** | Loaders, Splitters, Embeddings, FAISS, Chroma, InMemory |
| **Multi-Agent** | Crew + Graph orchestration |
| **Eval** | LLM-as-judge QAEvaluator |
| **Composition** | Runnable pipeline (`\|` style) |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
