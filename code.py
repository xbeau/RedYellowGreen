import board
import pulseio
import displayio
from time import sleep
from adafruit_clue import clue
from adafruit_display_shapes.circle import Circle

print('Traffic Light 21:12')

ledR = pulseio.PWMOut(board.D0)
ledY = pulseio.PWMOut(board.D1)
ledG = pulseio.PWMOut(board.D2)

display = board.DISPLAY
group = displayio.Group(max_size=4)

red_circle = Circle(40, 40, 30, outline=clue.RED)
ylw_circle = Circle(40, 120, 30, outline=clue.YELLOW)
grn_circle = Circle(40, 200, 30, outline=clue.GREEN)

group.append(red_circle)
group.append(ylw_circle)
group.append(grn_circle)
display.show(group)

def trafficCycle():
    red_circle.fill = None
    grn_circle.fill = clue.GREEN
    ledR.duty_cycle = 0
    ledG.duty_cycle = 60000
    sleep(0.5)
    grn_circle.fill = None
    ylw_circle.fill = clue.YELLOW
    ledG.duty_cycle = 0
    ledY.duty_cycle = 60000
    sleep(0.2)
    ylw_circle.fill = None
    red_circle.fill = clue.RED
    ledY.duty_cycle = 0
    ledR.duty_cycle = 10000
    sleep(0.5)

def gestureCheck():
    g = clue.gesture
    if g != 0:
        print(g)

while 1:
    #gestureCheck()
    while clue.proximity > 0:
        sleep(0.1)
    trafficCycle()