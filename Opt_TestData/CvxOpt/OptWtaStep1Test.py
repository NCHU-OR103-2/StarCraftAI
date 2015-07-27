import pickle
import time
import numpy as np
import cvxpy as cvx
from FuncDesigner import *
from openopt import MILP

opt_data = open('opt_data.pkl','r')
damage_table = pickle.load(opt_data)
hitpoints_table = pickle.load(opt_data)
maxhitpoints_table = pickle.load(opt_data)
injury_table = pickle.load(opt_data)
max_injury_table = pickle.load(opt_data)
opt_data.close()

WASTE_DAMAGE_COEF = 1.2

start_time = time.time()

m, n = len(injury_table), len(damage_table)
X = cvx.Bool(m, n)

### Build objective function
# Part 1: damage concept
tmp_func = hitpoints_table[0] - injury_table[0][0] * X[0, 0]
for i in range(1, m):
    #if injury_table[i][0] == 0:
    #    continue
    tmp_func  = tmp_func - injury_table[i][0] * X[i, 0]
obj_func = damage_table[0] / (hitpoints_table[0] * maxhitpoints_table[0]) * tmp_func 
for j in range(1, n):
    tmp_func = hitpoints_table[j] - injury_table[0][j] * X[0, j]
    for i in range(1, m):
        #if injury_table[i][0] == 0:
        #    continue
        tmp_func  = tmp_func - injury_table[i][j] * X[i, j]
    obj_func = obj_func + damage_table[j] / (hitpoints_table[j] * maxhitpoints_table[j]) * tmp_func

obj_func = cvx.Minimize(obj_func)
    
### Build constraints
cons = []
for i in range(m):
    tmp_cons = X[i, 0]
    for j in range(1, n):
        tmp_cons = tmp_cons + X[i, j]
    tmp_cons = tmp_cons <= 1
    cons.append(tmp_cons)
    
for j in range(n):
    tmp_cons = injury_table[0][j] * X[0, j]
    for i in range(1, m):
        tmp_cons  = tmp_cons + injury_table[i][j] * X[i, j]
    tmp_cons = tmp_cons <= hitpoints_table[j] + WASTE_DAMAGE_COEF * max_injury_table[j]
    cons.append(tmp_cons)

#for i in range(m):
#    for j in range(n):
#        if injury_table[i][j] == 0:
#            cons.append(X[i, j] == 0)

print("Step: 1 --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
### Start compute
prob = cvx.Problem(obj_func, cons)
prob.solve()

print("Step: 2 --- %s seconds ---" % (time.time() - start_time))
start_time = time.time()

result_table = []
for i in range(m):
    tmp_result_table = []
    for j in range(n):
        if X[i, j].value > 0.1:
            tmp_result_table.append(1)
        else:
            tmp_result_table.append(0)
    result_table.append(tmp_result_table)

real_result_table = []
for i in range(m):
    tmp_result_table = []
    for j in range(n):
        tmp_result_table.append(X[i, j].value)
    real_result_table.append(tmp_result_table)

print("Step: 3 --- %s seconds ---" % (time.time() - start_time))

print(result_table)