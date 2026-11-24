import pandas as pd
from data import get_df

df = get_df()

# 5.1 DataFrame managers с отделами и руководителями
managers = pd.DataFrame({
    "department": ["IT", "HR", "Finance"],
    "manager": ["Козлов А.", "Смирнова Е.", "Новикова О."],
})
print("5.1:")
print(managers, "\n")

# 5.2 Left join df с managers по department
# (если у отдела нет руководителя в managers -> будет NaN)
df = df.merge(managers, on="department", how="left")
print("5.2:")
print(df[["name", "department", "manager"]], "\n")

# 5.3 Новая строка с данными о сотруднике и добавление через concat
new_row = pd.DataFrame([{
    "name": "Ivan",
    "department": "IT",
    "salary": 90000,
    "bonus": 7000,
    "hire_date": pd.Timestamp("2025-06-01"),
    "manager": "Козлов А.",
}])
df = pd.concat([df, new_row])
print("5.3 (индекс после concat):")
print(df.tail(3), "\n")

# 5.4 Сбрасываем индекс после объединения
df = df.reset_index(drop=True)
print("5.4:")
print(df.tail(3))
