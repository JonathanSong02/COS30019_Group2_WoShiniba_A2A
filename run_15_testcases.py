"""COS30019 A2A: validate 15 test cases across implemented algorithms.

Place this file beside search.py and the testcases/ directory.
Run: python run_15_testcases.py
Results: A2A_15_Test_Results.csv

Checks: graph parses, path follows directed edges, end is a goal,
BFS minimum moves, A* minimum weighted cost, CUS2 minimum moves.
Not checked: assignment-specific equal-priority node expansion order.
This script is a testing aid, not a substitute for your final report.
"""

import csv
import heapq
from collections import deque
from pathlib import Path

import search
from graph import load_graph

ROOT = Path(__file__).resolve().parent
CASE_DIR = ROOT / "testcases"
METHODS = ("DFS", "BFS", "GBFS", "AS", "CUS1", "CUS2")


def shortest_cost(graph):
    queue = [(0, graph.origin)]
    best = {graph.origin: 0}
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != best[node]:
            continue
        if node in graph.destinations:
            return distance
        for neighbour, edge_cost in graph.neighbours(node):
            new_cost = distance + edge_cost
            if new_cost < best.get(neighbour, float("inf")):
                best[neighbour] = new_cost
                heapq.heappush(queue, (new_cost, neighbour))
    return None


def shortest_moves(graph):
    queue = deque([(graph.origin, 0)])
    seen = {graph.origin}
    while queue:
        node, moves = queue.popleft()
        if node in graph.destinations:
            return moves
        for neighbour, _ in graph.neighbours(node):
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append((neighbour, moves + 1))
    return None


def evaluate_path(graph, path):
    if not path or path[0] != graph.origin or path[-1] not in graph.destinations:
        raise ValueError("Path does not start at the origin and end at a goal")
    path_cost = 0
    for source, dest in zip(path, path[1:]):
        weights = [cost for neighbour, cost in graph.neighbours(source) if neighbour == dest]
        if not weights:
            raise ValueError(f"Illegal directed move: {source} -> {dest}")
        path_cost += weights[0]
    return path_cost


def main():
    cases = sorted(CASE_DIR.glob("test[0-9][0-9].txt"))
    if len(cases) != 15:
        print(f"ERROR: Expected 15 files, found {len(cases)} in {CASE_DIR}")
        return 1

    records = []
    for testcase in cases:
        graph = load_graph(str(testcase))
        best_cost = shortest_cost(graph)
        best_moves = shortest_moves(graph)
        for method in METHODS:
            row = {
                "test_case": testcase.name,
                "method": method,
                "status": "NOT IMPLEMENTED",
                "goal": "",
                "nodes_created": "",
                "path": "",
                "moves": "",
                "path_cost": "",
                "reference_min_moves": best_moves,
                "reference_min_cost": best_cost,
                "remarks": "",
            }
            runner = search.METHODS.get(method)
            if runner is not None:
                try:
                    goal, nodes_created = runner(graph)
                    if goal is None:
                        raise ValueError("No goal reached")
                    path = goal.path()
                    cost = evaluate_path(graph, path)
                    moves = len(path) - 1
                    if goal.state != path[-1]:
                        raise ValueError("Returned goal does not match path")
                    if nodes_created < len(path):
                        raise ValueError("Invalid number of created nodes")
                    if method in ("BFS", "CUS2") and moves != best_moves:
                        raise ValueError("Did not find the minimum number of moves")
                    if method == "AS" and abs(cost - best_cost) > 1e-9:
                        raise ValueError("Did not find the minimum weighted cost")
                    row.update({
                        "status": "PASS",
                        "goal": goal.state,
                        "nodes_created": nodes_created,
                        "path": " -> ".join(map(str, path)),
                        "moves": moves,
                        "path_cost": cost,
                    })
                except Exception as exc:
                    row.update({"status": "FAIL", "remarks": str(exc)})
            records.append(row)
            print(f"{testcase.name:12s} {method:4s}: {row['status']}")

    dest = ROOT / "A2A_15_Test_Results.csv"
    with dest.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    passed = sum(r["status"] == "PASS" for r in records)
    missing = sum(r["status"] == "NOT IMPLEMENTED" for r in records)
    failed = sum(r["status"] == "FAIL" for r in records)
    print(f"\n15 unique cases; {passed} PASS, {missing} NOT IMPLEMENTED, {failed} FAIL")
    print(f"Saved to: {dest.name}")
    if missing:
        print("Integrate the missing CUS1/CUS2 methods, then rerun the tests.")
    print("IMPORTANT: Verify assignment tie-breaking separately with your tutor.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
