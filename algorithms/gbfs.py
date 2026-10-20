
"""
GBFS - Greedy Best-First Search.

Selects the search node with the smallest estimated
straight-line distance to any destination.
"""

import heapq
from itertools import count
from node import Node


def search(graph):
    root = Node(graph.origin)
    nodes_created = 1

    # Track the order in which search nodes are created.
    order = count()

    # Priority: (heuristic, node ID, creation order, Node)
    frontier = [
        (graph.heuristic(root.state), root.state,
         next(order), root)
    ]

    while frontier:
        _, _, _, node = heapq.heappop(frontier)

        # Goal test when removing a node from frontier.
        if node.state in graph.destinations:
            return node, nodes_created

        for neighbour, cost in graph.neighbours(node.state):

            # Prevent cycles within the current path.
            if node.on_path(neighbour):
                continue

            child = Node(
                neighbour,
                node,
                node.path_cost + cost
            )
            nodes_created += 1

            heapq.heappush(
                frontier,
                (
                    graph.heuristic(child.state),
                    child.state,
                    next(order),
                    child
                )
            )

    return None, nodes_created
