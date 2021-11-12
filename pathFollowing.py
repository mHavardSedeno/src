# Mathilde HAVARD-SEDENO
# M2 ORO

import math, robot, tools, pathPlanning
import numpy as np
from matplotlib import pyplot

def pathFollowing(r, commands, loop=False):

    print("\n\t\t###########################################")
    print("\t\t ############## PATH FOLLOWING ###############")
    print("\t\t #############################################\n")

    print("   Launching the path following procedure...")

    # We go to the first pose
    r.actuate(commands[0])
    # and start drawing
    r.pen_down()

    # then we go through all the poses
    for (x,y) in commands:
        r.actuate([x,y])

    # if we want the drawing to go back to the first pose -- as in a circle for instance --
    if loop==True:
        r.actuate(commands[0])

    r.pen_up()
    input("Press [ENTER] to continue ...")

    # and to the initial position
    r.go_home()
