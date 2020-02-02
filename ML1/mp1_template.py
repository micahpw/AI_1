# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:24:06 2019

@author: Micah Webb

This program implements A* for solving a sliding tile puzzle
"""
import numpy as np
import queue

class PuzzleState():
    SOLVED_PUZZLE = np.arange(9).reshape((3, 3))

    def __init__(self,conf,g,predState):
        self.puzzle = conf     # Configuration of the state
        self.gcost = g         # Path cost
        self._compute_heuristic_cost()  # Set heuristic cost
        self.fcost = self.gcost + self.hcost
        self.pred = predState  # Predecesor state
        self.zeroloc = np.argwhere(self.puzzle == 0)[0]
        self.action_from_pred = None
    
    def __hash__(self):
        return tuple(self.puzzle.ravel()).__hash__()
    
    def _compute_heuristic_cost(self):
        """ TODO """
    
    def is_goal(self):
        return np.array_equal(PuzzleState.SOLVED_PUZZLE,self.puzzle)
    
    def __eq__(self, other):
        return np.array_equal(self.puzzle, other.puzzle)
    
    def __lt__(self, other):
        return self.fcost < other.fcost
    
    def __str__(self):
        return np.str(self.puzzle)
    
    move = 0
    
    def show_path(self):
        if self.pred is not None:
            self.pred.show_path()
        
        if PuzzleState.move==0:
            print('START')
        else:
            print('Move',PuzzleState.move, 'ACTION:', self.action_from_pred)
        PuzzleState.move = PuzzleState.move + 1
        print(self)
    
    def can_move(self, direction):
        """ TODO """
        
    def gen_next_state(self, direction):
        """ TODO """
            

print('Artificial Intelligence')
print('MP1: A* for Sliding Puzzle')
print('SEMESTER: Spring 2020')
print('NAME: Micah Webb')
print()