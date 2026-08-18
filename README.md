# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.15** — Human-in-the-loop support.

## Human-in-the-loop (v0.15)

### Graph
```python
graph.interrupt_before("execute", "deploy")  # require approval before these nodes
result = graph.run({"task": "..."})
```

### ReliableAgent
```python
agent = ReliableAgent(llm=llm, human_in_the_loop=True)
# Will ask for approval of: task start, plan, each step, and final answer
answer = agent.run("...")
```

Custom UIs can pass their own callback via `HumanInput(callback=...)`.

## Feature Highlights

| Area | PowerChain capability |
|------|-----------------------|
| **Reliable Agents** | Plan → Execute → Replan → Reflect → Correct + HITL |
| **Multi-Agent** | Shared memory, parallel, coordinated modes |
| **Graph** | Loops, conditionals, persistence, human interrupts |
| **RAG** | FAISS, Chroma, InMemory + loaders |
| **Models** | OpenAI, Anthropic, Groq, Ollama |
| **DX** | Clean, explicit, easy to extend |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
