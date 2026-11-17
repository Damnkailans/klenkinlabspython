# cython: boundscheck=False, wraparound=False, cdivision=True
"""Задача 5: сумма квадратов элементов на Cython."""


def sum_squares_cy(double[::1] arr):
    """Версия с типизированным memoryview (быстрая): принимает ndarray float64."""
    cdef Py_ssize_t i, n = arr.shape[0]
    cdef double s = 0.0
    for i in range(n):
        s += arr[i] * arr[i]
    return s


def sum_squares_cy_list(list lst):
    """Версия для обычного Python-списка: типизированы счётчик и аккумулятор."""
    cdef Py_ssize_t i, n = len(lst)
    cdef double s = 0.0
    cdef double x
    for i in range(n):
        x = lst[i]
        s += x * x
    return s
