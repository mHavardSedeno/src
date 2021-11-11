import os, fileinput, paving, math, random, numpy

# N random points to calibrate the robot
def randomPoints(sampleSize):
    k = 10
    q = [0,180]
    cmds = []
    t = [0 for _ in range(sampleSize)]

    for i in range(0,sampleSize):
        t[i] = random.uniform(0, 2*math.pi)
        a = random.randrange(10)
        b = random.randrange(10)
        q[0] += k * numpy.cos(t[i])
        q[1] += k * numpy.sin(t[i])

        cmds.extend(q)
    return(cmds)

def modify_poses_mbx(x):

    # Si on a le temps :
    # Modifier toujours le même fichier pour éviter d'en avoir 100 000 à la fin
    with open('mbx/5R.mbx', 'r') as input_file, open('mbx/5R_tmp.mbx', 'w') as output_file:
        for line in input_file:
            if 'x1 =' in line:
                output_file.write('\tx1 = '+str(x[0])+';\n')
            elif 'x2 =' in line:
                output_file.write('\tx2 = '+str(x[1])+';\n')
            else:
                output_file.write(line)

def modify_commands_mbx(x,i):

    print("x = " + str(x))

    # Si on a le temps :
    # Modifier toujours le même fichier pour éviter d'en avoir 100 000 à la fin
    with open('mbx/5R_cmd.mbx', 'r') as input_file, open('mbx/5R'+str(i)+'.mbx', 'w') as output_file:
        for line in input_file:
            if 'q1 =' in line:
                output_file.write('\tq1 = '+str(x[0])+';\n')
            elif 'q2 =' in line:
                output_file.write('\tq2 = '+str(x[1])+';\n')
            else:
                output_file.write(line)

def modify_archi_mbx(archi):

    print("x = " + str(archi))

    with open('projet1.mbx', 'r') as input_file, open('projet_calibrated.mbx', 'w') as output_file:
        for line in input_file:
            if 'a11 =' in line:
                output_file.write('\ta11 = '+str(archi[0])+';\n')
                output_file.write('\ta12 = '+str(archi[1])+';\n')
                output_file.write('\ta21 = '+str(archi[2])+';\n')
                output_file.write('\ta22 = '+str(archi[3])+';\n')

                output_file.write('\tl1 = '+str(archi[4])+';\n')
                output_file.write('\tl2 = '+str(archi[5])+';\n')
                output_file.write('\tl3 = '+str(archi[6])+';\n')
                output_file.write('\tl4 = '+str(archi[7])+';\n')

            else:
                output_file.write(line)


def solve_mbx(filename):

    # print('Creating the .cov file ....')
    solve = "ibexsolve -e 0.1 -E 1 " + str(filename) # + " -s"
    os.system(solve)


def find_commands(list, index):

    commands = []

    for i in list:
        print("list : ")
        print(i)
        # print('Reading the pose ' + str(i) +' .... ')
        modify_poses_mbx(i)

        # print('Solving the pose ' + str(i) +' .... ')
        filename = "mbx/5R_tmp.mbx"
        solve_mbx(filename)

        p = paving.Paving()

        # print('Reading the pose ' + str(i) +' .... ')
        filename = "mbx/5R_tmp.cov"
        p.from_covfile(filename)

        commands.append((p.boxes[index].vec[0], p.boxes[index].vec[2]))

        # print("Commands final : "+str(commands))

    return commands


def find_poses(list):

    print(list)
    poses = []
    index = 0

    for i in range(0,len(list),2):
        index += 1
        # print('Reading the pose ' + str(i) +' .... ')
        modify_commands_mbx([list[i], list[i+1]], index)

        # print('Solving the pose ' + str(i) +' .... ')
        filename = "mbx/5R" + str(index) + ".mbx"
        solve_mbx(filename)

        p = paving.Paving()

        # print('Reading the pose ' + str(i) +' .... ')
        filename = "mbx/5R" + str(index) + ".cov"
        p.from_covfile(filename)

        poses.append((p.boxes[0].vec[0], p.boxes[0].vec[2]))

        # print("Commands final : "+str(commands))

    return poses