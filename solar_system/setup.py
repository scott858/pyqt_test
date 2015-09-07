from distutils.core import setup
from Cython.Build import cythonize

setup(name='solar_system_derivative',
      ext_modules=cythonize('solar_system_derivative.pyx'))
