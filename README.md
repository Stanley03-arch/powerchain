# PowerChain

**A cleaner, more powerful alternative to LangChain.**

> Status: **v0.14** — Stronger Graph with loops, conditionals & state persistence.

## Graph (v0.14)

```python
from powerchain.multiagent import Graph

graph = Graph(name="MyWorkflow", verbose=True)
graph.add_node("plan", plan_fn)
graph.add_node("execute", execute_fn)
graph.add_node("finish", finish_fn)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")

# Conditional branching + loops
graph.add_conditional_edges(
    "execute",
    {"retry": "execute", "done": "finish"},
    lambda s: "done" if s.get("success") else "retry"
)

result = graph.run({"task": "..."})
graph.save_state(result, "state.json")
```

## Highlights vs earlier versions

| Version | Key addition |
|---------|--------------|
| v0.12 | ReliableAgent (plan → replan → reflect → correct) |
| v0.13 | Multi-Agent shared memory + parallel/coordinated modes |
| v0.14 | Graph with loops, conditional edges, state save/load |

## Install

```bash
git clone https://github.com/Stanley03-arch/powerchain.git
cd powerchain
pip install -e ".[all]"
```

## License

MIT
