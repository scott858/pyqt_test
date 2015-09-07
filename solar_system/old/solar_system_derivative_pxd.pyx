# cython: profile=True
include 'solar_system_data.pxi'
from libc.math cimport pow, sqrt
# cimport solar_system_data_cy as ssd
import numpy as np

earth_vector = np.array([ssd.x_earth, ssd.y_earth, ssd.z_earth])

cdef  double earth_distance

masses = np.array(
    [
        ssd.m_sun,
        ssd.m_mercury,
        ssd.m_venus,
        ssd.m_earth,
        ssd.m_mars,
        ssd.m_jupiter,
        ssd.m_saturn,
        ssd.m_uranus,
        ssd.m_neptune,
        ssd.m_pluto
    ],
    dtype=np.double
)

cdef int number_particles = len(masses)

vz0 = np.array(
    [
        ssd.vz_sun,
        ssd.vz_mercury,
        ssd.vz_venus,
        ssd.vz_earth,
        ssd.vz_mars,
        ssd.vz_jupiter,
        ssd.vz_saturn,
        ssd.vz_uranus,
        ssd.vz_neptune,
        ssd.vz_pluto
    ],
    dtype=np.double
)

x0 = np.array(
    [
       ssd.x_sun,
       ssd.x_mercury,
       ssd.x_venus,
       ssd.x_earth,
       ssd.x_mars,
       ssd.x_jupiter,
       ssd.x_saturn,
       ssd.x_uranus,
       ssd.x_neptune,
       ssd.x_pluto
    ],
    dtype=np.double
)

y0 = np.array(
    [
       ssd.y_sun,
       ssd.y_mercury,
       ssd.y_venus,
       ssd.y_earth,
       ssd.y_mars,
       ssd.y_jupiter,
       ssd.y_saturn,
       ssd.y_uranus,
       ssd.y_neptune,
       ssd.y_pluto
    ],
    dtype=np.double
)

z0 = np.array(
    [
        ssd.z_sun,
        ssd.z_mercury,
        ssd.z_venus,
        ssd.z_earth,
        ssd.z_mars,
        ssd.z_jupiter,
        ssd.z_saturn,
        ssd.z_uranus,
        ssd.z_neptune,
        ssd.z_pluto
    ],
    dtype=np.double
)

vx0 = np.array(
    [
        ssd.vx_sun,
        ssd.vx_mercury,
        ssd.vx_venus,
        ssd.vx_earth,
        ssd.vx_mars,
        ssd.vx_jupiter,
        ssd.vx_saturn,
        ssd.vx_uranus,
        ssd.vx_neptune,
        ssd.vx_pluto
    ],
    dtype=np.double
)

vy0 = np.array(
    [
        ssd.vy_sun,
        ssd.vy_mercury,
        ssd.vy_venus,
        ssd.vy_earth,
        ssd.vy_mars,
        ssd.vy_jupiter,
        ssd.vy_saturn,
        ssd.vy_uranus,
        ssd.vy_neptune,
        ssd.vy_pluto
    ],
    dtype=np.double
)

cdef int phase_index = 2
cdef int start_v_index = number_particles * ssd.number_dimensions

w0 = np.array([], dtype=np.double)
for x0i, y0i, z0i in zip(x0, y0, z0):
    w0 = np.concatenate([w0, [x0i], [y0i], [z0i]])
for vx0i, vy0i, vz0i in zip(vx0, vy0, vz0):
    w0 = np.concatenate([w0, [vx0i], [vy0i], [vz0i]])

t = np.arange(0, ssd.time_interval, ssd.dt, dtype=np.double)


cdef double[:] r_cy(int i, double[:] w):
    cdef:
        int start_index, end_index
    start_index = i * ssd.number_dimensions
    end_index = (i + 1) * ssd.number_dimensions

    cdef double[:] ri = np.empty(end_index - start_index, dtype=np.double)
    ri = w[start_index:end_index]
    return ri


cdef double[:] my_subtract(double[:] x, double[:] y):
    cdef:
        int i
        double[:] x_minus_y = np.empty(x.shape[0], dtype=np.double)

    for i in range(x.shape[0]):
        x_minus_y[i] = x[i] - y[i]

    return x_minus_y


cdef double[:] central_force(int i, int j, double[:] w):
    cdef:
        double mj, mag_displacement = 0
        double force_coefficient
        int k
    # exerted on i by j
    rj = r_cy(j, w)
    ri = r_cy(i, w)
    displacement = my_subtract(rj, ri)

    for k in range(displacement.shape[0]):
        mag_displacement += displacement[k] * displacement[k]
    mag_displacement = sqrt(mag_displacement)

    mj = masses[j]
    force_coefficient = ssd.G * mj / (pow(mag_displacement, 3))

    for k in range(displacement.shape[0]):
        displacement[k] = force_coefficient * displacement[k]
    return displacement


cdef double[:] f_core(double[:] w):
    cdef:
        int v_start, i, j, start_index, end_index
        double[:] particle_force = np.empty(ssd.number_dimensions, dtype=np.double)
        double[:] central_force_ij = np.empty(ssd.number_dimensions, dtype=np.double)
        double[:] w_ = np.empty(w.shape[0], np.double)
    v_start = ssd.number_dimensions * number_particles
    w_[:v_start] = w[v_start:]
    for i in range(number_particles):
        particle_force[0] = 0
        particle_force[1] = 0
        particle_force[2] = 0

        start_index = i * ssd.number_dimensions + v_start
        end_index = (i + 1) * ssd.number_dimensions + v_start
        for j in range(0, i):
            central_force_ij = central_force(i, j, w)
            particle_force[0] += central_force_ij[0]
            particle_force[1] += central_force_ij[1]
            particle_force[2] += central_force_ij[2]
        for j in range(i + 1, number_particles):
            central_force_ij = central_force(i, j, w)
            particle_force[0] += central_force_ij[0]
            particle_force[1] += central_force_ij[1]
            particle_force[2] += central_force_ij[2]
        w_[start_index:end_index] = particle_force
    return w_


def f(w, t):
    # f = dv / dt
    return np.asarray(f_core(np.asarray(w, dtype=np.double)), dtype=np.double)


def v(int i, w):
    cdef:
        int start_index, end_index
    start_index = i * ssd.number_dimensions
    end_index = (i + 1) * ssd.number_dimensions
    vi = w[start_v_index + start_index:end_index]
    return vi


def r(int i, w):
    cdef:
        int start_index, end_index
    start_index = i * ssd.number_dimensions
    end_index = (i + 1) * ssd.number_dimensions

    ri = w[start_index:end_index]
    return ri


