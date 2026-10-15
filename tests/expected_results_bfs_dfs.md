# Expected results: BFS and DFS (test03 to test07)

Conventions: the root counts as a created node, the goal test happens when a
node is popped from the frontier, and a neighbour already on the current path
is skipped.

| Test   | Checks                               | BFS (goal, nodes, path) | DFS (goal, nodes, path)  |
|--------|--------------------------------------|-------------------------|--------------------------|
| test03 | Basic chain, one destination         | 4, 4, `1 2 3 4`         | 4, 4, `1 2 3 4`          |
| test04 | Two-way cycles (cycle check)         | 5, 9, `1 3 4 5` (cost 8) | 5, 6, `1 2 3 4 5` (cost 12) |
| test05 | Tie broken by smaller node id        | 2, 3, `1 2`             | 2, 3, `1 2`              |
| test06 | Tie broken by insertion order        | 5, 5, `1 2 5`           | 5, 4, `1 2 5`            |
| test07 | BFS and DFS reach different goals    | 3, 4, `1 3`             | 5, 5, `1 2 4 5`          |

Sample file (`PathFinder-test.txt` / `test01.txt`): BFS `4 10`, path `2 1 4`;
DFS `5 7`, path `2 1 3 5`.

## Notes per test

**test03: basic chain.** 1 -> 2 -> 3 -> 4 with no branching, so every method
must return the same path and create exactly 4 nodes.

**test04: cycles.** Every edge goes both ways (1-2, 1-3, 2-3, 3-4, 4-5).
Without the on-path check, DFS would loop 1 -> 2 -> 1 -> 2 ... forever.
DFS goes deep through 2 first and returns `1 2 3 4 5` (4 moves, cost 12).
BFS returns the fewest-moves path `1 3 4 5` (3 moves, cost 8).

DFS trace (stack top on the right):

| Pop       | Children added | Nodes created |
|-----------|----------------|---------------|
| (root 1)  |                | 1             |
| 1         | 2, 3           | 3             |
| 1-2       | 3              | 4             |
| 1-2-3     | 4              | 5             |
| 1-2-3-4   | 5              | 6             |
| 1-2-3-4-5 | goal           | 6             |

**test05: smaller id first.** Node 1 has equal-cost edges to destinations 2
and 3. The file lists `(1,3)` before `(1,2)` on purpose. graph.py sorts the
neighbours, so 2 is expanded first and both methods return goal 2.

**test06: earlier-added first.** 1 -> 2 -> 5 and 1 -> 3 -> 4, destinations 4
and 5, both at depth 2. In BFS, node 5 (child of 2) is added to the queue
before node 4 (child of 3), so 5 is popped first even though 4 has the
smaller id. This is the "chronological order across branches" rule from
Note 2. A method that ranks by node id before insertion order returns goal 4
here (the current A* does, see Known issues in README.txt).

**test07: different goals.** Destination 3 is one move from the origin;
destination 5 is three moves away down the 2 branch. BFS finds 3 first. DFS
commits to the smaller neighbour 2 and follows it to 5 before it ever looks
at 3. This shows that DFS is not optimal in moves or in cost.
