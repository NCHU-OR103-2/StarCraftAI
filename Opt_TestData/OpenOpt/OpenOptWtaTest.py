from __future__ import division

import pickle
import time
import numpy as np
#import cvxpy as cvx

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

obj_func = []
var_map_table = []
for i in range(m):
    for j in range(n):
        if injury_table[i][j] != 0:
            obj_func.append(-damage_table[j] * injury_table[i][j] / hitpoints_table[j] / maxhitpoints_table[j])
            var_map_table.append((i, j))
var_amount = len(var_map_table)

intVars = range(var_amount)

A = np.zeros((n, var_amount))
Aeq = np.zeros((m, var_amount))
for var_num, index in zip(range(var_amount), var_map_table):
    Aeq[index[0]][var_num] = 1
    A[index[1]][var_num] = injury_table[index[0]][index[1]] / hitpoints_table[index[1]]

b = np.mat(hitpoints_table) + WASTE_DAMAGE_COEF * np.mat(max_injury_table)
beq = np.ones(m)

lb = np.zeros(var_amount)
ub = np.ones(var_amount)

p = MILP(f=obj_func, lb=lb, ub=ub, A=A, b=b, Aeq=Aeq, beq=beq, intVars=intVars, goal='min')
#r = p.solve('lpSolve')
r = p.solve('glpk', iprint =-1)
#r = p.solve('cplex')



###########################################################################################
#from FuncDesigner import *
#WASTE_DAMAGE_COEF = 1.2
#
#start_time = time.time()
#
#m, n = len(injury_table), len(damage_table)
#
#startPoint = {}
#x = oovars(m)
#for i in range(0, m):
#    x[i] = oovar('x' + str(i+1), size = n, domain = bool)
#    for j in range(0, n):
#        x[i][j].name = 'x' + str(i+1) + str(j+1)
#        startPoint[x[i][j]] = 0
#
#tmp_func = hitpoints_table[0] - injury_table[0][0] * x[0][0]
#for i in range(1, m):
#    tmp_func  = tmp_func - injury_table[i][0] * x[i][0]
#obj_func = damage_table[0] / (hitpoints_table[0] * maxhitpoints_table[0]) * tmp_func 
#for j in range(1, n):
#    tmp_func = hitpoints_table[j] - injury_table[0][j] * x[0][j]
#    for i in range(1, m):
#        tmp_func  = tmp_func - injury_table[i][j] * x[i][j]
#    obj_func = obj_func + damage_table[j] / (hitpoints_table[j] * maxhitpoints_table[j]) * tmp_func
#
#cons = []
#for i in range(m):
#    tmp_cons = x[i][0]
#    for j in range(1, n):
#        tmp_cons = tmp_cons + x[i][j]
#    tmp_cons = tmp_cons <= 1
#    cons.append(tmp_cons)
#    
#for j in range(n):
#    tmp_cons = injury_table[0][j] * x[0][j]
#    for i in range(1, m):
#        tmp_cons  = tmp_cons + injury_table[i][j] * x[i][j]
#    tmp_cons = tmp_cons <= hitpoints_table[j] + WASTE_DAMAGE_COEF * max_injury_table[j]
#    cons.append(tmp_cons)
#
#p = MILP(obj_func, startPoint, constraints=cons)
#
##r = p.minimize('lpSolve')
#
#r = p.minimize('glpk')
#
##print("--- %s seconds ---" % (time.time() - start_time))
#