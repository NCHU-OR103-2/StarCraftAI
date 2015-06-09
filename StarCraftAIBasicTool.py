from pybw_swig import * # import all constants and classes
import pybw

def set_basic_information(ai, game):
	ai.me = game.self
	ai.race = game.self.race
	ai.army = []

def get_specify_unittype(units_set, unittype):
	specify_units = []
	for unit in units_set:
		if unit.type.name == unittype:
			specify_units.append(unit)
	return specify_units

def print_unittype_in(units_set):
	for unit in units_set:
		print(unit.type.name)

def clear_up_death_unit(units_set, is_tuple=False):
	if len(units_set) == 0:
		return
	for item in units_set:
		if is_tuple:
			unit = item[0]
		else:
			unit = item
		if not unit.exists:
			units_set.remove(item)