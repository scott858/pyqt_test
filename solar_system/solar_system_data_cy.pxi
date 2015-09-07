import numpy as np

cdef:
    double m_sun = 1.9891 * 10 ** 30
    double m_mercury = 3.3020 * 10 ** 23
    double m_venus = 4.8685 * 10 ** 24
    double m_earth = 5.9736 * 10 ** 24
    double m_mars = 6.4185 * 10 ** 23
    double m_jupiter = 1.8986 * 10 ** 27
    double m_saturn = 5.98486 * 10 ** 26
    double m_uranus = 1.0243 * 10 ** 26
    double m_neptune = 8.6832 * 10 ** 25
    double m_pluto = 1.27 * 10 ** 22

    double x_sun = -7.0299 * 10 ** 8
    double x_mercury = 2.60517 * 10 ** 10
    double x_venus = 7.2129 * 10 ** 10
    double x_earth = -2.9104 * 10 ** 10
    double x_mars = -2.47064 * 10 ** 11
    double x_jupiter = 2.67553 * 10 ** 11
    double x_saturn = 6.999 * 10 ** 11
    double x_uranus = 2.65363 * 10 ** 12
    double x_neptune = 2.2993 * 10 ** 12
    double x_pluto = -1.31126 * 10 ** 12

    double y_sun = -7.5415 * 10 ** 8
    double y_mercury = -6.1102 * 10 ** 10
    double y_venus = 7.9106 * 10 ** 10
    double y_earth = 1.43576 * 10 ** 11
    double y_mars = -1.03161 * 10 ** 11
    double y_jupiter = 7.0482 * 10 ** 11
    double y_saturn = 1.16781 * 10 ** 12
    double y_uranus = -3.6396 * 10 ** 12
    double y_neptune = -1.90411 * 10 ** 12
    double y_pluto = -4.2646 * 10 ** 12

    double z_sun = 2.38988 * 10 ** 7
    double z_mercury = -7.3616 * 10 ** 9
    double z_venus = -3.0885 * 10 ** 9
    double z_earth = 2.39614 * 10 ** 7
    double z_mars = 5.8788 * 10 ** 9
    double z_jupiter = -8.911 * 10 ** 9
    double z_saturn = -4.817 * 10 ** 10
    double z_uranus = 1.37957 * 10 ** 10
    double z_neptune = -3.6864 * 10 ** 10
    double z_pluto = 8.3563 * 10 ** 11

    double vx_sun = 14.1931
    double vx_mercury = 34796
    double vx_venus = -25968.7
    double vx_earth = -29699.8
    double vx_mars = 1862.73
    double vx_jupiter = -12376.3
    double vx_saturn = -8792.6
    double vx_uranus = 4356.6
    double vx_neptune = 4293.6
    double vx_pluto = 5316.6

    double vy_sun = -6.9255
    double vy_mercury = 22185.2
    double vy_venus = 23441.6
    double vy_earth = -5883.3
    double vy_mars = -22150.6
    double vy_jupiter = 5259.2
    double vy_saturn = 4944.9
    double vy_uranus = 3233.3
    double vy_neptune = 4928.1
    double vy_pluto = -2884.6

    double vz_sun = -0.31676
    double vz_mercury = -1379.78
    double vz_venus = 1819.92
    double vz_earth = 0.050215
    double vz_mars = -509.6
    double vz_jupiter = 255.192
    double vz_saturn = 263.754
    double vz_uranus = -166.986
    double vz_neptune = -37.32
    double vz_pluto = -1271.99

    double ti = 0
    double days_per_year = 365
    double hours_per_day = 24
    double seconds_per_hour = 3600
    double dt = 24 * 3600
    double G = 6.67 * 10 ** (-11.0)
    int number_dimensions = 3

m = np.array(
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

cdef int number_particles = len(m)
cdef double[::1] g_masses = m

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
