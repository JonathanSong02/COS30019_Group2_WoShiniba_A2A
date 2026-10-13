COS30019 Introduction to AI - Assignment 2 Part A: Tree Based Search
Team: WoShiNiBa

=====================================================================
1. REQUIREMENTS
=====================================================================
- Windows 10/11
- Python 3.8 or newer (no external libraries needed)

Check Python is installed:
    python --version
If "python" is not recognised, try "py --version" instead.

=====================================================================
2. HOW TO RUN
=====================================================================
Open Command Prompt, go into the project folder, then run search.py:

    cd C:\path\to\COS30019_Group2_WoShiniba_A2A
    python search.py <filename> <method>

<filename>  path to a problem file, e.g. PathFinder-test.txt or tests\test01.txt
<method>    one of DFS, BFS, GBFS, AS, CUS1, CUS2 (not case-sensitive)

Examples:
    python search.py PathFinder-test.txt BFS
    python search.py tests\test01.txt BFS

Do NOT run the files inside algorithms\ directly. They only define a
search() function; search.py is the program that calls them.

=====================================================================
3. OUTPUT FORMAT
=====================================================================
When a destination is reached:

    filename method
    goal number_of_nodes
    path

Example:
    PathFinder-test.txt BFS
    4 10
    2 1 4

goal             the destination node that was reached
number_of_nodes  number of search-tree nodes created (including the root)
path             node ids from the origin to the goal

If no destination can be reached, the program prints:
    No goal is reachable; <number_of_nodes>

=====================================================================
4. PROJECT STRUCTURE
=====================================================================
search.py            Entry point. Reads the arguments, loads the problem
                     file, runs the chosen method and prints the result.
graph.py             Graph class and problem-file parser. Stores node
                     coordinates and directed edges, sorts neighbours in
                     ascending order, and provides the straight-line
                     distance heuristic (to the nearest destination).
node.py              Search-tree node: state, parent, path cost, depth.
                     Rebuilds the path and checks for cycles on the path.
algorithms\          One module per search method. Each exposes
                     search(graph) -> (goal_node or None, nodes_created).
    dfs.py           Depth-first search            (TODO)
    bfs.py           Breadth-first search          (done)
    gbfs.py          Greedy best-first search      (TODO)
    astar.py         A* search                     (TODO)
    cus1.py          Custom uninformed search      (TODO)
    cus2.py          Custom informed search        (TODO)
tests\               Test problem files (test01.txt ... test15.txt)
PathFinder-test.txt  Sample problem from the assignment specification

=====================================================================
5. PROBLEM FILE FORMAT
=====================================================================
Nodes:
1: (4,1)          node 1 at x=4, y=1
Edges:
(2,1): 4          directed edge from node 2 to node 1, cost 4
Origin:
2
Destinations:
5; 4              destinations separated by semicolons

=====================================================================
6. IMPLEMENTATION CONVENTIONS (shared by all methods)
=====================================================================
- Tie-breaking: when all else is equal, smaller node ids are expanded
  first; otherwise nodes added to the frontier earlier are expanded first.
- Goal test is done when a node is removed from the frontier.
- number_of_nodes counts every node created, including the root.
- Tree search: a neighbour already on the current path is skipped, so the
  search cannot loop around cycles such as 1 -> 3 -> 1.

=====================================================================
7. KNOWN ISSUES / NOTES
=====================================================================
- Only BFS is implemented so far. Other methods print
  "Method X is not implemented yet."
