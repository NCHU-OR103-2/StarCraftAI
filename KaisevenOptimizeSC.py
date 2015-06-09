from pybw_swig import * # import all constants and classes
import pybw
import math

import numpy as np
import cvxpy as cvx

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
def quick_wta(weapons, targets):
	#targets_number = len(targets)
	target_hitpoints = [target.hitPoints for target in targets]
	target_of_weapon = []
	for m, weapon in enumerate(weapons):
		m_position = m.position
		m_move_range = m.type.groundWeapon.damageCooldown * m.type.topSpeed
		m_fire_range = m.type.groundWeapon.maxRange + m_move_range
		m_targets = [n for n, target in enumerate(targets) if target.position.getDistance(m_position) <= m_fire_range]
		while len(m.targets) == 0:
			m_fire_range += m_move_range
			m_targets = [n for n, target in enumerate(targets) if target.position.getDistance(m_position) <= m_fire_range]
		m_targets_hitpoints = [target_hitpoints[n] for n in m_targets]
		m_target = m_targets[np.argmin(m_targets_hitpoints)]
		#target_of_weapon.append([0]*targets_number)
		#target_of_weapon[m][m_target] = 1
		target_of_weapon.append(m_target)
	return target_of_weapon

# not finish
def build_injury_table(weapons, targets):
	injury_table = []
	#for m, weapon in enumerate(weapons):

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