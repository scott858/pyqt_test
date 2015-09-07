import numpy as np

m_sun = 1.9891 * 10 ** 30
m_mercury = 3.3020 * 10 ** 23
m_venus = 4.8685 * 10 ** 24
m_earth = 5.9736 * 10 ** 24
m_mars = 6.4185 * 10 ** 23
m_jupiter = 1.8986 * 10 ** 27
m_saturn = 5.98486 * 10 ** 26
m_uranus = 1.0243 * 10 ** 26
m_neptune = 8.6832 * 10 ** 25
m_pluto = 1.27 * 10 ** 22

x_sun = -7.0299 * 10 ** 8
x_mercury = 2.60517 * 10 ** 10
x_venus = 7.2129 * 10 ** 10
x_earth = -2.9104 * 10 ** 10
x_mars = -2.47064 * 10 ** 11
x_jupiter = 2.67553 * 10 ** 11
x_saturn = 6.999 * 10 ** 11
x_uranus = 2.65363 * 10 ** 12
x_neptune = 2.2993 * 10 ** 12
x_pluto = -1.31126 * 10 ** 12

y_sun = -7.5415 * 10 ** 8
y_mercury = -6.1102 * 10 ** 10
y_venus = 7.9106 * 10 ** 10
y_earth = 1.43576 * 10 ** 11
y_mars = -1.03161 * 10 ** 11
y_jupiter = 7.0482 * 10 ** 11
y_saturn = 1.16781 * 10 ** 12
y_uranus = -3.6396 * 10 ** 12
y_neptune = -1.90411 * 10 ** 12
y_pluto = -4.2646 * 10 ** 12

z_sun = 2.38988 * 10 ** 7
z_mercury = -7.3616 * 10 ** 9
z_venus = -3.0885 * 10 ** 9
z_earth = 2.39614 * 10 ** 7
z_mars = 5.8788 * 10 ** 9
z_jupiter = -8.911 * 10 ** 9
z_saturn = -4.817 * 10 ** 10
z_uranus = 1.37957 * 10 ** 10
z_neptune = -3.6864 * 10 ** 10
z_pluto = 8.3563 * 10 ** 11

vx_sun = 14.1931
vx_mercury = 34796
vx_venus = -25968.7
vx_earth = -29699.8
vx_mars = 1862.73
vx_jupiter = -12376.3
vx_saturn = -8792.6
vx_uranus = 4356.6
vx_neptune = 4293.6
vx_pluto = 5316.6

vy_sun = -6.9255
vy_mercury = 22185.2
vy_venus = 23441.6
vy_earth = -5883.3
vy_mars = -22150.6
vy_jupiter = 5259.2
vy_saturn = 4944.9
vy_uranus = 3233.3
vy_neptune = 4928.1
vy_pluto = -2884.6

vz_sun = -0.31676
vz_mercury = -1379.78
vz_venus = 1819.92
vz_earth = 0.050215
vz_mars = -509.6
vz_jupiter = 255.192
vz_saturn = 263.754
vz_uranus = -166.986
vz_neptune = -37.32
vz_pluto = -1271.99

masses = np.array(
    [
        m_sun,
        m_mercury,
        m_venus,
        m_earth,
        m_mars,
        m_jupiter,
        m_saturn,
        m_uranus,
        m_neptune,
        m_pluto
    ],
    dtype=np.double
)

x0 = np.array(
    [
        x_sun,
        x_mercury,
        x_venus,
        x_earth,
        x_mars,
        x_jupiter,
        x_saturn,
        x_uranus,
        x_neptune,
        x_pluto
    ],
    dtype=np.double
)

y0 = np.array(
    [
        y_sun,
        y_mercury,
        y_venus,
        y_earth,
        y_mars,
        y_jupiter,
        y_saturn,
        y_uranus,
        y_neptune,
        y_pluto
    ],
    dtype=np.double
)

z0 = np.array(
    [
        z_sun,
        z_mercury,
        z_venus,
        z_earth,
        z_mars,
        z_jupiter,
        z_saturn,
        z_uranus,
        z_neptune,
        z_pluto
    ],
    dtype=np.double
)

vx0 = np.array(
    [
        vx_sun,
        vx_mercury,
        vx_venus,
        vx_earth,
        vx_mars,
        vx_jupiter,
        vx_saturn,
        vx_uranus,
        vx_neptune,
        vx_pluto
    ],
    dtype=np.double
)

vy0 = np.array(
    [
        vy_sun,
        vy_mercury,
        vy_venus,
        vy_earth,
        vy_mars,
        vy_jupiter,
        vy_saturn,
        vy_uranus,
        vy_neptune,
        vy_pluto
    ],
    dtype=np.double
)

vz0 = np.array(
    [
        vz_sun,
        vz_mercury,
        vz_venus,
        vz_earth,
        vz_mars,
        vz_jupiter,
        vz_saturn,
        vz_uranus,
        vz_neptune,
        vz_pluto
    ],
    dtype=np.double
)

ti = 0
years = 10
days_per_year = 365
hours_per_day = 24
seconds_per_hour = 3600
tf = years * days_per_year * hours_per_day * seconds_per_hour
time_interval = tf - ti
dt = 24 * 3600
G = 6.67 * 10 ** -11

number_particles = len(masses)
number_dimensions = 3
