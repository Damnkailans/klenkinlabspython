import os
import sys
import math
import subprocess
import numpy as np
from utils import bench

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

rng = np.random.default_rng(42)
print("Задача 5. Ускорение циклов с Cython\n")

# 5.1 Функция на Python
def sum_squares_py(lst):
    s = 0.0
    for x in lst:
        s += x * x
    return s

print(sum_squares_py([1.0, 2.0, 3.0]))

# 5.2 Версия на Cython и компиляция
print("\n5.2 Версия на Cython (файл sum_squares_cy.pyx) и компиляция\n")
print(open("sum_squares_cy.pyx", encoding="utf-8").read())

subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], check=True)

from sum_squares_cy import sum_squares_cy, sum_squares_cy_list

N = 10**7
arr = rng.random(N)
lst = arr.tolist()

r_py, r_cy, r_cyl, r_np = sum_squares_py(lst), sum_squares_cy(arr), sum_squares_cy_list(lst), float(arr @ arr)
print(r_py, r_cy, r_cyl, r_np)
print("результаты совпадают:", all(math.isclose(r, r_np, rel_tol=1e-9) for r in (r_py, r_cy, r_cyl)))

# 5.3 Сравнение времени на 10^7 элементов
print("\n5.3 Сравнение времени на 10^7 элементов\n")
bench('sum_squares_py(lst)', lambda: sum_squares_py(lst), number=1, repeat=3)
bench('sum_squares_cy_list(lst)', lambda: sum_squares_cy_list(lst))
bench('sum_squares_cy(arr)', lambda: sum_squares_cy(arr))
bench('arr @ arr', lambda: arr @ arr)