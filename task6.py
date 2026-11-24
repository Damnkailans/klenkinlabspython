from data import get_df

# Подготовка: чистим данные как в задачах 2-3
df = get_df()
df["salary"] = df["salary"].fillna(df.groupby("department")["salary"].transform("mean"))
df = df.dropna(subset=["salary"])
df["bonus"] = df["bonus"].fillna(0)
df["total_comp"] = df["salary"] + df["bonus"]

# 6.1 Топ-3 сотрудников по total_comp
print("6.1:")
print(df.nlargest(3, "total_comp")[["name", "department", "total_comp"]], "\n")

# 6.2 Средняя зарплата и средний бонус по отделам в одном DataFrame
print("6.2:")
print(df.groupby("department")[["salary", "bonus"]].mean(), "\n")

# 6.3 Доля сотрудников с зарплатой выше 75000 по каждому отделу
share = (df["salary"] > 75000).groupby(df["department"]).mean()
print("6.3:")
print(share)
