from pathlib import Path
import pandas as pd

# Загружаем orders.csv (лежит рядом со скриптом)
orders = pd.read_csv(Path(__file__).parent / "orders.csv")

# df1 - копия исходной таблицы + очищенные столбцы
df1 = orders.copy()

# client_clean 
df1["client_clean"] = df1["client"].str.strip().str.title()

# city_clean 
df1["city_clean"] = df1["city"].str.strip().str.title()

# category_clean
df1["category_clean"] = df1["category"].str.strip().str.lower()

# product_clean 
df1["product_clean"] = df1["product"].str.strip().str.upper()

# revenue = qty * price * (1 - discount), округляем до 2 знаков
df1["revenue"] = (df1["qty"] * df1["price"] * (1 - df1["discount"])).round(2)

if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)
    print(df1[["order_id", "client_clean", "city_clean", "category_clean",
               "product_clean", "revenue"]])
