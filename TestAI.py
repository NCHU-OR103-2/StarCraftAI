from pybw_swig import * # import all constants and classes
import pybw
import math

#import KaisevenOptimizeSC as k7opt
from KaisevenOptimizeSC import *
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *
#import cvxpy

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
        #self.game.printf('len(my_army) = ' + str(len(my_army)))
        #self.game.printf('len(my_army) = ' + str(len(my_enemy)))
        #opt_wta(my_army, my_enemy, move_coef = self.MOVE_COEF, game = self.game)
        #self.game.printf('opt_wta finish')
        #self.game.pauseGame()

    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        #self.game.printf(str(frame_count))
        my_army = []
        for key in self.me.units_dictionary.keys():
            if key in self.me.unittype_set_army:
                my_army += list(self.me.units_dictionary[key])
        self.army = my_army
        my_enemy = list(self.me.visible_enemy_units)
        self.tu = my_army[0]
        self.tur = int(math.ceil(fire_range_of(self.tu, move_coef = self.MOVE_COEF)))
        self.ts = UnitSet(self.game.getUnitsInRadius(self.tu.position, self.tur))
        #self.ts = UnitSet(self.tu.getUnitsInRadius(self.tur))
        self.game.printf('len(self.ts) : ' + str(len(self.ts)))
        
        #get_neighboring_enemys(self.game, self.army, self.me.enemy)
        if len(my_army) > 0:
            for unit in my_army:
                draw_range_circle_on(self.game, unit, move_coef = self.MOVE_COEF)
        if len(my_army) > 0 and len(my_enemy) > 0:
            target_list = quick_wta(my_army, my_enemy, move_coef = self.MOVE_COEF)
            #target_list = opt_wta(my_army, my_enemy, move_coef = self.MOVE_COEF, game = self.game)
            start_attack(self.game, my_army, target_list, draw_line_game = True) 

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

class StartAttack(object):
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
        my_enemy = list(self.me.visible_enemy_units)

    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        self.game.printf('\x02 ---- Frame Count : ' + str(frame_count) + ' ----')
        my_army = []
        for key in self.me.units_dictionary.keys():
            if key in self.me.unittype_set_army:
                my_army += list(self.me.units_dictionary[key])
        self.army = my_army
        my_enemy = list(self.me.visible_enemy_units)
        #if len(my_army) > 0:
        #    for unit in my_army:
        #        draw_range_circle_on(self.game, unit, move_coef = self.MOVE_COEF)
        if len(my_enemy) > 0:
            for unit in my_enemy:
                show_hitpoints_of(self.game, unit)
        #if len(my_army) > 0 and len(my_enemy) > 0:
        #    start_attack(self.game, my_army, my_enemy, draw_line_game = True) 
        self.tu = self.army[0]
        self.tue = my_enemy[0]
        if not self.tu.getTarget():
                self.tu.attack(self.tue)
                self.game.printf('not getTarget() ')
                #self.tu.rightClick(self.tue)
        elif self.tu.getTarget() != self.tue:
                self.tu.attack(self.tue)
                self.game.printf('getTarget() != tue ')
                #self.tu.rightClick(self.tue)
        elif self.tu.getOrderTarget() and self.tu.getOrderTarget() != self.tue:
                self.tu.attack(self.tue)
                self.game.printf('getOrderTarget() and getOrderTarget() != tue')
                #self.tu.rightClick(self.tue)    

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