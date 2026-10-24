COS30019 Introduction to AI - Assignment 2 Part A: Tree Based Search
Team: WoShiNiBa (Group 2)
Team Member: Jonathan Song Hua Jin, Darren Lee Kian Yee, Anson Hoo Zhi Xian
---------------------------------------------------------------------
1. REQUIREMENTS
---------------------------------------------------------------------
- Windows 10/11
- Python 3.8 or newer (standard library only, nothing to install)

Check Python is installed:
    python --version
If "python" is not recognised, try "py --version" instead.

---------------------------------------------------------------------
2. HOW TO RUN
---------------------------------------------------------------------
Open Command Prompt and go into the project folder:

    cd C:\path\to\COS30019_Group2_WoShiniba_A2A

Then use either form:

    python search.py <filename> <method>
        or
    search <filename> <method>          (uses search.bat)

<filename>  path to a problem file
<method>    DFS, BFS, GBFS, AS, CUS1 or CUS2 (not case-sensitive)

Examples:
    python search.py PathFinder-test.txt BFS
    .\search.bat  testcases\test04_misleading_heuristic.txt GBFS

Do NOT run the files inside algorithms\ directly. They only define a search() function; search.py is the program that calls them.

---------------------------------------------------------------------
3. OUTPUT FORMAT
---------------------------------------------------------------------
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

If no destination can be reached:

    filename method
    No goal is reachable; <number_of_nodes>

---------------------------------------------------------------------
4. PROJECT STRUCTURE
---------------------------------------------------------------------
search.py              Entry point. Reads the arguments, loads the problem
                       file, runs the chosen method and prints the result.

search.bat             Wrapper so "search <filename> <method>" works.

graph.py               Graph class and problem-file parser. Stores node
                       coordinates and directed edges, sorts neighbours in
                       ascending order, and provides the straight-line
                       distance heuristic (to the nearest destination).

node.py                Search-tree node: state, parent, path cost, depth.
                       Rebuilds the path and checks for cycles on the path.

algorithms\            One module per method. Each exposes
                       search(graph) -> (goal_node or None, nodes_created).
    dfs.py             Depth-first search (uninformed)
    bfs.py             Breadth-first search (uninformed)
    gbfs.py            Greedy best-first search (informed)
    astar.py           A* search (informed)
    cus1.py            CUS1: iterative deepening DFS (uninformed)
    cus2.py            CUS2: IDA* minimising the number of moves (informed)

testcases\             The 15 test problems (see section 8)

run_15_testcases.py    Runs every method on every test case and checks
                       the results against the expected outputs.

A2A_15_Test_Results.csv  Results saved by run_15_testcases.py

PathFinder-test.txt    Sample problem from the assignment specification

visit_all.py           Optional research: cheapest route through ALL
                       destinations (see section 10)

run_visit_all_research.py  Checks visit_all.py against a Bellman-Ford
                       baseline; saves visit_all_research_results.csv

research_cases\        Extra problems for the research extension

visualize_app.py       Optional study aid: interactive map viewer to help us understand the algorithms better.
                       (desktop window, tkinter)

---------------------------------------------------------------------
5. PROBLEM FILE FORMAT
---------------------------------------------------------------------
Nodes:
1: (4,1)          node 1 at x=4, y=1
Edges:
(2,1): 4          directed edge from node 2 to node 1, cost 4
Origin:
2
Destinations:
5; 4              destinations separated by semicolons

Files saved with a UTF-8 byte-order mark (e.g. by Windows Notepad) are also accepted.

---------------------------------------------------------------------
6. IMPLEMENTATION CONVENTIONS (shared by all methods)
---------------------------------------------------------------------
- Goal test is done when a node is removed from the frontier.
- number_of_nodes counts every search-tree node created, including the
  root. CUS1 and CUS2 rebuild the tree on every iteration, so nodes
  created in every iteration are counted.
- Tree search: a neighbour already on the current path is skipped, so the
  search cannot loop around cycles such as 1 -> 3 -> 1.
