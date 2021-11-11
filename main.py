import tools, calibration, robot, paving, print_functions, pathPlanning
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




###########################
#---- PATH FOLLOWING ----#
##########################

def part_following(r):
    return 0

##########################
#---- PATH PLANNING ----#
#########################


def compute_center(box):
    x = (box[0] + box[1])/2
    y = (box[2] + box[3])/2
    return (x,y)

# PATH FOLLOWING FUNCTION #
def pathFollowing(commands, loop=False):

    print("\n\t\t ############################################")
    print(" \t\t ############## PATH FOLLOWING ###############")
    print("\t\t ##############################################\n")

    print("   Launching the path following procedure...")
    # TODO Préciser les paramètres donnés dans l'énoncé

    # We go to the first pose
    r.actuate(commands[0])
    # and start drawing
    r.pen_down()

    # then we go through all the poses
    for (x,y) in commands:
        r.actuate([x,y])

    # if we want the drawing to go back to the first pose -- as in a circle for instance --
    if loop==True:
        r.actuate([commands[0]])

    r.pen_up()
    input("Press [ENTER] to continue ...")

    # and to the initial position
    r.go_home()

def part_planning(r):

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
    commands = tools.find_commands(poses, 2)

    # Execute the path following the commands
    pathFollowing(commands, 2)


##################
#----- MAIN -----#
##################

part = input("Choose the part you want to execute : \n 1 for Calibration \n 2 for Path following and \n 3 for Path planning\n")
while part not in ('1', '2', '3', '0'):
    print("Wrong input, please choose between 0,1,2 and 3 : ")
    part = input("Choose the part you want to execute : \n 1 for Calibration \n 2 for Path following and \n 3 for Path planning")

# Creation of the robot
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=5)
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]

if part=='1':
    part_calibration(r)
elif part=='2':
    part_following(r)
elif part=='3':
    part_planning(r)
elif part=='0':
    part_calibration(r)
    part_following(r)
    part_planning(r)
else:
    print("error: wrong input")
