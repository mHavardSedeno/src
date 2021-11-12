# Mathilde HAVARD-SEDENO
# M2 ORO

import tools, calibration, pathPlanning, pathFollowing
import math, robot, paving
import numpy as np
from matplotlib import pyplot
from scipy.sparse.csgraph import dijkstra


#######################
#---- CALIBRATION ----#
#######################

def part_calibration(r):

    # Generate N points to calibrate the robot
    sampleSize = 50
    print("\n\t\t #########################################")
    print(" \t\t ############## CALIBRATION ###############")
    print("\t\t ###########################################\n")
    print("   Launching the calibration with " + str(sampleSize) + " points...")

    cmds = tools.generate_points(sampleSize)

    # actuate the robot to every generated points given the matching commands
    # this returns the actual poses called measures
    measures = calibration.make_measurements(r, cmds)
    # print(measures)

    # using the measures, we calibrate the robot
    q = calibration.calibrate(calibration.f_r, architecture, measures)
    # just a loop to re-organize the calibrated architecture
    calibrated = []
    for k in q:
        calibrated.append(k)

    # print(r._architecture)

    print('   ---------------------------------------------------------------------------------------------\n')
    print("   --> Calibrated architecture is : " + str(calibrated))

    return(calibrated)


###########################
#---- PATH FOLLOWING ----#
##########################

def part_following(r, archi=[-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]):

    # draw the path to follow -- a circle centered at (0, −20) with radius 5 -- in dotted line
    centre_x = 0
    centre_y = -20
    radius = 5

    path = pyplot.Circle((centre_x,centre_y),radius,color='.5',fill=False, linestyle='dotted')
    r.ax.add_artist(path)
    r.refresh()


    # Discretize t in N points
    N = 50
    # t in [0,2pi]
    t = []
    nextT = 0

    for i in range(N):
        nextT += 1/N *2*math.pi
        t.append(nextT)

    poses = []

    for i in range(len(t)):
        pose_x  = centre_x + (radius * np.cos(t[i]))
        pose_y  = centre_y + (radius * np.sin(t[i]))
        poses.append([pose_x, pose_y])

    cmds = tools.find_commands(archi, poses, 0)

    pathFollowing.pathFollowing(r, cmds, True)


##########################
#---- PATH PLANNING ----#
#########################

def part_planning(r, archi=[-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]):

    p = paving.Paving()
    p.from_covfile("projet1.cov")

    # Determine the boxes corresopnding to the origin and destination points
    origin = (0, -15)
    dest = (0, 15)

    origin_box = pathPlanning.find_box(p, origin)
    dest_box = pathPlanning.find_box(p, dest)

    # create the adjacency matrix
    m = p.adjacency_matrix()

    # apply Dijkstra to it, given the origin box
    distance_matrix, predec = dijkstra(m, directed=False, return_predecessors=True, indices = origin_box[0].idx)
    # we obtain the distance matrix and the predecessors list

    # Create the path by backtracking the list of predecessors, leaving from the final one to the first one
    path = pathPlanning.create_path(origin_box, dest_box, predec)

    # Determine the center coordinates of each box
    poses = pathPlanning.box_center(p, path)

    # draw the path by colouring boxes in red
    # add the parameter 'paving=True' if you want to draw the whole paving (way slower)
    pathPlanning.draw_path(r, p, path)

    # Retrieve the commands given the poses determined above
    commands = tools.find_commands(archi, poses, 2)

    # Execute the path following the commands
    pathFollowing.pathFollowing(r, commands, 0)


##################
#----- MAIN -----#
##################

part = input("Enter the part you want to execute : \n1 for Calibration \n2 for Path following and \n3 for Path planning\n0 to execute everything with the two architectures")
while part not in ('1', '2', '3', '0'):
    print("Wrong input, please choose between 0,1,2 and 3 : ")
    part = input("Choose the part you want to execute : \n 1 for Calibration \n 2 for Path following and \n 3 for Path planning")

# Creation of the robot
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8], 0 ,2, eps_cmd=5)

if part=='0':
    print("--> WORKING WITH THE NOMINAL ARCHITECTURE:")
    part_following(r)
    part_planning(r)
    print("--> WORKING WITH THE CALIBRATED ARCHITECTURE:")
    architectureCali = part_calibration(r)
    part_following(r, architectureCali)
    part_planning(r, architectureCali)
elif part=='1':
    part_calibration(r)
else:
    archi = input("Enter the chosen architecture : \n0 for the nominal architecture\n1 for the calibreated architecture")
    while archi not in ('0', '1'):
        archi = input("Enter the chosen architecture : \n0 for the nominal architecture\n1 for the calibreated architecture")

    if archi=='0':
        if part=='2':
            part_following(r)
        elif part=='3':
            part_planning(r)
    elif archi=='1':
        architectureCali = part_calibration(r)
        if part=='2':
            part_following(r, architectureCali)
        elif part=='3':
            part_planning(r, architectureCali)
