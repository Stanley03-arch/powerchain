from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union


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
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None  # None = always


class Graph:
    """Powerful yet lightweight graph orchestration.

    Features:
    - Conditional edges
    - Loops (with max iteration protection)
    - Shared state dictionary
    - Simple save / load of final state
    - Clear execution trace when verbose=True
    """

    def __init__(self, name: str = "PowerGraph", verbose: bool = False):
        self.name = name
        self.verbose = verbose
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.entry_point: Optional[str] = None
        self._end_nodes: Set[str] = set()  # explicit terminal nodes (optional)

    def add_node(
        self,
        name: str,
        func: Callable[[Dict[str, Any]], Dict[str, Any]],
        description: str = "",
    ) -> "Graph":
        self.nodes[name] = Node(name=name, func=func, description=description)
        return self

    def add_edge(
        self,
        source: str,
        target: str,
        condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
    ) -> "Graph":
        self.edges.append(Edge(source=source, target=target, condition=condition))
        return self

    def add_conditional_edges(
        self,
        source: str,
        condition_map: Dict[str, str],
        condition_fn: Callable[[Dict[str, Any]], str],
    ) -> "Graph":
        """Add multiple conditional edges from one source.

        condition_fn should return a key that exists in condition_map.
        Example:
            graph.add_conditional_edges(
                "check",
                {"ok": "success", "fail": "retry"},
                lambda s: "ok" if s.get("valid") else "fail"
            )
        """
        for key, target in condition_map.items():
            self.add_edge(
                source,
                target,
                condition=lambda state, k=key: condition_fn(state) == k,
            )
        return self

    def set_entry_point(self, name: str) -> "Graph":
        if name not in self.nodes:
            raise ValueError(f"Node '{name}' does not exist")
        self.entry_point = name
        return self

    def set_finish_point(self, name: str) -> "Graph":
        """Mark a node as an explicit terminal node."""
        self._end_nodes.add(name)
        return self

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _get_next_nodes(self, current: str, state: Dict[str, Any]) -> List[str]:
        next_nodes = []
        for edge in self.edges:
            if edge.source == current:
                if edge.condition is None or edge.condition(state):
                    next_nodes.append(edge.target)
        return next_nodes

    def run(
        self,
        initial_state: Dict[str, Any],
        max_steps: int = 30,
    ) -> Dict[str, Any]:
        if not self.entry_point:
            raise ValueError("Entry point not set. Call set_entry_point() first.")

        state = dict(initial_state)
        current: Optional[str] = self.entry_point
        steps = 0
        history: List[str] = []

        self._log(f"\n[Graph:{self.name}] Starting at '{current}'")

        while current and steps < max_steps:
            if current not in self.nodes:
                raise ValueError(f"Unknown node: {current}")

            history.append(current)
            node = self.nodes[current]
            self._log(f"  → Executing node: {current}")

            result = node.func(state)
            if isinstance(result, dict):
                state.update(result)

            # Explicit finish point
            if current in self._end_nodes:
                self._log(f"  ✓ Reached finish point: {current}")
                break

            next_nodes = self._get_next_nodes(current, state)

            if not next_nodes:
                self._log(f"  ✓ No outgoing edges — stopping at '{current}'")
                break

            # Take first matching edge (can be extended later for fan-out)
            current = next_nodes[0]
            steps += 1

        if steps >= max_steps:
            self._log(f"  ! Max steps ({max_steps}) reached")

        state["__graph_history__"] = history
        state["__graph_steps__"] = steps
        return state

    def save_state(self, state: Dict[str, Any], path: Union[str, Path]) -> None:
        """Save graph state to a JSON file."""
        path = Path(path)
        # Remove non-serializable items if any
        serializable = {k: v for k, v in state.items() if not callable(v)}
        path.write_text(json.dumps(serializable, indent=2, default=str))

    @staticmethod
    def load_state(path: Union[str, Path]) -> Dict[str, Any]:
        """Load previously saved state."""
        return json.loads(Path(path).read_text())

    def __repr__(self) -> str:
        return f"Graph(name={self.name!r}, nodes={list(self.nodes.keys())})"
