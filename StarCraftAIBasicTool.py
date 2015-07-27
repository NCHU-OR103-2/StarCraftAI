from pybw_swig import * # import all constants and classes
import pybw

def set_basic_information(ai, game):
    ai.me = game.self
    ai.race = game.self.race    
    build_unittype_dictionary(ai.me)
    ai.enemys = []
    players = game.getPlayers()
    for player in players:
        if ai.me.isEnemy(player):
            ai.enemys.append(player)
    ai.enemy = ai.enemys[0]
    ai.me.enemy = ai.enemy
    ai.me.visible_enemy_units = set()
    ai.army = []

def initial_units_scan(player, scan_visible_enemy = False, game = None):
    for unit_type in player.unittype_set:
        player.units_dictionary[unit_type] = set()
    if not scan_visible_enemy:
        for unit in player.units:
            try:
                player.units_dictionary[unit.type].add(unit)
            except KeyError:
                pass
    else:
        player.visible_enemy_units.clear()
        for unit in game.allUnits:
            if unit.player == player:
                try:
                    player.units_dictionary[unit.type].add(unit)
                except KeyError:
                    pass
            elif unit.player == player.enemy:
                try:
                    player.visible_enemy_units.add(unit)
                except KeyError:
                    pass

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

def get_specify_unittype(units_set, unittype):
    specify_units = []
    for unit in units_set:
        if unit.type.name == unittype:
            specify_units.append(unit)
    return specify_units

def get_distance_of(unit1, unit2):
    return unit1.position.getDistance(unit2.position)

def get_group_center_of(unitset):
    total_x, total_y, total_n = 0, 0, 0
    for unit in unitset:
        total_x += unit.position.x
        total_y += unit.position.y
        total_n += 1
    return total_x / total_n, total_y / total_n

#def is_escape(unit):
#    return not unit.orderTarget and unit.isMoving

def is_near_cooldown(unit, weapon_type):
    if weapon_type == "ground":
        return unit.groundWeaponCooldown <= 10
    else:
        return unit.airWeaponCooldown <= 10

def weapon_range_diff(unit_1, unit_2):
    unit_1_weapon_range = unit_1.type.airWeapon.maxRange if unit_2.type.isFlyer else unit_1.type.groundWeapon.maxRange
    unit_2_weapon_range = unit_2.type.airWeapon.maxRange if unit_1.type.isFlyer else unit_2.type.groundWeapon.maxRange
    return unit_1_weapon_range - unit_2_weapon_range

def build_unittype_dictionary(player):
    if player.race == Terran:
        player.unittype_set = UNITTYPES_TERRAN        
        player.unittype_set_ground_unit = UNITTYPES_TERRAN_GROUND_UNIT
        player.unittype_set_air_unit = UNITTYPES_TERRAN_AIR_UNIT
        player.unittype_set_building = UNITTYPES_TERRAN_BUILDING
    elif player.race == Zerg:
        player.unittype_set = UNITTYPES_ZERG
        player.unittype_set_ground_unit = UNITTYPES_ZERG_GROUND_UNIT
        player.unittype_set_air_unit = UNITTYPES_ZERG_AIR_UNIT
        player.unittype_set_building = UNITTYPES_ZERG_BUILDING
    elif player.race == Protoss:
        player.unittype_set = UNITTYPES_PROTOSS
        player.unittype_set_ground_unit = UNITTYPES_PROTOSS_GROUND_UNIT
        player.unittype_set_air_unit = UNITTYPES_PROTOSS_AIR_UNIT
        player.unittype_set_building = UNITTYPES_PROTOSS_BUILDING
    player.unittype_set_army = player.unittype_set_ground_unit | player.unittype_set_air_unit
    player.unittype_set_army.remove(player.race.worker)
    player.units_dictionary = dict()
    for unit_type in player.unittype_set:
        player.units_dictionary.setdefault(unit_type, set())


#########################################################################################

UNITTYPES_TERRAN \
    = { Terran_SCV, Terran_Marine, Terran_Firebat, Terran_Medic, Terran_Ghost \
      , Terran_Vulture, Terran_Siege_Tank_Tank_Mode, Terran_Siege_Tank_Siege_Mode, Terran_Goliath \
      , Terran_Wraith, Terran_Dropship, Terran_Battlecruiser, Terran_Science_Vessel, Terran_Valkyrie \
      , Terran_Command_Center, Terran_Supply_Depot, Terran_Refinery \
      , Terran_Barracks, Terran_Academy, Terran_Factory \
      , Terran_Starport, Terran_Science_Facility, Terran_Engineering_Bay \
      , Terran_Armory, Terran_Missile_Turret, Terran_Bunker }

