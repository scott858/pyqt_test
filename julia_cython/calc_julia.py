import numpy as np
import matplotlib.pyplot as plt

import julia

jl = julia.calc_julia(1.5, 4000, (0.322 + 0.05j), 2.25, 1000)
area = julia.julia_fraction(jl)
print(area)

plt.imshow(np.log(jl))
plt.show()
