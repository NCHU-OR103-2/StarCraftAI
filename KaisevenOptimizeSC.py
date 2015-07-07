from __future__ import division

from pybw_swig import * # import all constants and classes
import pybw
import math
import time

import numpy as np
import cvxpy as cvx
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *

## Create two scalar optimization variables.
#x = cvx.Variable()
#y = cvx.Variable()
#
## Create two constraints.
#constraints = [x + y == 1,
#               x - y >= 1]
#
## Form objective.
#obj = cvx.Minimize(cvx.square(x - y))
#
## Form and solve problem.
#prob = cvx.Problem(obj, constraints)
#prob.solve()  # Returns the optimal value.
#print "status:", prob.status
#print "optimal value", prob.value
#print "optimal var", x.value, y.value

# finish
def opt_wta(weapon_units, target_units, move_coef = 1, game = None, ai = None):
    start_time = time.time()

    damage_table = build_damage_table(target_units)
    #ai.damage_table = damage_table
    #game.printf('len(damage_table) = ' + str(len(damage_table)))
    hitpoints_table = build_hitpoints_table(target_units)
    injury_table = build_injury_table(weapon_units, target_units, move_coef = move_coef)
    #ai.injury_table = injury_table
    #game.printf('len(injury_table) = ' + str(len(injury_table)))
    move_cost_table, total_move_cost = build_move_cost_table(weapon_units, target_units)
    #write_1D_table_in_file(damage_table, "opt_wta_damage_table.txt")
    #write_2D_table_in_file(injury_table, "opt_wta_injury_table.txt")
    write_2D_table_in_file(injury_table, "opt_wta_move_cost_table.txt")
    #write_data_in_pickle_file(damage_table, 'dt.pkl')
    #write_data_in_pickle_file(injury_table, 'it.pkl')
    #write_data_in_pickle_file(hitpoints_table, 'ht.pkl')
    m, n = len(weapon_units), len(target_units)
    X = cvx.Bool(m, n)

    tmp_func = hitpoints_table[0] - injury_table[0][0] * X[0, 0]
    for i in range(1, m):
        tmp_func  = tmp_func - injury_table[i][0] * X[i, 0]
    obj_func = damage_table[0] / (target_units[0].hitPoints * target_units[0].type.maxHitPoints) * tmp_func 
    for j in range(1, n):
        tmp_func = hitpoints_table[j] - injury_table[0][j] * X[0, j]
        for i in range(1, m):
            tmp_func  = tmp_func - injury_table[i][j] * X[i, j]
        obj_func = obj_func + damage_table[j] / (target_units[j].hitPoints * target_units[j].type.maxHitPoints) * tmp_func
    
    if total_move_cost > 0:
        for i in range(1, m):
            for j in range(1, n):
                obj_func = obj_func + X[i, j] * (move_cost_table[i][j] / total_move_cost)**2
    
    obj_func = cvx.Minimize(obj_func)
    
    cons = []
    for i in range(m):
        tmp_cons = X[i, 0]
        for j in range(1, n):
            tmp_cons = tmp_cons + X[i, j]
        tmp_cons = tmp_cons <= 1
        cons.append(tmp_cons)

    mT = []
    for j in range(n):
        min_value = float('inf')
        for i in range(m):
            if injury_table[i][j] != 0 and injury_table[i][j] < min_value:
                min_value = injury_table[i][j]
        if min_value == float('inf'):
            mT.append(0)
        else:
            mT.append(min_value)
    
    some_coef = 1.2
    for j in range(n):
        tmp_cons = injury_table[0][j] * X[0, j]
        for i in range(1, m):
            tmp_cons  = tmp_cons + injury_table[i][j] * X[i, j]
        tmp_cons = tmp_cons <= hitpoints_table[j] + some_coef * mT[j]
        cons.append(tmp_cons)
    
    prob = cvx.Problem(obj_func, cons)
    prob.solve()
    
    #R = []
    #for i in range(m):
    #    r = []
    #    for j in range(n):
    #        if X[i, j].value < 0.1:
    #            r.append(0)
    #        else:
    #            r.append(1)
    #    R.append(r)
    #write_2D_table_in_file(R, "opt_result_table.txt")

    target_of_weapon = []
    #opt_wta_table = []
    for i in range(m):
        target_of_weapon.append(None)
        #opt_wta_table.append(None)
        for j in range(n):
            if X[i, j].value > 0.1:
                target_of_weapon[i] = target_units[j]
                #opt_wta_table[i] = j
                break
        if not target_of_weapon[i]:
            target_of_weapon[i] = target_units[0]
            #opt_wta_table[i] = 0
    #write_1D_table_in_file(opt_wta_table, "opt_wta_table.txt")
    print("--- %s seconds ---" % (time.time() - start_time))
    return target_of_weapon

# finish
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

