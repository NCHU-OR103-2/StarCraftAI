from pybw_swig import * # import all constants and classes
import pybw

def whole_battlefield_scan(ai, game):
    pass

def set_basic_information(ai, game):
    ai.me = game.self
    ai.race = game.self.race
    ai.army = []
    build_unittype_dictionary(ai.me)

def get_specify_unittype(units_set, unittype):
    specify_units = []
    for unit in units_set:
        if unit.type.name == unittype:
            specify_units.append(unit)
    return specify_units

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

def get_distance_of(unit1, unit2):
    return unit1.position.getDistance(unit2.position)

def build_unittype_dictionary(player):
    if player.race == Terran:
        player.iunittype_set = { Terran_SCV, Terran_Marine, Terran_Firebat, Terran_Medic, Terran_Ghost \
                               , Terran_Vulture, Terran_Siege_Tank_Tank_Mode, Terran_Siege_Tank_Siege_Mode, Terran_Goliath \
                               , Terran_Wraith, Terran_Dropship, Terran_Battlecruiser, Terran_Science_Vessel, Terran_Valkyrie \
                               , Terran_Command_Center, Terran_Supply_Depot, Terran_Refinery \
                               , Terran_Barracks, Terran_Academy, Terran_Factory \
                               , Terran_Starport, Terran_Science_Facility, Terran_Engineering_Bay \
                               , Terran_Armory, Terran_Missile_Turret, Terran_Bunker }
    elif player.race == Zerg:
        player.unittype_set = { Zerg_Drone, Zerg_Zergling, Zerg_Hydralisk, Zerg_Lurker \
                              , Zerg_Ultralisk, Zerg_Defiler, Zerg_Broodling, Zerg_Infested_Terran \
                              , Zerg_Overlord, Zerg_Mutalisk, Zerg_Queen, Zerg_Scourge \
                              , Zerg_Guardian, Zerg_Devourer \
                              , Zerg_Hatchery, Zerg_Lair, Zerg_Hive, Zerg_Extractor, Zerg_Infested_Command_Center \
                              , Zerg_Spawning_Pool, Zerg_Evolution_Chamber, Zerg_Hydralisk_Den \
                              , Zerg_Creep_Colony, Zerg_Spore_Colony, Zerg_Sunken_Colony \
                              , Zerg_Spire, Zerg_Greater_Spire, Zerg_Queens_Nest \
                              , Zerg_Ultralisk_Cavern, Zerg_Defiler_Mound, Zerg_Nydus_Canal }
    elif player.race == Protoss:
        player.unittype_set = { Protoss_Probe, Protoss_Zealot, Protoss_Dragoon, Protoss_Reaver \
                              , Protoss_High_Templar, Protoss_Dark_Templar, Protoss_Archon, Protoss_Dark_Archon \
                              , Protoss_Scout, Protoss_Shuttle, Protoss_Carrier \
                              , Protoss_Observer, Protoss_Corsair, Protoss_Arbiter \
                              , Protoss_Nexus, Protoss_Pylon, Protoss_Assimilator, Protoss_Photon_Cannon \
                              , Protoss_Gateway, Protoss_Cybernetics_Core, Protoss_Forge \
                              , Protoss_Citadel_of_Adun, Protoss_Templar_Archives, Protoss_Shield_Battery \
                              , Protoss_Robotics_Facility, Protoss_Observatory, Protoss_Robotics_Support_Bay \
                              , Protoss_Stargate, Protoss_Fleet_Beacon, Protoss_Arbiter_Tribunal }
    player.units_dictionary = dict()
    for unit_type in player.unittype_set:
        player.units_dictionary.setdefault(unit_type, [])

