import commands, calibration, robot, numpy, random, math


# Creation of the robot
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=20)
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]
# results : [-22.5094405   -0.27500596  12.14860075  -2.14414988  17.99607628  17.97150902  24.76445834   6.83243853]
# results : [-21.97622248  -0.12185495  -9.19353704 -17.13846395 -17.96172577  -17.46323074 -22.17598842   2.77415273]




# N random points to calibrate the robot
# Ajouter fonction pour avoir des randoms sans singularité (fonction q tp 1, merci Jules !)
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

print(cmds)

# Giving some poses, we try to find the corresponding commands
#pose = [(3,-15), (5,-2), (8,-15), (5,17), (10,-9), (-7, 14), (-10, 9), (12, 8), (0, -5), (10, 3)]
#commands = commands.find_commands(pose)


# Giving some commands, we find the matching poses
poses = commands.find_poses(cmds)

# create a table associating the commands to the resulting poses
commands = []
for i in range(0,len(cmds),2):
    commands.append([cmds[i], cmds[i+1]])
print(commands)

measures = calibration.make_measurements(r, commands)

calibration.calibrate(calibration.f_r, architecture, measures)