def start_attack(game, units, target_of_units, draw_line_game = False, moving_fire = None, my_center = None, enemy_center = None):
    if not moving_fire:
        for unit, target_unit in zip(units, target_of_units):
            if not target_unit or unit.isAttackFrame:
                continue
            if unit.target:
                if unit.target != target_unit:
                    unit.attack(target_unit)
                    #unit.rightClick(target_unit)
            else:
                if not unit.orderTarget:
                    unit.attack(target_unit)
                    #unit.rightClick(target_unit)
                elif unit.orderTarget != target_unit:
                    unit.attack(target_unit)
                    #unit.rightClick(target_unit)
    else:
        retreat_hp_ratio = 0.3
        delta_x = my_center[0] - enemy_center[0]
        delta_y = my_center[1] - enemy_center[1]
        hypotenuse = math.sqrt(delta_x**2 + delta_y**2)

        for unit, target_unit in zip(units, target_of_units):
            if not target_unit or unit.isAttackFrame:
                continue
            target_is_flyer = target_unit.type.isFlyer
            if not target_is_flyer:
                cooldown = unit.groundWeaponCooldown
                max_range = unit.groundWeapon.maxRange
            else:
                cooldown = unit.airWeaponCooldown
                max_range = unit.airWeapon.maxRange
            target_max_range = target_unit.groundWeapon.maxRange
            residue_hp_ratio = unit.hitPoints / unit.type.maxHitPoints
            x, y = unit.position.x, unit.position.y

            if unit.isMoving:
                if residue_hp_ratio <= retreat_hp_ratio and len(unit.aim_by_units) != 0:
                    if unit.target:
                        destination = Position(x + int(32 * delta_x / hypotenuse), y + int(32 * delta_y / hypotenuse))
                        unit.move(destination)
                elif residue_hp_ratio > retreat_hp_ratio and len(unit.aim_by_units) != 0:
                    if max_range > target_max_range:
                        pass
                    else:
                        pass
                elif residue_hp_ratio <= retreat_hp_ratio and len(unit.aim_by_units) == 0:
                    if unit.target:
                        if unit.target != target_unit:
                            unit.attack(target_unit)
                            continue
                    if not unit.orderTarget:
                        unit.attack(target_unit)
                    elif unit.orderTarget != target_unit:
                        unit.attack(target_unit)
                elif residue_hp_ratio > retreat_hp_ratio and len(unit.aim_by_units) == 0:
                    if not unit.orderTarget:
                        unit.attack(target_unit)
                    elif unit.orderTarget != target_unit:
                        unit.attack(target_unit)

            else:
                if residue_hp_ratio <= retreat_hp_ratio and unit.isUnderAttack:
                    if unit.target or unit.orderTarget:
                        destination = Position(x + int(32 * delta_x / hypotenuse), y + int(32 * delta_y / hypotenuse))
                        unit.move(destination)
                elif residue_hp_ratio > retreat_hp_ratio and unit.isUnderAttack:
                    pass
                elif residue_hp_ratio <= retreat_hp_ratio and not unit.isUnderAttack:
                    if not unit.orderTarget:
                        unit.attack(target_unit)
                    elif unit.orderTarget != target_unit:
                        unit.attack(target_unit)
                elif residue_hp_ratio > retreat_hp_ratio and not unit.isUnderAttack:
                    pass 
    if draw_line_game:
        for unit, target_unit in zip(units, target_of_units):
            if not target_unit:
                continue
            draw_line_between(game, unit, target_unit, color = COLOR_RED)

def assign_attack(my_unit, target_unit):
    if not target_unit or my_unit.isAttackFrame:
        return
    if my_unit.target:
        if my_unit.target != target_unit:
            my_unit.attack(target_unit)
    else:
        if not my_unit.orderTarget:
            my_unit.attack(target_unit)
        elif my_unit.orderTarget != target_unit:
            my_unit.attack(target_unit)      

def set_under_aim(my_units, target_units):
    for unit in my_units:
        unit.aim_by_units = []
    for target_unit in target_units:
        if target_unit.orderTarget:
            target_unit.orderTarget.aim_by_units.append(target_unit)

# not finish
def keep_the_distance_between(my_unit, target_unit):
    my_x, my_y = my_unit.position.x, my_unit.position.y
    target_x, target_y = target_unit.position.x, target_unit.position.y
    delta_x = my_x - target_x
    delta_y = my_y - target_y
    hypotenuse = math.sqrt(delta_x**2 + delta_y**2)
    destination = Position(my_x + int(32 * delta_x / hypotenuse), my_y + int(32 * delta_y / hypotenuse))
    my_unit.move(destination)

def attack_neighboring_enemy(game, unit):
    enemys = UnitSet(game.getUnitsInRadius(unit.position, unit.type.groundWeapon.maxRange))


# not debug
def build_damage_table(target_units):
    return [target_unit.type.groundWeapon.damageAmount/target_unit.type.groundWeapon.damageCooldown for target_unit in target_units]

def build_hitpoints_table(target_units):
    return [target_unit.hitPoints for target_unit in target_units]

# not debug
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