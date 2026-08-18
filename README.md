# PowerChain

**A cleaner, more powerful alternative to LangChain.**

PowerChain is designed from the ground up to fix the main pain points of LangChain while delivering stronger agent capabilities, better composition, and excellent observability.

> Status: **v0.4** — Core + RAG + Multi-Agent + Advanced Memory.

## Features at a glance

| Version | Capabilities |
|---------|--------------|
| **v0.1** | LLM interface, Tools, Agent, ConversationMemory, PromptTemplate, Runnable composition, Tracing |
| **v0.2** | Full RAG pipeline (Documents, Splitters, Embeddings, VectorStore, RAGChain) |
| **v0.3** | Multi-agent (`AgentNode`, `Crew`) + lightweight `Graph` orchestration |
| **v0.4** | **SummaryMemory** + **VectorMemory** (just added) |

## Memory Systems

```python
from powerchain import ChatOpenAI, Agent, OpenAIEmbeddings
from powerchain.core.memory import SummaryMemory, VectorMemory

llm = ChatOpenAI()

# 1. Summary Memory — automatically summarizes old turns
summary_mem = SummaryMemory(llm=llm, max_messages=10)

# 2. Vector Memory — recent buffer + long-term semantic retrieval
vector_mem = VectorMemory(embedding=OpenAIEmbeddings(), max_recent=6, k_long_term=4)

agent = Agent(llm=llm, memory=summary_mem)  # or vector_mem
```

## Quick Examples

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
crew = Crew(agents=[
    AgentNode("Researcher", llm, role="Researcher", goal="Find facts"),
    AgentNode("Writer", llm, role="Writer", goal="Write clearly"),
])
print(crew.run_sequential("Explain PowerChain"))
```

### RAG
```python
from powerchain import ChatOpenAI, Document, OpenAIEmbeddings, InMemoryVectorStore, RAGChain

store = InMemoryVectorStore(embedding=OpenAIEmbeddings())
store.add_documents([Document(page_content="PowerChain is a modern LLM framework.")])
rag = RAGChain(llm=ChatOpenAI(), retriever=store.as_retriever())
print(rag.invoke("What is PowerChain?"))
```

## Project Structure

```
powerchain/
├── core/
│   ├── models/
│   ├── tools/
│   ├── agents/
│   ├── memory/          # Conversation, Summary, Vector
│   ├── prompts/
│   ├── runnables/
│   └── tracing/
├── rag/
├── multiagent/         # AgentNode, Crew, Graph
└── examples/
```

## Roadmap

- [x] Core
- [x] RAG foundation
- [x] Multi-agent & Graph
- [x] Better memory (Summary + Vector)
- [ ] Reliability (retries, fallbacks, better streaming)
- [ ] More loaders & vector backends
- [ ] Evaluation harness
- [ ] Additional LLM providers

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[openai]"
```

## License

MIT
