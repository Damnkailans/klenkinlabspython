import os
import pandas as pd
from labspython.lab3.task1 import create_employees_df


def main() -> None:
    df = create_employees_df(n_rows=100_000)

    # Агрегированный DataFrame по отделам
    df_agg = (
        df.groupby("department", as_index=False)
        .agg(
            employees_count=("id", "count"),
            avg_salary=("salary", "mean"),
            max_salary=("salary", "max"),
            avg_age=("age", "mean"),
        )
    )

    h5_fixed_file = "employees_fixed.h5"
    h5_table_file = "employees_table.h5"
    csv_file = "employees_hdf_ref.csv"

    # Удаляем старые файлы, если существуют, чтобы не дописывать в них
    for f in (h5_fixed_file, h5_table_file, csv_file):
        if os.path.exists(f):
            os.remove(f)

    # 5.1 Сохранение двух DataFrame в один HDF5-файл под разными ключами (формат fixed)
    df.to_hdf(h5_fixed_file, key="employees", mode="w", format="fixed")
    df_agg.to_hdf(h5_fixed_file, key="dept_summary", mode="a", format="fixed")

    # 5.2 Чтение только одного объекта по ключу
    df_summary_read = pd.read_hdf(h5_fixed_file, key="dept_summary")
    print(" 5.2 Прочитанный объект по ключу 'dept_summary' ")
    print(df_summary_read, "\n")

    # 5.3 Сохранение в формате table (поддерживает индексацию и фильтрацию where)
    # Примечание: строковые столбцы для table лучше привести к обычным str/object с фиксированным лимитом
    df_for_table = df.copy()
    df_for_table["name"] = df_for_table["name"].astype(str)
    df_for_table["department"] = df_for_table["department"].astype(str)

    df_for_table.to_hdf(
        h5_table_file,
        key="employees",
        mode="w",
        format="table",
        data_columns=["department", "salary", "age", "is_active"],
    )

    # 5.4 Запрос к таблице HDF5 без загрузки всего файла в память
    df_filtered = pd.read_hdf(
        h5_table_file,
        key="employees",
        where="department == 'IT' and salary > 300000 and is_active == True",
    )
    print(" 5.4 Выборка из HDF5 (table) через where без загрузки всего файла ")
    print(f"Найдено записей: {len(df_filtered)}")
    print(df_filtered.head(), "\n")

    # 5.5 Сравнение размеров файлов HDF5 (fixed vs table) и CSV
    df.to_csv(csv_file, index=False)
    sz_csv = os.path.getsize(csv_file)
    sz_fixed = os.path.getsize(h5_fixed_file)
    sz_table = os.path.getsize(h5_table_file)

    print(" 5.5 Сравнение размеров файлов ")
    print(f"CSV:          {sz_csv:>10,} байт ({sz_csv / 1024**2:.2f} МБ)")
    print(f"HDF5 (fixed): {sz_fixed:>10,} байт ({sz_fixed / 1024**2:.2f} МБ) (включает 2 таблицы)")
    print(f"HDF5 (table): {sz_table:>10,} байт ({sz_table / 1024**2:.2f} МБ) (с индексами для where)")


if __name__ == "__main__":
    main()
