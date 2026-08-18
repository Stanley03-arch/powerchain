# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.6** — Core + RAG + Multi-Agent + Memory + Reliability + Loaders + Evaluation.

## Feature Overview

| Version | Highlights |
|---------|------------|
| **v0.1** | LLM, Tools, Agent, Memory, Runnables, Tracing |
| **v0.2** | Full RAG pipeline |
| **v0.3** | Multi-agent Crew + Graph orchestration |
| **v0.4** | SummaryMemory + VectorMemory |
| **v0.5** | Retry, Fallback, real streaming |
| **v0.6** | **WebLoader, DirectoryLoader, QAEvaluator** |

## New in v0.6

### More Loaders
```python
from powerchain import WebLoader, DirectoryLoader, TextLoader

docs = WebLoader("https://example.com").load()
docs = DirectoryLoader("./my_docs", glob="**/*.txt").load()
```

### Evaluation Harness
```python
from powerchain import ChatOpenAI, QAEvaluator

evaluator = QAEvaluator(llm=ChatOpenAI())
result = evaluator.evaluate(
    input="What is PowerChain?",
    prediction="A modern LLM framework",
    reference="A cleaner alternative to LangChain"
)
print(result.score, result.passed)
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
- [x] Reliability
- [x] More loaders + Evaluation
- [ ] Additional LLM providers (Anthropic, Groq, Ollama…)
- [ ] More vector store backends

## License

MIT
