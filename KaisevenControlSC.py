from __future__ import division

from pybw_swig import * # import all constants and classes
import pybw
import math

from KaisevenOptimizeSC import *
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *

# Start Attack Configure
RETREAT_HP_RATIO = 0.7
STRICT_RETREAT_HP_RATIO = 0.5
STRICT_MOVING_FIRE_LEVEL = 32 * 1.5

##### Start Attack #####################################################################################################
def start_attack(game, units, target_of_units, my_units, enemy_units, draw_line_game = False, moving_fire = False):
    ### Remark
    # bool strict_moving_fire need more discuss ...
    # the function is_near_cooldown() in StarCraftBasicTool.py need more discuss ...

    if not moving_fire:
        for unit, target_unit in zip(units, target_of_units):
            if not target_unit or unit.isAttackFrame:
                continue
            if unit.target:
                if unit.target != target_unit:
                    unit.attack(target_unit)
            else:
                if not unit.orderTarget:
                    unit.attack(target_unit)
                elif unit.orderTarget != target_unit:
                    unit.attack(target_unit)
    else:
        under_aim_table = build_under_aim_table(units, enemy_units)
        my_center = Position(*get_group_center_of(my_units))
        enemy_center = Position(*get_group_center_of(enemy_units))
        delta_x = my_center.x - enemy_center.x
        delta_y = my_center.y - enemy_center.y
        hypotenuse = math.sqrt(delta_x**2 + delta_y**2)
        retreat_position = Position(int(32 * delta_x / hypotenuse), int(32 * delta_y / hypotenuse))

        for unit, target_unit in zip(units, target_of_units):
            if not target_unit:
                continue
            if unit.isAttackFrame:
                #draw_text_on(game, unit, "\x08 -- attacking --")
                continue
            residue_hp_ratio = unit.hitPoints / unit.type.maxHitPoints
            strict_moving_fire = True if weapon_range_diff(unit, target_unit) >= STRICT_MOVING_FIRE_LEVEL else False

            # Case Escape ------------------------------------
            if not unit.orderTarget:
                #draw_text_on(game, unit, "\x11 -- escape --")
                # neardeath
                if residue_hp_ratio <= STRICT_RETREAT_HP_RATIO:
                    moving_fire_case_escape_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                # dangerous
                elif residue_hp_ratio <= RETREAT_HP_RATIO:
                    moving_fire_case_escape_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                # energetic
                else:
                    moving_fire_case_escape_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)       
            # Case Assault -----------------------------------
            elif unit.isMoving:
                #draw_text_on(game, unit, "\x17 -- assault --")
                # neardeath
                if residue_hp_ratio <= STRICT_RETREAT_HP_RATIO:
                    moving_fire_case_assault_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                # dangerous
                elif residue_hp_ratio <= RETREAT_HP_RATIO:
                    moving_fire_case_assault_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                #-- energetic ----------------------------------#
                else:
                    moving_fire_case_assault_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
            # Case Attack ------------------------------------
            elif unit.isInWeaponRange(target_unit):
                #draw_text_on(game, unit, "\x06 -- attack --")
                # neardeath
                if residue_hp_ratio <= STRICT_RETREAT_HP_RATIO:
                    moving_fire_case_attack_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                # dangerous
                elif residue_hp_ratio <= RETREAT_HP_RATIO:
                    moving_fire_case_attack_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
                # energetic
                else:
                    moving_fire_case_attack_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position)
            # Case Unknow ------------------------------------
            else:
                #draw_text_on(game, unit, "\x07 -- unknow --")
                if not unit.orderTarget:
                    unit.attack(target_unit)
                    continue
                draw_circle_on(game, unit.orderTarget, 16, COLOR_GREEN)
                if unit.orderTarget != target_unit:                 
                    unit.attack(target_unit)
                #draw_circle_on(game, unit, 4, COLOR_GREEN)
    
    if draw_line_game:
        for unit, target_unit in zip(units, target_of_units):
            if not target_unit:
                continue
            draw_line_between(game, unit, target_unit, color = COLOR_RED)

# Case Escape-----------------------------------------------------------------------------------------------------------
def moving_fire_case_escape_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if under_aim_table[unit]:
        unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        weapon_type = "air" if target_unit.type.isFlyer else "ground"    
        if is_near_cooldown(unit, weapon_type):
            unit.attack(target_unit)
        else:
            unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))

def moving_fire_case_escape_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if under_aim_table[unit]:
        weapon_type = "air" if target_unit.type.isFlyer else "ground"
        if is_near_cooldown(unit, weapon_type):
            unit.attack(target_unit)
        else:
            unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        unit.attack(target_unit)

