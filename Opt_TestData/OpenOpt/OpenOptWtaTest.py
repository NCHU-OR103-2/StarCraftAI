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

startPoint = {}
x = oovars(m)	
for i in range(0, m):
    x[i] = oovar('x' + str(i+1), size = n, domain = bool)
    for j in range(0, n):
        x[i][j].name = 'x' + str(i+1) + str(j+1)
        startPoint[x[i][j]] = 0

tmp_func = hitpoints_table[0] - injury_table[0][0] * x[0][0]
for i in range(1, m):
    tmp_func  = tmp_func - injury_table[i][0] * x[i][0]
obj_func = damage_table[0] / (hitpoints_table[0] * maxhitpoints_table[0]) * tmp_func 
for j in range(1, n):
    tmp_func = hitpoints_table[j] - injury_table[0][j] * x[0][j]
    for i in range(1, m):
        tmp_func  = tmp_func - injury_table[i][j] * x[i][j]
    obj_func = obj_func + damage_table[j] / (hitpoints_table[j] * maxhitpoints_table[j]) * tmp_func

cons = []
for i in range(m):
    tmp_cons = x[i][0]
    for j in range(1, n):
        tmp_cons = tmp_cons + x[i][j]
    tmp_cons = tmp_cons <= 1
    cons.append(tmp_cons)
    
for j in range(n):
    tmp_cons = injury_table[0][j] * x[0][j]
    for i in range(1, m):
        tmp_cons  = tmp_cons + injury_table[i][j] * x[i][j]
    tmp_cons = tmp_cons <= hitpoints_table[j] + WASTE_DAMAGE_COEF * max_injury_table[j]
    cons.append(tmp_cons)

p = MILP(obj_func, startPoint, constraints=cons)

#r = p.minimize('lpSolve')
#r = p.minimize('glpk')

#print("--- %s seconds ---" % (time.time() - start_time))
