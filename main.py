import commands, calibration, robot, paving
from matplotlib import pyplot
from scipy.sparse.csgraph import dijkstra



# Creation of the robot
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=20)
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]
#  [-21.95095607  -0.14550282  -1.21483752 -15.10359506 -17.88915666 -17.50832154 -10.82271588   2.23823878]

# on devrait trouver :
# [-22.032366652764818, -0.13257078161336416, 22.578971924246233, 0.02930428944787633, 17.967029715933474, 17.51957804230543, 17.717044418970193, 17.649707969457445]



#---- CALIBRATION ----#
# Generate N points to calibrate the robot
sampleSize = 50
cmds = commands.randomPoints(sampleSize)

# create a table associating the commands to the resulting poses
com = []
for i in range(0,len(cmds),2):
    com.append([cmds[i], cmds[i+1]])

measures = calibration.make_measurements(r, com)

# print(measures)

q = calibration.calibrate(calibration.f_r, architecture, measures)

# print(r._architecture)

calibrated = []
for k in q:
    calibrated.append(k)

# print(calibrated)



#----- PATH FOLLOWING -----#



#----- PATH PLANNING -----#
# rc=robot.FiveBars(calibrated, 0,2, eps_cmd=10)
#
# commands.modify_archi_mbx(calibrated)
# commands.solve_mbx('projet_calibrated.mbx')

p = paving.Paving()
p.from_covfile("proget.cov")

# p.draw2D(rc.ax, 1, 2)
#
# rc.refresh()
# input("Press [ENTER] to continue ...")

m = p.adjacency_matrix()

dist_matrix = dijkstra(m, directed=False)
