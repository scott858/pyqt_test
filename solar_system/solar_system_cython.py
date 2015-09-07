# cython: profile=True
from solar_system.solar_system_derivative import f, get_w0, get_t


from scipy.integrate import odeint as sp_odeint

def run(years):
    # w, s = sp_odeint(f, w0, t, full_output=True)
    w = sp_odeint(f, get_w0(), get_t(years))
    return w


if __name__ == '__main__':
    import cProfile

    cProfile.run('run()', sort='time')