def moving_fire_case_escape_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if not strict_moving_fire:
        unit.attack(target_unit)
    else:
        unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
        if target_unit.orderTarget and target_unit.orderTarget == unit:
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                unit.attack(target_unit)
        else:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if not is_near_cooldown(unit, weapon_type):
                if unit.getDistance(target_unit) < unit_weapon_range + 8:
                    return
                else:
                    unit.stop
                    return
            unit.attack(target_unit)

# Case Assault----------------------------------------------------------------------------------------------------------
def moving_fire_case_assault_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if under_aim_table[unit]:
        unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        weapon_type = "air" if target_unit.type.isFlyer else "ground"    
        if is_near_cooldown(unit, weapon_type):
            if unit.orderTarget == target_unit:
                return
            unit.attack(target_unit)
        else:
            unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))

def moving_fire_case_assault_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if not strict_moving_fire:
        if under_aim_table[unit]:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if is_near_cooldown(unit, weapon_type):
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)
            else:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
        else:
            if unit.orderTarget == target_unit:
                return
            unit.attack(target_unit)
    else:
        unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
        if target_unit.orderTarget and target_unit.orderTarget == unit:
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                weapon_type = "air" if target_unit.type.isFlyer else "ground"
                if not is_near_cooldown(unit, weapon_type):
                    unit.stop
                else:
                    return
        else:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if not is_near_cooldown(unit, weapon_type):
                if unit.getDistance(target_unit) < unit_weapon_range:                               
                    unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
                else:
                    unit.stop
            else:
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)

def moving_fire_case_assault_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if not strict_moving_fire:
        if unit.orderTarget == target_unit:
            return
        unit.attack(target_unit)
    else:
        unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
        if target_unit.orderTarget and target_unit.orderTarget == unit:
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                weapon_type = "air" if target_unit.type.isFlyer else "ground"
                if not is_near_cooldown(unit, weapon_type):
                    unit.stop
                else:
                    return
        else:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if not is_near_cooldown(unit, weapon_type):
                if unit.getDistance(target_unit) < unit_weapon_range:                               
                    unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
                else:
                    unit.stop
            else:
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)

# Case Attack-----------------------------------------------------------------------------------------------------------
def moving_fire_case_attack_neardeath(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if under_aim_table[unit]:
        unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        if not strict_moving_fire:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if is_near_cooldown(unit, weapon_type):
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)
            else:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
        else:
            unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                weapon_type = "air" if target_unit.type.isFlyer else "ground"
                if is_near_cooldown(unit, weapon_type):
                    if unit.orderTarget == target_unit:
                        return
                    unit.attack(target_unit)
                else:
                    unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))

def moving_fire_case_attack_dangerous(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if not strict_moving_fire:
        weapon_type = "air" if target_unit.type.isFlyer else "ground"
        if is_near_cooldown(unit, weapon_type):
            if unit.orderTarget == target_unit:
                return
            unit.attack(target_unit)
        else:
            unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
        if target_unit.orderTarget and target_unit.orderTarget == unit:
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                weapon_type = "air" if target_unit.type.isFlyer else "ground"
                if is_near_cooldown(unit, weapon_type):
                    if unit.orderTarget == target_unit:
                        return
                    unit.attack(target_unit)
                else:
                    unit.stop
        else:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if is_near_cooldown(unit, weapon_type):
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)
            else:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))

def moving_fire_case_attack_energetic(unit, target_unit, my_units, enemy_units, under_aim_table, strict_moving_fire, retreat_position):
    if not strict_moving_fire:
        weapon_type = "air" if target_unit.type.isFlyer else "ground"
        if is_near_cooldown(unit, weapon_type):
            if unit.orderTarget == target_unit:
                return
            unit.attack(target_unit)
        else:
            unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
    else:
        unit_weapon_range = unit.type.airWeapon.maxRange if target_unit.type.isFlyer else unit.type.groundWeapon.maxRange
        if target_unit.orderTarget and target_unit.orderTarget == unit:
            if unit.getDistance(target_unit) < unit_weapon_range + 8:
                unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
            else:
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)
        else:
            weapon_type = "air" if target_unit.type.isFlyer else "ground"
            if is_near_cooldown(unit, weapon_type):
                if unit.orderTarget == target_unit:
                    return
                unit.attack(target_unit)
            else:
                if unit.getDistance(target_unit) < unit_weapon_range:
                    unit.move(Position(unit.position.x + retreat_position.x, unit.position.y + retreat_position.y))
                else:
                    if unit.orderTarget == target_unit:
                        return
                    unit.attack(target_unit)

########################################################################################################################
