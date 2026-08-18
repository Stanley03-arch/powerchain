"""
Human-in-the-loop examples.

1. Graph with interrupt_before
2. ReliableAgent with human approvals
"""

from powerchain.multiagent import Graph
from powerchain import ChatOpenAI, ReliableAgent


def demo_graph_hitl():
    print("=== Graph with Human-in-the-loop ===\n")

    def plan(state):
        return {"plan": "Step 1: Research\nStep 2: Write", "status": "planned"}

    def execute(state):
        return {"result": "Work completed", "status": "done"}

    def finish(state):
        return {"final": state.get("result", "")}

    graph = Graph(name="HITLDemo", verbose=True)
    graph.add_node("plan", plan)
    graph.add_node("execute", execute)
    graph.add_node("finish", finish)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "execute")
    graph.add_edge("execute", "finish")
    graph.set_finish_point("finish")

    # Require human approval before the execute node
    graph.interrupt_before("execute")

    result = graph.run({"task": "Demo task"})
    print("\nFinal:", result.get("final"))
    print("History:", result.get("__graph_history__"))


def demo_agent_hitl():
    print("\n\n=== ReliableAgent with Human-in-the-loop ===\n")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    agent = ReliableAgent(llm=llm, reflect=True, human_in_the_loop=True, verbose=True)

    answer = agent.run("List three benefits of clean software architecture in one short paragraph.")
    print("\nFINAL:", answer)


if __name__ == "__main__":
    demo_graph_hitl()
    # Uncomment to try the agent version (requires OPENAI_API_KEY):
    # demo_agent_hitl()
