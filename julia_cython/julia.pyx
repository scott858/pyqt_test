#distutils: extra_compile_args = -fopenmp
#distutils: extra_link_args = -fopenmp

from cython import boundscheck, wraparound
import numpy as np
from cython.parallel cimport prange

cdef int escape(double complex z,
                double complex c,
                double z_max,
                int n_max) nogil:
    cdef:
        int i = 0
        double z_max2 = z_max * z_max

    while norm2(z) < z_max2 and i < n_max:
        z = z * z + c
        i += 1

    return i

cdef  inline double norm2(double complex z) nogil:
    return z.real * z.real + z.imag + z.imag


@boundscheck(False)
@wraparound(False)
def calc_julia(double bound,
               int resolution,
               double complex c,
               double z_max,
               int n_max):
    cdef:
        double step = 2.0 * bound /resolution
        double complex z
        int i, j
        double real, imag
        int[:, ::1] counts

    counts = np.zeros((resolution + 1, resolution + 1), dtype=np.int32)

    for i in prange(resolution + 1, nogil=True,
                    schedule='static', chunksize=1):
    # for i in range(resolution + 1):
        real = -bound +  i * step
        for j in range(resolution + 1):
            imag = -bound + j * step
            z = real + imag * 1j
            counts[i,j] = escape(z, c, z_max, n_max)
    return np.asarray(counts)

@boundscheck(False)
@wraparound(False)
def julia_fraction(int[:, ::1] counts, int maxval=1000):
    cdef:
        int total = 0
        int i, j, N, M
    N = counts.shape[0]; M = counts.shape[1]
    for i in prange(N, nogil=True):
        for j in range(M):
            if counts[i, j] == maxval:
                total += 1
    return total / float(counts.size)
