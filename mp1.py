#%%
import numpy as np
import queue

I = np.fromfile('./mp1input.txt', sep=' ', dtype=int).reshape(3,3)

G = np.array([[0,1,2],[3,4,5],[6,7,8]])


class Edge():
    def __init__(self,conf, pathstring):
        self.state = conf
        self.path = pathstring
        self.empty = np.argwhere(self.state == 0)[0]

    def Expand(self, move):  

        NewState = np.array(self.state)
        row, col = self.empty[0], self.empty[1]
        if move == 'L':
            NewState[row][col] = NewState[row][col-1]
            NewState[row][col-1] = 0
        if move == 'R':
            NewState[row][col] = NewState[row][col+1]    
            NewState[row][col+1] = 0
        if move == 'U':
            NewState[row][col] = NewState[row-1][col]
            NewState[row-1][col] = 0
        if move == 'D':
            NewState[row][col] = NewState[row+1][col]    
            NewState[row+1][col] = 0
        
        return NewState
    


    def DetermineMoves(self):
        moves = []
        row, col = self.empty[0], self.empty[1]

        if row < 2:
            moves.append('D')
        if row > 0: 
            moves.append('U')
        if col < 2:
            moves.append('R')
        if col > 0: 
            moves.append('L')

        return moves

    def __hash__(self):
        return np.array_str(self.state)
        




def PrintTransformations(InitialState, pathstring):
    puzzle = Edge(InitialState, pathstring)
    print(puzzle.state)
    for i in range(0, len(pathstring)):
        move = pathstring[i]
        state = puzzle.Expand(move)
        puzzle = Edge(state, pathstring)

        print(puzzle.state)
        


class Solver():
    def __init__(self, Goal):
        self.GoalState = Goal              

    def g(self, TestState):
        distance = 0
        #Loop through each number and compare locations between goal and state
        for i in range (1, self.GoalState.size): 
            goalloc = np.argwhere(self.GoalState == i)
            stateloc = np.argwhere(TestState == i)
        
            distance += np.absolute(np.subtract(stateloc,goalloc)).sum() #calculate distance
       
        return distance
    
    def Solve(self, InitialState):        
        priority_queue = queue.PriorityQueue()

        root = Edge(InitialState, "")

        VisitedStates = set([root.__hash__()])

        dist = self.g(InitialState)
        if dist == 0:
            print("initialized state matches goal state, problem solved!")
            PrintTransformations(InitialState, "")        
            return
        else:        

            priority_queue.put((dist, root))
    

            n = 0 # number of iterations to use for tiebreaking
            while priority_queue.empty() == False:
                next_node = priority_queue.get()[1]

                moves = next_node.DetermineMoves()
                for move in moves:
                    new_state = next_node.Expand(move)

                    new_node = Edge(new_state, next_node.path+move)
                    hash = new_node.__hash__()

                    if hash not in VisitedStates:
                        VisitedStates.add(hash)
                        mdist = self.g(new_node.state)
                        if mdist > 0:
                            new_distance = len(new_node.path)/2 + mdist + n*0.0000001 # added n * 0.001 for tiebreaking, defaults to FIFO for equal scores
                            n += 1
                            priority_queue.put((new_distance, new_node)) 
                            print(new_distance)
                        else:                    
                            print('problem solved')                    
                            PrintTransformations(InitialState, new_node.path)
                            return



PuzzleSolver = Solver(G)

PuzzleSolver.Solve(I)        
    

    