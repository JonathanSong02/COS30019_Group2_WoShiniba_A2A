"""Run Jonathan's five COS30019 A2A cases with BFS, GBFS and A*.

Place this file in your project's tests/ folder. From the project root run:
    python tests/run_jonathan_tests.py

Requires no external libraries. Also produces jonathan_test_results.csv.
"""
import csv
import heapq
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from graph import load_graph  # noqa: E402

TEST_FILES = (
    "test02_direct_route.txt",
    "test03_misleading_heuristic.txt",
    "test04_cycles_deadends.txt",
    "test05_multiple_goals.txt",
    "test06_ties_duplicate_states.txt",
)
METHODS = ("BFS", "GBFS", "AS")


def lowest_cost(graph):
    """Independent Dijkstra reference for minimum edge-cost solution."""
    queue = [(0, graph.origin)]
    best = {graph.origin: 0}
    while queue:
        cost, node = heapq.heappop(queue)
        if cost != best[node]:
            continue
        if node in graph.destinations:
            return cost
        for neighbor, weight in graph.neighbours(node):
            candidate = cost + weight
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                heapq.heappush(queue, (candidate, neighbor))
    return None


def min_moves(graph):
    """Independent BFS reference for minimum number of edges."""
    from collections import deque
    queue = deque([(graph.origin, 0)])
    visited = {graph.origin}
    while queue:
        node, steps = queue.popleft()
        if node in graph.destinations:
            return steps
        for neighbor, _ in graph.neighbours(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, steps + 1))
    return None


def check_path(graph, path):
    """Check a returned route follows directed edges; calculate its cost."""
    if not path or path[0] != graph.origin or path[-1] not in graph.destinations:
        raise ValueError("Path does not start at origin or end at a destination")
    cost = 0
    for source, dest in zip(path, path[1:]):
        possible = [weight for node, weight in graph.neighbours(source) if node == dest]
        if not possible:
            raise ValueError(f"Path uses missing directed edge {source} -> {dest}")
        cost += possible[0]
    return cost


def main():
    results = []
    for filename in TEST_FILES:
        relpath = str(Path("tests") / filename)
        graph = load_graph(str(ROOT / relpath))
        reference_cost = lowest_cost(graph)
        reference_moves = min_moves(graph)
        print(f"\n{filename}: optimal cost={reference_cost}, minimum moves={reference_moves}")
        for method in METHODS:
            result = subprocess.run(
                [sys.executable, "search.py", relpath, method],
                cwd=ROOT, text=True, capture_output=True, check=False
            )
            row = {
                "Test case": filename, "Method": method,
                "Goal": "", "Nodes created": "", "Path": "",
                "Moves": "", "Path cost": "", "Optimal cost": reference_cost,
                "Minimum moves": reference_moves, "Result": "FAIL",
            }
            try:
                if result.returncode != 0:
                    raise ValueError(result.stdout.strip() or result.stderr.strip())
                lines = result.stdout.strip().splitlines()
                if len(lines) != 3:
                    raise ValueError("Expected three lines of output")
                goal_str, count_str = lines[1].split()
                path = [int(node) for node in lines[2].split()]
                cost = check_path(graph, path)
                goal = int(goal_str)
                if goal != path[-1]:
                    raise ValueError("Goal does not match path")
                count = int(count_str)
                if count < len(path):
                    raise ValueError("Nodes created is smaller than path length")
                if method == "BFS" and len(path) - 1 != reference_moves:
                    raise ValueError("BFS did not find the fewest moves")
                if method == "AS" and abs(cost - reference_cost) > 1e-9:
                    raise ValueError("A* did not find the lowest cost")
                if filename == "test06_ties_duplicate_states.txt" and path != [1, 2, 4, 5]:
                    raise ValueError("Unexpected tie-break path")
                row.update({"Goal": goal, "Nodes created": count,
                            "Path": " -> ".join(map(str, path)), "Moves": len(path)-1,
                            "Path cost": cost, "Result": "PASS"})
            except (ValueError, IndexError) as error:
                row["Result"] = f"FAIL: {error}"
            results.append(row)
            print(f"  {method:4s}: {row['Result']:6s} goal={row['Goal']} "
                  f"nodes={row['Nodes created']} path={row['Path']} cost={row['Path cost']}")

    outfile = ROOT / "jonathan_test_results.csv"
    with outfile.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    passed = sum(row["Result"] == "PASS" for row in results)
    print(f"\n{passed}/{len(results)} runs passed. Results saved to: {outfile.name}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
