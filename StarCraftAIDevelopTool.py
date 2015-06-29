from __future__ import division

from pybw_swig import * # import all constants and classes
import pybw
import math
import pickle

def draw_circle_on(game, unit, radius = 16, color = Color(0, 0, 0)):
    x = unit.position.x
    y = unit.position.y
    game.drawCircleMap(x, y, radius, color)

def draw_range_circle_on(game, unit, weapon_type = 'ground', move_coef = 0):
    if weapon_type == 'ground':
        weapon = unit.type.groundWeapon
    elif weapon_type == 'air':
        weapon = unit.type.airWeapon
    x = unit.position.x
    y = unit.position.y
    game.drawCircleMap(x, y, weapon.maxRange, COLOR_RED)
    if move_coef > 0:
        fire_range = weapon.maxRange + move_coef * weapon.damageCooldown * unit.type.topSpeed
        game.drawCircleMap(x, y, int(math.ceil(fire_range)), COLOR_DEEP_PINK) 

def draw_line_between(game, unit_1, unit_2, color = Color(0, 0, 0)):
    x_1, y_1 = unit_1.position.x, unit_1.position.y
    x_2, y_2 = unit_2.position.x, unit_2.position.y
    game.drawLineMap(x_1, y_1, x_2, y_2, color)

def draw_box_on(game, unit, color = Color(0, 0, 0)):
    game.drawBoxMap(unit.left, unit.top, unit.right, unit.bottom, color)

def show_hitpoints_of(game, unit):
    x = unit.right
    y = unit.bottom
    hp = unit.hitPoints
    max_hp = unit.type.maxHitPoints
    ratio = hp / max_hp
    if ratio > 0.5:
        text = '\x07 ' + str(hp)
    elif ratio > 0.2:
        text = '\x17 ' + str(hp)
    else:
        text = '\x08' + str(hp)
    game.drawTextMap(x, y, text)

def print_unittype_in(units_set):
    for unit in units_set:
        print(unit.type.name)

def write_2D_table_in_file(table, file_name, title = None):
    my_file = open(file_name, "w")
    for row in table:
        for item in row:
            my_file.write("{0:>12f}".format(item))
        my_file.write("\n")
    my_file.close()

def write_1D_table_in_file(table, file_name, title = None):
    my_file = open(file_name, "w")
    for item in table:
        my_file.write("{0:>12f}".format(item))
    my_file.write("\n")
    my_file.close()

def write_data_in_pickle_file(data, file_name):
    my_file = open(file_name, 'w')
    pickle.dump(data, my_file)
    my_file.close()

def write_dataset_in_pickle_file(dataset, file_name):
    my_file = open(file_name, 'w')
    for data in dataset:
        pickle.dump(data, my_file)
    my_file.close()

COLOR_YELLOW = Color(255, 255, 0)
COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_DEEP_PINK = Color(255, 20, 147)