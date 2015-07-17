from __future__ import division

from pybw_swig import * # import all constants and classes
import pybw
import math
import time

import numpy as np
import cvxpy as cvx
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *

def opt_wta(weapon_units, target_units, move_coef = 1, game = None, ai = None):
    start_time = time.time()

    ### Set parameter
    WASTE_DAMAGE_COEF = 1.2
    REMAIN_DAMAGE_RATIO = 0.05
    ### Remark
    # Part 2: distence concept, in Build objective function, need more discuss ...

    ### Build information table
    damage_table, remain_damage_point = build_damage_table(target_units)
    hitpoints_table = build_hitpoints_table(target_units)
    injury_table = build_injury_table(weapon_units, target_units, move_coef = move_coef)
    max_injury_table = build_max_injury_table(weapon_units, target_units, injury_table)
    move_cost_table, total_move_cost = build_move_cost_table(weapon_units, target_units)
    
    m, n = len(weapon_units), len(target_units)
    X = cvx.Bool(m, n)

    ### Build objective function
    # Part 1: damage concept
    tmp_func = hitpoints_table[0] - injury_table[0][0] * X[0, 0]
    for i in range(1, m):
        tmp_func  = tmp_func - injury_table[i][0] * X[i, 0]
    obj_func = damage_table[0] / (target_units[0].hitPoints * target_units[0].type.maxHitPoints) * tmp_func 
    for j in range(1, n):
        tmp_func = hitpoints_table[j] - injury_table[0][j] * X[0, j]
        for i in range(1, m):
            tmp_func  = tmp_func - injury_table[i][j] * X[i, j]
        obj_func = obj_func + damage_table[j] / (target_units[j].hitPoints * target_units[j].type.maxHitPoints) * tmp_func
    # Part 2: distence concept
    if total_move_cost > 0:
        for i in range(1, m):
            for j in range(1, n):
                obj_func = obj_func + remain_damage_point * REMAIN_DAMAGE_RATIO * X[i, j] * (move_cost_table[i][j] / total_move_cost)**2
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
    
    ### Start compute
    prob = cvx.Problem(obj_func, cons)
    prob.solve()

    ### Build result
    target_of_weapon = []
    for i in range(m):
        target_of_weapon.append(None)
        for j in range(n):
            if X[i, j].value > 0.1:
                target_of_weapon[i] = target_units[j]
                break
        if not target_of_weapon[i]:
            target_of_weapon[i] = target_units[0]
    print("--- %s seconds ---" % (time.time() - start_time))
    #game.printf("\x04 ---------------------------")
    #game.printf("\x10 Minimize : " + str(prob.value))
    #game.printf("\x1E R.D.P    : " + str(remain_damage_point))
    return target_of_weapon

def quick_wta(weapon_units, target_units, move_coef = 1, init_counter = 6):
    target_of_weapon = []
    for unit in weapon_units:
        position = unit.position
        one_move_range = move_range_of(unit)
        fire_range = fire_range_of(unit, move_coef = move_coef)
        neighboring_targets = [target_unit for target_unit in target_units if target_unit.position.getDistance(position) <= fire_range]
        counter = init_counter
        while len(neighboring_targets) == 0 and counter > 0:
            counter -= 1
            fire_range += one_move_range
            neighboring_targets = [target_unit for target_unit in target_units if target_unit.position.getDistance(position) <= fire_range]
        if len(neighboring_targets) == 0:
            target_of_weapon.append(None)
            continue
        target_unit = min(neighboring_targets, key = lambda t: t.hitPoints)
        target_of_weapon.append(target_unit)
    return target_of_weapon

def build_under_aim_table(my_units, target_units):
    under_aim_table = {}
    for my_unit in my_units:
        under_aim_table[my_unit] = False
    for target_unit in target_units:
        if target_unit.orderTarget:
            under_aim_table[target_unit.orderTarget] = True

    return under_aim_table

# not finish
def keep_the_distance_between(my_unit, target_unit):
    my_x, my_y = my_unit.position.x, my_unit.position.y
    target_x, target_y = target_unit.position.x, target_unit.position.y
    delta_x = my_x - target_x
    delta_y = my_y - target_y
    hypotenuse = math.sqrt(delta_x**2 + delta_y**2)
    destination = Position(my_x + int(32 * delta_x / hypotenuse), my_y + int(32 * delta_y / hypotenuse))
    my_unit.move(destination)

# not finish
def attack_neighboring_enemy(game, unit):
    enemys = UnitSet(game.getUnitsInRadius(unit.position, unit.type.groundWeapon.maxRange))