- Tie-breaking (assignment NOTE 2):
    * Children of the same node are generated in ascending node-id order.
    * When two frontier nodes are otherwise equal (same depth for BFS,
      same h for GBFS, same f for A*), the node added to the frontier
      first is expanded first.
  GBFS and A* order their frontier by (priority, insertion order). The
  node id is not part of the key: ascending order among siblings already
  follows from children being created in ascending order.
- GBFS and A* use the straight-line distance to the nearest destination.
  A* scales it by min(1, smallest cost/length ratio over all edges) so
  the heuristic never overestimates, even if an edge costs less than its
  length. For the sample file the scale is 1 (plain distance).
- CUS2 uses h(n) = ceil(distance to nearest destination / longest edge
  length), a lower bound on the number of moves still needed.

---------------------------------------------------------------------
7. TESTING
---------------------------------------------------------------------
Run all 15 test cases with all 6 methods:

    python run_15_testcases.py

For each run the script checks the exact expected goal, number of nodes
and path, that the path only uses real directed edges, and that BFS,
CUS1 and CUS2 find the fewest moves and A* the lowest cost. It also
checks that a file with a UTF-8 byte-order mark loads. Results are saved
to A2A_15_Test_Results.csv.

---------------------------------------------------------------------
8. TEST CASES (testcases\)
---------------------------------------------------------------------
test01_assignment_sample            The example graph from the spec

test02_direct_vs_indirect_route     Direct edge vs a costlier detour

test03_unreachable_destination      No route to the goal; all methods
                                    must stop and report no goal

test04_misleading_heuristic         Node nearest the goal has a costly
                                    edge; GBFS takes it, A* does not

test05_bidirectional_cycles         Two-way edges everywhere (cycle check)

test06_cycles_dead_end              A cycle plus a dead-end branch

test07_equal_cost_goals_tie         Equal goals; smaller id wins

test08_fewest_moves_vs_lowest_cost  BFS/CUS1/CUS2 and A* reach different
                                    goals

test09_cross_branch_goal_tie        Equal-f goals on different branches;
                                    the earlier-added one wins

test10_diamond_converging_paths     Two routes to the same node

test11_shallow_vs_deep_goal         DFS goes deep, BFS finds shallow goal

test12_origin_is_destination        Zero-move solution

test13_one_way_edges                Directed (one-way) edges

test14_zero_heuristic_gapped_ids    All coordinates equal (h = 0) and
                                    non-consecutive node ids

test15_large_graph_multi_goal       9 nodes, 16 edges, two destinations

======================================================================
Additional specific research test cases (/research_cases)
======================================================================
research01_greedy_trap              Nearest goal (3) is a trap: visiting it
                                    first makes the rest cost 10+. Cheapest
                                    route takes the far goal first (cost 4)

research02_transit_goal             Goals 2 and 4 lie on the cheap route to
                                    goal 5, so they are collected on the way
                                    instead of taking the direct 1->5 edge
                                    (cost 20)

research03_must_revisit_hub         Star graph: each goal connects only to
                                    hub node 1, so the route must pass back
                                    through the hub (node revisits needed)

research04_zero_cost_and_ties       Every edge costs 0; checks zero-cost
                                    edges and ties between equal routes
                                    
research05_three_goal_ordering      Three goals where visit order matters;
                                    the direct links between goals (3->6,
                                    6->5) are expensive (best cost 8)
---------------------------------------------------------------------
9. KNOWN ISSUES
---------------------------------------------------------------------
- None known. All six methods pass all 15 test cases.

---------------------------------------------------------------------
10. OPTIONAL EXTRAS 
---------------------------------------------------------------------
Visit all destinations (research):

    python visit_all.py PathFinder-test.txt
    python run_visit_all_research.py

visit_all.py finds the cheapest route that passes through EVERY
destination (not every node). run_visit_all_research.py runs it on the
15 test cases plus the 5 files in research_cases\ and compares each
result with an independent Bellman-Ford solver.

Map viewer (study aid):

    python visualize_app.py                  all maps
    python visualize_app.py <file> [<file>]  only the selected files

Opens a window that draws each map on a grid, shows each method's goal,
nodes created, path and cost, and can step through the search tree in
the order nodes are created. Keys: Left/Right = back/next, Home/End =
first/last, Space = play/pause. The algorithms are not modified: their
Node class is swapped for a logging subclass only while the viewer runs
them.