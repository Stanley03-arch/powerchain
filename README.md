# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.13** — Upgraded Multi-Agent with shared memory & parallel execution.

## Multi-Agent (v0.13)

```python
from powerchain import ChatOpenAI
from powerchain.multiagent import AgentNode, Crew, SharedMemory

llm = ChatOpenAI()
crew = Crew(
    agents=[
        AgentNode("Researcher", llm, role="Researcher", goal="Find facts"),
        AgentNode("Writer", llm, role="Writer", goal="Write clearly"),
        AgentNode("Critic", llm, role="Critic", goal="Improve quality"),
    ],
    shared_memory=SharedMemory(),
)

# Four execution modes:
crew.run_sequential(task)
crew.run_round_robin(task, rounds=2)
crew.run_parallel(task)          # concurrent
crew.run_coordinated(task)       # shared memory heavy
```

## ReliableAgent (v0.12)

Plan → Execute → Replan on failure → Reflect → Correct

## Full Feature Set

- ReliableAgent, PlanningAgent, ReflectiveAgent
- Multi-Agent Crew (sequential / round-robin / parallel / coordinated)
- SharedMemory across agents
- Graph orchestration
- RAG (FAISS, Chroma, InMemory)
- Multiple LLM providers
- Output parsers, Evaluation, CLI, Tests

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
