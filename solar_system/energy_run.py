import numpy as np
import matplotlib.pyplot as plt

from solar_system_energy import calc_energy, kinetic, potential
import solar_system.solar_system_python as ssp
from solar_system.solar_system_cython import run

wc = run(300)
# e = calc_energy(wc, wc.shape[0])
# kinetic = np.asarray(e[0])
# potential = np.asarray(e[1])

kinetic_energy = kinetic(wc, wc.shape[0])
kinetic_energy = np.asarray(kinetic_energy)

potential_energy = potential(wc, wc.shape[0])
potential_energy = np.asarray(potential_energy)
# ssp.solar_animate(wc)

plt.figure()
# mean_kinetic = np.mean(kinetic_energy)
# plt.plot((kinetic_energy - mean_kinetic) / mean_kinetic)
plt.plot(kinetic_energy)

plt.figure()
# mean_potential = np.mean(potential_energy)
# plt.plot((potential_energy - mean_potential) / mean_potential)
plt.plot(potential_energy)

mean_kinetic = np.mean(kinetic_energy)
mean_potential = np.mean(potential_energy)
print("Virial theorem implies 2*mean_kinetic = -mean_potential")
print("Mean Kinetic: " + str(mean_kinetic))
print("Mean Potential : " + str(mean_potential))

energy = potential_energy + kinetic_energy
mean_energy = np.mean(energy)
plt.figure()
fractional_energy = (energy - mean_energy) / mean_energy
plt.plot(fractional_energy)
plt.show()
