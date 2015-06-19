from pybw_swig import * # import all constants and classes
import pybw
import math

#import KaisevenOptimizeSC as k7opt
from KaisevenOptimizeSC import *
from StarCraftAIDevelopTool import *
from StarCraftAIBasicTool import *
#import cvxpy

class zerg_FastBreakAI(object):
    def __init__(self):
        # Add ourselves to the console manager as variable "k"
        pybw.consoleManager.locals.update({'k': self})

    def onConnect(self):
        # Get the game instance
        self.game = getGame() 

    def onMatchStart(self):
        self.game.pauseGame()
        if self.game.isReplay:
            return
        # setting basic information
        #self.me = self.game.self
        #self.race = self.me.race
        set_basic_information(self, self.game)
        self.MOVE_COEF = 3
        #self.enemy = self.game.getPlayer(1)    # semantics error
        self.enemys = []
        players = self.game.getPlayers()
        for player in players:
            if self.me.isEnemy(player) and player.name != 'Neutral':
                self.enemys.append(player)
        self.enemy = self.enemys[0]
        Hatcherys = [u for u in self.me.units if u.type == self.race.center]
        self.Hatchery = Hatcherys[0]
        locations = self.game.startLocations
        for location in locations:
            if location != self.Hatchery.tilePosition:
                self.enemy_tileposition = location
                #self.game.printf('set enemy location.')
        self.enemy_position = Position(self.enemy_tileposition)
        # inactive_workers , Worker Queue , workers wait for minning [ ( int workingtime, Unit worker ), ... ]
        self.inactive_workers = []
        # inactive_zerglings , Zergling Queue , [ Unit zergling, ... ]
        self.inactive_zerglings = []
        # wait_frame , wait for a moment.
        self.wait_frame = 15
        # drawUnits , wait for drawing
        self.drawUnits = []

        myoverlord = get_specify_unittype(self.me.units, 'Zerg Overlord')
        #myoverlord = [u for u in self.me.units if u.type.name == 'Zerg Overlord']
        myoverlord = myoverlord[0]
        myoverlord.move(self.enemy_position)
        
        # Get all minerals on the map
        self.minerals = list(self.game.minerals)
        self.mineral_queue = []
        for mineral in self.minerals:
            distance_to_center = mineral.position.getDistance( self.Hatchery.position )
            # Only queue workers to get minerals next to the main base
            if distance_to_center < 250:                 
                self.mineral_queue.append(( distance_to_center, mineral ))
        self.mineral_queue.sort() 
        self.StrategyStep = 0
    
    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        #self.game.printf("frame_count" + str(frame_count))
        try:
            while self.inactive_workers[0][0] == frame_count:
                #self.game.printf("frame_count: " + str(frame_count))
                worker = self.inactive_workers.pop(0)[1]
                self.minning(worker)
        except IndexError:
            pass

        try:
            while self.inactive_zerglings[0][0] == frame_count:
                #self.game.printf("frame_count: " + str(frame_count))
                zergling = self.inactive_zerglings.pop(0)[1]
                zergling.attack(self.enemy_position)
        except IndexError:
            pass
        except TypeError:
            self.game.pauseGame()
        
        if self.game.isReplay or self.race.name != 'Zerg':
            return
        if self.StrategyStep == 0 and self.me.minerals >= 200:
            #self.game.pauseGame()
            MyWorkers = [u for u in self.game.self.units if u.type.isWorker]
            builder = MyWorkers[0]
            self.buildSpawningPool(builder)
            return
        
        if self.StrategyStep == 1 and self.me.minerals >= 50 and self.me.minerals < 200:
            self.Hatchery.train(Zerg_Drone)
            self.StrategyStep = 2
        
        if self.StrategyStep == 2 and self.me.minerals >= 50:
            self.Hatchery.train(Zerg_Zergling)

        #draw_box_on(self.game, self.Hatchery)

        clear_up_death_unit(self.drawUnits, is_tuple=True)
        if len(self.drawUnits) > 0:
            for drawing in self.drawUnits:
                r = int(math.ceil(fire_range_of(drawing[0], move_coef = self.MOVE_COEF)))
                draw_circle_on(self.game, drawing[0], radius = r, colornum = drawing[2])

        clear_up_death_unit(self.army)       
        if len(self.army) > 0:
            enemys = get_neighboring_enemys(self.game, self.army, self.enemy)
            #if self.game.frameCount % 10 == 0:    
            #    self.game.printf('I catch ' + str(len(enemys)) + ' neighboring enemys .')
            target_list = quick_wta(self.army, enemys, move_coef = self.MOVE_COEF)
            start_attack(self.army, target_list, draw_line_game = self.game)
        
    def onUnitCreate(self, unit):
        if unit.type.isWorker:
            #self.game.printf('creat a worker.')
            mineral = self.mineral_queue.pop(0)
            unit.rightClick( mineral[1] )
            self.mineral_queue.append( mineral )             
        if unit.type.name == "Zerg Zergling":
            #self.game.printf('creat a zergling')
            unit.attack(self.enemy_position)
            self.drawUnits.append((unit, 16, COLOR_YELLOW))
            self.army.append(unit)
            
    def onUnitMorph(self, unit):
        if unit.type.isWorker:
            #self.game.printf('morph a worker.')
            minning_time = self.game.frameCount + self.wait_frame
            self.inactive_workers.append(( minning_time, unit ))
        if unit.type.name == "Zerg Zergling":
            #self.game.printf('morph a Zergling.')
            attack_time = self.game.frameCount + self.wait_frame
            self.inactive_zerglings.append(( attack_time, unit ))
            self.drawUnits.append((unit, 16, COLOR_YELLOW))
            self.army.append(unit)
    
    def minning(self, worker):        
        #self.game.printf("go minning")
        mineral = self.mineral_queue.pop(0)
        worker.rightClick( mineral[1] )
        self.mineral_queue.append( mineral )
    
    def buildSpawningPool(self, builder):
        x = self.Hatchery.tilePosition.x
        y = self.Hatchery.tilePosition.y
        for i in  range(1, 4):
            #self.game.printf("test")
            tmpD = TilePosition(x, y - i)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x, y + i)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x - i, y)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x + i, y)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
        self.StrategyStep = 1

