# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp

#cython: boundscheck=False
#cython: wraparound=False

include 'solar_system_data_cy.pxi'
from libc.math cimport pow, sqrt
from cython.parallel cimport prange
from cython cimport cdivision


cdef double[::1] r(int i, double[::1] w):
    cdef:
        int start_index, end_index
    start_index = i * number_dimensions
    end_index = (i + 1) * number_dimensions
    return w[start_index:end_index]


cdef:
    double d[3]
    double[::1] g_displacement = d
cdef double calc_potential_energy(int i, int j, double[::1] position):
    cdef:
        double[::1] masses = g_masses
        double[::1] displacement = g_displacement
        double[::1] rj = r(j, position)
        double[::1] ri = r(i, position)

        double mj, mag_displacement = 0
        double potential_energy = 0
        int k

    # exerted on i by j
    for k in range(number_dimensions):
        displacement[k] = rj[k] - ri[k]

    for k in range(number_dimensions):
        mag_displacement += displacement[k] * displacement[k]
    mag_displacement = sqrt(mag_displacement)

    mj = masses[j]
    mi = masses[i]
    with cdivision:
        potential_energy = - G * mj * mi / (mag_displacement + 1)
    return potential_energy


cdef double[::1] total_potential_energy(double[:, ::1] w, int time_points):
    cdef:
        double[::1] potential_energy = np.zeros(time_points, dtype=np.double)

        double[:, ::1] positions

        int v_start = number_dimensions * number_particles
        int i, j, k, start_index, end_index

    positions = w[:, :v_start]
    for k in range(time_points):
        for i in range(number_particles):
            start_index = i * number_dimensions
            end_index = (i + 1) * number_dimensions
            for j in range(i + 1, number_particles):
                potential_energy[k] += calc_potential_energy(i, j, positions[k, :])

    return potential_energy


cdef double calc_kinetic_energy(int j, double[::1] velocity):
    cdef:
        double[::1] masses = g_masses
        double mj, velocity_squared = 0
        double kinetic_energy = 0
        int k

    for k in range(number_dimensions):
        velocity_squared += velocity[k] * velocity[k]

    mj = masses[j]
    with cdivision:
        kinetic_energy = mj * velocity_squared / 2.

    return kinetic_energy


cdef double[::1] total_kinetic_energy(double[:, ::1] w, int time_points):
    cdef:
        double[::1] kinetic_energy = np.zeros(time_points, dtype=np.double)

        double[:, ::1] velocities

        int v_start = number_dimensions * number_particles
        int i, j, k, start_index, end_index

    velocities = w[:, v_start:]
    for k in range(time_points):
        for i in range(number_particles):
            start_index = i * number_dimensions
            end_index = (i + 1) * number_dimensions
            kinetic_energy[k] += calc_kinetic_energy(i, velocities[k, start_index:end_index])

    return kinetic_energy


cpdef calc_energy(w, time_points):
    kinetic_energy = total_kinetic_energy(w, time_points)
    potential_energy = total_potential_energy(w, time_points)
    return [kinetic_energy, potential_energy]


cpdef kinetic(w, time_points):
    return total_kinetic_energy(w, time_points)


cpdef potential(w, time_points):
    return total_potential_energy(w, time_points)
