# Hexagon-Game

The hexagon game involves two players, who gradually construct a six-vertex undirected graph with solid and dashed edges. Player 1 adds solid edges, whereas Player 2 uses dashes. The players begin with a six-vertex graph that has no edges, and add new edges, one by one; Player 1 makes the first move. At each move, a player has to add a new edge between two vertices that are not connected by any old edge. If Player 1 constructs a solid-line triangle, he loses the game; similarly, a dashed triangle means a loss of Player 2. This implementation uses the Minimax Algorithm to simulate the AI opponent.

To be able to compile this code you must make sure that you are using python 3.11.

After making sure that the above conditions are completed you can go into the command line and type python3 HexagonGame.py and it will show you the initial graph state.

Now you can choose to be either player 1 or player 2. Once your decision is made you can then pick your starting vertex and destination vertex once it is your turn.

You will continue to play until you or the computer AI loses.
