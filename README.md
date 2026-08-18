# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.8** — Production-ready foundation with multiple vector stores & LLM providers.

## Vector Stores

| Store | Class | Persistence | Install |
|-------|------|-------------|--------|
| In-Memory | `InMemoryVectorStore` | No | Built-in |
| FAISS | `FAISSVectorStore` | Yes (`save_local` / `load_local`) | `pip install faiss-cpu` |
| Chroma | `ChromaVectorStore` | Yes | `pip install chromadb` |

```python
from powerchain import OpenAIEmbeddings, FAISSVectorStore, ChromaVectorStore

embeddings = OpenAIEmbeddings()

# FAISS
faiss_store = FAISSVectorStore(embedding=embeddings)
faiss_store.add_documents(docs)
faiss_store.save_local("./my_index")

# Chroma
chroma_store = ChromaVectorStore(embedding=embeddings, persist_directory="./chroma_db")
```

## LLM Providers

`ChatOpenAI` · `ChatAnthropic` · `ChatGroq` · `ChatOllama`

## Full Feature Set

- Agents + Tools + Memory (Conversation / Summary / Vector)
- RAG (Loaders, Splitters, Embeddings, Vector Stores, RAGChain)
- Multi-Agent Crews + Graph orchestration
- Retry + Fallback models
- Streaming
- Evaluation harness
- Multiple LLM providers & vector backends

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
