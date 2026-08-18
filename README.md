# PowerChain

**A cleaner, more powerful alternative to LangChain.**

PowerChain is designed from the ground up to fix the main pain points of LangChain while delivering stronger agent capabilities, better composition, first-class streaming readiness, and excellent observability.

> Status: **v0.3** — Core + RAG + Multi-Agent & Graph orchestration.

## Why PowerChain?

| Area              | LangChain pain point              | PowerChain approach                          |
|-------------------|-----------------------------------|----------------------------------------------|
| Composition       | LCEL can feel heavy / magical     | Explicit, typed, easy-to-debug Runnables     |
| Agents            | Often brittle                     | First-class agent loop + planning + reflection |
| Tools             | Schema + execution mixed          | Clean schema + robust execution              |
| Memory            | Many overlapping classes          | Simple hierarchical memory                   |
| Observability     | Bolted on                         | Built-in tracing & callbacks                 |
| Typing            | Inconsistent                      | Strong Pydantic + modern type hints          |
| RAG               | Complex setup                     | Clean, modular pipeline                      |
| Multi-agent       | Fragmented (LangGraph, CrewAI…)   | Native Crew + lightweight Graph              |

## Features

### v0.1 — Core
- Unified LLM / ChatModel interface
- Strong typed Tool system + `@tool` decorator
- Modern Agent loop
- Conversation Memory
- Prompt templates
- Runnable composition (`|` style)
- Tracing / callback hooks

### v0.2 — RAG
- Document model, TextLoader
- RecursiveCharacterTextSplitter
- OpenAIEmbeddings
- InMemoryVectorStore + Retriever
- RAGChain

### v0.3 — Multi-Agent (just added)
- `AgentNode` — named agents with role & goal
- `Crew` — sequential & round-robin multi-agent execution
- `Graph` — lightweight graph-based orchestration (LangGraph-style but simpler)

## Quick Start

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[openai]"
export OPENAI_API_KEY=sk-...
```

### Single Agent
```python
from powerchain import ChatOpenAI, tool, Agent

@tool
def get_weather(city: str) -> str:
    return f"Sunny in {city}"

agent = Agent(llm=ChatOpenAI(), tools=[get_weather])
print(agent.run("Weather in Nairobi?"))
```

### Multi-Agent Crew
```python
from powerchain import ChatOpenAI
from powerchain.multiagent import AgentNode, Crew

llm = ChatOpenAI()
researcher = AgentNode(name="Researcher", llm=llm, role="Researcher", goal="Find facts")
writer = AgentNode(name="Writer", llm=llm, role="Writer", goal="Write clearly")

crew = Crew(agents=[researcher, writer])
print(crew.run_sequential("Explain quantum computing simply"))
```

### Graph Orchestration
```python
from powerchain.multiagent import Graph

graph = Graph()
graph.add_node("plan", lambda s: {"plan": "..."})
graph.add_node("execute", lambda s: {"result": "done"})
graph.set_entry_point("plan")
graph.add_edge("plan", "execute")

print(graph.run({"task": "My task"}))
```

## Project Structure

```
powerchain/
├── core/           # models, tools, agents, memory, runnables, tracing
├── rag/            # documents, loaders, splitters, embeddings, vectorstores, retrievers
├── multiagent/     # AgentNode, Crew, Graph
└── examples/
```

## Roadmap

- [x] Core (models, tools, agents, memory, composition)
- [x] RAG foundation
- [x] Multi-agent & graph orchestration
- [ ] Better memory (summary + vector memory)
- [ ] More loaders & vector store backends
- [ ] Streaming polish & reliability (retries, fallbacks)
- [ ] Evaluation harness
- [ ] More LLM providers

## License

MIT
