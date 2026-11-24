import os
import time
import pandas as pd
from task1 import create_employees_df


def main() -> None:
    df = create_employees_df(n_rows=100_000)

    file_with_index = "employees_with_index.csv"
    file_no_index = "employees_no_index.csv"

    # 2.1 Сохранение в CSV двумя способами
    df.to_csv(file_with_index)
    df.to_csv(file_no_index, index=False)

    # 2.2 Чтение обратно и проверка типов данных
    t0 = time.perf_counter()
    df_read_default = pd.read_csv(file_no_index)
    t_default = time.perf_counter() - t0

    print("2.2 Типы данных после обычного read_csv()")
    print("Исходные типы:\n", df.dtypes, "\n")
    print("Типы после read_csv() (hiredate стал object/str, int32 -> int64):\n", df_read_default.dtypes, "\n")

     # 2.3 Сравнение размеров файлов
    size_with_idx = os.path.getsize(file_with_index)
    size_no_idx = os.path.getsize(file_no_index)
    print("2.3 Сравнение размеров CSV")
    print(f"С индексом (index=True):     {size_with_idx:,} байт ({size_with_idx / 1024**2:.2f} МБ)")
    print(f"Без индекса (index=False):   {size_no_idx:,} байт ({size_no_idx / 1024**2:.2f} МБ)")
    print(f"Экономия без индекса:        {size_with_idx - size_no_idx:,} байт\n")

    # 2.4 Оптимизированное чтение с dtype, parse_dates, usecols
    dtypes_map = {
        "id": "int64",
        "name": "string",
        "age": "int32",
        "salary": "float64",
        "department": "category",
        "is_active": "bool",
    }
    selected_cols = ["id", "name", "department", "salary", "hiredate"]

    t0 = time.perf_counter()
    df_read_opt = pd.read_csv(
        file_no_index,
        usecols=selected_cols,
        dtype={k: v for k, v in dtypes_map.items() if k in selected_cols},
        parse_dates=["hiredate"],
    )
    t_opt = time.perf_counter() - t0

    print(" 2.4 Оптимизированное чтение (usecols + dtype + parse_dates)")
    print(df_read_opt.dtypes, "\n")
    print(f"Время обычного чтения (все столбцы):       {t_default:.4f} с")
    print(f"Время оптимизированного чтения (5 столбцов): {t_opt:.4f} с")
    print(
        f"Память DataFrame: {df_read_default.memory_usage(deep=True).sum() / 1024**2:.2f} МБ -> "
        f"{df_read_opt.memory_usage(deep=True).sum() / 1024**2:.2f} МБ"
    )


if __name__ == "__main__":
    main()
