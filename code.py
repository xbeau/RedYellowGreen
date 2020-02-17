#https://github.com/xbeau/RedYellowGreen
#
#                       ##
#                      _[]_
#                     [____]
#                 .----'  '----.
#             .===|    .==.    |===.
#             \   |   /####\   |   /
#             /   |   \####/   |   \
#             '===|    `""`    |==='
#             .===|    .==.    |===.
#             \   |   /::::\   |   /
#             /   |   \::::/   |   \
#             '===|    `""`    |==='
#             .===|    .==.    |===.
#             \   |   /&&&&\   |   /
#             /   |   \&&&&/   |   \
#             '===|    `""`    |==='
#          jgs    '--.______.--'

import board
import pulseio
import displayio
import terminalio
from time import sleep
from adafruit_clue import clue
from adafruit_display_text.label import Label
from adafruit_display_shapes.circle import Circle

print('Traffic Light 00:42')

RED_PWM = 10000
YLW_PWM = 60000
GRN_PWM = 60000

color = None
sound = 0

ledR = pulseio.PWMOut(board.D0)
ledY = pulseio.PWMOut(board.D1)
ledG = pulseio.PWMOut(board.D2)

display = board.DISPLAY
group = displayio.Group(max_size=2)
light_group = displayio.Group(max_size=3)
text_group = displayio.Group(max_size=2, scale=4, x=100, y=16)

red_circle = Circle(40, 40, 30, outline=clue.RED)
ylw_circle = Circle(40, 120, 30, outline=clue.YELLOW)
grn_circle = Circle(40, 200, 30, outline=clue.GREEN)

light_group.append(red_circle)
light_group.append(ylw_circle)
light_group.append(grn_circle)

title = Label(terminalio.FONT, text="Sound", color=clue.WHITE)
data = Label(terminalio.FONT, text="----.-", color=clue.WHITE)
data.y = 24
text_group.append(title)
text_group.append(data)

group.append(light_group)
group.append(text_group)

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

def setSignal(c):
    global color
    if c != color:
        grn_circle.fill = None
        ylw_circle.fill = None
        red_circle.fill = None
        ledG.duty_cycle = 0
        ledY.duty_cycle = 0
        ledR.duty_cycle = 0
        if c == clue.GREEN:
            grn_circle.fill = c
            ledG.duty_cycle = GRN_PWM
        elif c == clue.YELLOW:
            ylw_circle.fill = c
            ledY.duty_cycle = YLW_PWM
        else: #RED
            red_circle.fill = clue.RED
            ledR.duty_cycle = RED_PWM
        color = c

def gestureCheck():
    g = clue.gesture
    if g != 0:
        print(g)

def soundCheck():
    global sound
    sound += (clue.sound_level - sound) * 0.1
    if sound < 50:
        setSignal(clue.GREEN)
    elif sound < 200:
        setSignal(clue.YELLOW)
    else:
        setSignal(clue.RED)
    print((sound,))
    data.text = "{:.1f}".format(sound)

#TODO: Show Code (dump to screen)

while 1:
    #gestureCheck()
    while clue.proximity > 0:
        sleep(0.1)
    #trafficCycle()
    soundCheck()