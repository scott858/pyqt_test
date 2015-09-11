# -*- coding: utf-8 -*-
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

        self.continue_calculation = True

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

        self.simulation_duration_label = None
        self.simulation_duration_spin_box = None

        self.start_btn = None
        self.stop_btn = None
        self.recalculate_btn = None

        self.menu_bar = None
        self.horizontal_group_box = None
        self.grid_group_box = None
        self.file_menu = None
        self.exit_action = None

        self.plot_grid_box = None
        self.plot_widget = None
        self.plot_widget_kinetic = None
        self.plot_widget_potential = None
        self.plot_widget_fractional_total = None
        self.gl_widget = None

        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.create_menu()
        self.create_horizontal_btn_box()
        self.create_grid_box()

        self.main_layout = QtGui.QVBoxLayout()
        self.setWindowTitle("The Solar System")

        self.create_plot_grid_box()

        self.main_layout.setMenuBar(self.menu_bar)
        self.main_layout.addWidget(self.horizontal_group_box)
        self.main_layout.addWidget(self.grid_group_box)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

        self.calculate_trajectories()

        self.frame_count = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(.01)

        # Display the widget as a new window
        self.show()

        QtGui.QApplication.instance().exec_()

    def create_plot_grid_box(self):
        self.plot_grid_box = QtGui.QGroupBox("Solar Plots")
        grid_layout = QtGui.QGridLayout()
        self.plot_grid_box.setLayout(grid_layout)
        self.main_layout.addWidget(self.plot_grid_box)

        self.plot_widget = QtGui.QWidget()
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

        self.calculate_trajectories()
        self.current_position = self.trajectories[0, :, :]

        self.initialize_colors()
        self.initialize_sizes()
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
        self.scatter_plot.show()

    def create_menu(self):
        self.menu_bar = QtGui.QMenuBar()
        self.file_menu = QtGui.QMenu("File")
        self.exit_action = self.file_menu.addAction("Exit")
        self.menu_bar.addMenu(self.file_menu)
        self.exit_action.triggered.connect(self.accept)

    def create_horizontal_btn_box(self):
        self.horizontal_group_box = QtGui.QGroupBox("Simulation Control")
        layout = QtGui.QHBoxLayout()

        self.start_btn = QtGui.QPushButton("Start")
        self.start_btn.clicked.connect(self.start_calculation)
        layout.addWidget(self.start_btn)

        self.stop_btn = QtGui.QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_calculation)
        layout.addWidget(self.stop_btn)

        self.horizontal_group_box.setLayout(layout)

    def create_grid_box(self):
        self.grid_group_box = QtGui.QGroupBox("Simulation Duration")
        grid_layout = QtGui.QGridLayout()

        self.simulation_duration_label = QtGui.QLabel("Simulation Duration (years)")
        self.simulation_duration_spin_box = QtGui.QSpinBox()
        self.simulation_duration_spin_box.setValue(10)
        self.simulation_duration_spin_box.setMaximum(100000)

        self.recalculate_btn = QtGui.QPushButton("Recalculate")
        self.recalculate_btn.clicked.connect(self.calculate_trajectories)

        grid_layout.addWidget(self.simulation_duration_label, 1, 0)
        grid_layout.addWidget(self.simulation_duration_spin_box, 1, 1)
        grid_layout.addWidget(self.recalculate_btn, 1, 2)

        grid_layout.setColumnStretch(1, 10)
        grid_layout.setColumnStretch(2, 20)
        self.grid_group_box.setLayout(grid_layout)

    def calculate_trajectories(self):
        years = self.simulation_duration_spin_box.value()
        self.trajectories = ssc.run(years)
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
        self.color = np.empty((self.number_particles, 4))
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
        self.size = np.empty(self.number_particles)
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

    def start_calculation(self):
        if self.trajectories.shape[0] <= 0:
            self.calculate_trajectories()
        self.continue_calculation = True

    def stop_calculation(self):
        self.continue_calculation = False

    def update(self):
        if self.continue_calculation:
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
