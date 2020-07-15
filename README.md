# Futoshiki-Solver
Futoshiki-Solver


Program to solve futoshiki puzzles. 

Implemented using a backtracking algorithm. The heuristics used for the algorithm are the most constrained variable, followed by most constraining variable.

The input file format is a .txt file that is in the form of 3 boards. The first board is a 5x5 board with numbers meant to distinguish the starting state of the futoshiki puzzle. The second board is a 4x5 board with the horizontal of the board, and the final board is a 5x4 board with the vertical restrictions between panels.

If the futoshiki puzzle has a solution, the program will output a .txt file with a filled 5x5 board fulfilling all restrictions set by the initial board.
