import commands, calibration, robot

# Creation of the robot
r=robot.FiveBars([-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8],0,2, eps_cmd=10)
architecture = [-22.5, 0, 22.5, 0, 17.8, 17.8, 17.8, 17.8]


# 10 random points to calibrate the robot
# Ajouter fonction pour avoir des randoms sans singularité (fonction q tp 1, merci Jules !)
pose = [(3,-15), (5,-2), (8,-15), (5,17), (10,-9), (-7, 14), (-10, 9), (12, 8), (0, -5), (10, 3)]


commands = commands.find_commands(pose)

measures = calibration.make_measurements(r, commands)

calibration.calibrate(calibration.f_r, architecture, measures)
