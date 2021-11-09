import paving
from matplotlib import pyplot
from scipy.sparse.csgraph import dijkstra

# ajouter les singularités dans les contraintes
# jacobienne² > 0

p = paving.Paving()
p.from_covfile("projet.cov")

fig1,ax1 = pyplot.subplots()
p.draw2D(ax1, 1, 2)
ax1.axis(p.hull([1,2]))

fig1.show()
# input("Press [ENTER] to continue ...")

m = p.adjacency_matrix()

dijkstra(m, directed=False)
