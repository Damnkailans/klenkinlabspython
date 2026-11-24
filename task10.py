import pandas as pd
from task9 import df3

# Дубль = одинаковая комбинация client_clean + order_date + product_clean
key = ["client_clean", "order_date", "product_clean"]

df4 = df3.copy()

# duplicate_group_flag - True, если такая комбинация встречается больше одного раза
# (keep=False помечает ВСЕ строки группы, а не только повторы)
df4["duplicate_group_flag"] = df4.duplicated(subset=key, keep=False)

# Оставляем по одной строке на комбинацию - с максимальной revenue:
# сортируем по revenue по убыванию и берём первую из каждой группы
df4 = df4.sort_values("revenue", ascending=False)
df4 = df4.drop_duplicates(subset=key, keep="first")

# После удаления дублей сортируем по order_id
df4 = df4.sort_values("order_id").reset_index(drop=True)

if __name__ == "__main__":
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", None)
    print("Было строк:", len(df3), "-> стало:", len(df4))
    print(df4[["order_id", "client_clean", "order_date", "product_clean",
               "revenue", "duplicate_group_flag"]])
