# -*- coding: utf-8 -*-
"""
Demonstrates use of GLScatterPlotItem with rapidly-updating plots.

"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
from solar_system import solar_system_cython as ssc

app = QtGui.QApplication([])
wgl = gl.GLViewWidget()
distance = 10 ** 11
wgl.opts['distance'] = distance
wgl.show()
wgl.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
wgl.setCameraPosition(distance=10 * distance, azimuth=-90)

# g = gl.GLGridItem()
# g.setSpacing(30 * distance, 30 * distance)
# g.setSize(150 * distance, 150 * distance)
# w.addItem(g)


##
##  First example is a set of points with pxMode=False
##  These demonstrate the ability to have points with real size down to a very small scale
##

trajectories = ssc.run(10)
trajectories = trajectories[:, :30]
trajectories = trajectories.astype(np.float)
number_particles = 10
number_dimensions = 3
time_points = trajectories.shape[0]
trajectories = np.reshape(trajectories, (time_points, number_particles, number_dimensions))
current_position = trajectories[0, :, :]
# pos = pos.T
# pos = np.array([[10**6, 10**12, 10**11]], dtype=np.float64)
size = np.empty(number_particles)
color = np.empty((number_particles, 4))

d = 6.0
color[0] = (255, 255, 0, .75)
color[1] = (255, 0, 0, .75)
color[2] = (255, 0, 255, .75)
color[3] = (0, 204, 255, .75)
color[4] = (200, 0, 0, .75)
color[5] = (50, 100, 0, .75)
color[6] = (51, 0, 100, .75)
color[7] = (0, 102, 255, .75)
color[8] = (20, 102, 255, .75)
color[9] = (100, 102, 255, .75)

size[0] = 10
size[1] = .5
size[2] = 2
size[3] = 1.5
size[4] = 1
size[5] = 4
size[6] = 3
size[7] = 3
size[8] = 3
size[9] = .1

size = size * distance / 20

sp = gl.GLScatterPlotItem(pos=current_position, size=size, color=color, pxMode=False)
wgl.addItem(sp)

frame_count = 0


def update():
    ## update surface positions and colors
    global sp, d, current_position, frame_count
    if frame_count < time_points:
        pos = trajectories[frame_count, :, :]
    sp.setData(pos=pos, size=size, color=color)
    frame_count += 1


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(.1)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
