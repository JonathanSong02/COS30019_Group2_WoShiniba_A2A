"""
search.py
Entry point. Usage:
    python search.py <filename> <method>
where <method> is one of DFS, BFS, GBFS, AS, CUS1, CUS2.
"""

import sys

from graph import load_graph

from algorithms import bfs, gbfs, astar

METHODS = {
    "BFS": bfs.search,
    "GBFS": gbfs.search,
    "AS": astar.search,
}


ALL_METHODS = ("DFS", "BFS", "GBFS", "AS", "CUS1", "CUS2")


def main(argv):
    if len(argv) != 3:
        print("Usage: python search.py <filename> <method>")
        print("Methods: " + ", ".join(ALL_METHODS))
        return 1

    filename, method = argv[1], argv[2].upper()

    if method not in ALL_METHODS:
        print(f"Unknown method '{argv[2]}'. Choose from: " + ", ".join(ALL_METHODS))
        return 1
    if method not in METHODS:
        print(f"Method {method} is not implemented yet.")
        return 1

    try:
        graph = load_graph(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return 1
    except ValueError as error:
        print(f"Invalid problem file: {error}")
        return 1

    goal_node, nodes_created = METHODS[method](graph)

    print(f"{filename} {method}")
    if goal_node is None:
        print(f"No goal is reachable; {nodes_created}")
    else:
        print(f"{goal_node.state} {nodes_created}")
        print(" ".join(str(state) for state in goal_node.path()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
