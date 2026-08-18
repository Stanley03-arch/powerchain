"""
Stronger Graph example with conditional branching and a loop.

Demonstrates:
- Conditional edges
- A retry loop
- State persistence
"""

from powerchain.multiagent import Graph


def main():
    def plan(state: dict) -> dict:
        print("  [plan] Creating plan...")
        return {"plan": f"Plan for: {state['task']}", "attempts": 0, "status": "planned"}

    def execute(state: dict) -> dict:
        attempts = state.get("attempts", 0) + 1
        print(f"  [execute] Attempt {attempts}...")
        # Simulate success on 2nd try
        success = attempts >= 2
        return {
            "attempts": attempts,
            "status": "success" if success else "failed",
            "result": "Completed successfully" if success else "Still failing",
        }

    def should_retry(state: dict) -> str:
        if state.get("status") == "success":
            return "done"
        if state.get("attempts", 0) >= 3:
            return "give_up"
        return "retry"

    def finish(state: dict) -> dict:
        print("  [finish] Done.")
        return {"final": state.get("result", "No result")}

    def give_up(state: dict) -> dict:
        print("  [give_up] Max attempts reached.")
        return {"final": "Failed after max retries"}

    graph = Graph(name="RetryDemo", verbose=True)

    graph.add_node("plan", plan)
    graph.add_node("execute", execute)
    graph.add_node("finish", finish)
    graph.add_node("give_up", give_up)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")

    # Conditional branching from execute
    graph.add_conditional_edges(
        "execute",
        {
            "retry": "execute",   # loop back
            "done": "finish",
            "give_up": "give_up",
        },
        should_retry,
    )

    graph.set_finish_point("finish")
    graph.set_finish_point("give_up")

    result = graph.run({"task": "Process important data"})

    print("\nFinal state:")
    print(f"  status : {result.get('status')}")
    print(f"  final  : {result.get('final')}")
    print(f"  history: {result.get('__graph_history__')}")

    # Persist state
    graph.save_state(result, "/tmp/powerchain_graph_state.json")
    print("\nState saved to /tmp/powerchain_graph_state.json")


if __name__ == "__main__":
    main()
