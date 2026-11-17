import timeit
import numpy as np
import scipy.sparse as sp
from utils import bench

rng = np.random.default_rng(42)
print("Задача 4. Разреженные матрицы\n")

# 4.1 Матрица 5x5 с плотностью ~20% в формате CSR
S = sp.random(5, 5, density=0.2, format="csr", random_state=42)
print("формат:", S.format, "| ненулевых:", S.nnz, "из 25 =", S.nnz / 25)
print(S.toarray().round(2))
print("\ndata   :", S.data.round(2))
print("indices:", S.indices)
print("indptr :", S.indptr)

# 4.2 Преобразование в COO и CSC
print("\n4.2 Преобразование в COO и CSC\n")
S_coo = S.tocoo()
S_csc = S.tocsc()

print("COO: row =", S_coo.row, "\n     col =", S_coo.col, "\n     data =", S_coo.data.round(2))
print("\nCSC: data   =", S_csc.data.round(2), "\n     indices (строки) =", S_csc.indices, "\n     indptr  =", S_csc.indptr)
print("\nвсе три формата описывают одну матрицу:",
      np.array_equal(S.toarray(), S_coo.toarray()) and np.array_equal(S.toarray(), S_csc.toarray()))

# 4.3 Умножение разреженной матрицы на плотный вектор
print("\n4.3 Умножение разреженной матрицы на плотный вектор\n")
v = rng.random(5)
y_sparse = S @ v
y_dense  = S.toarray() @ v
print(y_sparse)
print("совпадает с плотным вариантом:", np.allclose(y_sparse, y_dense))

# 4.4 Сравнение скорости: 1000x1000, плотность 0.01
print("\n4.4 Сравнение скорости: 1000x1000, плотность 0.01\n")
n = 1000
big_csr   = sp.random(n, n, density=0.01, format="csr", random_state=42)
big_dense = big_csr.toarray()
vec = rng.random(n)

print("совпадают:", np.allclose(big_csr @ vec, big_dense @ vec))
print("ненулевых:", big_csr.nnz, "из", n * n)

bench('big_dense @ vec', lambda: big_dense @ vec)
bench('big_csr @ vec', lambda: big_csr @ vec)

mem_dense  = big_dense.nbytes
mem_sparse = big_csr.data.nbytes + big_csr.indices.nbytes + big_csr.indptr.nbytes
print(f"память: dense {mem_dense/1e6:.2f} МБ, CSR {mem_sparse/1e6:.2f} МБ ({mem_dense/mem_sparse:.0f}x меньше)")

print(f"\n{'плотность':>10} {'dense, мс':>10} {'CSR, мс':>9}")
for d in (0.001, 0.01, 0.05, 0.1, 0.3, 0.5):
    M = sp.random(n, n, density=d, format="csr", random_state=42)
    Dn = M.toarray()
    td = min(timeit.repeat(lambda: Dn @ vec, number=50, repeat=5)) / 50 * 1e3
    ts = min(timeit.repeat(lambda: M  @ vec, number=50, repeat=5)) / 50 * 1e3
    print(f"{d:>10} {td:>10.3f} {ts:>9.3f}")