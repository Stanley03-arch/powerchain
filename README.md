# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.7** — Full-featured foundation with multiple LLM providers.

## Supported LLM Providers

| Provider | Class | Notes |
|----------|------|-------|
| OpenAI / compatible | `ChatOpenAI` | Also works with Azure, Together, Fireworks, etc. |
| Anthropic | `ChatAnthropic` | Claude models |
| Groq | `ChatGroq` | Extremely fast inference |
| Ollama | `ChatOllama` | Local models |

```python
from powerchain import ChatOpenAI, ChatAnthropic, ChatGroq, ChatOllama

openai_llm = ChatOpenAI(model="gpt-4o-mini")
claude = ChatAnthropic(model="claude-3-5-sonnet-20241022")
groq = ChatGroq(model="llama-3.3-70b-versatile")
local = ChatOllama(model="llama3.2")
```

## Feature Overview

| Version | Highlights |
|---------|------------|
| **v0.1** | Core (LLM, Tools, Agent, Memory, Runnables) |
| **v0.2** | RAG pipeline |
| **v0.3** | Multi-agent Crew + Graph |
| **v0.4** | SummaryMemory + VectorMemory |
| **v0.5** | Retry, Fallback, Streaming |
| **v0.6** | WebLoader, DirectoryLoader, Evaluation |
| **v0.7** | **Anthropic, Groq, Ollama providers** |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"          # OpenAI + Anthropic
# or selectively:
pip install -e ".[openai]"
pip install anthropic            # for ChatAnthropic
```

## Quick Examples

### Agent
```python
from powerchain import ChatOpenAI, tool, Agent

@tool
def get_weather(city: str) -> str:
    return f"Sunny in {city}"

agent = Agent(llm=ChatOpenAI(), tools=[get_weather])
print(agent.run("Weather in Nairobi?"))
```

### Multi-Agent + RAG + Eval all available
See the `examples/` folder.

## Roadmap

- [x] Core
- [x] RAG
- [x] Multi-agent + Graph
- [x] Advanced Memory
- [x] Reliability
- [x] Loaders + Evaluation
- [x] Multiple LLM providers
- [ ] More vector store backends (Chroma, FAISS, etc.)
- [ ] Deeper agent improvements (planning, reflection)

## License

MIT
