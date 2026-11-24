import pandas as pd
from data import data

# 1.1 Series из списка чисел с произвольным индексом
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
print("1.1 Series:")
print(s, "\n")

# 1.2 DataFrame из словаря (словарь data из data.py)
df = pd.DataFrame(data)
print("1.2 DataFrame:")
print(df, "\n")

# 1.3 Первые и последние строки, типы данных, статистика
print("1.3 head(3):")
print(df.head(3), "\n")

print("tail(3):")
print(df.tail(3), "\n")

print("dtypes:")
print(df.dtypes, "\n")

print("info():")
df.info()

print("\ndescribe():")
print(df.describe())