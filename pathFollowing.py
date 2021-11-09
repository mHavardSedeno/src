import math, robot
import numpy as np
from matplotlib import pyplot

r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=20)

# draw the path to follow -- a circle centered at (0, −20) with radius 5 -- in dotted line
centre_x = 0
centre_y = -20
radius = 5

path = pyplot.Circle((centre_x,centre_y),radius,color='.5',fill=False, linestyle='dotted')
r.ax.add_artist(path)
r.refresh()


# Discretize t in N points
N = 10
# t in [0,2pi]
t = []
nextT = 0

for i in range(N):
    nextT += 0.2*math.pi
    t.append(nextT)

print(t)

poses = []

for i in range(len(t)):
    pose_x  = centre_x + (radius * np.cos(t[i]))
    pose_y  = centre_y + (radius * np.sin(t[i]))
    poses.append([pose_x, pose_y])

print(poses)
