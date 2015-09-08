from scipy.integrate import odeint as sp_odeint

from solar_system.solar_system_derivative import f, get_w0, get_t
from solar_system.solar_system_energy import kinetic, potential


def run(years):
    # w, s = sp_odeint(f, w0, t, full_output=True)
    w = sp_odeint(f, get_w0(), get_t(years))
    return w
