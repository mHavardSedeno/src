import paving, robot, tools
from matplotlib import pyplot
from scipy.sparse.csgraph import dijkstra

def compute_center(box):
    x = (box[0] + box[1])/2
    y = (box[2] + box[3])/2
    return (x,y)


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
