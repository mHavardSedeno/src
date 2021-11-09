import math, robot, commands
import numpy as np
from matplotlib import pyplot

r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=1)

# draw the path to follow -- a circle centered at (0, −20) with radius 5 -- in dotted line
centre_x = 0
centre_y = -20
radius = 5

path = pyplot.Circle((centre_x,centre_y),radius,color='.5',fill=False, linestyle='dotted')
r.ax.add_artist(path)
r.refresh()


# Discretize t in N points
N = 100
# t in [0,2pi]
t = []
nextT = 0

for i in range(N):
    nextT += 1/N *2*math.pi
    t.append(nextT)

print(t)

poses = []

for i in range(len(t)):
    pose_x  = centre_x + (radius * np.cos(t[i]))
    pose_y  = centre_y + (radius * np.sin(t[i]))
    poses.append([pose_x, pose_y])

print(poses[0])

cmds = commands.find_commands(poses)
print(cmds)

# We go to the first pose
r.actuate(cmds[0])
# and start drawing
r.pen_down()

# then we go through all the poses
for (x,y) in cmds:
    r.actuate([x,y])

# and return to the beginning of the circle
r.actuate(cmds[0])
r.pen_up()
input("Press [ENTER] to continue ...")

# and to the initial position
r.go_home()
