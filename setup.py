import os
import sys
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) == 1:
    sys.argv += ["build_ext", "--inplace"]

setup(
    ext_modules=cythonize(
        Extension("sum_squares_cy", ["sum_squares_cy.pyx"],
                  include_dirs=[np.get_include()]),
        language_level=3,
    )
)