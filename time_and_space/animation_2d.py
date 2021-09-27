from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
import random

def spiraling(time = True):
    fig = plt.figure()
    ax = plt.subplot()

    N=400
    l=N
    int=0.03
    space_factor=200
    t = np.arange(N)*int
    t=np.linspace(0,np.pi*2,N)
    mp4_name = "spiraling_flip.mp4"


    # p = get_saw_dimerization(N, 16, 2)
    # x, y = zip(*zip(*sorted(p.items(), key=operator.itemgetter(1)))[0])
    # p=sorted(zip(t,np.array(x)*int,np.array(y)*int))
    dir=[-2*int,-int,int,3*int]
    x=[0]
    for j in range(len(t)-1):
        x.append(x[-1]+random.choice(dir))
    x=np.cos(t)*int*space_factor
    #print x
    y=[0]
    for j in range(len(t)-1):
        y.append(y[-1]+random.choice(dir))
    y=np.sin(t)*int*space_factor
    p=sorted(zip(x,y,t))
    p=sorted(zip(t,x,y))

    #t = np.arange(0, .075, 0.00001)
    nverts = len(t)
    theta = np.array(range(nverts)) * (2*np.pi)/(nverts-1)
    theta = 90*np.pi*t
    xoffset, yoffset = .5, .5
    y = 1.4*t * np.sin(theta) + yoffset
    x = t * np.cos(theta) + xoffset
    p=sorted(zip(t, x, y))
    p=sorted(zip(x,y,t))

    def update(num, data, line):
        low=num-l if num-l>0 else 0

        line.set_data(data[:2, low:num])
        #line.set_3d_properties(data[2, low:num])


    # N = 100
    # data = np.array(list(gen(N))).T
    data = np.array(p).T[1:, :]
    line, = ax.plot(data[0, 0:1], data[1, 0:1], '.', markersize=12)

    # Setting the axes properties
    ax.set_xlim([-int*space_factor, int*space_factor])
    ax.set_xlabel('X')

    ax.set_ylim([-int*space_factor, int*space_factor])
    ax.set_ylabel('Y')

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=36)

    ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=1, blit=False)

    ani.save(mp4_name, writer=writer)

    # ani.save('matplot003.gif', writer='imagemagick')
    plt.show()


    # points = random_choice()
    # points = spiral_choice()
    # points = sphere_choice()

    # Setting the axes properties
    # ax.set_xlim3d([-int * space_factor, int * space_factor])
    # ax.set_xlabel('X')
    #
    # ax.set_ylim3d([-int * space_factor, int * space_factor])
    # ax.set_ylabel('Y')
    #
    # ax.set_zlim3d([-int * space_factor, int * space_factor])
    # ax.set_zlabel('Z')


    # def random_choice():
    #     x = [0]
    #     for j in range(len(t) - 1):
    #         x.append(x[-1] + random.choice([-int, int]))
    #     y = [0]
    #     for j in range(len(t) - 1):
    #         y.append(y[-1] + random.choice([-int, int]))
    #     z = [0]
    #     for j in range(len(t) - 1):
    #         z.append(z[-1] + random.choice([-int, int]))
    #     p = get_saw_dimerization(N, 16, 3)
    #     x, y, z = zip(*zip(*sorted(p.items(), key=operator.itemgetter(1)))[0])
    #     p = sorted(zip(t, np.array(x) * int, np.array(y) * int, np.array(z) * int))
    #     p = sorted(zip(np.array(x) * int, t * int, np.array(y) * int, np.array(z) * int))
    #     print p
    #     return p
    #
    #
    # def spiral_choice():
    #     t = np.linspace(-np.pi * 12, np.pi * 12, N)
    #     s = np.linspace(1, 0, N)
    #     x = (np.cos(t) * int * space_factor) * s
    #     y = (np.sin(t) * int * space_factor) * s
    #     z = np.linspace(-space_factor * int, space_factor * int, N)
    #     p = sorted(zip(x, t * int, y, z))
    #     # p = sorted(zip(t * int,x, y, z))
    #     p = sorted(zip(z, t * int, x, y))
    #     return p
    #
    #
    # def sphere_choice():
    #     rs = np.linspace(1, 1, N)
    #     thetas = np.linspace(0, 2 * np.pi, N)
    #     phis = np.linspace(0, 2 * np.pi, N)
    #     x, y, z = [], [], []
    #     for r in rs:
    #         for theta in thetas:
    #             for phi in phis:
    #                 x.append(r * np.sin(theta) * np.cos(phi))
    #                 y.append(r * np.sin(theta) * np.sin(phi))
    #                 z.append(r * np.cos(theta))
    #
    #     t = np.linspace(0, int * space_factor, N)
    #     x = (np.cos(t) * int * space_factor) + t * int
    #     p = sorted(zip(t, x, y, z))
    #     return p


    # points = {0: object}
    # for i in range(1, t_final):
    #     points[i] = []
    #     for point in points[i-1]:
    #         points[i].append(advance(point))