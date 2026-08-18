from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class Node:
    """A node in the execution graph."""
    name: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]
    description: str = ""


@dataclass
class Edge:
    """Directed edge with optional condition."""
    source: str
    target: str
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None  # None = always take


class Graph:
    """Simple but powerful graph-based orchestration.

    Inspired by LangGraph ideas but kept deliberately lightweight and readable.
    """

    def __init__(self, name: str = "PowerGraph"):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]], description: str = "") -> "Graph":
        self.nodes[name] = Node(name=name, func=func, description=description)
        return self

    def add_edge(self, source: str, target: str, condition: Optional[Callable[[Dict[str, Any]], bool]] = None) -> "Graph":
        self.edges.append(Edge(source=source, target=target, condition=condition))
        return self

    def set_entry_point(self, name: str) -> "Graph":
        if name not in self.nodes:
            raise ValueError(f"Node '{name}' does not exist")
        self.entry_point = name
        return self

    def _get_next_nodes(self, current: str, state: Dict[str, Any]) -> List[str]:
        next_nodes = []
        for edge in self.edges:
            if edge.source == current:
                if edge.condition is None or edge.condition(state):
                    next_nodes.append(edge.target)
        return next_nodes

    def run(self, initial_state: Dict[str, Any], max_steps: int = 20) -> Dict[str, Any]:
        if not self.entry_point:
            raise ValueError("Entry point not set. Call set_entry_point() first.")

        state = dict(initial_state)
        current = self.entry_point
        visited_steps = 0

        while current and visited_steps < max_steps:
            if current not in self.nodes:
                raise ValueError(f"Unknown node: {current}")

            node = self.nodes[current]
            # Execute node — it receives state and must return updated state (or partial)
            result = node.func(state)
            if isinstance(result, dict):
                state.update(result)

            # Find next nodes
            next_nodes = self._get_next_nodes(current, state)

            if not next_nodes:
                break  # terminal node

            # For simplicity we take the first matching edge.
            # (Can be extended later to support parallel fan-out)
            current = next_nodes[0]
            visited_steps += 1

        return state

    def __repr__(self) -> str:
        return f"Graph(name={self.name!r}, nodes={list(self.nodes.keys())})"
