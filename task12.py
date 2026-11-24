from pathlib import Path
import pandas as pd
from task11 import df5

df6 = df5.copy()


# priority - правила проверяются строго по порядку
def get_priority(row):
    if row["status"] in ("cancelled", "returned"):
        return "archive"
    if row["revenue"] >= 20000 and row["delivery_days"] <= 3:
        return "A"
    if row["revenue"] >= 5000:
        return "B"
    return "C"


df6["priority"] = df6.apply(get_priority, axis=1)

# manager_email - имя.фамилия@shop.ru (нижний регистр, пробелы -> точки)
df6["manager_email"] = (
    df6["manager"].str.strip().str.lower().str.replace(" ", ".", regex=False) + "@shop.ru"
)

# final_comment - "<client_clean>: <priority>, <revenue_segment>"
df6["final_comment"] = (
    df6["client_clean"] + ": " + df6["priority"] + ", " + df6["revenue_segment"].astype(str)
)

# Сохраняем итог в orders_final.csv
out_path = Path(__file__).parent / "orders_final.csv"
df6.to_csv(out_path, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", None)
    print(df6[["order_id", "status", "revenue", "delivery_days", "priority",
               "manager_email", "final_comment"]])
    print("\nСохранено:", out_path)
