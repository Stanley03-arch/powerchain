# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.11** — Tests + CLI added.

## CLI

```bash
pip install -e ".[openai]"
export OPENAI_API_KEY=sk-...

powerchain version
powerchain chat
powerchain chat --model gpt-4o-mini
```

## Run Tests

```bash
pip install -e ".[dev]"
pytest
```

## Feature Overview

| Area | Capabilities |
|------|--------------|
| **Models** | OpenAI · Anthropic · Groq · Ollama + Retry/Fallback |
| **Agents** | Agent · PlanningAgent · ReflectiveAgent |
| **Tools** | Typed `@tool` |
| **Memory** | Conversation · Summary · Vector |
| **Output Parsing** | Pydantic · JSON · List |
| **RAG** | Loaders · FAISS · Chroma · InMemory |
| **Multi-Agent** | Crew · Graph |
| **Eval** | LLM-as-judge |
| **CLI** | `powerchain chat` / `version` |
| **Tests** | Basic unit tests included |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
