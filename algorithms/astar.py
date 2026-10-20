"""A* search for the COS30019 route-finding assignment.

Nodes are prioritised by f(n) = g(n) + h(n), where g is the total
edge cost from the origin and h estimates the minimum remaining cost.
"""

import heapq
from itertools import count

from node import Node


def _heuristic_scale(graph):
    """Make straight-line distance a safe cost lower bound.

    Each edge's cost must be at least scale times its geometric length.
    By the triangle inequality, this also makes the scaled Euclidean
    distance to the nearest goal admissible and consistent.
    """
    scale = 1.0
    for source, neighbours in graph.edges.items():
        for destination, cost in neighbours:
            distance = graph.distance(source, destination)
            if distance > 0:
                scale = min(scale, cost / distance)
    return scale


def search(graph):
    """Return (goal_node, nodes_created), or (None, nodes_created)."""
    root = Node(graph.origin)
    nodes_created = 1
    creation_order = count()
    scale = _heuristic_scale(graph)

    # Tie-break first by smaller state ID, then earlier creation order.
    # Each item: (f, state_id, creation_order, search_node).
    frontier = [
        (root.path_cost + scale * graph.heuristic(root.state),
         root.state, next(creation_order), root)
    ]

    while frontier:
        _, _, _, current = heapq.heappop(frontier)

        # The goal test occurs when the node is removed from the frontier.
        if current.state in graph.destinations:
            return current, nodes_created

        for neighbour, edge_cost in graph.neighbours(current.state):
            # Search-tree cycle checking (do not revisit nodes on this path).
            if current.on_path(neighbour):
                continue

            child = Node(
                neighbour,
                current,
                current.path_cost + edge_cost,
            )
            nodes_created += 1
            estimate = scale * graph.heuristic(child.state)
            priority = child.path_cost + estimate
            heapq.heappush(
                frontier,
                (priority, child.state, next(creation_order), child),
            )

    return None, nodes_created
