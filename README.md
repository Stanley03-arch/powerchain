# PowerChain

**A cleaner, more powerful alternative to LangChain.**

Agents • Graphs • RAG • Multi-Agent • Human-in-the-Loop — without the complexity tax.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Stanley03-arch/powerchain?style=social)](https://github.com/Stanley03-arch/powerchain)

⭐ **If PowerChain helps you build better agents, please star the repo!**

---

## Why PowerChain?

LangChain is powerful but often feels heavy and opaque.  
PowerChain keeps the good ideas and makes them **explicit, composable, and easy to extend**.

| Feature | PowerChain |
|---------|------------|
| **Reliable Agents** | Plan → Execute → Replan → Reflect → Correct + HITL |
| **Multi-Agent** | Shared memory, parallel, coordinated modes |
| **Graph** | Loops, conditionals, persistence, human interrupts |
| **RAG** | FAISS, Chroma, InMemory + loaders & splitters |
| **Models** | OpenAI, Anthropic, Groq, Ollama + Retry / Fallback |
| **DX** | Clean API, type hints, minimal magic |

---

## Quick Start

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

### Simple Agent

```python
from powerchain import ChatOpenAI, Agent, tool

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = Agent(llm=llm, tools=[search])
print(agent.run("What is the capital of Kenya?"))
```

### Reliable Agent (Plan → Execute → Reflect)

```python
from powerchain import ChatOpenAI, ReliableAgent

agent = ReliableAgent(llm=ChatOpenAI(model="gpt-4o-mini"))
answer = agent.run("Write a short plan to learn PyTorch in 30 days")
print(answer)
```

### Human-in-the-Loop

```python
from powerchain import ReliableAgent, ChatOpenAI

agent = ReliableAgent(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    human_in_the_loop=True,   # asks for approval at key steps
)
answer = agent.run("Deploy a small FastAPI service")
```

### Graph with Interrupts

```python
from powerchain import Graph

graph = Graph()
# ... add nodes ...
graph.interrupt_before("execute", "deploy")  # require human approval
result = graph.run({"task": "..."})
```

### RAG in a few lines

```python
from powerchain import (
    TextLoader, RecursiveCharacterTextSplitter,
    OpenAIEmbeddings, InMemoryVectorStore, RAGChain, ChatOpenAI
)

docs = TextLoader("docs.txt").load()
chunks = RecursiveCharacterTextSplitter().split(docs)
store = InMemoryVectorStore(OpenAIEmbeddings()).from_documents(chunks)

rag = RAGChain(llm=ChatOpenAI(), retriever=store.as_retriever())
print(rag.run("What is PowerChain?"))
```

---

## Core Concepts

- **Models** — `ChatOpenAI`, `ChatAnthropic`, `ChatGroq`, `ChatOllama` + `RetryChatModel` / `FallbackChatModel`
- **Agents** — `Agent`, `PlanningAgent`, `ReflectiveAgent`, `ReliableAgent`
- **Tools** — `@tool` decorator or `BaseTool`
- **Memory** — Conversation, Summary, Vector
- **Graphs** — Nodes, Edges, loops, conditionals, persistence, HITL
- **Multi-Agent** — `Crew`, shared memory, parallel execution
- **RAG** — Loaders, splitters, embeddings, FAISS / Chroma / InMemory
- **Output Parsers** — JSON, Pydantic, List
- **Eval** — Simple QA evaluator

---

## Examples

See the `examples/` folder:

- `basic_agent.py`
- `reliable_agent_example.py`
- `human_in_the_loop_example.py`
- `graph_example.py` / `graph_v2_example.py`
- `multi_agent_example.py`
- `rag_example.py`
- `memory_example.py`
- and more…

---

## Status

**v0.15.0** — Human-in-the-loop support is production-ready.

The project is under active development. APIs may still evolve slightly.

---

## License

MIT

---

**Built with ❤️ by [Stanley Samwel](https://github.com/Stanley03-arch)**

⭐ **Star the repo if you find PowerChain useful!**
