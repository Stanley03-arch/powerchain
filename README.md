# PowerChain

**A cleaner, more powerful alternative to LangChain.**

PowerChain is designed from the ground up to fix the main pain points of LangChain while delivering stronger agent capabilities, better composition, first-class streaming readiness, and excellent observability.

> Status: **v0.2** — Core + RAG foundation complete.

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
| RAG               | Complex setup                     | Clean, modular, easy to extend               |

## Features

### v0.1 — Core
- Unified LLM / ChatModel interface (streaming + tool calling ready)
- Strong typed Tool system + `@tool` decorator
- Modern Agent loop
- Conversation Memory
- Prompt templates
- Runnable composition (`|` style)
- Tracing / callback hooks

### v0.2 — RAG (just added)
- `Document` model
- Text loaders
- Recursive character text splitter
- Embeddings interface + OpenAI embeddings
- In-memory vector store (cosine similarity)
- Vector store retriever
- Simple + effective `RAGChain`

## Quick Start

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[openai]"
```

### Agent example

```python
from powerchain import ChatOpenAI, tool, Agent, ConversationMemory

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Sunny and 24°C in {city}"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = Agent(llm=llm, tools=[get_weather], memory=ConversationMemory())

print(agent.run("What's the weather in Nairobi?"))
```

### RAG example

```python
from powerchain import (
    ChatOpenAI, Document, RecursiveCharacterTextSplitter,
    OpenAIEmbeddings, InMemoryVectorStore, RAGChain
)

docs = [Document(page_content="PowerChain is a modern LLM framework...")]
splitter = RecursiveCharacterTextSplitter(chunk_size=500)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
store = InMemoryVectorStore(embedding=embeddings)
store.add_documents(chunks)

rag = RAGChain(llm=ChatOpenAI(), retriever=store.as_retriever())
print(rag.invoke("What is PowerChain?"))
```

## Project Structure

```
powerchain/
├── core/
│   ├── models/
│   ├── prompts/
│   ├── tools/
│   ├── agents/
│   ├── memory/
│   ├── runnables/
│   └── tracing/
├── rag/
│   ├── documents.py
│   ├── loaders/
│   ├── splitters/
│   ├── embeddings/
│   ├── vectorstores/
│   ├── retrievers/
│   └── chain.py
└── ...
```

## Roadmap

- [x] Core (models, tools, agents, memory, composition)
- [x] RAG foundation
- [ ] Multi-agent & graph orchestration
- [ ] Better memory (summary + vector memory)
- [ ] More loaders & vector store backends
- [ ] Streaming polish & reliability (retries, fallbacks)
- [ ] Evaluation harness
- [ ] More LLM providers

## License

MIT
