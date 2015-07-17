from pybw_swig import * # import all constants and classes
import pybw
import math

from KaisevenOptimizeSC import *
from KaisevenControlSC import *
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *

class Sample(object):
    def __init__(self):
        # Add ourselves to the console manager as variable "k"
        pybw.consoleManager.locals.update({'k': self})

    def onConnect(self):
        # Get the game instance
        self.game = getGame() 

    def onMatchStart(self):
        if self.game.isReplay:
            return
        set_basic_information(self, self.game)
        initial_units_scan(self.me, scan_visible_enemy = True, game = self.game)

    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        #self.game.printf("frame_count" + str(frame_count))
        self.su = list(self.game.selectedUnits)

        if len(self.su) > 0:
            self.tsu = self.su[0]
            if self.tsu.isUnderAttack:
                draw_circle_on(self.game, self.tsu, radius = 14, color = COLOR_RED)
            if self.tsu.isIdle:
                draw_circle_on(self.game, self.tsu, radius = 10, color = COLOR_GREEN)
            elif self.tsu.isMoving:
                draw_circle_on(self.game, self.tsu, radius = 10, color = COLOR_BLUE)

    def onUnitDestroy(self, unit):
        #self.game.printf('Unit destroy : ' + unit.type.name)
        if unit.player == self.me:
            self.me.units_dictionary[unit.type].remove(unit)

    def onUnitCreate(self, unit):
        pass

    def onUnitMorph(self, unit):
        pass

    def onUnitComplete(self, unit):
        #self.game.printf('Unit complete : ' + unit.type.name)
        if unit.player == self.me:
            self.me.units_dictionary[unit.type].add(unit)

    def onUnitHide(self, unit):
        #self.game.printf('Unit hide : ' + unit.type.name)
        if unit.player == self.enemy:
            self.me.visible_enemy_units.remove(unit)

    def onUnitShow(self, unit):
        #self.game.printf('Unit show : ' + unit.type.name)
        if unit.player == self.enemy:
            self.me.visible_enemy_units.add(unit)

#####################################################################################################

class GetNeighboringEnemys(object):
    def __init__(self):
        # Add ourselves to the console manager as variable "k"
        pybw.consoleManager.locals.update({'k': self})

    def onConnect(self):
        # Get the game instance
        self.game = getGame() 

    def onMatchStart(self):
        if self.game.isReplay:
            return
        set_basic_information(self, self.game)
        initial_units_scan(self.me, scan_visible_enemy = True, game = self.game)
        self.MOVE_COEF = 1
        my_army = []
        for key in self.me.units_dictionary.keys():
            if key in self.me.unittype_set_army:
                my_army += list(self.me.units_dictionary[key])
        #self.game.printf('len(self.me.visible_enemy_units)' + str(len(self.me.visible_enemy_units)))
        my_enemy = list(self.me.visible_enemy_units)
        if len(my_army) > 0:
            for unit in my_army:
                draw_range_circle_on(self.game, unit, move_coef = self.MOVE_COEF)

    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        #self.game.printf("frame_count" + str(frame_count))
        my_army = []
        for key in self.me.units_dictionary.keys():
            if key in self.me.unittype_set_army:
                my_army += list(self.me.units_dictionary[key])
        self.army = my_army
        my_enemy = list(self.me.visible_enemy_units)
        self.my_unit = my_army[0]
        self.get_units_radio = int(math.ceil(fire_range_of(self.my_unit, move_coef = self.MOVE_COEF)))
        self.catch_units_set = UnitSet(self.game.getUnitsInRadius(self.my_unit.position, self.get_units_radio))
        #self.catch_units_set = UnitSet(self.my_unit.getUnitsInRadius(self.get_units_radio))
        if frame_count % 4 == 0:
            self.game.printf('\x04 catch units number : ' + str(len(self.catch_units_set)))
        
        if len(my_army) > 0:
            for unit in my_army:
                draw_range_circle_on(self.game, unit, move_coef = self.MOVE_COEF)

    def onUnitDestroy(self, unit):
        #self.game.printf('Unit destroy : ' + unit.type.name)
        if unit.player == self.me:
            self.me.units_dictionary[unit.type].remove(unit)

    def onUnitCreate(self, unit):
        pass

    def onUnitMorph(self, unit):
        pass

    def onUnitComplete(self, unit):
        #self.game.printf('Unit complete : ' + unit.type.name)
        if unit.player == self.me:
            self.me.units_dictionary[unit.type].add(unit)

    def onUnitHide(self, unit):
        #self.game.printf('Unit hide : ' + unit.type.name)
        if unit.player == self.enemy:
            self.me.visible_enemy_units.remove(unit)

    def onUnitShow(self, unit):
        #self.game.printf('Unit show : ' + unit.type.name)
        if unit.player == self.enemy:
            self.me.visible_enemy_units.add(unit)
