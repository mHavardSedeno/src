#######################################################
# TwoBars robot demo
import math
import numpy

# >>> from importlib import reload
# >>> import demo,robot

##################################################
# Definition of a RR robot with approximate architecture
import robot

# >>> nominal_architecture = [0,0,3,2]
# >>> r = robot.TwoBars(nominal_architecture,seed=1,man_var=0,mes_var=0,eps_cmd=2)
# >>> r = robot.TwoBars(nominal_architecture,seed=1,man_var=0.2,mes_var=0.02)

##################################################
# CALIBRATION

# RR kinematic functions
def f_r(architecture,pose,command):
    a1 = [0,0]
    a2= [0,0]
    [a1[0], a1[1], a2[0], a2[1], l11, l12, l21, l22] = architecture   # [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]
    #print("## archi : " + str(architecture))
    [x1,x2] = pose
    [q1,q2] = numpy.radians(command)
    #    -l3^2 + (L1 + x1 - l1*cos(q1*pi/180))^2 + (x2 - l1*sin(q1*pi/180))^2 = 0;
    #   -l4^2 + (L2 + x1 - l2*cos(q2*pi/180))^2 + (x2 - l2*sin(q2*pi/180))^2
    f1 = pow((x1 - a1[0] - l11 * numpy.cos(q1)), 2) + pow((x2 - a1[1] - l11 * numpy.sin(q1)), 2) - pow(l12,2)
    f2 = pow((x1 - a2[0] - l21 * numpy.cos(q2)), 2) + pow((x2 - a2[1] - l21 * numpy.sin(q2)), 2) - pow(l22,2)
    return [f1,f2]

# Actuation of the robot in order to generate measures for calibration
def make_measurements(r,commands,col='black',mar='*'):
    r.actuate(commands[0])
    if col!='black':
        r.pen_down(col)
    measures=[]
    print('   Taking measures ...')
    for q in commands:
        r.actuate(q)
        x = r.measure_pose()
        r.ax.plot([x[0]],[x[1]],color=col,marker=mar)
        measures.append((x,q))
    if col!='black':
        r.pen_up()
    r.go_home()
    return measures

# >>> commands = [[q,q] for q in range(0,100,10)]
# >>> measures = demo.make_measurements(r,commands,col='red')

# >>> commands = [[q1,q2] for q1 in range(0,181,45) for q2 in range(0,181,30)]
# >>> measures = demo.make_measurements(r,commands,col='blue',mar='o')

# calibration from measurements
from scipy.optimize import least_squares

def calibrate(kinematic_functions,nominal_architecture,measures):
    # error function ----
    def errors(a):
        # print(a)
        err=[]
        for (x,q) in measures:
            # print("x : " + str(x) + ", q : " + str(q))
            for fi in kinematic_functions(a,x,q):
                err.append(fi)
        return err
    # -------------------
    print('   Calibration processing ...')
    sol = least_squares(errors,nominal_architecture)
    print('   status : ',sol.message)
    print('   error : ',sol.cost)
    print('   result : ',sol.x)
    return sol.x

# >>> calibrated_architecture = demo.calibrate(demo.f_RR,nominal_architecture,measures)
# >>> r.get_architecture()