###############################################################################################

class AlphaTestAI(object):
    def __init__(self):
        # Add ourselves to the console manager as variable "k"
        pybw.consoleManager.locals.update({'k': self})

    def onConnect(self):
        # Get the game instance
        self.game = getGame() 

    def onMatchStart(self):
        if self.game.isReplay:
            return
        # setting basic information
        #self.me = self.game.self
        #self.race = self.me.race
        set_basic_information(self, self.game)
        #self.enemy = self.game.getPlayer(1)
        self.army = get_specify_unittype(self.me.units, 'Zerg_Zergling')
        self.enemys = []
        players = self.game.getPlayers()
        for player in players:
            if self.me.isEnemy(player) and player.name != 'Neutral':
                self.enemys.append(player)
        self.enemy = self.enemys[0]
        Hatcherys = [u for u in self.me.units if u.type == self.race.center]
        self.Hatchery = Hatcherys[0]
        locations = self.game.startLocations
        for location in locations:
            if location != self.Hatchery.tilePosition:
                self.enemy_tileposition = location
                #self.game.printf('set enemy location.')
        self.enemy_position = Position(self.enemy_tileposition)
        # inactive_workers , Worker Queue , workers wait for minning [ ( int workingtime, Unit worker ), ... ]
        self.inactive_workers = []
        # inactive_zerglings , Zergling Queue , [ Unit zergling, ... ]
        self.inactive_zerglings = []
        # wait_frame , wait for a moment.
        self.wait_frame = 15
        # drawUnits , wait for drawing
        self.drawUnits = []

        myoverlord = get_specify_unittype(self.me.units, 'Zerg Overlord')
        #myoverlord = [u for u in self.me.units if u.type.name == 'Zerg Overlord']
        myoverlord = myoverlord[0]
        myoverlord.move(self.enemy_position)
        
        # Get all minerals on the map
        self.minerals = list(self.game.minerals)
        self.mineral_queue = []
        for mineral in self.minerals:
            distance_to_center = mineral.position.getDistance( self.Hatchery.position )
            # Only queue workers to get minerals next to the main base
            if distance_to_center < 250:                 
                self.mineral_queue.append(( distance_to_center, mineral ))
        self.mineral_queue.sort()
    
    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount
        #self.game.printf("frame_count" + str(frame_count))
        try:
            while self.inactive_zerglings[0][0] == frame_count:
                #self.game.printf("frame_count: " + str(frame_count))
                zergling = self.inactive_zerglings.pop(0)[1]
                zergling.attack(self.enemy_position)
        except IndexError:
            pass
        except TypeError:
            self.game.pauseGame()
        
        if self.game.isReplay or self.race.name != 'Zerg':
            return
        
        if self.me.minerals >= 50:
            self.Hatchery.train(Zerg_Zergling)

        if len(self.drawUnits) > 0:
            for drawing in self.drawUnits:
                r = int(math.ceil(fire_range_of(drawing[0], move_coef = 3)))
                #self.game.printf('r : ' + str(r))
                draw_circle_on(self.game, drawing[0], radius = r, colornum = drawing[2])

        clear_up_death_unit(self.army)       
        if len(self.army) > 0:
            enemys = get_neighboring_enemys(self.game, self.army, self.enemy)
            #if self.game.frameCount % 10 == 0:    
            #    self.game.printf('I catch ' + str(len(enemys)) + ' neighboring enemys .')
            target_list = quick_wta(self.army, enemys, move_coef = 3)
            start_attack(self.army, target_list, draw_line_game = self.game)

    def onUnitCreate(self, unit):
        if unit.type.isWorker:
            #self.game.printf('creat a worker.')
            mineral = self.mineral_queue.pop(0)
            unit.rightClick( mineral[1] )
            self.mineral_queue.append( mineral )             
        if unit.type.name == "Zerg Zergling":
            #self.game.printf('creat a zergling')
            unit.attack(self.enemy_position)
            self.drawUnits.append((unit, 16, COLOR_YELLOW))
            self.army.append(unit)
            
    def onUnitMorph(self, unit):
        if unit.type.isWorker:
            #self.game.printf('morph a worker.')
            minning_time = self.game.frameCount + self.wait_frame
            self.inactive_workers.append(( minning_time, unit ))
        if unit.type.name == "Zerg Zergling":
            #self.game.printf('morph a Zergling.')
            attack_time = self.game.frameCount + self.wait_frame
            self.inactive_zerglings.append(( attack_time, unit ))
            self.drawUnits.append((unit, 16, COLOR_YELLOW))
            self.army.append(unit)
    
    def minning(self, worker):        
        #self.game.printf("go minning")
        mineral = self.mineral_queue.pop(0)
        worker.rightClick( mineral[1] )
        self.mineral_queue.append( mineral )
    
    def buildSpawningPool(self, builder):
        x = self.Hatchery.tilePosition.x
        y = self.Hatchery.tilePosition.y
        for i in  range(1, 4):
            #self.game.printf("test")
            tmpD = TilePosition(x, y - i)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x, y + i)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x - i, y)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
            tmpD = TilePosition(x + i, y)
            if builder.build(tmpD, Zerg_Spawning_Pool):
                break
        self.StrategyStep = 1

###############################################################################################

class BetaTestAI(object):
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

    def onSendText(self, message):
        self.message = message

    def onMatchFrame(self):
        frame_count = self.game.frameCount

    def onUnitCreate(self, unit):
        pass

    def onUnitMorph(self, unit):
        pass
