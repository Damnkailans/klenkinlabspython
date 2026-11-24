import numpy as np
import pandas as pd
from task10 import df4

df5 = df4.copy()

# revenue_segment: low [0,1000), medium [1000,5000), high [5000,20000), vip [20000, +inf)
# right=False -> левая граница включена, правая нет
df5["revenue_segment"] = pd.cut(
    df5["revenue"],
    bins=[0, 1000, 5000, 20000, np.inf],
    labels=["low", "medium", "high", "vip"],
    right=False,
)

# status_ru - перевод статуса
status_map = {
    "new": "новый",
    "paid": "оплачен",
    "shipped": "отправлен",
    "cancelled": "отменён",
    "returned": "возврат",
}
df5["status_ru"] = df5["status"].map(status_map)

# promo_used - True, если promo_code не равен NO_PROMO
df5["promo_used"] = df5["promo_code"] != "NO_PROMO"

if __name__ == "__main__":
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", None)
    print(df5[["order_id", "revenue", "revenue_segment", "status", "status_ru",
               "promo_code", "promo_used"]])
