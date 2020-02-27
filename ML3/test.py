#%%
import pandas as pd
import numpy as np
from constraint import *

#%%
course_offerings = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
course_prereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')

# %%
problem = Problem()


def AvailabilityConstraint(row):

    #Add Constraints for foundation, core, elective, or capstone
    if row['type'] == 'Elective':
        problem.addConstraint(row['Course'], possible_semesters.tolist().append(0)) # include 0 represent not chosen
    
    else:
        problem.addConstraint(row['Course'], variables=possible_semesters.tolist())

       
    #Add constraints for prequisites
    #problem.addConstraint(lambda a, b: a < b,
                          #("a", "b"))


def PrereqConstraint(row):
    #Prereq comes before the course or course not taken if elective
    problem.addConstraint(lambda a, b: a < b | b == 0, (row['prereq'], row['course']))

course_offerings.apply(AvailabilityConstraint, axis=1)

course_prereqs.apply(PrereqConstraint, axis=1)

# %%
    foundation_courses = course_offerings[course_offerings.Type=='foundation']
    for r,row in foundation_courses.iterrows():
        problem.addVariable(row.Course, create_term_list(list(row[row==1].index)))
