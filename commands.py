import robot, os, fileinput, paving, calibration, math

# Creation of the robot
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=10)
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]


# 10 random points to calibrate the robot
# Ajouter fonction pour avoir des randoms sans singularité (fonction q tp 1, merci Jules !)
x = [(3,-15), (5,-2), (8,-15), (5,17), (10,-9), (-7, 14), (-10, 9), (12, 8), (0, -5), (10, 3)]

def degree(x):
    pi=math.pi
    degree=(x*180)/pi
    return degree

def modify_mbx(x):

    # Si on a le temps :
    # Modifier toujours le même fichier pour éviter d'en avoir 100 000 à la fin
    with open('mbx/5R.mbx', 'r') as input_file, open('mbx/5R'+str(x[0])+'-'+str(x[1])+'.mbx', 'w') as output_file:
        for line in input_file:
            if 'x1 =' in line:
                output_file.write('\tx1 = '+str(x[0])+';\n')
            elif 'x2 =' in line:
                output_file.write('\tx2 = '+str(x[1])+';\n')
            else:
                output_file.write(line)


def solve_mbx(filename):

    print('Creating the .cov file ....')
    solve = "ibexsolve " + str(filename) + " -s"
    os.system(solve)


def find_commands(list):

    commands = []

    for i in list:
        print('Reading the pose ' + str(i) +' .... ')
        modify_mbx(i)

        print('Solving the pose ' + str(i) +' .... ')
        filename = "mbx/5R" + str(i[0]) + '-' + str(i[1]) + ".mbx"
        solve_mbx(filename)

        p = paving.Paving()

        print('Reading the pose ' + str(i) +' .... ')
        filename = "mbx/5R" + str(i[0]) + '-' + str(i[1]) + ".cov"
        p.from_covfile(filename)

        commands.append((p.boxes[0].vec[0], p.boxes[0].vec[2]))

        print("Commands final : "+str(commands))

    return commands

# modify_mbx(y)
commands = find_commands(x)

measures = calibration.make_measurements(r, commands)

kineticF = calibration.f_r(architecture, x[0], commands[0])
calibration.calibrate(kineticF, architecture, measures)
