import random

MAX_DEPTH = 3

#The Edge class to represent an edge in the graph
class Edge:
    def __init__(self, startPoint, destination, style):
        self.startPoint = startPoint
        self.destination = destination
        self.style = style
    
    def getStartPoint(self):
        return self.startPoint

    def getDestination(self):
        return self.destination

    def getStyle(self):
        return self.style

#The Graph class to represent the game board
class Graph:
    def __init__(self):
        #Define the vertices of the graph
        self.vertices = [1, 2, 3, 4, 5, 6]
        #Initialize an empty dictionary to represent the edges of the graph
        self.edges = {}
    
    #Add a new edge to the graph
    def addEdge(self, start, des, style):
        #Check if the edge already exists
        if(start, des) in self.edges or (des, start) in self.edges:
            return False

        #Create a new Edge object and add it to the dictionary of edges
        e = Edge(start, des, style)
        self.edges[(start, des)] = e

        return True
    
    #Remove and edge from the graph
    def removeEdge(self, start, des):
        if (start, des) in self.edges:
            del self.edges[(start, des)]
        elif (des, start) in self.edges:
            del self.edges[(des, start)]
#The HexagonGame class which represents all the functions of the game
class HexagonGame:
    def __init__(self):
        self.graph = Graph()

    #The main game loop
    def game(self):
        gameOver = False
        player = int(input("Enter a player number (1 or 2): "))
        computerAI = 0
        playerLost = 0

        #Set the computer player based on the human player selection
        if player == 1:
            computerAI = 2
        else:
            computerAI = 1

        print("\nCurrent Board (0 = No line still, S = solid line, D = Dashed Line)\n")
        self.printGame()  

        while not gameOver:
            gameOverFlag = False
            #If the Human Player is player 1 get their move and check if triangle is formed
            if player == 1:
                if not gameOverFlag:
                    self.playerMove(player)
                    self.printGame()
                    playerLost = self.triangleFormed()
                    if playerLost > 0:
                        gameOverFlag = True
                if not gameOverFlag:
                    self.computerMove(computerAI)
                    self.printGame()
                    playerLost = self.triangleFormed()
                    if playerLost > 0:
                        gameOverFlag = True
            #If the Computer Player is player 1 get their move and check if triangle is formed
            else:
                if not gameOverFlag:
                    self.computerMove(computerAI)
                    self.printGame()
                    playerLost = self.triangleFormed()
                    if playerLost > 0:
                        gameOverFlag = True
                if not gameOverFlag:
                    self.playerMove(player)
                    self.printGame()
                    playerLost = self.triangleFormed()
                    if playerLost > 0:
                        gameOverFlag = True
            gameOver = gameOverFlag

        #Prints the correct message for the player who lost
        if playerLost == 1:
            print("Player 1 Loses!\n")
        else:
            print("Player 2 Loses!\n")

        print("\nFinal Game Board!!")
        self.printGame()
    
    #This function performs the moves of the human player
    def playerMove(self, player):
        valid = False

        #Prompt the player for the starting and ending vertices and then add an edge to the graph
        while not valid:
            try:
                start = int(input("Enter a starting vertex: "))
                des = int(input("Enter a destination vertex: "))
            except ValueError:
                print("Please enter a valid vertex")
                continue

            style = ""

            #Set the style based on which player the human player is
            if player == 1:
                style = 'Solid'
            else:
                style = 'Dashed'

            #Check if the edge already exists and add it to the graph if it doesn't
            if start == des:
                print("Can't add an Edge between the same vertices")
            elif start not in self.graph.vertices or des not in self.graph.vertices or not start or not des:
                print("Please enter a valid vertex")
            elif (start, des) not in self.graph.edges and (des, start) not in self.graph.edges:
                self.graph.addEdge(start, des, style)
                valid = True
            else:
                print("An Edge already exists for those two points")
    
    #This function performs the moves for the Computer Player using minimax
    def computerMove(self, computerAI):
        bestScore = -1000
        bestMove = 0
        style = ""
        edgeCSuccessful = False

        #Determine the style of the computerAI edges
        if computerAI == 1:
            style = 'Solid'
        else:
            style = 'Dashed'

        #Loop through all possible moves to find the best move
        for move in self.generateMoves():
           edgeCSuccessful = self.graph.addEdge(move[0], move[1], style)
           #If the edge was successfully added, calculate the score using the minimax algorithm
           if edgeCSuccessful:
               score = self.minimax(1, False, style)
               #Remove the edge from the graph
               self.graph.removeEdge(move[0], move[1])
               if score > bestScore:
                   bestScore = score
                   bestMove = move

        #Add the best move to the graph
        self.graph.addEdge(bestMove[0], bestMove[1], style)
        print(f"Computer AI placed edge from vertex {bestMove[0]} to {bestMove[1]}")
        return
    
    #Uses the minimax algorithm to dertemine the best possible move for the ComputerAI
    def minimax(self, depth, isMaximizing, lineType):
        #Check if a triangle has been formed
        result = self.triangleFormed()
        
        #If a triangle has been formed by the current player return a score of 1
        if result == 1:
            return 1
        #If a triangle has been formed by the other player return a score of -1
        elif result == 2:
            return -1
        #If there are no more moves available return a score of 0
        elif len(self.generateMoves()) == 0:
            return 0
        #If the maximum depth has been reached evaluate the board and return the score
        elif depth == MAX_DEPTH:
            return self.evaluate()
        
        #If the current player is maximizing find the best move by evaluating all possible moves
        if isMaximizing:
            bestScore = -800

            for move in self.generateMoves():
                edgeCSuccessful = self.graph.addEdge(move[0], move[1], lineType)
                if edgeCSuccessful:
                    score = self.minimax(depth + 1, False, lineType)
                    self.graph.removeEdge(move[0], move[1])
                    if score > bestScore:
                        bestScore = score
            return bestScore
        #If the current player is minimizing find the best move by evaluating all possible moves
        else:
            bestScore = 800
            
            for move in self.generateMoves():
                edgeCSuccessful = self.graph.addEdge(move[0], move[1], lineType)
                if edgeCSuccessful:
                    score = self.minimax(depth + 1, True, lineType)
                    self.graph.removeEdge(move[0], move[1])
                    if score < bestScore:
                        bestScore = score
            return bestScore

    #This function generates all the current possible moves for the Computer AI to use to determine the best move
    def generateMoves(self):
        moves = []
        
        #Loop through all pairs of vertices in the graph
        for v1 in self.graph.vertices:
            for v2 in self.graph.vertices:
                if v1 < v2 and (v1, v2) not in self.graph.edges:
                    moves.append((v1, v2))
        return moves

    #Evaluates the game state and returns a score based on that
    def evaluate(self):
        triangle = self.triangleFormed()

        if triangle == 1:
            return -1000
        elif triangle == 2:
            return 1000
        elif len(self.generateMoves()) == 0:
            return 0
        else:
            return random.randint(-10, 10)


    #Checks for the formation of a triangle and checks if the same style
    def triangleFormed(self):
        if len(self.graph.edges) < 3:
            return 0

        for v1, v2 in self.graph.edges:
            for v3 in self.graph.vertices:
                if v3 != v1 and v3 != v2:
                    if ((v1, v2) in self.graph.edges and (v1, v3) in self.graph.edges and (v2, v3) in self.graph.edges):
                        edgeStyle1 = self.graph.edges[(v1, v2)].getStyle()
                        edgeStyle2 = self.graph.edges[(v1, v3)].getStyle()
                        edgeStyle3 = self.graph.edges[(v2, v3)].getStyle()
                        if edgeStyle1 ==  edgeStyle2 == edgeStyle3 and edgeStyle1 == 'Solid':
                            return 1
                        elif edgeStyle1 == edgeStyle2 == edgeStyle3 and edgeStyle1 == 'Dashed':
                            return 2
        return 0
    
    #Prints the current graph state
    def printGame(self):
        print(" " * 5, end = "")
        for v1 in self.graph.vertices:
            print("  " + str(v1) + "  ", end =" ")
        print("\n")
        for v1 in self.graph.vertices:
            print("  " + str(v1) + "  ", end="")
            value = "| 0 | "
            for v2 in self.graph.vertices:
                if (v1, v2) in self.graph.edges:
                    edge = self.graph.edges[(v1, v2)]
                    if edge.style == 'Solid':
                        value = "| S | "
                    else:
                        value = "| D | "
                print(value, end="")
                value = "| 0 | "
            print("\n")

def main():
    hex = HexagonGame()
    hex.game()

if __name__ == "__main__":
    main()