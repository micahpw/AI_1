
"""
Created on Thu Jan  3 14:24:06 2019

@author: Micah Webb

This program implements A* for solving a sliding tile puzzle
"""

print('Artificial Intelligence')
print('MP1: A* for Sliding Puzzle')
print('SEMESTER: Spring 2020')
print('NAME: Micah Webb')
#%%
import numpy as np
import queue

difficulty = 3

I = np.fromfile('./mp1input.txt', sep=' ', dtype=int).reshape(difficulty,difficulty)


G = np.arange(0,difficulty*difficulty).reshape(difficulty, difficulty)

print(G)
#%%

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

        if row < difficulty-1:
            moves.append('D')
        if row > 0: 
            moves.append('U')
        if col < difficulty-1:
            moves.append('R')
        if col > 0: 
            moves.append('L')

        return moves

    def __hash__(self):
        return np.array_str(self.state)
        




def PrintSolution(InitialState, pathstring):
    puzzle = Edge(InitialState, pathstring)
    print("START")
    print(puzzle.state)
    map = {'U':'up','D':'down', 'L':'left', 'R': 'right'}
    for i in range(0, len(pathstring)):
        move = pathstring[i]
        state = puzzle.Expand(move)
        puzzle = Edge(state, pathstring)
        s = "Move {m} ACTION: {a}".format(m = i, a = map[move])
        print(s)
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
            PrintSolution(InitialState, "")        
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
                            new_distance = len(new_node.path)+ mdist + n*0.0000001 # added n * 0.001 for tiebreaking, defaults to FIFO for equal scores
                            n += 1
                            priority_queue.put((new_distance, new_node)) 
                            if n%10000 == 0:
                                print(new_distance, n, mdist)                        
                        else:                                       
                            PrintSolution(InitialState, new_node.path)
                            print("Number of States Visited = {s}".format(s = len(VisitedStates)))
                            return

            print("exiting solver")            

PuzzleSolver = Solver(G)

PuzzleSolver.Solve(I)        
    

    