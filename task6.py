import os
import time
import pandas as pd
from task1 import create_employees_df


def benchmark_format(name: str, file_path: str, write_fn, read_fn) -> dict:
    if os.path.exists(file_path):
        os.remove(file_path)

    t0 = time.perf_counter()
    write_fn()
    write_time = time.perf_counter() - t0

    file_size = os.path.getsize(file_path)

    t0 = time.perf_counter()
    df_loaded = read_fn()
    read_time = time.perf_counter() - t0

    types_preserved = bool((df_loaded.dtypes == REFERENCE_DTYPES).all())

    return {
        "Формат": name,
        "Размер (МБ)": round(file_size / (1024 ** 2), 2),
        "Размер (байт)": file_size,
        "Время записи (с)": round(write_time, 4),
        "Время чтения (с)": round(read_time, 4),
        "Типы сохранены": "Да" if types_preserved else "Нет",
    }


df = create_employees_df(n_rows=100_000)
REFERENCE_DTYPES = df.dtypes


def main() -> None:
    # Подготовка копии с явными строками для корректной работы HDF5 table
    df_h5 = df.copy()
    df_h5["name"] = df_h5["name"].astype(str)
    df_h5["department"] = df_h5["department"].astype(str)

    benchmarks = [
        benchmark_format(
            name="CSV (index=False)",
            file_path="bench.csv",
            write_fn=lambda: df.to_csv("bench.csv", index=False),
            read_fn=lambda: pd.read_csv("bench.csv"),
        ),
        benchmark_format(
            name="JSON (records)",
            file_path="bench.json",
            write_fn=lambda: df.to_json("bench.json", orient="records", force_ascii=False),
            read_fn=lambda: pd.read_json("bench.json", orient="records"),
        ),
        benchmark_format(
            name="Parquet (snappy)",
            file_path="bench_snappy.parquet",
            write_fn=lambda: df.to_parquet("bench_snappy.parquet", compression="snappy", index=False),
            read_fn=lambda: pd.read_parquet("bench_snappy.parquet"),
        ),
        benchmark_format(
            name="Parquet (gzip)",
            file_path="bench_gzip.parquet",
            write_fn=lambda: df.to_parquet("bench_gzip.parquet", compression="gzip", index=False),
            read_fn=lambda: pd.read_parquet("bench_gzip.parquet"),
        ),
        benchmark_format(
            name="HDF5 (fixed)",
            file_path="bench_fixed.h5",
            write_fn=lambda: df.to_hdf("bench_fixed.h5", key="data", mode="w", format="fixed"),
            read_fn=lambda: pd.read_hdf("bench_fixed.h5", key="data"),
        ),
        benchmark_format(
            name="HDF5 (table)",
            file_path="bench_table.h5",
            write_fn=lambda: df_h5.to_hdf("bench_table.h5", key="data", mode="w", format="table"),
            read_fn=lambda: pd.read_hdf("bench_table.h5", key="data"),
        ),
    ]

    # 6.2 Итоговый DataFrame-отчёт
    report_df = pd.DataFrame(benchmarks)
    print(" 6.2 Итоговый отчёт по форматам хранения данных ")
    print(report_df.to_string(index=False), "\n")

    # 6.3 Ответы на вопросы
    vivod = """ 6.3 Выводы: выбор формата под задачу 
1. Для аналитики и больших данных -> Parquet
 Колоночное хранение позволяет читать только нужные столбцы (column pruning)
 Высокая степень сжатия и миним альный размер на диске
Полностью сохраняет схемы и типы данных (включая datetime, int32, bool)

2. Для обмена данными - CSV или JSON:
 CSV: для плоских таблиц небольшого объёма, совместим с Excel, БД и любыми инструментами
 JSON: для веб-API и передачи иерархических/вложенных структур (списки, словари)

3. Для научных расчётов - PyTables
   Позволяет хранить несколько разнородных наборов данных и метаданных в одном файле по ключам
   Обеспечивает сверхбыстрый произвольный доступ (random access) и выборку через where без загрузки всего файла в ОЗУ
"""
    print(vivod)


if __name__ == "__main__":
    main()
