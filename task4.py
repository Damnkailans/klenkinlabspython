from data import get_df

df = get_df()
df["bonus"] = df["bonus"].fillna(0)

# 4.1 Средняя зарплата по каждому отделу
print("4.1:")
print(df.groupby("department")["salary"].mean(), "\n")

# 4.2 Для каждого отдела: средняя зарплата, максимальный бонус, количество сотрудников
stats = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    max_bonus=("bonus", "max"),
    employees=("name", "count"),
)
print("4.2:")
print(stats, "\n")

# 4.3 Сводная таблица: индекс - отдел, значения - средняя зарплата
pivot = df.pivot_table(index="department", values="salary", aggfunc="mean")
print("4.3:")
print(pivot, "\n")

# 4.4 Сортировка отделов по средней зарплате по убыванию
print("4.4:")
print(pivot.sort_values("salary", ascending=False))
