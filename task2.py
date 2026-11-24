from data import get_df

df = get_df()

# 2.1 Столбцы name и salary для сотрудников из IT
print("2.1:")
print(df.loc[df["department"] == "IT", ["name", "salary"]], "\n")

# 2.2 iloc: первые 3 строки и первые 2 столбца
print("2.2:")
print(df.iloc[:3, :2], "\n")

# 2.3 Сотрудники с зарплатой выше 70000
print("2.3:")
print(df[df["salary"] > 70000], "\n")

# 2.4 Новый столбец total_comp = salary + bonus (пропуски в bonus считаем нулём)
df["total_comp"] = df["salary"] + df["bonus"].fillna(0)
print("2.4:")
print(df[["name", "salary", "bonus", "total_comp"]], "\n")

# 2.5 Удаляем столбец hire_date
df = df.drop(columns="hire_date")
print("2.5:")
print(df)
