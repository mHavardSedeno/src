import matplotlib.pyplot as plt

figure, axes = plt.subplots()
plt.xlim(-27,27)
plt.ylim(-40,40)

circles = [(-12, -6, 1.5), (-6, 18, 0.4), (6, -12, 2.8), (-12, 0, 1.1), (0, -24, 2.4), (6, -6, 0.4), (-12, 6, 1.8), (0, -12, 1.9), (6, 0, 1.9), (-6, -18, 2.8), (0, -6, 0.5), (6, 6, 0.3), (-6, -12, 2.9), (0, 0, 1.8), (6, 12, 2.3), (-6, -6, 0.6), (0, 6, 2.9), (6, 18, 1.2), (-6, 0, 1.6), (0, 12, 1.7), (12, -6, 2.8), (-6, 6, 0.4), (0, 24, 0.5), (12, 0, 1.3), (-6, 12, 1.9), (6, -18, 1.9), (12, 6, 2.1)]
for i in circles:
    print(i)
    c = plt.Circle((i[0], i[1]), i[2], color='red' )
    axes.add_artist(c)

# c2 = plt.Circle((-6 , 18 ), 0.4, color='red' )
# c3 = plt.Circle((6 , -12 ), 2.8, color='red' )

axes.set_aspect(1)
# axes.add_artist(c1)
# axes.add_artist(c2)
# axes.add_artist(c3)



plt.title( 'Obstacles' )
plt.show()


'''


'''
