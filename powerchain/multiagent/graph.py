from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union

from powerchain.core.human import HumanInput


@dataclass
class Node:
    name: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]
    description: str = ""


@dataclass
class Edge:
    source: str
    target: str
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None


class Graph:
    """Powerful yet lightweight graph orchestration with human-in-the-loop support.

    Features:
    - Conditional edges & loops
    - Shared state
    - save/load state
    - Human approval nodes / interrupt before selected nodes
    """

    def __init__(self, name: str = "PowerGraph", verbose: bool = False):
        self.name = name
        self.verbose = verbose
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.entry_point: Optional[str] = None
        self._end_nodes: Set[str] = set()
        self._interrupt_before: Set[str] = set()  # nodes that require human approval
        self.human = HumanInput()

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
        self._end_nodes.add(name)
        return self

    def interrupt_before(self, *node_names: str) -> "Graph":
        """Require human approval before these nodes run."""
        for n in node_names:
            self._interrupt_before.add(n)
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

    def _human_approve(self, node_name: str, state: Dict[str, Any]) -> bool:
        self._log(f"\n[Human-in-the-loop] About to run node: '{node_name}'")
        if self.verbose:
            print("Current state keys:", list(state.keys()))
        return self.human.confirm(f"Approve running '{node_name}'?", default=True)

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

            # Human-in-the-loop check
            if current in self._interrupt_before:
                approved = self._human_approve(current, state)
                if not approved:
                    self._log(f"  ✗ Human rejected node '{current}'. Stopping.")
                    state["__human_rejected__"] = current
                    break

            history.append(current)
            node = self.nodes[current]
            self._log(f"  → Executing node: {current}")

            result = node.func(state)
            if isinstance(result, dict):
                state.update(result)

            if current in self._end_nodes:
                self._log(f"  ✓ Reached finish point: {current}")
                break

            next_nodes = self._get_next_nodes(current, state)

            if not next_nodes:
                self._log(f"  ✓ No outgoing edges — stopping at '{current}'")
                break

            current = next_nodes[0]
            steps += 1

        if steps >= max_steps:
            self._log(f"  ! Max steps ({max_steps}) reached")

        state["__graph_history__"] = history
        state["__graph_steps__"] = steps
        return state

    def save_state(self, state: Dict[str, Any], path: Union[str, Path]) -> None:
        path = Path(path)
        serializable = {k: v for k, v in state.items() if not callable(v)}
        path.write_text(json.dumps(serializable, indent=2, default=str))

    @staticmethod
    def load_state(path: Union[str, Path]) -> Dict[str, Any]:
        return json.loads(Path(path).read_text())

    def __repr__(self) -> str:
        return f"Graph(name={self.name!r}, nodes={list(self.nodes.keys())})"
