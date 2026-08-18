"""
Simple Graph orchestration example.
"""

from powerchain.multiagent import Graph


def main():
    def plan(state: dict) -> dict:
        print("→ Planning...")
        return {"plan": f"Plan for: {state['task']}", "step": "research"}

    def research(state: dict) -> dict:
        print("→ Researching...")
        return {"research": "Found useful information about the topic.", "step": "write"}

    def write(state: dict) -> dict:
        print("→ Writing...")
        return {
            "output": f"Final answer based on plan '{state.get('plan')}' and research '{state.get('research')}'",
            "step": "done",
        }

    def should_continue(state: dict) -> bool:
        return state.get("step") != "done"

    graph = Graph(name="SimplePipeline")
    graph.add_node("plan", plan)
    graph.add_node("research", research)
    graph.add_node("write", write)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_edge("research", "write")
    # write is terminal (no outgoing edge)

    result = graph.run({"task": "Explain PowerChain benefits"})
    print("\nFinal state:")
    print(result)


if __name__ == "__main__":
    main()
