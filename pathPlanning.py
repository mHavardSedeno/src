import paving, robot, tools
from matplotlib import pyplot
from scipy.sparse.csgraph import dijkstra

def compute_center(box):
    x = (box[0] + box[1])/2
    y = (box[2] + box[3])/2
    return (x,y)


# r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=10)
#
# p = paving.Paving()
# p.from_covfile("projet1.cov")
#
# # Determine the boxes corresopnding to the origin and destination points
# # Origin point : (0, -15)
# origin = (0, -15)
# # Destination point : (0,15)
# dest = (0, 15)
#
# # A point can belong to several points if it's on the edge of the box, so it's a list
# dest_box = []
# origin_box = []
#
# for i in p.boxes:
#     if dest[0] >= i.vec[0] and dest[0] <= i.vec[1]:
#         if dest[1] >= i.vec[2] and dest[1] <= i.vec[3]:
#             dest_box.append(i)
#     if origin[0] >= i.vec[0] and origin[0] <= i.vec[1]:
#         if origin[1] >= i.vec[2] and origin[1] <= i.vec[3]:
#             origin_box.append(i)
#
# # return the origin box and the destination box
# print(origin_box)
# print(dest_box)
#
# m = p.adjacency_matrix()
#
# distance_matrix, predec = dijkstra(m, directed=False, return_predecessors=True, indices = origin_box[0].idx)
# # print(distance_matrix)
# print(predec)
#
# path = [dest_box[0].idx]
# pred = dest_box[0].idx
#
# while pred != origin_box[0].idx :
#      pred = predec[pred]
#      path.append(pred)
#
# # print(path)
#
# # Determine the center coordinates of each box
# poses = []
# for i in path:
#     print(p.boxes[i].vec)
#     pose = compute_center(p.boxes[i].vec)
#     poses.append(pose)
#
# poses.reverse()
#
# subp = p.subpaving(path)
# # p.draw2D(r.ax, 1, 2, ec='b')
# subp.draw2D(r.ax, 1, 2, ec='r')
# # input("Press [ENTER] to continue ...")
#
# commands = tools.find_commands(poses, 2)
# print(commands)

# PATH FOLLOWING FUNCTION #
def pathFollowing(commands, loop=False):
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

def find_box(p, point):
    # A point can belong to several points if it's on the edge of the box, so it's a list
    point_box = []

    for i in p.boxes:
        if point[0] >= i.vec[0] and point[0] <= i.vec[1]:
            if point[1] >= i.vec[2] and point[1] <= i.vec[3]:
                point_box.append(i)

    # return the origin box and the destination box
    return(point_box)


def create_path(origin_box, dest_box, predec):
    path = [dest_box[0].idx]
    pred = dest_box[0].idx

    while pred != origin_box[0].idx :
         pred = predec[pred]
         path.append(pred)

    return(path)

def box_center(p, path):
    poses = []
    for i in path:
        print(p.boxes[i].vec)
        pose = compute_center(p.boxes[i].vec)
        poses.append(pose)

    poses.reverse()
    return(poses)

def draw_path(r, p, path, paving=False):
    subp = p.subpaving(path)
    # p.draw2D(r.ax, 1, 2, ec='b')
    subp.draw2D(r.ax, 1, 2, ec='r')
