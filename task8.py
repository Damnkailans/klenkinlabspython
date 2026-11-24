import pandas as pd
from task7 import df1

df2 = df1.copy()

# revenue_rank 
df2["revenue_rank"] = df2["revenue"].rank(method="dense", ascending=False).astype(int)

# Сортировка: revenue по убыванию, при равенстве - order_date по возрастанию
# (order_date пока строка формата YYYY-MM-DD, она сортируется правильно)
df2 = df2.sort_values(by=["revenue", "order_date"], ascending=[False, True])
df2 = df2.reset_index(drop=True)

if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)
    print(df2[["order_id", "order_date", "revenue", "revenue_rank"]])