def build_damage_table(target_units):
    damage_table = []
    remain_damage_point = 0.0
    for target_unit in target_units:
        damage = target_unit.type.groundWeapon.damageAmount/target_unit.type.groundWeapon.damageCooldown
        damage_table.append(damage)
        remain_damage_point += damage * target_unit.hitPoints / target_unit.type.maxHitPoints
    return damage_table, remain_damage_point

def build_hitpoints_table(target_units):
    return [target_unit.hitPoints for target_unit in target_units]

def build_injury_table(weapon_units, target_units, move_coef = 1):
    injury_table = []
    for m, weapon_unit in enumerate(weapon_units):
        row = []
        fire_range = fire_range_of(weapon_unit, move_coef = move_coef)
        for n, target_unit in enumerate(target_units):
            if get_distance_of(weapon_unit, target_unit) > fire_range:
                row.append(0)
                continue
            row.append(weapon_unit.type.groundWeapon.damageAmount - target_unit.type.armor)
        injury_table.append(row)
    return injury_table

def build_max_injury_table(weapon_units, target_units, injury_table):
    m, n = len(weapon_units), len(target_units)
    max_injury_table = []
    for j in range(n):
        min_value = float('inf')
        for i in range(m):
            if injury_table[i][j] != 0 and injury_table[i][j] < min_value:
                min_value = injury_table[i][j]
        if min_value == float('inf'):
            max_injury_table.append(0)
        else:
            max_injury_table.append(min_value)
    return max_injury_table

def build_move_cost_table(weapon_units, target_units):
    move_cost_table = []
    total_move_cost = 0
    for weapon_unit in weapon_units:
        row = []
        for target_unit in target_units:
            if weapon_unit.isInWeaponRange(target_unit):
                row.append(0)
                continue
            if not target_unit.type.isFlyer:
                if weapon_unit.type.groundWeapon.damageAmount == 0:
                    row.append(8192)
                else:
                    move_distance = weapon_unit.getDistance(target_unit) - weapon_unit.type.groundWeapon.maxRange
                    move_cost = int(math.ceil(move_distance / weapon_unit.type.topSpeed))
                    total_move_cost += move_cost
                    row.append(move_cost)
            else:
                if weapon_unit.type.airWeapon.damageAmount == 0:
                    row.append(8192)
                else:
                    move_distance = weapon_unit.getDistance(target_unit) - weapon_unit.type.airWeapon.maxRange
                    move_cost = int(math.ceil(move_distance / weapon_unit.type.topSpeed))
                    total_move_cost += move_cost
                    row.append(move_cost)
        move_cost_table.append(row)

    return move_cost_table, total_move_cost

def move_range_of(unit, weapon_type = 'ground', move_coef = 1):
    unit_type = unit.type
    if weapon_type == 'ground':
        return move_coef * unit_type.groundWeapon.damageCooldown * unit_type.topSpeed
    elif weapon == 'air':
        return move_coef * unit_type.airWeapon.damageCooldown * unit_type.topSpeed
    else:
        return -1

def fire_range_of(unit, weapon_type = 'ground', move_coef = 1):
    unit_type = unit.type
    if weapon_type == 'ground':
        return unit_type.groundWeapon.maxRange + move_coef * unit_type.groundWeapon.damageCooldown * unit_type.topSpeed
    elif weapon == 'air':
        return unit_type.airWeapon.maxRange + move_coef * unit_type.airWeapon.damageCooldown * unit_type.topSpeed
    else:
        return -1

def get_neighboring_enemys(game, my_unit_set, enemy_player, method = 'alpha'):  
    if method == 'alpha':
        total_enemys = [ unit for unit in game.allUnits if unit.player == enemy_player ]
        #game.printf('len(total_enemys) : ' + str(len(total_enemys)))
        neighboring_enemys = []
        for my_unit in my_unit_set:
            my_unit_fire_range = int(math.ceil(fire_range_of(my_unit, move_coef = 1)))
            # the below statement can't work, and I don't know why . It take me 1.5 hours to debug.   Orz ...
            #my_unit_neighboring_units = UnitSet(my_unit.getUnitsInRadius(my_unit_fire_range))
            my_unit_neighboring_units = UnitSet(game.getUnitsInRadius(my_unit.position, my_unit_fire_range))
            #game.printf('len(my_unit_neighboring_units) : ' + str(len(my_unit_neighboring_units)))
            for enemy in total_enemys:
                if enemy in my_unit_neighboring_units:
                    #game.printf('I got you !')
                    neighboring_enemys.append(enemy)
                    total_enemys.remove(enemy)
        game.printf('len(neighboring_enemys) : ' + str(len(neighboring_enemys)))
        return neighboring_enemys
    else:
        return []