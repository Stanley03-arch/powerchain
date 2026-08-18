# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.10** — Structured output parsers added.

## Structured Output (v0.10)

```python
from pydantic import BaseModel, Field
from powerchain import ChatOpenAI, ChatMessage, Role, PydanticOutputParser

class MovieReview(BaseModel):
    title: str
    rating: float
    summary: str

parser = PydanticOutputParser(MovieReview)
prompt = f"Review Inception.\n\n{parser.get_format_instructions()}"

response = ChatOpenAI().invoke([ChatMessage(role=Role.USER, content=prompt)])
review = parser.parse(response.content)  # -> MovieReview instance
```

Also available: `JsonOutputParser`, `ListOutputParser`.

## Complete Feature Set

| Area | Capabilities |
|------|--------------|
| **Models** | OpenAI · Anthropic · Groq · Ollama + Retry/Fallback |
| **Agents** | Agent · PlanningAgent · ReflectiveAgent |
| **Tools** | Typed `@tool` decorator |
| **Memory** | Conversation · Summary · Vector |
| **Output Parsing** | Pydantic · JSON · List |
| **RAG** | Loaders · Splitters · FAISS · Chroma · InMemory |
| **Multi-Agent** | Crew · Graph |
| **Eval** | LLM-as-judge |
| **Composition** | Runnable pipelines |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
