from pybw_swig import * # import all constants and classes
import pybw
import math

import numpy as np
import cvxpy as cvx
from StarCraftAIDevelopTool import *

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

# not finish
def opt_wta(weapons, targets):
    damage_table = [target.type.groundWeapon.damageAmount/target.type.groundWeapon.damageAmount for target in targets]
    injury_table = build_injury_table(weapons, targets)
    m, n = len(weapons), len(targets)
    X = cvx.Bool(m, n)

# not debug
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

def start_attack(units, target_of_units, draw_line_game = None):
    for unit, target_unit in zip(units, target_of_units):
        if target_unit:
            if not unit.getTarget:
                unit.attack(target_unit)
            elif unit.getOrderTarget() and unit.getOrderTarget().id != target_unit.id:
                unit.attack(target_unit)

            if draw_line_game:
                draw_line_between(draw_line_game, unit, target_unit, colornum = COLOR_RED)

# not finish
def build_injury_table(weapons, targets):
    injury_table = []
    #for m, weapon in enumerate(weapons):

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
        neighboring_enemys = []
        for my_unit in my_unit_set:
            my_unit_fire_range = int(math.ceil(fire_range_of(my_unit, move_coef = 2)))
            # the below statement can't work, and I don't know why . It take me 1.5 hours to debug.   Orz ...
            #my_unit_neighboring_units = UnitSet(my_unit.getUnitsInRadius(my_unit_fire_range))
            my_unit_neighboring_units = UnitSet(game.getUnitsInRadius(my_unit.position, my_unit_fire_range))
            for enemy in total_enemys:
                if enemy in my_unit_neighboring_units:
                    #game.printf('I got you !')
                    neighboring_enemys.append(enemy)
                    total_enemys.remove(enemy)
        #game.printf('len(neighboring_enemys) : ' + str(len(neighboring_enemys)))
        return neighboring_enemys
    else:
        return []