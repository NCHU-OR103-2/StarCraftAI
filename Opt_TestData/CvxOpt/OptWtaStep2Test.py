from __future__ import division

import pickle
import time
import numpy as np
import cvxpy as cvx
#from FuncDesigner import *
#from openopt import MILP

#opt_data = open('opt_data.pkl','r')
#damage_table = pickle.load(opt_data)
#hitpoints_table = pickle.load(opt_data)
#maxhitpoints_table = pickle.load(opt_data)
#injury_table = pickle.load(opt_data)
#max_injury_table = pickle.load(opt_data)
#opt_data.close()

opt_wta_step_2_data = open('opt_wta_step_2_data.pkl')
type_assign_table = pickle.load(opt_wta_step_2_data)
type_record_table = pickle.load(opt_wta_step_2_data) 
distance_table = pickle.load(opt_wta_step_2_data)
opt_wta_step_2_data.close()

m, n = len(distance_table), len(distance_table[0])
X = cvx.Bool(m, n)

obj_func = 0
for i in range(m):
    for j in range(n):
        obj_func += distance_table[i][j] * X[i, j]
obj_func = cvx.Minimize(obj_func)
    
unit_types = type_assign_table.keys()
cons = []
for i in range(m):
    tmp_cons = 0
    for j in range(n):
        tmp_cons = tmp_cons + X[i, j]
    cons.append(tmp_cons <= 1)

for unit_type in unit_types:
    units_index, target_assign_list = type_record_table[unit_type], type_assign_table[unit_type]
    for j in range(n):
        tmp_cons = 0
        for index in units_index:
            tmp_cons += X[index, j]    
        cons.append(tmp_cons == target_assign_list[j])

prob = cvx.Problem(obj_func, cons)
prob.solve()

wta_result_2 = []
zero_list = []
for i in range(n):
    zero_list.append(0)
for i in range(m):
    wta_result_2.append(list(zero_list))
    for j in range(n):
        if X[i, j].value > 0.1:
            wta_result_2[i][j] = 1
            break
