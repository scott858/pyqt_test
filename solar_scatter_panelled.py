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


class PlotDialog(QtGui.QDialog):
    NUM_GRID_ROWS = 3
    NUM_BUTTONS = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.distance = 10 ** 11
        self.number_particles = 10
        self.number_dimensions = 3

        self.trajectories = None
        self.kinetic_energy = None
        self.potential_energy = None
        self.fractional_total_energy = None
        self.mean_total_energy = None
        self.time_points = None

        self.current_position = None
        self.size = np.zeros((self.number_particles,))
        self.color = np.zeros((self.number_particles, 4))

        self.scatter_plot = None
        self.plot_kinetic = None
        self.plot_potential = None
        self.plot_fractional_total = None

        self.labels = []
        self.line_edits = []
        self.buttons = []
        self.menu_bar = None
        self.horizontal_group_box = None
        self.grid_group_box = None
        self.form_group_box = None
        self.small_editor = None
        self.file_menu = None
        self.exit_action = None

        self.plot_grid_box = None
        self.plot_widget_kinetic = None
        self.plot_widget_potential = None
        self.plot_widget_fractional_total = None
        self.gl_widget = None

        self.big_editor = QtGui.QTextEdit()
        self.big_editor.setPlainText(
            "This widget takes up all the remaining space in the top level layout."
        )

        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_box()
        self.create_form_group_box()

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setMenuBar(self.menu_bar)
        self.main_layout.addWidget(self.horizontal_group_box)
        self.main_layout.addWidget(self.grid_group_box)
        self.main_layout.addWidget(self.form_group_box)
        self.main_layout.addWidget(self.big_editor)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Basic Layouts")

        self.initialize_colors()
        self.initialize_sizes()
        self.calc_trajectories()

        self.plot_widget = QtGui.QWidget()

        self.frame_count = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(.1)

        # Display the widget as a new window
        self.show()

        QtGui.QApplication.instance().exec_()

    def create_plot_grid_box(self):
        self.plot_grid_box = QtGui.QGroupBox("Grid Layout")
        grid_layout = QtGui.QGridLayout()
        self.main_layout.addWidget(grid_layout)

        self.plot_widget_kinetic = pg.PlotWidget()
        self.plot_widget_potential = pg.PlotWidget()
        self.plot_widget_fractional_total = pg.PlotWidget()
        self.gl_widget = gl.GLViewWidget()
        self.size_plot_widgets()

        grid_layout.addWidget(self.gl_widget, 0, 1, 1, 3)
        grid_layout.addWidget(self.plot_widget_kinetic, 2, 1, 2, 1)
        grid_layout.addWidget(self.plot_widget_potential, 2, 2, 2, 1)
        grid_layout.addWidget(self.plot_widget_fractional_total, 2, 3, 2, 1)

        self.gl_widget.opts['distance'] = self.distance
        self.gl_widget.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
        self.gl_widget.setCameraPosition(distance=10 * self.distance, azimuth=-90)

        # g = gl.GLGridItem()
        # g.setSpacing(30 * distance, 30 * distance)
        # g.setSize(150 * distance, 150 * distance)
        # w.addItem(g)

        # First example is a set of points with pxMode=False
        # These demonstrate the ability to have points with real size down to a very small scale

        self.calc_trajectories()
        self.current_position = self.trajectories[0, :, :]
        self.size = np.empty(self.number_particles)
        self.color = np.empty((self.number_particles, 4))

        self.size = self.size * self.distance / 20

        self.scatter_plot = gl.GLScatterPlotItem(pos=self.current_position,
                                                 size=self.size, color=self.color,
                                                 pxMode=False)
        self.gl_widget.addItem(self.scatter_plot)

        self.plot_kinetic = self.plot_widget_kinetic.plot()
        self.plot_widget_kinetic.setTitle("Kinetic Energy")

        self.plot_potential = self.plot_widget_potential.plot()
        self.plot_widget_potential.setTitle("Potential Energy")

        self.plot_fractional_total = self.plot_widget_fractional_total.plot()
        self.plot_widget_fractional_total.setTitle("Total Energy (fractional)")

    def create_menu(self):
        self.menu_bar = QtGui.QMenuBar()
        self.file_menu = QtGui.QMenu("File")
        self.exit_action = self.file_menu.addAction("Exit")
        self.menu_bar.addMenu(self.file_menu)
        # TODO: ?
        self.exit_action.triggered.connect(self.accept)

    def create_horizontal_group_box(self):
        self.horizontal_group_box = QtGui.QGroupBox("Horizontal Layout")
        layout = QtGui.QHBoxLayout()

        for button_index in range(self.NUM_BUTTONS):
            self.buttons.append(QtGui.QPushButton("Button {}".format(button_index + 1)))
            layout.addWidget(self.buttons[button_index])

        self.horizontal_group_box.setLayout(layout)

    def create_grid_box(self):
        self.grid_group_box = QtGui.QGroupBox("Grid Layout")
        grid_layout = QtGui.QGridLayout()

        for label_index in range(self.NUM_GRID_ROWS):
            self.labels.append(QtGui.QLabel("Line {}".format(label_index + 1)))
            self.line_edits.append(QtGui.QLineEdit())
            grid_layout.addWidget(self.labels[label_index], label_index + 1, 0)
            grid_layout.addWidget(self.line_edits[label_index], label_index + 1, 1)

        self.small_editor = QtGui.QTextEdit()
        self.small_editor.setPlainText(
            "This widget takes up about two thirds of the grid layout."
        )
        grid_layout.addWidget(self.small_editor, 0, 2, 4, 1)
        grid_layout.setColumnStretch(1, 10)
        grid_layout.setColumnStretch(2, 20)
        self.grid_group_box.setLayout(grid_layout)

    def create_form_group_box(self):
        self.form_group_box = QtGui.QGroupBox("Form Layout")
        form_layout = QtGui.QFormLayout()
        form_layout.addRow(QtGui.QLabel("Line 1:"), QtGui.QLineEdit())
        form_layout.addRow(QtGui.QLabel("Line 2:"), QtGui.QComboBox())
        form_layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.form_group_box.setLayout(form_layout)

    def calc_trajectories(self):
        self.trajectories = ssc.run(10)
        self.kinetic_energy = ssc.kinetic(self.trajectories, self.trajectories.shape[0])
        self.kinetic_energy = np.asarray(self.kinetic_energy)
        self.potential_energy = ssc.potential(self.trajectories, self.trajectories.shape[0])
        self.potential_energy = np.asarray(self.potential_energy)

        self.fractional_total_energy = self.potential_energy + self.kinetic_energy
        self.mean_total_energy = np.mean(self.fractional_total_energy)
        self.fractional_total_energy = (self.fractional_total_energy - self.mean_total_energy) / self.mean_total_energy

        self.trajectories = self.trajectories[:, :30]
        self.trajectories = self.trajectories.astype(np.float)
        self.number_particles = 10
        self.number_dimensions = 3
        self.time_points = self.trajectories.shape[0]
        self.trajectories = np.reshape(self.trajectories,
                                       (
                                           self.time_points,
                                           self.number_particles,
                                           self.number_dimensions,
                                       )
                                       )
        self.time_points = self.trajectories.shape[0]

    def size_plot_widgets(self):
        self.plot_widget_kinetic.sizeHint = self.gl_widget.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
        self.gl_widget.setSizePolicy(self.plot_widget_kinetic.sizePolicy())

        self.plot_widget_potential.sizeHint = self.gl_widget.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
        self.gl_widget.setSizePolicy(self.plot_widget_potential.sizePolicy())

        self.plot_widget_fractional_total.sizeHint = self.gl_widget.sizeHint = lambda: pg.QtCore.QSize(1000, 1000)
        self.gl_widget.setSizePolicy(self.plot_widget_fractional_total.sizePolicy())

    def initialize_colors(self):
        self.color[0] = (255, 255, 0, .75)
        self.color[1] = (255, 0, 0, .75)
        self.color[2] = (255, 0, 255, .75)
        self.color[3] = (0, 204, 255, .75)
        self.color[4] = (200, 0, 0, .75)
        self.color[5] = (50, 100, 0, .75)
        self.color[6] = (51, 0, 100, .75)
        self.color[7] = (0, 102, 255, .75)
        self.color[8] = (20, 102, 255, .75)
        self.color[9] = (100, 102, 255, .75)

    def initialize_sizes(self):
        self.size[0] = 10
        self.size[1] = .5
        self.size[2] = 2
        self.size[3] = 1.5
        self.size[4] = 1
        self.size[5] = 4
        self.size[6] = 3
        self.size[7] = 3
        self.size[8] = 3
        self.size[9] = .1

    def update(self):
        # update surface positions and colors
        if self.frame_count < self.time_points:
            self.current_position = self.trajectories[self.frame_count, :, :]
        else:
            self.frame_count = 0
            self.current_position = self.trajectories[self.frame_count, :, :]
        self.scatter_plot.setData(pos=self.current_position, size=self.size, color=self.color)
        if not self.frame_count % 10:
            self.plot_potential.setData(self.potential_energy[:self.frame_count])
            self.plot_kinetic.setData(self.kinetic_energy[:self.frame_count])
            self.plot_fractional_total.setData(self.fractional_total_energy[:self.frame_count])
        self.frame_count += 1


PlotDialog()
