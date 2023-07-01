def getCynByAxis(redius = 1, heightStart = 0, heightEnd = 5, \
    offset = [0, 0, 0], devision = 20, mainAxis = 'z'):
    '''NyanNyanNyan'''
    import numpy as np

    mainAxis = mainAxis.lower()

    theta = np.linspace(0, 2*np.pi, devision)
    cz = np.array([redius * np.cos(theta)])
    cy = np.array([heightStart, heightEnd])
    cz, cy = np.meshgrid(cz, cy)
    cx = np.array([redius * np.sin(theta)] * 2)

    if mainAxis == 'z':
        return offset[0] + cx, offset[1] + cy, offset[2] + cz
    elif mainAxis == 'y':
        return offset[0] + cx, offset[1] + cz, offset[2] + cy
    elif mainAxis == 'x':
        return offset[0] + cz, offset[1] + cy, offset[2] + cx
    else:
        raise ValueError("'x', 'y' or 'z' PLZ")

def drawCylinder():
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np

    cx, cy, cz = getCynByAxis(offset = [1, 1, 1], devision = 40,\
        mainAxis = 'x', heightEnd = 6, heightStart = 2,\
        redius = 1.0)

    fig = plt.figure(figsize = (11, 10))
    ax = plt.axes(projection = '3d')
    ax.plot_surface(cx, cy, cz, rstride = 1, cstride = 1,\
        linewidth = 0, alpha = 0.25)
    ax.set_xlim(-3, 5)
    ax.set_ylim(-3, 5)
    ax.set_zlim(-3, 10)
    plt.xlabel("x")

    plt.ylabel("y")
    x = [0,1,2,1.5,2]
    y = [0,1,0,1.5,3]
    z = [3,-2,2,8,2]
    plt.plot(x, y, z,'*')
    plt.show()

if __name__ == '__main__':
    drawCylinder()
