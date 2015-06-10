from pybw_swig import * # import all constants and classes
import pybw

def draw_circle_on(game, unit, radius = 16, colornum = 1):
    x = unit.position.x
    y = unit.position.y
    color = Color(colornum)
    game.drawCircleMap(x, y, radius, color)

def draw_line_between(game, unit_1, unit_2, colornum = 1):
    x_1, y_1 = unit_1.position.x, unit_1.position.y
    x_2, y_2 = unit_2.position.x, unit_2.position.y
    color = Color(colornum)
    game.drawLineMap(x_1, y_1, x_2, y_2, color)

def draw_box_on(game, unit, colornum = 1):
    color = Color(colornum)
    game.drawBoxMap(unit.left, unit.top, unit.right, unit.bottom, color)

def print_unittype_in(units_set):
    for unit in units_set:
        print(unit.type.name)

COLOR_YELLOW = 61
COLOR_RED = 111
COLOR_GREEN = 118
