# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp

#cython: boundscheck=False
#cython: wraparound=False

include 'solar_system_data_cy.pxi'
from libc.math cimport pow, sqrt
from cython.parallel cimport prange
from cython cimport cdivision


cpdef get_t(double years):
    cdef:
        double tf = years * days_per_year * hours_per_day * seconds_per_hour
        double time_interval = tf - ti
    return np.arange(0, time_interval, dt, dtype=np.double)


cpdef get_w0():
    w0 = np.array([], dtype=np.double)
    for x0i, y0i, z0i in zip(x0, y0, z0):
        w0 = np.concatenate([w0, [x0i], [y0i], [z0i]])
    for vx0i, vy0i, vz0i in zip(vx0, vy0, vz0):
        w0 = np.concatenate([w0, [vx0i], [vy0i], [vz0i]])
    return w0


cdef double[::1] r(int i, double[::1] w):
    cdef:
        int start_index, end_index
    start_index = i * number_dimensions
    end_index = (i + 1) * number_dimensions
    return w[start_index:end_index]


cdef:
    double d[3]
    double[::1] g_displacement = d
    double c[3]
    double[::1] g_central_force_ij = c
cdef void calc_central_force(int i, int j, double[::1] w):
    cdef:
        double[::1] masses = g_masses
        double[::1] displacement = g_displacement
        double[::1] central_force_ij = g_central_force_ij
        double[::1] rj = r(j, w)
        double[::1] ri = r(i, w)

        double mj, mag_displacement = 0
        double force_coefficient
        int k

    # exerted on i by j
    for k in range(number_dimensions):
        displacement[k] = rj[k] - ri[k]

    for k in range(number_dimensions):
        mag_displacement += displacement[k] * displacement[k]
    mag_displacement = sqrt(mag_displacement)

    mj = masses[j]
    with cdivision:
        force_coefficient = G * mj / (pow(mag_displacement, 3) + 1)

    for k in range(number_dimensions):
        central_force_ij[k] = force_coefficient * displacement[k]


cdef double[::1] f_core(double[::1] w):
    cdef:
        double[::1] central_force_ij = g_central_force_ij
        double[::1] w_ = np.zeros(2 * number_dimensions * number_particles, np.double)
        double p[3]
        double[::1] particle_force = p

        int v_start = number_dimensions * number_particles
        int i, j, start_index, end_index

    w_[:v_start] = w[v_start:]
    for i in range(number_particles):
        particle_force[...] = 0

        start_index = i * number_dimensions + v_start
        end_index = (i + 1) * number_dimensions + v_start
        for j in range(0, i):
            calc_central_force(i, j, w)
            particle_force[0] += central_force_ij[0]
            particle_force[1] += central_force_ij[1]
            particle_force[2] += central_force_ij[2]
        for j in range(i + 1, number_particles):
            calc_central_force(i, j, w)
            particle_force[0] += central_force_ij[0]
            particle_force[1] += central_force_ij[1]
            particle_force[2] += central_force_ij[2]
        w_[start_index:end_index] = particle_force[:]
    return w_


cpdef f(w, t):
    # f = dv / dt
    return f_core(w)
