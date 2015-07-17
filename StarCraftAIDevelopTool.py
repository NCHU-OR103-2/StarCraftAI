from __future__ import division

from pybw_swig import * # import all constants and classes
import pybw
from StarCraftAIBasicTool import *
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
    if not unit_1 or not unit_2:
        return
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

def show_cooldown_of(game, unit, weapon_type = "ground"):
    x = unit.left - 5
    y = unit.bottom
    if weapon_type == "ground":
        cooldown = '\x1F ' + str(unit.groundWeaponCooldown)
    else:
        cooldown = '\x1F ' + str(unit.airWeaponCooldown)
    game.drawTextMap(x, y, cooldown)

def draw_text_on(game, unit, text):
    origin_x = unit.position.x - 32 * 3
    origin_y = unit.position.y - 16
    if isinstance(text, list):
        for t in text:
            game.drawTextMap(origin_x, origin_y, t)
            origin_y += 12
    else:
        game.drawTextMap(origin_x, origin_y, text)

def show_unit_status(game, unit, target_unit = None):
    origin_x = unit.position.x - 32 * 3
    origin_y = unit.position.y - 16
    # ---- version 1 ----
    #if unit.isIdle:
    #    game.drawTextMap(origin_x, origin_y, "\x05 Idle ...")
    #    origin_y += 12
    #if unit.isMoving:
    #    game.drawTextMap(origin_x, origin_y, "\x19 Moving")
    #    origin_y += 12
    #if unit.orderTarget:
    #    game.drawTextMap(origin_x, origin_y, "\x07 has OrderTarget")
    #    origin_y += 12
    #if unit.target:
    #    game.drawTextMap(origin_x, origin_y, "\x18 has Target")
    #    origin_y += 12
    #if is_escape(unit):
    #    game.drawTextMap(origin_x, origin_y, "\x11 escape !")
    #    origin_y += 12
    #if unit.isAttackFrame:
    #    game.drawTextMap(origin_x, origin_y, "\x08 attacking ")
    #    origin_y += 12
    #if unit.groundWeaponCooldown >= 1:
    #    game.drawTextMap(origin_x, origin_y, "\x1F wait cooldown ")
    #    origin_y += 12
    
    # ---- version 2 ----
    if target_unit:
        if not unit.orderTarget:
            game.drawTextMap(origin_x, origin_y, "\x07 not have OrderTarget")
            origin_y += 12
        elif unit.isMoving:
            game.drawTextMap(origin_x, origin_y, "\x19 Moving")
            origin_y += 12
        elif unit.isInWeaponRange(target_unit):
            game.drawTextMap(origin_x, origin_y, "\x08 in weaponrange ")
            origin_y += 12
        else:
            pass

    if origin_y == unit.position.y - 16:
        game.drawTextMap(origin_x, origin_y, "\x04 -- unknow status --")

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


COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_YELLOW = Color(255, 255, 0)
COLOR_MAGENTA = Color(255, 0, 255)
COLOR_CYAN = Color(0, 255, 255)
COLOR_WHITE = Color(255, 255, 255)
COLOR_DEEP_PINK = Color(255, 20, 147)