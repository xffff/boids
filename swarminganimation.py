# 3D plot with z as total x+y velocity

from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import SwarmAgent as swarm

fig = plt.figure()
ax = axes3d.Axes3D(fig)
sw = swarm.Swarm(75)
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
wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)

def update(i, ax, fig):
    ax.cla()
    genboids()
    wframe = ax.plot_wireframe(xs, ys, zs, rstride=1, cstride=1)
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(0,2)
    return wframe,

ani = animation.FuncAnimation(fig, update, 
                              frames=xrange(100), 
                              fargs=(ax, fig), interval=100)
plt.show()
