from data import get_df

df = get_df()

# 3.1 Количество пропусков в каждом столбце
print("3.1:")
print(df.isna().sum(), "\n")

# 3.2 Заполняем пропуски в salary средним значением по отделу
df["salary"] = df["salary"].fillna(
    df.groupby("department")["salary"].transform("mean")
)
print("3.2:")
print(df[["name", "department", "salary"]], "\n")

# 3.3 Пропуски в bonus заполняем нулём
df["bonus"] = df["bonus"].fillna(0)
print("3.3:")
print(df[["name", "bonus"]], "\n")

# 3.4 Удаляем строки, где salary всё ещё пропущен
# (после заполнения средним по отделу пропусков не должно остаться,
# но если в отделе все зарплаты пустые - строка удалится)
df = df.dropna(subset=["salary"])
print("3.4:")
print(df)
print("\nПропусков осталось:")
print(df.isna().sum())
