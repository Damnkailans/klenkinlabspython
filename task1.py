import numpy as np
import pandas as pd


def create_employees_df(n_rows: int = 100_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    first_names = np.array([
        "Алексей", "Мария", "Дмитрий", "Елена", "Сергей",
        "Анна", "Иван", "Ольга", "Максим", "Наталья",
        "Андрей", "Татьяна", "Артём", "Екатерина", "Никита",
    ])
    last_names = np.array([
        "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев",
        "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров",
        "Морозов", "Волков", "Алексеев", "Лебедев", "Семёнов",
    ])
    departments = np.array(["IT", "Analytics", "HR", "Finance", "Marketing", "Sales"])

    ids = np.arange(1, n_rows + 1, dtype=np.int64)
    names = np.char.add(
        np.char.add(rng.choice(first_names, size=n_rows), " "),
        rng.choice(last_names, size=n_rows),
    )
    ages = rng.integers(20, 65, size=n_rows, dtype=np.int32)
    salaries = np.round(rng.uniform(45_000, 350_000, size=n_rows), 2)
    dept_col = rng.choice(departments, size=n_rows)

    start_date = np.datetime64("2015-01-01")
    end_date = np.datetime64("2026-01-01")
    days_range = (end_date - start_date).astype(int)
    hiredates = pd.to_datetime(start_date + rng.integers(0, days_range, size=n_rows))

    is_active = rng.choice([True, False], size=n_rows, p=[0.85, 0.15])

    df = pd.DataFrame({
        "id": ids,
        "name": names,
        "age": ages,
        "salary": salaries,
        "department": dept_col,
        "hiredate": hiredates,
        "is_active": is_active,
    })
    return df


if __name__ == "__main__":
    df = create_employees_df(n_rows=100_000)
    print("Первые 5 строк DataFrame:")
    print(df.head(), "\n")
    print("Информация о типах данных:")
    print(df.dtypes, "\n")
    print(f"Размер в оперативной памяти: {df.memory_usage(deep=True).sum() / 1024**2:.2f} МБ")
