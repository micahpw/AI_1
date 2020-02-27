#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/26/2020

@author: mwebb

Program checks if there are possible schedules for students for a given
start and finish term, given all constraints.
This works by mapping a term number to each course, given all constraints.
It assigns a negative term number if course is not taken (e.g. elective that is not needed)

ASSUMPTION: term numbers start with 1
"""
import pandas as pd
import numpy as np
from constraint import *

def create_term_list(terms, years=4):
    '''Create a list of term indexes for years in the future'''
    all_terms = []
    for year in range(years):
        for term in terms:    
            all_terms.append(year*6+term)
    return all_terms
    
def map_to_term_label(term_num):
    '''Returns the label of a term, given its number'''
    term_num_to_label_map = {
            0: 'Fall 1',
            1: 'Fall 2',
            2: 'Spring 1',
            3: 'Spring 2',
            4: 'Summer 1',
            5: 'Summer 2',
    }
    if (term_num < 1):
        return 'Not Taken'
    else:
        return 'Year ' + str((term_num - 1) // 6 + 1) + ' ' + term_num_to_label_map[(term_num - 1) % 6]

def prereq(a, b):
    '''Used for encoding prerequisite constraints, a is a prerequisite for b'''
    if a > 0 and b > 0: # Taking both prereq a and course b
        return a < b
    elif a > 0 and b < 0: # Taking prereq a, but not course b
        return True
    elif a < 0 and b > 0: #  Taking course b, but not prereq a
        return False
    else:
        return True # Not taking prereq a or course b



#Make  surre only 3 electives are taken
def numelectives(e1,e2,e3,e4,e5,e6,e7,e8):    
        elective_values = np.array([e1,e2,e3,e4,e5,e6,e7,e8])
        cnt = np.where(elective_values > 0)[0] #Count electives 

        if cnt.size == 3:
            return True
        else:
            return False



def get_possible_course_list(start, finish):
    '''Returns a possible course schedule, assuming student starts in start term
       finishes in finish term'''
    problem = Problem()
    
    # Read course_offerings file
    course_offerings = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
    course_prereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')

    # nonelective course terms/must take
    nonelective_courses = course_offerings[course_offerings.Type !='elective']
    for r,row in nonelective_courses.iterrows():        
        problem.addVariable(row.Course, create_term_list(list(row[row==1].index)))           
        problem.addConstraint(FunctionConstraint(lambda x: 1 <= x <=14) , [row.Course]) #Make sure course is taken before year 3 fall2 



    # Elective courses are optional, pass extra negative values as placeholders for not taking a class
    elective_courses = course_offerings[course_offerings.Type=='elective']
        
    for r,row in elective_courses.iterrows():  
        term_list = create_term_list(list(row[row==1].index)).copy()
        nullable_term_list = [-1,-2,-3,-4,-5] #include more negatives so the AllDifferentConstraint works
        nullable_term_list.extend(term_list)
        problem.addVariable(row.Course, nullable_term_list) 
        problem.addConstraint(FunctionConstraint(lambda x:  x <=14), [row.Course]) #Make sure courses are taken before year3 fall2 or not taken

    

    #Control total electives - exactly 3 courses must be chosen
    #Pass all elective values to function to count up positive values (courses taken)
    electives = elective_courses.Course.values.tolist() 
    problem.addConstraint(FunctionConstraint(numelectives), variables = electives )
    

    #Prereqs
    for r, row in course_prereqs.iterrows():
        problem.addConstraint(FunctionConstraint(prereq), [row['prereq'], row['course']])

    
    #All Different implies no two courses are taken in the same semester. 
    #By Default a variable (e.g. class #) won't take on two values at once as in taking the course twice
    problem.addConstraint(AllDifferentConstraint())
    
    # Control start and finish terms    
    problem.addConstraint(SomeInSetConstraint([1,14])) #Make sure first and last semester are always part of solution
    
    
    
    # Generate a possible solution
    sol = problem.getSolutions()
    print(len(sol))
    s = pd.Series(sol[0])
    return s.sort_values().map(map_to_term_label)

# Print heading
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Micah Webb")

# Check for possible schedules for all start terms
for start in [1]:
    print('START TERM = ' + map_to_term_label(start))
    s = get_possible_course_list(start,start+13)
    if s.empty:
        print('NO POSSIBLE SCHEDULE!')
    else:
        s2 = pd.Series(s.index.values, index=s)
        print(s2.to_string())
    print()

