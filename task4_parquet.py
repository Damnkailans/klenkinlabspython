import os
import time
import pandas as pd
from task1 import create_employees_df


def main() -> None:
    df = create_employees_df(n_rows=100_000)

    csv_file = "employees_ref.csv"
    df.to_csv(csv_file, index=False)
    csv_size = os.path.getsize(csv_file)

    # 4.1 Сохранение в Parquet с разными алгоритмами сжатия
    codecs = ["snappy", "gzip", "brotli"]
    parquet_files = {}

    for codec in codecs:
        fname = f"employees_{codec}.parquet"
        df.to_parquet(fname, engine="pyarrow", compression=codec, index=False)
        parquet_files[codec] = fname

    # 4.2 Сравнение размеров с CSV
    print(" 4.2 Сравнение размеров CSV и Parquet ")
    print(f"CSV (без сжатия):        {csv_size:>10,} байт ({csv_size / 1024**2:.2f} МБ)")
    for codec, fname in parquet_files.items():
        sz = os.path.getsize(fname)
        ratio = csv_size / sz
        print(f"Parquet ({codec:<6}):        {sz:>10,} байт ({sz / 1024**2:.2f} МБ) | сжатие в {ratio:.2f}x")
    print()

    # 4.3 Сравнение времени чтения Parquet и CSV
    t0 = time.perf_counter()
    _ = pd.read_csv(csv_file, parse_dates=["hiredate"])
    t_csv = time.perf_counter() - t0

    t0 = time.perf_counter()
    df_pq = pd.read_parquet(parquet_files["snappy"], engine="pyarrow")
    t_pq = time.perf_counter() - t0

    print(" 4.3 Сравнение времени полного чтения ")
    print(f"Чтение CSV:              {t_csv:.4f} с")
    print(f"Чтение Parquet (snappy): {t_pq:.4f} с (быстрее в {t_csv / t_pq:.2f}x)\n")

    # 4.4 Выборочное чтение столбцов (column pruning)
    cols = ["department", "salary"]
    t0 = time.perf_counter()
    df_pruned = pd.read_parquet(parquet_files["snappy"], columns=cols, engine="pyarrow")
    t_pruned = time.perf_counter() - t0

    print(" 4.4 Выборочное чтение столбцов (column pruning) ")
    print(f"Прочитаны только столбцы {cols} за {t_pruned:.4f} с")
    print(df_pruned.groupby("department")["salary"].mean(), "\n")

    # 4.5 Проверка сохранения типов данных
    print(" 4.5 Проверка сохранения типов данных ")
    comparison = pd.DataFrame({
        "Исходный dtype": df.dtypes,
        "Parquet dtype": df_pq.dtypes,
        "Совпадает": df.dtypes == df_pq.dtypes,
    })
    print(comparison)


if __name__ == "__main__":
    main()
