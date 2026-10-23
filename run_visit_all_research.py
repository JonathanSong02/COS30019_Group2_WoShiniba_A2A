"""Validate optional research extension against INDEPENDENT Bellman-Ford baseline.

Runs the 15 required tests plus seven extra research-specific test files.
Writes visit_all_research_results.csv for reproducible report evidence.
"""
import csv
from pathlib import Path
from graph import load_graph
from visit_all import solve_visit_all


def reference_cost(graph):
    """Exact Bellman-Ford over expanded states; independent of the Dijkstra solver."""
    goals = sorted(graph.destinations)
    bits = {node: 1 << i for i, node in enumerate(goals)}
    full = (1 << len(goals)) - 1
    masks = range(full + 1)
    states = [(v, m) for v in graph.coords for m in masks]
    dist = {s: float('inf') for s in states}
    dist[(graph.origin, bits.get(graph.origin, 0))] = 0
    for _ in range(len(states) - 1):
        changed = False
        for v, m in states:
            d = dist[(v,m)]
            if d == float('inf'): continue
            for neighbour, weight in graph.neighbours(v):
                target = (neighbour, m | bits.get(neighbour, 0))
                if d + weight < dist[target]:
                    dist[target] = d + weight
                    changed = True
        if not changed: break
    result = min(dist[(v, full)] for v in graph.coords)
    return None if result == float('inf') else result


def check_path(graph, path, cost):
    if path is None:
        return cost is None
    if path[0] != graph.origin or not graph.destinations.issubset(set(path)):
        return False
    accumulated = 0
    for u, v in zip(path, path[1:]):
        options = [w for child, w in graph.neighbours(u) if child == v]
        if not options: return False
        accumulated += min(options)
    return accumulated == cost


def main():
    root = Path(__file__).parent
    files = sorted((root / 'testcases').glob('*.txt')) + sorted((root / 'research_cases').glob('*.txt'))
    records = []
    for file in files:
        graph = load_graph(str(file))
        path, cost, generated, expanded = solve_visit_all(graph)
        baseline = reference_cost(graph)
        passed = (cost == baseline and check_path(graph, path, cost))
        records.append({'file':file.name, 'origin':graph.origin,
                        'destinations':';'.join(map(str,sorted(graph.destinations))),
                        'goals_count':len(graph.destinations), 'reachable':'yes' if path is not None else 'no',
                        'minimum_cost':cost if cost is not None else 'N/A',
                        'moves':len(path)-1 if path is not None else 'N/A',
                        'path':' -> '.join(map(str,path)) if path is not None else 'NONE',
                        'queue_entries_created':generated, 'states_expanded':expanded,
                        'independent_bellman_ford_cost':baseline if baseline is not None else 'N/A',
                        'result':'PASS' if passed else 'FAIL'})
        print('{} {:47} cost={:<4} path={}'.format('PASS' if passed else 'FAIL', file.name, str(cost), records[-1]['path']))
    dest = root/'visit_all_research_results.csv'
    with dest.open('w',newline='',encoding='utf-8-sig') as f:
        out=csv.DictWriter(f,fieldnames=list(records[0]))
        out.writeheader(); out.writerows(records)
    passed = sum(1 for row in records if row['result']=='PASS')
    print('\n{}/{} cases PASS. Wrote {}'.format(passed,len(records),dest.name))
    return 0 if passed == len(records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
