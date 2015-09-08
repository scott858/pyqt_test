# -*- coding: utf-8 -*-
"""
Demonstrates use of GLScatterPlotItem with rapidly-updating plots.

"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from solar_system import solar_system_cython as ssc

app = QtGui.QApplication([])

## Define a top-level widget to hold everything
wq = QtGui.QWidget()

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
wq.setLayout(layout)

## Create some widgets to be placed inside
w_plot_kinetic = pg.PlotWidget()
w_plot_potential = pg.PlotWidget()
w_plot_fractional_total = pg.PlotWidget()
wgl = gl.GLViewWidget()

w_plot_kinetic.sizeHint = wgl.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
wgl.setSizePolicy(w_plot_kinetic.sizePolicy())

w_plot_potential.sizeHint = wgl.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
wgl.setSizePolicy(w_plot_potential.sizePolicy())

w_plot_fractional_total.sizeHint = wgl.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
wgl.setSizePolicy(w_plot_fractional_total.sizePolicy())

compute_btn = QtGui.QPushButton('Calculate')
calc_type_btn = QtGui.QPushButton('Choose Calculation')

layout.addWidget(compute_btn, 0, 0)
layout.addWidget(calc_type_btn, 2, 0)
layout.addWidget(wgl, 0, 1, 1, 3)
layout.addWidget(w_plot_kinetic, 2, 1, 2, 1)
layout.addWidget(w_plot_potential, 2, 2, 2, 1)
layout.addWidget(w_plot_fractional_total, 2, 3, 2, 1)


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
kinetic_energy = ssc.kinetic(trajectories, trajectories.shape[0])
kinetic_energy = np.asarray(kinetic_energy)
potential_energy = ssc.potential(trajectories, trajectories.shape[0])
potential_energy = np.asarray(potential_energy)

fractional_total_energy = potential_energy + kinetic_energy
mean_total_energy = np.mean(fractional_total_energy)
fractional_total_energy = (fractional_total_energy - mean_total_energy) / mean_total_energy

trajectories = trajectories[:, :30]
trajectories = trajectories.astype(np.float)
number_particles = 10
number_dimensions = 3
time_points = trajectories.shape[0]
trajectories = np.reshape(trajectories, (time_points, number_particles, number_dimensions))
pos = trajectories[0, :, :]
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

sp = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
wgl.addItem(sp)

plot_kinetic = w_plot_kinetic.plot()
w_plot_kinetic.setTitle("Kinetic Energy")

plot_potential = w_plot_potential.plot()
w_plot_potential.setTitle("Potential Energy")

plot_fractional_total = w_plot_fractional_total.plot()
w_plot_fractional_total.setTitle("Total Energy (fractional)")

frame_count = 0


def update():
    ## update surface positions and colors
    global sp, d, pos, frame_count
    if frame_count < time_points:
        pos = trajectories[frame_count, :, :]
    else:
        frame_count = 0
    sp.setData(pos=pos, size=size, color=color)
    if not frame_count % 10:
        plot_potential.setData(potential_energy[:frame_count])
        plot_kinetic.setData(kinetic_energy[:frame_count])
        plot_fractional_total.setData(fractional_total_energy[:frame_count])
    frame_count += 1


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(.1)

## Display the widget as a new window
wq.show()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