UNITTYPES_ZERG \
    = { Zerg_Drone, Zerg_Zergling, Zerg_Hydralisk, Zerg_Lurker \
      , Zerg_Ultralisk, Zerg_Defiler, Zerg_Broodling, Zerg_Infested_Terran \
      , Zerg_Overlord, Zerg_Mutalisk, Zerg_Queen, Zerg_Scourge \
      , Zerg_Guardian, Zerg_Devourer \
      , Zerg_Hatchery, Zerg_Lair, Zerg_Hive, Zerg_Extractor, Zerg_Infested_Command_Center \
      , Zerg_Spawning_Pool, Zerg_Evolution_Chamber, Zerg_Hydralisk_Den \
      , Zerg_Creep_Colony, Zerg_Spore_Colony, Zerg_Sunken_Colony \
      , Zerg_Spire, Zerg_Greater_Spire, Zerg_Queens_Nest \
      , Zerg_Ultralisk_Cavern, Zerg_Defiler_Mound, Zerg_Nydus_Canal }

UNITTYPES_PROTOSS \
    = { Protoss_Probe, Protoss_Zealot, Protoss_Dragoon, Protoss_Reaver \
      , Protoss_High_Templar, Protoss_Dark_Templar, Protoss_Archon, Protoss_Dark_Archon \
      , Protoss_Scout, Protoss_Shuttle, Protoss_Carrier \
      , Protoss_Observer, Protoss_Corsair, Protoss_Arbiter \
      , Protoss_Nexus, Protoss_Pylon, Protoss_Assimilator, Protoss_Photon_Cannon \
      , Protoss_Gateway, Protoss_Cybernetics_Core, Protoss_Forge \
      , Protoss_Citadel_of_Adun, Protoss_Templar_Archives, Protoss_Shield_Battery \
      , Protoss_Robotics_Facility, Protoss_Observatory, Protoss_Robotics_Support_Bay \
      , Protoss_Stargate, Protoss_Fleet_Beacon, Protoss_Arbiter_Tribunal }

UNITTYPES_TERRAN_GROUND_UNIT \
    = { Terran_SCV, Terran_Marine, Terran_Firebat, Terran_Medic, Terran_Ghost \
      , Terran_Vulture, Terran_Siege_Tank_Tank_Mode, Terran_Siege_Tank_Siege_Mode, Terran_Goliath }

UNITTYPES_TERRAN_AIR_UNIT \
    = { Terran_Wraith, Terran_Dropship, Terran_Battlecruiser, Terran_Science_Vessel, Terran_Valkyrie }

UNITTYPES_TERRAN_BUILDING \
    = { Terran_Command_Center, Terran_Supply_Depot, Terran_Refinery \
      , Terran_Barracks, Terran_Academy, Terran_Factory \
      , Terran_Starport, Terran_Science_Facility, Terran_Engineering_Bay \
      , Terran_Armory, Terran_Missile_Turret, Terran_Bunker }

UNITTYPES_ZERG_GROUND_UNIT \
    = { Zerg_Drone, Zerg_Zergling, Zerg_Hydralisk, Zerg_Lurker \
      , Zerg_Ultralisk, Zerg_Defiler, Zerg_Broodling, Zerg_Infested_Terran }

UNITTYPES_ZERG_AIR_UNIT \
    = { Zerg_Overlord, Zerg_Mutalisk, Zerg_Queen, Zerg_Scourge \
      , Zerg_Guardian, Zerg_Devourer }

UNITTYPES_ZERG_BUILDING \
    = { Zerg_Hatchery, Zerg_Lair, Zerg_Hive, Zerg_Extractor, Zerg_Infested_Command_Center \
      , Zerg_Spawning_Pool, Zerg_Evolution_Chamber, Zerg_Hydralisk_Den \
      , Zerg_Creep_Colony, Zerg_Spore_Colony, Zerg_Sunken_Colony \
      , Zerg_Spire, Zerg_Greater_Spire, Zerg_Queens_Nest \
      , Zerg_Ultralisk_Cavern, Zerg_Defiler_Mound, Zerg_Nydus_Canal }

UNITTYPES_PROTOSS_GROUND_UNIT \
    = { Protoss_Probe, Protoss_Zealot, Protoss_Dragoon, Protoss_Reaver \
      , Protoss_High_Templar, Protoss_Dark_Templar, Protoss_Archon, Protoss_Dark_Archon }

UNITTYPES_PROTOSS_AIR_UNIT \
    = { Protoss_Scout, Protoss_Shuttle, Protoss_Carrier \
      , Protoss_Observer, Protoss_Corsair, Protoss_Arbiter }

UNITTYPES_PROTOSS_BUILDING \
    = { Protoss_Gateway, Protoss_Cybernetics_Core, Protoss_Forge \
      , Protoss_Citadel_of_Adun, Protoss_Templar_Archives, Protoss_Shield_Battery \
      , Protoss_Robotics_Facility, Protoss_Observatory, Protoss_Robotics_Support_Bay \
      , Protoss_Stargate, Protoss_Fleet_Beacon, Protoss_Arbiter_Tribunal }