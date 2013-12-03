# 3D plot with z as total x+y velocity

from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import SwarmAgent as swarm

fig = plt.figure()
ax = axes3d.Axes3D(fig)
sw = swarm.Swarm(25)
xs = None
ys = None
zs = None
co = None

def genboids():
    global co,xs,ys,zs
    co = sw.getBoids()
    xs = [i for i in co[0]]
    ys = [i for i in co[1]]
    zs = np.add(co[2], co[3])
       
genboids()
X, Y = np.meshgrid(xs, ys)
Z = zs
wframe = ax.plot_surface(X,Y,Z)

def update(i, ax, fig):
    global xs,ys,zs
    ax.cla()
    genboids()
    X, Y = np.meshgrid(xs, ys)
    Z = zs
    wframe = ax.plot_surface(X,Y,Z,cmap=cm.jet,linewidth=0,alpha=0.6)
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(-1,1)
    return wframe,

ani = animation.FuncAnimation(fig, update, 
                              frames=xrange(10), 
                              fargs=(ax, fig), interval=10)
plt.show()
