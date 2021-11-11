import commands, calibration, robot, numpy, random, math
from itertools import repeat

sampleSize = 10
k = 10
q = [0,180]
cmds = []
t = [0 for _ in range(10)]

for i in range(0,sampleSize):
    t[i] = random.uniform(0, 2*math.pi)

    q[0] += k * numpy.cos(t[i])
    q[1] += k * numpy.sin(t[i])

    cmds.extend(q)
