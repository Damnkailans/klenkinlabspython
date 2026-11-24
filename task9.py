import pandas as pd
from task8 import df2

df3 = df2.copy()

# order_date -> datetime
df3["order_date"] = pd.to_datetime(df3["order_date"])

# order_year, order_month, order_quarter
df3["order_year"] = df3["order_date"].dt.year
df3["order_month"] = df3["order_date"].dt.month
df3["order_quarter"] = df3["order_date"].dt.quarter

# order_weekday - название дня недели
df3["order_weekday"] = df3["order_date"].dt.day_name()

# is_weekend - суббота (5) или воскресенье (6)
df3["is_weekend"] = df3["order_date"].dt.dayofweek >= 5

# delivery_date = дата заказа + delivery_days
df3["delivery_date"] = df3["order_date"] + pd.to_timedelta(df3["delivery_days"], unit="D")

# days_to_month_end - сколько дней осталось до конца месяца заказа
df3["days_to_month_end"] = df3["order_date"].dt.days_in_month - df3["order_date"].dt.day

if __name__ == "__main__":
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", None)
    print(df3[["order_id", "order_date", "order_year", "order_month", "order_quarter",
               "order_weekday", "is_weekend", "delivery_date", "days_to_month_end"]])
