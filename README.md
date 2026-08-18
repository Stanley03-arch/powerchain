# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.5** — Core + RAG + Multi-Agent + Advanced Memory + Reliability.

## Feature Overview

| Version | What was added |
|---------|----------------|
| **v0.1** | LLM interface, Tools, Agent, ConversationMemory, Runnables, Tracing |
| **v0.2** | Full RAG pipeline |
| **v0.3** | Multi-agent (`Crew`) + `Graph` orchestration |
| **v0.4** | `SummaryMemory` + `VectorMemory` |
| **v0.5** | **RetryChatModel**, **FallbackChatModel**, proper streaming |

## Reliability Features (v0.5)

```python
from powerchain import ChatOpenAI, RetryChatModel, FallbackChatModel

# Automatic retries with exponential backoff
reliable = RetryChatModel(ChatOpenAI(), max_attempts=3)

# Primary + backup models
fallback = FallbackChatModel([
    ChatOpenAI(model="gpt-4o"),
    ChatOpenAI(model="gpt-4o-mini"),  # cheaper backup
])

# Real token streaming
for chunk in ChatOpenAI().stream(messages):
    print(chunk, end="", flush=True)
```

## Quick Examples

### Agent + Tools
```python
from powerchain import ChatOpenAI, tool, Agent

@tool
def get_weather(city: str) -> str:
    return f"Sunny in {city}"

agent = Agent(llm=ChatOpenAI(), tools=[get_weather])
print(agent.run("Weather in Nairobi?"))
```

### Multi-Agent
```python
from powerchain import ChatOpenAI
from powerchain.multiagent import AgentNode, Crew

crew = Crew(agents=[
    AgentNode("Researcher", ChatOpenAI(), role="Researcher", goal="Find facts"),
    AgentNode("Writer", ChatOpenAI(), role="Writer", goal="Write clearly"),
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

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[openai]"
export OPENAI_API_KEY=sk-...
```

## Roadmap

- [x] Core
- [x] RAG
- [x] Multi-agent + Graph
- [x] Advanced Memory
- [x] Reliability (retries, fallbacks, streaming)
- [ ] More document loaders & vector store backends
- [ ] Evaluation harness
- [ ] Additional LLM providers

## License

MIT
